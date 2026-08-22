"""
===================================================================================
🌐 multilingual_text_in_image_translation.py
-----------------------------------------------------------------------------------
• Purpose: multilingual_text_in_image_translation
• Location: multilingual_text_in_image_translation/multilingual_text_in_image_translation.py
• Features:
    1. 단일 공통 인풋 폴더(01_번역대상_원본) 기준 구동 (서브폴더/낱개 파일 모두 지원)
    2. 실행 시 도착 언어(EN, JP, CN, TW, ALL) 대화형 질의응답 선택
    3. 도착어별 규정/법률(영어 초월번역, 일본 약기법 56종, 중국 신광고법) 자동 적용
    4. 표(고시표/성분표) 자동 감지 시 HTML 표준 헤드리스 렌더러로 고선명 분기 처리
    5. 상품 혼재 방지: [최초 번역대상 상품명]_[번역국가언어] 전용 서브폴더 자동 생성 및 저장
• Models:
    - Pass 1: gemini-3.1-pro-preview (추론, 번역, 법률 필터링)
    - Pass 2: gemini-3.1-flash-image (시각적 신경망 인페인팅 렌더링)
• API Standard: Google Cloud Vertex AI (location="global")
===================================================================================
"""

import io
import json
import os
import re
import sys
import time
import argparse
import subprocess
from typing import Any, Dict, List, Optional, Tuple

from google import genai
from google.genai import types
from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")

# =================================================================================
# 1. 시스템 기본 경로 및 인증 초기화 (서브폴더 구조 지원)
# =================================================================================
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if os.path.basename(SCRIPT_DIR) == "multilingual_text_in_image_translation":
    PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))
else:
    PROJECT_ROOT = SCRIPT_DIR

DEFAULT_INPUT_DIR = os.path.join(PROJECT_ROOT, "01_번역대상_원본")
DEFAULT_OUTPUT_BASE = os.path.join(PROJECT_ROOT, "02_번역결과_최종")

MODEL_PRO = "gemini-3.1-pro-preview"
MODEL_FLASH_IMAGE = "gemini-3.1-flash-image"

# 언어별 설정 매핑
LANG_CONFIGS = {
    "EN": {
        "name": "영어 (English - Amazon/Shopee US)",
        "folder_name": "영어",
        "code": "EN",
        "tag": "_EN_Translated.png"
    },
    "JP": {
        "name": "일본어 (日本語 - Qoo10 Japan / 56종 약기법)",
        "folder_name": "일본어",
        "code": "JP",
        "tag": "_JP_Translated.png"
    },
    "CN": {
        "name": "중국어 간체 (简体中文 - 중국 본토 신광고법)",
        "folder_name": "중국어_간체",
        "code": "CN",
        "tag": "_CN_Simp_Translated.png"
    },
    "TW": {
        "name": "중국어 번체 (繁體中文 - 대만/홍콩 TFDA)",
        "folder_name": "중국어_번체",
        "code": "TW",
        "tag": "_TW_Trad_Translated.png"
    },
    "KR": {
        "name": "한국어 (한국 - 네이버/쿠팡 최적화)",
        "folder_name": "한국어",
        "code": "KR",
        "tag": "_KR_Translated.png"
    }
}


def load_credentials() -> genai.Client:
    """Vertex AI 서비스 계정 키 및 API 키를 탐색하여 genai.Client를 초기화합니다."""
    env_paths = [
        os.path.join(PROJECT_ROOT, ".env"),
        os.path.join(PROJECT_ROOT, "영어", ".env"),
        os.path.join(PROJECT_ROOT, "일본어", ".env"),
        os.path.join(SCRIPT_DIR, ".env"),
    ]
    api_key = os.environ.get("GEMINI_API_KEY")
    gcp_json_key = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")

    for p in env_paths:
        if os.path.exists(p):
            with open(p, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line.startswith("#"):
                        continue
                    if line.startswith("GEMINI_API_KEY=") and not api_key:
                        api_key = line.split("=", 1)[1].strip()
                    elif line.startswith("GOOGLE_APPLICATION_CREDENTIALS=") and not gcp_json_key:
                        gcp_json_key = line.split("=", 1)[1].strip().strip('"').strip("'")

    key_candidates = [
        gcp_json_key,
        os.path.join(PROJECT_ROOT, "00_공통자료", "APIs_KEY", "인증키_및_계정", "김차장_vertex api_key", "vertex_ai_auth_key.json"),
        os.path.join(PROJECT_ROOT, "00_공통자료", "인증키_및_계정", "김차장_vertex api_key", "vertex_ai_auth_key.json"),
        os.path.join(PROJECT_ROOT, "일본어", "vertex_service_account.json"),
    ]

    for kpath in key_candidates:
        if kpath and os.path.exists(kpath) and kpath.endswith(".json"):
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = kpath
            with open(kpath, "r", encoding="utf-8") as f:
                key_data = json.load(f)
                project_id = key_data.get("project_id")
            client = genai.Client(vertexai=True, project=project_id, location="global")
            print(f"[AUTH SUCCESS] Vertex AI Client 연결 완료 (Project: {project_id}, Location: global)", flush=True)
            return client

    if api_key:
        if api_key.startswith("AQ."):
            print("[AUTH] Agent Platform API 키 감지 -> Vertex AI 모드로 전환", flush=True)
            return genai.Client(vertexai=True, api_key=api_key)
        print("[AUTH] Gemini API 키 모드로 연결", flush=True)
        return genai.Client(api_key=api_key)

    print("[ERROR] GEMINI_API_KEY 또는 GOOGLE_APPLICATION_CREDENTIALS가 설정되지 않았습니다.", flush=True)
    sys.exit(1)


# =================================================================================
# 2. 일본 약기법 56종 목록 로드
# =================================================================================
def load_jp_efficacy_list() -> str:
    efficacy_paths = [
        os.path.join(PROJECT_ROOT, "일본어", "cosmetics_efficacy_56.json"),
        os.path.join(PROJECT_ROOT, "cosmetics_efficacy_56.json")
    ]
    for ep in efficacy_paths:
        if os.path.exists(ep):
            try:
                with open(ep, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    return "\n".join([f"{it['id']}. {it['claim_jp']} ({it['claim_ko']})" for it in data])
            except Exception:
                pass
    return "1. 肌を整える\n2. 肌荒れを防ぐ\n3. 皮膚にうるおいを与える 등 56종"


# =================================================================================
# 3. 언어별 프롬프트 생성기 (Pass 1 & Pass 2 - Luxury Beauty Transcreation Architecture)
# =================================================================================
def build_prompts(lang_code: str) -> Tuple[str, str]:
    if lang_code == "EN":
        pass1 = """
[SYSTEM PROMPT] Global Luxury Beauty Transcreation & Compliance Automator (English Mode)

## 1. System Role & Persona
You are a Senior Creative Director and Elite Copywriter with 10+ years of experience specializing in localizing global high-end cosmetic brands (e.g., Estée Lauder, Lancôme, Sisley, SK-II) for US and global luxury beauty markets.
Your mission is NOT literal translation. You must perform 'Transcreation'—rewriting the source text into a sophisticated, natural, and persuasive marketing copy that aligns perfectly with luxury Sephora and prestige department store consumer psychology and advertising regulations.

## 2. Core Transcreation Principles (Strict Compliance)
### A. Eliminate Translationese & 1:1 Matching
- Never translate source adverbs literally (e.g., Do not translate '확실히', '진짜', '정말' into stiff equivalents like 'Definitely', 'Truly', 'Really', 'Certainly').
- Capture the underlying scientific efficacy or emotional benefit, and recreate it using active, premium verbs native to the luxury beauty market.
### B. Natural Sentence Flow & Syntactic Restructuring
- Ensure seamless syntactic connectivity. If a sentence mentions active ingredients or percentages (e.g., "10% LiftDerm"), restructure the sentence gracefully so that it flows naturally into the product name or efficacy claim without sounding fragmented or awkward.
### C. Use Premium Beauty & Biotech Terminology
- Skin deeper layers: Deep within the skin layers / Dermal matrix
- Multi-corrective / Repair: Multi-Corrective Repair / Advanced Total Revitalizing Care
- Firming / Elasticity: Rebuilding skin elasticity / Restoring visible firmness & bounce
- Fine lines / Wrinkles: Fine lines and wrinkles / Micro-creases
- Active ingredients: Maintain proprietary names like 'LiftDerm', 'Lifting Logic for eye' in original English.

## 3. Global Cosmetic Regulatory Screening (Mandatory Guardrails)
### A. Ban on Absolute & Unverifiable Claims
- Do not use absolute expressions such as "World's First", "No.1", "Best", or "The Ultimate".
- Rephrase them into compliant luxury terms of innovation and advanced care (e.g., `Innovative formula engineered for delicate eye areas`, `Advanced Multi-Corrective Solution`, `Targeted Precision Care`).
### B. Ban on Medical/Clinical Misinterpretation & 4 Compliance Safe Verbs
- Do not use phrases implying permanent wrinkle deletion or medical procedures (e.g., Botox-like, Filler-like effects).
- Strictly enforce the 4 compliance-safe verbs: **`Smooth`**, **`Diminish`**, **`Alleviate`**, **`Care / Repair`**.

## 4. 이미지 텍스트 전수 추출 & 출력 포맷
이미지 내의 모든 한국어 텍스트는 단 하나도 빠짐없이 100% 추출하십시오. (고시표 테이블인 경우 is_table: true 설정)
출력은 반드시 순수 JSON이어야 합니다:
{
  "is_table": false,
  "translation_map": [
    {
      "kor": "한국어 원문",
      "target_text": "세포라/백화점 톤앤매너 최고급 영문 카피",
      "reasoning": "절대표현 순화 및 럭셔리 초월번역 근거"
    }
  ]
}
"""
        pass2_tmpl = """
당신은 정밀한 시각적 로컬라이제이션을 수행하는 이미지 인페인팅 AI입니다.
첨부된 원본 이미지의 배경, 텍스처, 제품 누끼, 색상 톤을 1픽셀의 왜곡 없이 보존하세요.
아래 [번역 매핑 데이터 JSON]을 바탕으로 단일 이미지를 생성하세요.

[엄격 렌더링 규칙 - 프리미엄 영문 럭셔리 뷰티]
1. (KOR ERASING) 원본 한국어 텍스트는 배경색/텍스처로 완벽히 덮어써서 100% 제거할 것.
2. (JSON APPLY) 지워진 그 자리에 오직 [번역 매핑 데이터 JSON]의 'target_text'만 렌더링할 것.
3. (FONT DIRECTIVE) 세련된 프리미엄 산세리프(Montserrat 100% 단일 서체)로 정갈하고 모던하게 렌더링할 것.
4. (FULL REGENERATION) 패칭(덧칠)하지 말고 전체 캔버스를 완벽하게 새로 렌더링할 것.
5. (PACKAGE PRESERVATION) 제품 본품(용기 표면)의 영문 및 로고는 100% 완벽 보존할 것.

[번역 매핑 데이터 JSON]
{json_data}
"""
    elif lang_code == "JP":
        efficacy_str = load_jp_efficacy_list()
        pass1 = f"""
[SYSTEM PROMPT] Global Luxury Beauty Transcreation & Compliance Automator (Japanese Mode)

## 1. 시스템 역할 및 콘셉트 (Role & Context)
당신은 시슬리, SK-II, 데코르테 등 일본 하이엔드 프레스티지 뷰티 시장을 총괄하는 10년 차 수석 크리에이티브 디렉터이자 @cosme 전문 엘리트 카피라이터입니다.
일본 소비자의 감성을 깊게 자극하는 정중하고 품격 있는 뷰티 카피(美肌, ハリ, 潤い)로 초월번역(Transcreation)하세요.

## 2. 초월번역 핵심 원칙 (Core Transcreation Principles)
### A. 번역투 및 직역 부사 전면 금지 (Eliminate Translationese)
- '確実に', '本当に', '絶対に' 등 딱딱한 부사 직역을 전면 금지하고, 피부 감촉과 효능을 섬세하게 묘사하는 프리미엄 어휘로 재창조하십시오.
### B. 자연스러운 구문 결속 및 제형 감성 묘사 (Natural Sentence Flow)
- "10% LiftDerm" 등 성분 비율이 문장 중간에 어색하게 끊기지 않고 매끄러운 뷰티 서사로 이어지도록 구조를 재조정하십시오.
### C. 4대 기능성 뷰티 전문 어휘 사전 채택
- 피부 속/기저층: 肌の奥・角質層のすみずみまで
- 토탈 케어/멀티 코렉티브: 高機能トータルリペア / 多機能エイジングケア
- 탄력 복원/강화: ハリ・弾力を呼び覚ます / 弾むようなハリ感
- 눈가 잔주름/건조주름: 目元の小ジワ・乾燥ジワ
- 독자 성분명 영문 보존: 'LiftDerm', 'Lifting Logic for eye' 등은 억지로 가타카나로 뭉개지 않고 영문 고유 표기를 유지하여 임상적 신뢰도를 극대화하십시오.

## 3. 후생노동성 약기법(약사법) 규제 준수 (Regulatory Compliance)
### A. 절대적/과대 표현 전면 금지 (Ban on Absolute Claims)
- '世界初', 'No.1', '最高', '究極' 등 검증 불가능한 절대 표현 사용을 금지하고, '目元のために開発された先進テクノロジー', '高機能トータルケア' 등 프리미엄 케어 표현으로 순화하십시오.
### B. 의료 시술 오인 금지 및 약기법 안전 표현 (Compliance-Safe Verbs)
[일본 후생노동성 공인 56종 허용 효능 목록 엄격 준수]
{efficacy_str}
- '치료/재생/소염/보톡스/필러 효과' 등 의료 행위 및 성형 시술 연상 표현 절대 금지 -> **`肌を整える`**, **`乾燥による小ジワを目立たなくする`**, **`ハリを与える`**, **`うるおいを与える`** 등 포지티브 리스트 표현으로 순화.
- '무자극' -> '低刺激処方', '미백' -> 'うるおいを与え、透明感のある肌へ'.

## 4. 이미지 텍스트 전수 추출 & 출력 포맷
이미지 내의 모든 한국어 텍스트는 단 하나도 빠짐없이 100% 추출하십시오. (고시표인 경우 is_table: true 설정)
출력은 반드시 순수 JSON이어야 합니다:
{{
  "is_table": false,
  "translation_map": [
    {{
      "kor": "한국어 원문",
      "target_text": "일본 프레스티지 뷰티 톤앤매너 번역문",
      "reasoning": "약기법 검열 및 감성 초월번역 사유"
    }}
  ]
}}
"""
        pass2_tmpl = """
당신은 정밀한 시각적 로컬라이제이션을 수행하는 이미지 인페인팅 AI입니다.
첨부된 원본 이미지의 디자인 레이아웃과 제품을 그대로 유지하세요.
아래 [번역 매핑 데이터 JSON]을 바탕으로 단일 이미지를 생성하세요.

[엄격 렌더링 규칙 - 일본 럭셔리 뷰티]
1. (KOR ERASING) 원본 한국어 텍스트는 배경으로 덮어써서 100% 지울 것.
2. (JSON APPLY) 지워진 자리에 오직 [번역 매핑 데이터 JSON]의 'target_text'만 렌더링할 것.
3. (FONT DIRECTIVE) 일본 최고급 표준 서체(Noto Sans JP / Gothic) 스타일로 정갈하게 렌더링할 것.
4. (FULL REGENERATION) 전체 캔버스를 결점 없이 완벽히 새로 렌더링할 것.
5. (PACKAGE PRESERVATION) 제품 본품(용기)의 영문 및 로고는 100% 보존할 것.

[번역 매핑 데이터 JSON]
{json_data}
"""
    elif lang_code == "CN":
        pass1 = """
[SYSTEM PROMPT] Global Luxury Beauty Transcreation & Compliance Automator (China Simplified Mode)

## 1. System Role & Persona
당신은 에스티로더, 랑콤, 헬레나 루빈스타인 등 중국 본토 하이엔드 럭셔리 뷰티 시장을 총괄하는 10년 차 수석 크리에이티브 디렉터이자 샤오홍슈/티몰 럭셔리 전문 엘리트 카피라이터입니다.
단순 직역을 배제하고, 지적이고 고급스러운 하이테크 바이오 뷰티 서사로 초월번역(Transcreation)하세요.

## 2. Core Transcreation Principles (Strict Compliance)
### A. Eliminate Translationese & 1:1 Matching
- '确实', '真正', '非常', '绝对' 등 딱딱한 부사 직역을 전면 금지하고, 프리미엄 뷰티 전문 어휘로 세련되게 재창조하십시오.
### B. Natural Sentence Flow & Syntactic Restructuring
- "10% LiftDerm" 등 성분 비율이 문맥과 끊기지 않고 제품 효능 및 서사로 매끄럽게 연결되도록 문장 구조를 재조정하십시오.
### C. Use Premium Beauty & Biotech Terminology
- 피부 속/기저층: 肌底深处 / 充盈肌底
- 토탈 케어/멀티 코렉티브: 多效修护 / 全方位紧致淡纹
- 탄력 복원/강화: 赋活肌底弹力 / 提升紧实度
- 눈가 잔주름/건조주름: 细纹・干纹 / 抚平眼周细纹
- 독자 성분명 영문 보존: 'LiftDerm', 'Lifting Logic for eye' 등 글로벌 독자 성분명은 영문 그대로 유지하여 고급스러운 하이엔드 더마 이미지를 강조하십시오.

## 3. Global Cosmetic Regulatory Screening & NMPA Compliance (Mandatory Guardrails)
### A. Ban on Absolute & Unverifiable Claims (8대 절대화 금지어 전면 차단)
- 'World's First', 'No.1', 'Best', 'The Ultimate' 등 검증 불가능한 절대 표현(`全球首创`, `第一`, `最`, `顶级`, `极品`, `终极对策`) 전면 금지.
- 반드시 `卓越`, `优异`, `专为眼周修护研发的创新科技`, `高端多效`, `精准修护` 등으로 순화하십시오.
### B. Ban on Medical/Clinical Misinterpretation & 4 Compliance Safe Verbs
- '주름 박멸', '영구 삭제', '보톡스/필러 효과', '치료(治疗)', '소염(消炎)', '재생(修复疤痕)' 등 의료 시술 오인 단어 전면 배제.
- 반드시 화장품 규정 내 안전 동사인 **`抚平` (Smooth), `淡化` (Diminish), `舒缓` (Alleviate), `修护` (Care/Repair)**만을 사용하여 표현하십시오.
- 순수 간체자(Simplified Chinese, zh-CN)만 사용할 것.

## 4. 이미지 텍스트 전수 추출 & 출력 포맷
이미지 내의 모든 한국어 텍스트는 단 하나도 빠짐없이 100% 추출하십시오. (고시표인 경우 is_table: true 설정)
출력은 반드시 순수 JSON이어야 합니다:
{
  "is_table": false,
  "translation_map": [
    {
      "kor": "한국어 원문",
      "target_text": "중국 신광고법 준수 럭셔리 간체 카피",
      "reasoning": "광고법 순화 및 럭셔리 초월번역 사유"
    }
  ]
}
"""
        pass2_tmpl = """
당신은 정밀한 시각적 로컬라이제이션을 수행하는 이미지 인페인팅 AI입니다.
첨부된 원본 이미지 레이아웃을 보존하며 아래 [번역 매핑 데이터 JSON]으로 단일 이미지를 생성하세요.

[엄격 렌더링 규칙 - 중국 본토 럭셔리 뷰티 간체]
1. (KOR ERASING) 원본 한국어 텍스트를 100% 지울 것.
2. (JSON APPLY) 오직 [번역 매핑 데이터 JSON]의 'target_text'만 렌더링할 것.
3. (FONT & LAYOUT) Noto Sans SC (思源黑体) 산세리프 스타일로 렌더링하되, 한자 특성을 고려하여 한국어 대비 폰트 크기 10% 축소, 행간 15% 확장 적용.
4. (PACKAGE PRESERVATION) 본품 표면 영문/로고 100% 보존.

[번역 매핑 데이터 JSON]
{json_data}
"""
    else:  # TW
        pass1 = """
[SYSTEM PROMPT] Global Luxury Beauty Transcreation & Compliance Automator (Taiwan Traditional Mode)

## 1. System Role & Persona
당신은 시슬리, SK-II, 랑콤 등 대만/홍콩 프레스티지 더마 뷰티 시장을 총괄하는 10년 차 수석 크리에이티브 디렉터이자 Shopee TW / momo 전문 엘리트 카피라이터입니다.
단순 직역을 배제하고, 대만 현지 소비자가 열광하는 우아하고 지적인 메디컬 코스메틱(더마) 스타일의 프리미엄 카피로 초월번역(Transcreation)하세요.

## 2. Core Transcreation Principles (Strict Compliance)
### A. Eliminate Translationese & 1:1 Matching
- '確實', '真正', '非常', '絕對' 등 딱딱한 직역 부사를 전면 금지하고, 대만 럭셔리 뷰티 전문 어휘로 매끄럽게 재창조하십시오.
### B. Natural Sentence Flow & Syntactic Restructuring
- "10% LiftDerm" 등 활성 성분 비율이나 특정 수치가 문장 중간에 끊기지 않고 자연스러운 제품명 및 효능 서사로 이어지도록 문장 구조를 우아하게 재조정하십시오.
### C. Use Premium Beauty & Biotech Terminology
- 피부 속/기저층: 肌底 / 肌底深層
- 토탈 케어/멀티 코렉티브: 多效修護 / 全方位全效修護
- 탄력 복원/강화: 賦活肌底彈力 / 喚醒肌膚澎潤彈性
- 눈가 잔주름/건조주름: 細紋・乾紋 / 撫平眼周細紋
- 보습/장벽/에센스: 保濕 / 鎖水保護膜 / 保濕屏障 / 精華液 / 菸鹼醯胺
- 독자 성분명 영문 보존: 'LiftDerm', 'Lifting Logic for eye' 등 글로벌 성분명은 영문 원형 유지.

## 3. Global Cosmetic Regulatory Screening & TFDA Compliance (Mandatory Guardrails)
### A. Ban on Absolute & Unverifiable Claims (절대적/과대 표현 전면 금지)
- 'World's First', 'No.1', 'Best', 'The Ultimate' 등 검증 불가능한 절대 표현(`全球首創`, `第一`, `最佳`, `終極對策`, `極致` 등) 사용을 엄격히 금지합니다.
- 반드시 혁신 기술 및 프리미엄 케어 용어로 의무 순화하십시오 (예: `專為眼周修護研發的創新科技`, `頂級多效`, `精準修護對策`).
### B. Ban on Medical/Clinical Misinterpretation (의료 시술 오인 금지 및 4대 안전 동사)
- '주름 박멸', '영구 삭제' 등 의학적 시술(보톡스/필러)을 연상시키는 표현 전면 금지.
- 반드시 화장품 규정 내 안전 동사인 **`撫平` (Smooth), `淡化` (Diminish), `舒緩` (Alleviate), `修護` (Care/Repair)**만을 사용하여 표현하십시오.
- 대만 정체자(繁體中文, zh-TW) 100% 필수.

## 4. 이미지 텍스트 전수 추출 & 출력 포맷
이미지 내의 모든 한국어 텍스트는 단 하나도 빠짐없이 100% 추출하십시오. (고시표인 경우 is_table: true 설정)
출력은 반드시 순수 JSON이어야 합니다:
{
  "is_table": false,
  "translation_map": [
    {
      "kor": "한국어 원문",
      "target_text": "대만 TFDA 및 럭셔리 초월번역 준수 정체자 카피",
      "reasoning": "TFDA 절대표현 순화 및 럭셔리 초월번역 사유"
    }
  ]
}
"""
        pass2_tmpl = """
당신은 정밀한 시각적 로컬라이제이션을 수행하는 이미지 인페인팅 AI입니다.
아래 [번역 매핑 데이터 JSON]을 바탕으로 단일 이미지를 생성하세요.

[엄격 렌더링 규칙 - 대만 정체자(繁體中文) 전용]
1. (KOR ERASING) 원본 한국어 텍스트 100% 지울 것.
2. (JSON APPLY) 오직 'target_text'의 대만 정체자만 렌더링할 것.
3. (FONT & LAYOUT) Noto Sans TC / 思源黑體 스타일로 렌더링하되, 한자 특성을 고려하여 한국어 대비 폰트 크기 10% 축소, 행간 15% 확장 적용.
4. (PACKAGE PRESERVATION) 본품 표면 영문/로고 100% 보존.
5. (🚨 CRITICAL: ABSOLUTE TRADITIONAL GLYPH ENFORCEMENT)
   - 절대 중국 본토 간체자(Simplified Chinese) 획수를 그리지 마십시오! 
   - 확산 모델의 간체자 쏠림(Drift)을 엄격히 차단하고, 반드시 획수가 많은 순수 번체자(繁體字/正體字) 글리프를 정확히 그리십시오:
     * 養 (O) vs 养 (X - 절대금지) -> 保養, 營養, 調理
     * 對 (O) vs 对 (X - 절대금지) -> 對策, 針對
     * 護 (O) vs 护 (X - 절대금지) -> 修護, 護理
     * 創 (O) vs 创 (X - 절대금지) -> 首創, 創造
     * 變 (O) vs 变 (X - 절대금지) -> 變得, 變化
     * 顯 (O) vs 显 (X - 절대금지) -> 明顯
     * 實 (O) vs 实 (X - 절대금지) -> 確實, 實驗
     * 體 (O) vs 体 (X - 절대금지) -> 體驗, 身體
     * 驗 (O) vs 验 (X - 절대금지) -> 體驗, 實驗
     * 緊 (O) vs 紧 (X - 절대금지) -> 緊緻
     * 緻 (O) vs 致 (X - 절대금지) -> 細緻, 緊緻
     * 膚 (O) vs 肤 (X - 절대금지) -> 肌膚, 膚質
     * 雙 (O) vs 双 (X - 절대금지) -> 雙重
     * 氣 (O) vs 气 (X - 절대금지) -> 空氣
     * 隊 (O) vs 队 (X - 절대금지) -> 團隊
     * 劃 (O) vs 划 (X - 절대금지) -> 企劃
     * 歲 (O) vs 岁 (X - 절대금지) -> 30歲
     * 乾 (O) vs 干 (X - 절대금지) -> 乾燥, 乾性
     * 華 (O) vs 华 (X - 절대금지) -> 精華液
     * 濕 (O) vs 湿 (X - 절대금지) -> 保濕
     * 鎖 (O) vs 锁 (X - 절대금지) -> 鎖水
     * 膠 (O) vs 胶 (X - 절대금지) -> 膠原蛋白
     * 纖 (O) vs 纤 (X - 절대금지) -> 纖維

[번역 매핑 데이터 JSON]
{json_data}
"""
    return pass1, pass2_tmpl


# =================================================================================
# 4. 고시정보 표 자동 HTML 렌더러 연동 및 DOCX 파싱 지원
# =================================================================================
def parse_docx_content(docx_path: str) -> List[Tuple[str, str]]:
    """DOCX 파일에서 항목-내용 쌍을 추출합니다."""
    import zipfile
    import xml.etree.ElementTree as ET

    items = []
    try:
        with zipfile.ZipFile(docx_path) as z:
            xml_content = z.read("word/document.xml")
            tree = ET.fromstring(xml_content)
            
            # 테이블 탐색
            ns = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
            tables = tree.findall(".//w:tbl", ns)
            if tables:
                for tbl in tables:
                    rows = tbl.findall(".//w:tr", ns)
                    for tr in rows:
                        cells = tr.findall(".//w:tc", ns)
                        if len(cells) >= 2:
                            c0_texts = [t.text for t in cells[0].findall(".//w:t", ns) if t.text]
                            c1_texts = [t.text for t in cells[1].findall(".//w:t", ns) if t.text]
                            lbl = "".join(c0_texts).strip()
                            val = "\n".join(["".join([t.text for t in p.findall(".//w:t", ns) if t.text]) for p in cells[1].findall(".//w:p", ns)]).strip()
                            if lbl and lbl != "항목":
                                items.append((lbl, val))
            
            # 테이블이 없거나 비어있는 경우 단락 파싱
            if not items:
                paragraphs = []
                for p in tree.findall(".//w:p", ns):
                    txt = "".join([t.text for t in p.findall(".//w:t", ns) if t.text]).strip()
                    if txt:
                        paragraphs.append(txt)
                
                # 라인 단위로 항목-내용 파싱
                i = 0
                while i < len(paragraphs):
                    p = paragraphs[i]
                    if p in ["상품상세정보", "항목", "내용"]:
                        i += 1
                        continue
                    if i + 1 < len(paragraphs):
                        items.append((p, paragraphs[i+1]))
                        i += 2
                    else:
                        items.append((p, ""))
                        i += 1
    except Exception as e:
        print(f"  ❌ [DOCX ERROR] 파싱 실패: {e}")
    return items


def render_notice_table(mapping_data: Dict[str, Any], lang_code: str, out_path: str, orig_width: int = 860) -> bool:
    """render_notice_table_standard.py 모듈을 활용하여 고선명 표 이미지를 렌더링합니다."""
    std_script_dir = os.path.join(PROJECT_ROOT, "00_공통자료")
    if std_script_dir not in sys.path:
        sys.path.insert(0, std_script_dir)

    try:
        import render_notice_table_standard as rnts
        items = []
        for row in mapping_data.get("translation_map", []):
            kor = row.get("kor", "")
            tgt = row.get("target_text", "")
            if ":" in tgt or "：" in tgt:
                parts = re.split(r"[:：]", tgt, 1)
                lbl = parts[0].strip()
                val = parts[1].strip() if len(parts) > 1 else ""
            elif ":" in kor or "：" in kor:
                parts = re.split(r"[:：]", kor, 1)
                lbl = parts[0].strip()
                val = tgt
            else:
                lbl = kor
                val = tgt
            items.append({"label": lbl, "value": val})

        title_map = {
            "EN": "PRODUCT DETAILS",
            "JP": "商品基本情報",
            "CN": "商品基本信息",
            "TW": "商品基本資訊"
        }
        title = title_map.get(lang_code, "PRODUCT DETAILS")
        return rnts.render_notice_table_to_png(title, items, out_path, lang=lang_code)
    except Exception as e:
        print(f"  -> [TABLE RENDER FAIL] 표 렌더러 예외: {e}")
        return False


def process_docx_notice_table(client: genai.Client, docx_path: str, out_path: str, lang_code: str) -> bool:
    """DOCX 고시정보표를 번역하여 표준 고선명 HTML 테이블 PNG로 렌더링합니다."""
    print(f"\n================================================================================")
    print(f"📄 [DOCX 고시정보표 번역] {os.path.basename(docx_path)} -> [{LANG_CONFIGS[lang_code]['name']}]")
    print(f"================================================================================")
    
    raw_items = parse_docx_content(docx_path)
    if not raw_items:
        print(f"  ❌ [ERROR] DOCX 파일에서 고시정보 항목을 추출하지 못했습니다.")
        return False

    prompt_en = """
You are a senior regulatory affairs and e-commerce localization expert.
Translate the following Korean cosmetic product details (specifications table) into professional English for Amazon / Sephora US.

[CRITICAL INSTRUCTION: STANDARD FIELD NAME MAPPING]
You MUST strictly map the following Korean labels to these standardized global beauty e-commerce terms. Do not use direct translations if they deviate from this list:
- 용량 또는 중량 (내용물의 용량): Size / Net Wt.
- 제품 주요 사양: Skin Type
- 사용기한 또는 개봉 후 사용기간: Shelf Life / PAO
- 사용방법: Directions
- 화장품제조업자 및 책임판매업자: Manufacturer / Distributed by
- 제조국: Country of Origin
- 전성분: Ingredients (국제화장품원료집(INCI) 및 한국화장품성분사전(KCID) 표준 기반 미국 FDA/PCPC 표기법 및 띄어쓰기 규격 강제 적용)
- 기능성 화장품 심사 필 유무: Functional Cosmetics Review Status
- 사용할 때의 주의사항: Precautions for Use / Cautions
- 품질보증기준: Quality Assurance Standard
- 소비자 상담 전화번호: Customer Service / Contact (MUST format Korean phone number with international country code, e.g. +82-2-6743-3206)

Output MUST be a JSON object:
{
  "title": "PRODUCT DETAILS",
  "items": [
    {"label": "Volume / Net Weight", "value": "25ml"},
    ...
  ]
}
"""

    prompt_cn = """
你是资深化妆品法规与电商本地化专家。请将以下韩国化妆品产品详细信息（中文告示表）翻译为规范的简体中文，严格遵守中国国家药监局(NMPA)及新广告法规范。

[CRITICAL INSTRUCTION: STANDARD FIELD NAME MAPPING]
You MUST strictly map the following Korean labels to these standardized Chinese e-commerce/legal terms. Do not use direct translations if they deviate from this list:
- 용량 또는 중량 (내용물의 용량): 净含量 / 容量
- 제품 주요 사양: 适用肤质 / 产品规格
- 사용기한 또는 개봉 후 사용기간: 使用期限 / 保质期
- 사용방법: 使用方法
- 화장품제조업자 및 책임판매업자: 化妆品生产企业 / 责任销售商
- 제조국: 原产国 / 产地
- 전성분: 全成分 (INCI 및 KCID 기반 중국 국가약품감독관리국(NMPA) 표준 명칭 및 띄어쓰기 규격 강제 적용)
- 기능성 화장품 심사 필 유무: 特殊用途化妆品审查状态 (如：已完成审查 (美白、改善皱纹双重功效))
- 사용할 때의 주의사항: 使用注意事项
- 품질보증기준: 质量保证标准
- 소비자 상담 전화번호: 消费者咨询电话 (电话号码必须带有韩国国际区号，格式为：+82-2-6743-3206)

输出必须为纯 JSON 格式：
{
  "title": "商品基本信息",
  "items": [
    {"label": "净含量", "value": "25ml"},
    ...
  ]
}
"""

    prompt_jp = """
あなたは日本の化粧品薬機法およびQoo10 Japanの専門家です。以下の韓国化粧品の商品基本情報表を自然で正確な日本語に翻訳してください。

[CRITICAL INSTRUCTION: STANDARD FIELD NAME MAPPING]
You MUST strictly map the following Korean labels to these standardized Japanese e-commerce/legal terms. Do not use direct translations if they deviate from this list:
- 용량 또는 중량 (내용물의 용량): 内容量
- 제품 주요 사양: お肌のタイプ / 対象肌
- 사용기한 또는 개봉 후 사용기간: 使用期限
- 사용방법: ご使用方法
- 화장품제조업자 및 책임판매업자: 製造販売元
- 제조국: 原産国
- 전성분: 全成分 (INCI 및 KCID 기반 일본 화장품공업연합회(JCIA) 표준 명칭 및 띄어쓰기 규격 강제 적용)
- 기능성 화장품 심사 필 유무: 医薬部外品承認 / 機能性化粧品審査
- 사용할 때의 주의사항: ご使用上の注意
- 품질보증기준: 品質保証基準
- 소비자 상담 전화번호: お客様相談窓口 (お客様相談電話番号は必ず韓国国際国番号付き +82-2-6743-3206 で表記してください)

出力は純粋なJSONオブジェクトである必要があります：
{
  "title": "商品基本情報",
  "items": [
    {"label": "内容量", "value": "25ml"},
    ...
  ]
}
"""
    prompt_tw = """
你是資深化妝品法規與電商本地化專家。請將以下產品詳細資訊翻譯為規範的繁體中文（台灣/香港TFDA標準）。

[CRITICAL INSTRUCTION: STANDARD FIELD NAME MAPPING]
You MUST strictly map the following Korean labels to these standardized Taiwanese e-commerce/legal terms. Do not use direct translations if they deviate from this list:
- 용량 또는 중량 (내용물의 용량): 淨含量 / 容量
- 제품 주요 사양: 適用膚質
- 사용기한 또는 개봉 후 사용기간: 保存期限
- 사용방법: 使用方法
- 화장품제조업자 및 책임판매업자: 製造商 / 責任銷售商
- 제조국: 產地
- 전성분: 全成分 (INCI 및 KCID 기반 대만 위생복리부(TFDA) 표준 명칭 및 띄어쓰기 규격 강제 적용)
- 기능성 화장품 심사 필 유무: 含藥化妝品許可 / 特殊用途化妝品審查
- 사용할 때의 주의사항: 注意事項
- 품질보증기준: 售後服務 / 質量保證
- 소비자 상담 전화번호: 客服專線 (客服諮詢電話必須帶有韓國國際區號，例如：+82-2-6743-3206)

輸出必須為純 JSON 格式：
{
  "title": "商品基本資訊",
  "items": [
    {"label": "容量 / 淨含量", "value": "25ml"},
    ...
  ]
}
"""
    if lang_code == "KR":
        print(f"  🎨 [한국어 원본 고시표 렌더러 가동] Gemini 3.1 Pro 지능형 정제 및 860px 렌더링...", flush=True)
        try:
            import render_notice_table_korean as rntk
        except ImportError:
            sys.path.insert(0, SCRIPT_DIR)
            import render_notice_table_korean as rntk
        items_kr = [{"label": lbl, "value": val} for lbl, val in raw_items if lbl != "항목"]
        rntk.render_korean_notice_table("상품 상세 정보", items_kr, out_path, max_height=2580, use_gemini=True)
        base_name, ext = os.path.splitext(out_path)
        part1_path = f"{base_name}_Part1{ext}"
        part2_path = f"{base_name}_Part2{ext}"
        if os.path.exists(out_path) or (os.path.exists(part1_path) and os.path.exists(part2_path)):
            print(f"  🎉 [SUCCESS] 한국어 원본 고시정보 표 PNG 렌더링 완료: {os.path.basename(out_path)}")
            return True
        else:
            print(f"  ❌ [ERROR] 한국어 원본 고시정보 표 PNG 렌더링 실패")
            return False

    p_map = {"EN": prompt_en, "CN": prompt_cn, "JP": prompt_jp, "TW": prompt_tw}
    selected_prompt = p_map.get(lang_code, prompt_en)

    input_text = "\n".join([f"[{lbl}]\n{val}" for lbl, val in raw_items])
    full_prompt = f"{selected_prompt}\n\n[입력 고시정보 표 데이터]\n{input_text}"

    print(f"  🔍 [PASS 1] 고시정보 표 텍스트 다국어 번역 및 표준화 중 ({MODEL_PRO})...", flush=True)
    try:
        resp = client.models.generate_content(
            model=MODEL_PRO,
            contents=[full_prompt],
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                temperature=0.1
            )
        )
        res_json = json.loads(resp.text.strip())
        items = res_json.get("items", [])
        title = res_json.get("title", LANG_CONFIGS[lang_code]["name"])
        
        # [사용자 규칙 강제]: 고객상담 전화번호는 반드시 +82 국제전화 국가번호로 표기
        for item in items:
            lbl = item.get("label", "")
            val = item.get("value", "")
            if any(k in lbl.lower() for k in ["customer", "contact", "phone", "电话", "電話", "상담", "문의"]):
                if "02-" in val or "02)" in val or "02." in val or "6743-3206" in val:
                    val_cleaned = re.sub(r"^02[-.)\s]*", "+82-2-", val)
                    if "+82" not in val_cleaned and "6743-3206" in val_cleaned:
                        val_cleaned = "+82-2-6743-3206"
                    item["value"] = val_cleaned

        print(f"  ✅ [PASS 1 완료] 총 {len(items)}개 고시 항목 번역 완료 (국제 전화번호 +82 규격 동기화)")
    except Exception as e:
        print(f"  ❌ [ERROR] DOCX 번역 실패: {e}")
        return False

    # 렌더링 호출
    print(f"  🎨 [PASS 2] 고선명 HTML 표준 헤드리스 렌더러 가동...", flush=True)
    std_script_dir = os.path.join(PROJECT_ROOT, "00_공통자료")
    if std_script_dir not in sys.path:
        sys.path.insert(0, std_script_dir)
    import render_notice_table_standard as rnts
    success = rnts.render_notice_table_to_png(title, items, out_path, lang=lang_code)
    
    base_name, ext = os.path.splitext(out_path)
    part1_path = f"{base_name}_Part1{ext}"
    part2_path = f"{base_name}_Part2{ext}"

    if success and (os.path.exists(out_path) or (os.path.exists(part1_path) and os.path.exists(part2_path))):
        print(f"  🎉 [SUCCESS] 고시정보 표 PNG 렌더링 완료: {os.path.basename(out_path)}")
        return True
    else:
        print(f"  ❌ [ERROR] 고시정보 표 PNG 렌더링 실패")
        return False


# =================================================================================
# 5. 핵심 번역 파이프라인
# =================================================================================
def process_single_image(client: genai.Client, in_path: str, out_path: str, lang_code: str) -> bool:
    print(f"\n================================================================================")
    print(f"🖼️ [번역 시작] {os.path.basename(in_path)} -> [{LANG_CONFIGS[lang_code]['name']}]")
    print(f"================================================================================")

    try:
        original_image = Image.open(in_path)
        original_image.load()
        orig_w, orig_h = original_image.size
    except Exception as e:
        print(f"  ❌ [ERROR] 이미지 파일 로드 실패: {e}")
        return False

    pass1_prompt, pass2_tmpl = build_prompts(lang_code)

    # PASS 1: 텍스트 추출 및 번역 매핑 (재시도 로직 포함)
    p1_json = None
    for attempt in range(1, 4):
        print(f"  🔍 [PASS 1] 텍스트 스캔 및 다국어 매핑 추출 중 ({MODEL_PRO}, 시도 {attempt}/3)...", flush=True)
        try:
            response_p1 = client.models.generate_content(
                model=MODEL_PRO,
                contents=[original_image, pass1_prompt],
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    temperature=0.1
                )
            )
            p1_text = response_p1.text.strip()
            p1_json = json.loads(p1_text)
            break
        except Exception as e:
            print(f"  ⚠️ [WARN] PASS 1 시도 {attempt} 실패: {e}")
            if attempt < 3:
                wait_t = 15 * attempt
                print(f"  ⏳ {wait_t}초 대기 후 재시도합니다...", flush=True)
                time.sleep(wait_t)
            else:
                print(f"  ❌ [ERROR] PASS 1 최종 실패")
                return False

    t_map = p1_json.get("translation_map", [])
    print(f"  ✅ [PASS 1 완료] 총 {len(t_map)}개 텍스트 블록 추출 완료")
    for i, item in enumerate(t_map[:3]):
        print(f"     ({i+1}) 원문: {item.get('kor', '')[:30]} -> 번역: {item.get('target_text', '')[:30]}")
    if len(t_map) > 3:
        print(f"     ... 외 {len(t_map)-3}개 항목")

    # 고시정보표 감지 시 분기 처리
    is_table = p1_json.get("is_table", False)
    fname_lower = os.path.basename(in_path).lower()
    if is_table or "notice" in fname_lower or "상세정보" in fname_lower or "spec" in fname_lower or "details" in fname_lower:
        print(f"  📊 [TABLE DETECTED] 고시정보표 레이아웃 감지 -> HTML 표준 렌더러 분기 가동")
        rendered = render_notice_table(p1_json, lang_code, out_path, orig_width=orig_w)
        if rendered:
            print(f"  🎉 [SUCCESS] 고선명 표 이미지 생성 완료: {os.path.basename(out_path)}")
            return True
        else:
            print(f"  ⚠️ [INFO] HTML 표 렌더러 실패 -> 일반 인페인팅 모드로 폴백 진행")

    # PASS 2: 신경망 인페인팅 렌더링 (지수 백오프 재시도 포함)
    clean_json_str = json.dumps(p1_json, ensure_ascii=False, indent=2)
    pass2_prompt = pass2_tmpl.format(json_data=clean_json_str)

    for attempt in range(1, 4):
        print(f"  🎨 [PASS 2] 시각적 신경망 인페인팅 렌더링 가동 ({MODEL_FLASH_IMAGE}, 시도 {attempt}/3)...", flush=True)
        try:
            response_p2 = client.models.generate_content(
                model=MODEL_FLASH_IMAGE,
                contents=[original_image, pass2_prompt],
                config=types.GenerateContentConfig(
                    response_modalities=["IMAGE"],
                    temperature=0.2
                )
            )

            rendered_img_bytes = None
            for part in response_p2.candidates[0].content.parts:
                if part.inline_data:
                    rendered_img_bytes = part.inline_data.data
                    break

            if not rendered_img_bytes:
                raise ValueError("PASS 2 이미지 데이터 반환 없음")

            img = Image.open(io.BytesIO(rendered_img_bytes))
            if img.size != (orig_w, orig_h):
                img = img.resize((orig_w, orig_h), Image.Resampling.LANCZOS)

            os.makedirs(os.path.dirname(out_path), exist_ok=True)
            img.save(out_path, format="PNG", optimize=True)
            print(f"  🎉 [SUCCESS] 렌더링 완료 및 저장: {os.path.basename(out_path)} ({orig_w}x{orig_h})")
            return True
        except Exception as e:
            print(f"  ⚠️ [WARN] PASS 2 인페인팅 렌더링 실패: {e}")
            if attempt < 3:
                wait_time = 15 * attempt
                print(f"  ⏳ {wait_time}초 대기 후 PASS 2 재시도합니다... ({attempt}/3)")
                time.sleep(wait_time)
            else:
                print("  ❌ [ERROR] PASS 2 인페인팅 최종 실패.")
                return False
    return False


def run_translation_batch_for_folder(client: genai.Client, current_source_dir: str, target_lang: str, product_name: str):
    """지정된 단일 리프 폴더(current_source_dir)에 대해 이미지 및 DOCX 번역 배치를 실행합니다."""
    config = LANG_CONFIGS[target_lang]
    target_dir = os.path.join(DEFAULT_OUTPUT_BASE, f"{product_name}_{config['folder_name']}")
    os.makedirs(target_dir, exist_ok=True)

    print(f"================================================================================")
    print(f"📂 [작업 대상 폴더] {current_source_dir}")
    print(f"📦 [상품 식별명] {product_name}")
    print(f"🌐 [도착 언어] {config['name']}")
    print(f"📁 [저장 위치] {target_dir}")
    print(f"================================================================================\n")

    # 1. 이미지 파일 처리
    image_files = sorted([f for f in os.listdir(current_source_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')) and not f.startswith('~')])
    docx_files = sorted([f for f in os.listdir(current_source_dir) if f.lower().endswith('.docx') and not f.startswith('~')])

    total_tasks = len(image_files) + len(docx_files)
    if total_tasks == 0:
        print(f"⚠️ [WARNING] '{current_source_dir}' 폴더에 처리할 이미지나 DOCX 파일이 없습니다.")
        return

    current_idx = 0
    success_count = 0

    for img_name in image_files:
        current_idx += 1
        in_path = os.path.join(current_source_dir, img_name)
        stem = os.path.splitext(img_name)[0]
        out_name = f"{stem}{config['tag']}"
        out_path = os.path.join(target_dir, out_name)

        if os.path.exists(out_path):
            print(f"  ⚠️ [SKIP] 이미 결과물이 존재함: {out_name}")
            success_count += 1
            continue

        print(f"\n[{current_idx}/{total_tasks}] 이미지 작업 시작: {img_name}")
        success = process_single_image(client, in_path, out_path, target_lang)
        if success:
            success_count += 1

        if current_idx < total_tasks:
            print("⏳ API 쿼터 안전 대기 (12초)...", flush=True)
            time.sleep(12)

    # 2. DOCX 고시정보표 처리
    for docx_name in docx_files:
        current_idx += 1
        in_path = os.path.join(current_source_dir, docx_name)
        stem = os.path.splitext(docx_name)[0]
        out_name = f"{stem}{config['tag']}"
        out_path = os.path.join(target_dir, out_name)

        if os.path.exists(out_path):
            print(f"  ⚠️ [SKIP] 이미 결과물이 존재함: {out_name}")
            success_count += 1
            continue

        print(f"\n[{current_idx}/{total_tasks}] DOCX 작업 시작...")
        success = process_docx_notice_table(client, in_path, out_path, target_lang)
        if success:
            success_count += 1

        if current_idx < total_tasks:
            print("⏳ API 쿼터 안전 대기 (12초)...", flush=True)
            time.sleep(12)

    # 3. SEO / GEO / AEO 메타데이터 TXT 자동 생성
    generate_seo_geo_aeo_txt(client, current_source_dir, target_dir, target_lang, product_name)

    print(f"\n🏁 [{config['name']}] 번역 및 SEO/GEO/AEO 생성 완료: 총 {total_tasks}개 중 {success_count}개 성공!")
    print(f"📂 저장 경로: {target_dir}\n")


def generate_seo_geo_aeo_txt(client: genai.Client, source_dir: str, target_dir: str, target_lang: str, product_name: str):
    """번역 완료 후 해당 국가 언어에 맞춘 SEO 상품명(100자 이내), GEO 및 AEO TXT 문서를 자동 생성합니다."""
    config = LANG_CONFIGS[target_lang]
    txt_filename = f"{product_name}_{config['folder_name']}_SEO_GEO_AEO.txt"
    txt_path = os.path.join(target_dir, txt_filename)

    print(f"\n================================================================================")
    print(f"📝 [SEO / GEO / AEO 생성] {txt_filename} -> [{config['name']}]")
    print(f"================================================================================")

    # 1. 소스 폴더 내 텍스트/고시표 정보 및 대표 이미지 수집
    context_texts = []
    docx_files = [os.path.join(source_dir, f) for f in os.listdir(source_dir) if f.lower().endswith('.docx') and not f.startswith('~')]
    if docx_files:
        items = parse_docx_content(docx_files[0])
        context_texts.append("[고시정보/전성분 데이터]\n" + "\n".join([f"{k}: {v}" for k, v in items]))

    # 이미지 목록 확인
    image_files = [f for f in os.listdir(source_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp'))]
    context_texts.append(f"[상품 식별명] {product_name}")
    context_texts.append(f"[이미지 파일 수] {len(image_files)}장 구성")

    # 대표 이미지 1장 로드 (있는 경우 멀티모달 컨텍스트로 주입)
    content_payload = []
    if image_files:
        first_img_path = os.path.join(source_dir, sorted(image_files)[0])
        try:
            sample_img = Image.open(first_img_path)
            content_payload.append(sample_img)
        except Exception:
            pass

    full_context = "\n\n".join(context_texts)

    prompt_en = f"""
You are an expert Global E-Commerce Product Copywriter and Search Optimization Specialist for Amazon US, Shopee, and Global Online Marketplaces.

Based on the provided product details and image, generate a comprehensive, highly polished, consumer-facing product detail and search-optimized document in ENGLISH.

[CRITICAL INSTRUCTION - CONSUMER-FACING PROFESSIONAL COPYWRITING & NO AI JARGON]
- This document is intended for direct publication on product detail pages (PDP) where global consumers and buyers will read it.
- NO MARKDOWN SYMBOLS ALLOWED: E-commerce platforms block special characters. Do NOT use **, ##, ###, or -. Use standard Arabic numerals (1., 2., 3.) for main sections, and use closing parenthesis numbers (1), 2), 3), 4), 5)) exclusively for all sub-items and lists.
- ABSOLUTELY PROHIBIT internal AI/engineering jargon such as "Generative AI", "GEO", "AEO", "Knowledge Graph Dossier", "AI Models", "Large Language Models", "Semantic Entity Anchors", "SECTION 1/2/3", or folder names like "[05_Multi-Corrective-Eye-Cream]".
- Every section title and subheading MUST be a clear, professional, consumer-friendly e-commerce section title that defines exactly what the section contains.

[STANDARD 3-SECTOR DOCUMENT STRUCTURE]
1. Sector 1 Header: 1. Official Global E-Commerce Product Title (Under 100 Characters)
   - Strict Formula: [Brand Name] [Key Active Ingredient / Patent] [Product Type] [Core Benefit / Solution] [Volume]
   - MUST be UNDER 100 CHARACTERS (including spaces). Provide exact character count.
   
2. Sector 2 Header: 2. Core Value & Active Ingredient Summary
   - (CRITICAL: ULTRA-COMPACT MICRO-SUMMARY. NO PARAGRAPHS. ONLY KEYWORDS AND VERY SHORT PHRASES. Maximum 5 lines total for Sector 2.)
   - Brand: [Brand Name] ([1-line philosophy])
   - Core Ingredients: [List 3-4 key ingredients separated by commas]
   - Key Benefits: [List 3-4 key benefits separated by commas]
   - Formulation: [List 2-3 key formulation features separated by commas]
   - Search Tags: [Comma-separated 10 keywords]
     
3. Sector 3 Header: 3. Product Usage Guide & Frequently Asked Questions (FAQ)
   - Top 5 Consumer Q&A Pairs with clear, descriptive question headings:
     - Q1. [Key Benefits & Visible Improvements]: What are the primary skin improvements delivered by [Product Name]?
     - Q2. [Skincare Routine & Application Method]: How and when should [Product Name] be applied for maximum absorption?
     - Q3. [Skin Compatibility & Hypoallergenic Safety]: Is this high-potency formula suitable for sensitive skin?
     - Q4. [Active Ingredient Synergy]: How do [Key Active Ingredients] work together to smooth wrinkles and firm skin?
     - Q5. [Storage Precautions & Customer Support]: How to store the product and official customer service contact (+82-2-6743-3206).

[CONTEXT DATA]
{full_context}

Output format MUST be clean, well-structured plain text with Markdown headers.
"""

    prompt_cn = f"""
你是全球顶尖的跨境电商资深文案与搜索优化专家，服务于亚马逊中国、天猫国际、京东全球购等国际电商平台。

请根据提供的产品信息与图像，生成一份专业、规范、供直接展示在商品详情页（PDP）给消费者阅读的【简体中文】商品搜索与产品详情方案文档。

【核心要求：面向消费者的专业电商文案，全面剔除 AI / 工程化术语】
- 本文档将直接用于商品详情页与电商页面，供广大终端消费者与买家阅读。
- 严禁使用 Markdown 特殊符号（如 **, ##, ###, - 等）。电商平台不支持这些符号。主标题必须仅使用阿拉伯数字（1., 2., 3.），而所有下级特征、成分及列表项必须使用带右括号的数字（1), 2), 3), 4), 5)）进行标记。
- 严禁出现“生成式 AI”、“GEO”、“AEO”、“大模型知识图谱”、“语义实体锚定”、“第一部分/第二部分/第三部分”、“SECTION 1/2/3”等任何偏向开发者或内部算法的死板术语。
- 每一个大标题与子标题，必须是清晰定义该板块内容、兼顾高权重搜索关键词与消费者阅读体验的【专业电商详情页标题】。

【标准三段式详情结构】
1. 第一板块标题：1. 跨境电商官方高转化商品标题 (严格控制在100字符以内)
   - 标准公式：[品牌名] [核心专利/核心成分] [产品正规品名] [核心功效/定位] [净含量]
   - 必须严格控制在 100 字符以内（含空格与标点），并注明字符数。
   
2. 第二板块标题：2. 核心价值与成分科技摘要
   - (核心要求：极简微型摘要！严禁段落！只能使用关键词和极短句！整个第二板块最多5行字。)
   - 品牌内核: [品牌名] ([一句话哲理])
   - 核心成分: [逗号分隔列出3-4个核心成分]
   - 核心功效: [逗号分隔列出3-4个核心功效]
   - 配方特点: [逗号分隔列出2-3个配方特点]
   - 搜索标签: [10个关键词，逗号分隔]
     
3. 第三板块标题：3. 商品使用指南与消费者常见问题解答 (FAQ)
   - 5大消费者高频关切 Q&A 问答对（问题标题必须为清晰的消费指南标题）：
     - Q1. 【核心功效与改善效果】：【产品品名】能带来怎样的紧致淡纹与焕亮改善？
     - Q2. 【护肤步骤与正确手法】：含有高浓度活性成分的【产品品名】早晚使用顺序与涂抹手法？
     - Q3. 【肤质适用与温和性说明】：高浓度活性配方是否适用于敏感肌及所有肤质？
     - Q4. 【成分协同与紧致机理】：【核心复合成分】如何协同解决眼周细纹与眼窝凹陷？
     - Q5. 【产品保存与官方咨询】：产品保存注意事项与官方售后客服热线 (+82-2-6743-3206)。

【上下文数据】
{full_context}

输出格式必须为结构清晰、排版优雅的纯文本。
"""

    prompt_jp = f"""
日本のQoo10 Japan、楽天市場、Amazon Japan等の商品詳細ページ（PDP）にそのまま掲載できる、消費者向けに洗練された検索最適化＆製品紹介ドキュメントを作成してください。
「生成AI」「GEO」「AEO」「ナレッジグラフ」等の開発者・AI用語は完全に排除し、消費者が読んで魅力を感じる専門的かつ分かりやすい見出しで構成してください。
- Markdown記号（**, ##, ###, - 等）は使用禁止です。ECサイトのシステムでエラーになるため、大項目はアラビア数字（1., 2., 3.）を使用し、下位の特性や成分リスト等には必ず片括弧付きの数字（1), 2), 3), 4), 5)）を使用してください。

1. 見出し1：1. 公式EC検索最適化 商品タイトル（100文字以内厳格）
2. 見出し2：2. ブランドストーリー＆高濃度成分サイエンス：【独自Liftderm 10%と肌構造メカニズム】（主要キーワード10選・他社比較の強み含む）
3. 見出し3：3. ご使用方法＆よくあるご質問 FAQ（5大Q&A、公式サポート：+82-2-6743-3206）

【製品コンテキスト】
{full_context}
"""

    prompt_tw = f"""
以跨境電商商品詳情頁（PDP）向終端消費者展示為核心，生成【繁體中文】商品搜尋優化與產品特色說明文件。
全面剔除「生成式AI」、「GEO」、「AEO」、「大模型知識圖譜」等工程技術術語，採用消費者友善且具高度說服力的電商專屬章節標題。
- 嚴禁使用 Markdown 特殊符號（如 **, ##, ###, - 等），避免電商平台系統錯誤。只能使用阿拉伯數字（1., 2., 3.）及純文字排版。

1. 標題一：1. 跨境電商官方高轉化商品標題（嚴格100字內）
2. 標題二：2. 品牌科研故事與核心成分機制：【Liftderm 10% 專利科技與抗老科學】（含10大核心關鍵字、獨家優勢）
3. 標題三：3. 商品使用指南與顧客常見問題 FAQ（5大Q&A，售後服務專線：+82-2-6743-3206）

【產品上下文】
{full_context}
"""
    p_map = {"EN": prompt_en, "CN": prompt_cn, "JP": prompt_jp, "TW": prompt_tw}
    
    prompt_kr = f"""
대한민국 국내 이커머스(네이버 스마트스토어, 쿠팡, 올리브영 등) 상품 상세페이지(PDP)에 전시될 소비자용 제품 안내 및 검색 최적화(SEO) 문서를 [한국어]로 작성해주세요.
개발자나 AI를 의미하는 용어(생성형 AI, GEO, AEO, 지식그래프 등)는 절대 배제하고, 소비자가 읽었을 때 매력적이고 전문적인 이커머스 전용 문안으로 작성해야 합니다.
- 마크다운 특수기호(**, ##, ###, - 등) 사용을 절대 금지합니다. (쇼핑몰 플랫폼 등록 시 오류 발생 방지). 메인 섹션 제목은 1., 2., 3. 으로 표기하되, 2번 핵심 가치나 3번 FAQ의 하위 특성 정보(리스트)들은 반드시 1), 2), 3), 4), 5) 와 같이 닫는 괄호를 사용하여 순번을 마킹하세요.

1. 섹션 1: 1. 공식 이커머스 최적화 상품명 (100자 이내)
2. 섹션 2: 2. 핵심 가치 및 성분 사이언스 마이크로 요약 (문단 금지, 단어/짧은 구 형식으로 5줄 이내 핵심만 요약)
3. 섹션 3: 3. 사용 가이드 및 자주 묻는 질문 FAQ (고객센터 번호: 02-6743-3206 포함 5개 Q&A)

[제품 데이터]
{full_context}
"""
    p_map["KR"] = prompt_kr

    selected_prompt = p_map.get(target_lang, prompt_en)
    content_payload.append(selected_prompt)

    try:
        print(f"  🔍 [AI 추론] {config['name']} SEO / GEO / AEO 생성 중 ({MODEL_PRO})...", flush=True)
        response = client.models.generate_content(
            model=MODEL_PRO,
            contents=content_payload,
            config=types.GenerateContentConfig(
                temperature=0.2
            )
        )
        generated_text = response.text.strip()

        # 파일 저장
        os.makedirs(target_dir, exist_ok=True)
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(generated_text)
        print(f"  🎉 [SUCCESS] SEO / GEO / AEO TXT 저장 완료: {txt_filename}")
        return True
    except Exception as e:
        print(f"  ❌ [ERROR] SEO / GEO / AEO 생성 실패: {e}")
        return False


def find_target_leaf_folders(base_dir: str) -> List[Tuple[str, str]]:
    """이미지나 docx가 존재하는 실제 리프 폴더들을 탐색하여 (폴더경로, 상품명) 목록을 반환합니다."""
    leaf_dirs = []
    for root, dirs, files in os.walk(base_dir):
        valid_files = [f for f in files if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp', '.docx')) and not f.startswith('~')]
        if valid_files:
            rel = os.path.relpath(root, base_dir)
            if rel == ".":
                pname = extract_product_name_from_files(valid_files, os.path.basename(base_dir))
            else:
                # 최상위 서브폴더 기준 또는 현재 폴더 기준 이름 추출
                top_part = rel.split(os.sep)[0]
                pname = extract_product_name_from_files(valid_files, top_part)
            leaf_dirs.append((root, pname))
    return leaf_dirs


def run_translation_batch(client: genai.Client, source_dir: str, target_lang: str):
    """source_dir 내에 서브폴더나 중첩 폴더를 탐색하여 모든 대상 리프 폴더를 번역합니다."""
    leaf_folders = find_target_leaf_folders(source_dir)
    if not leaf_folders:
        print(f"⚠️ [WARNING] '{source_dir}' 폴더에 처리할 이미지나 DOCX 파일이 없습니다.")
        return

    for sdir, pname in leaf_folders:
        run_translation_batch_for_folder(client, sdir, target_lang, pname)


# =================================================================================
# 6. 메인 실행 및 대화형 사용자 질의응답
# =================================================================================
def main():
    parser = argparse.ArgumentParser(description="multilingual_text_in_image_translation")
    parser.add_argument("--source", default=DEFAULT_INPUT_DIR, help="원본 이미지 디렉터리")
    parser.add_argument("--lang", choices=["EN", "JP", "CN", "TW", "ALL"], default=None, help="도착 언어 코드")
    args = parser.parse_args()

    source_dir = os.path.abspath(args.source)
    os.makedirs(source_dir, exist_ok=True)

    chosen_lang = args.lang
    if not chosen_lang:
        # 하위 이미지 총 개수 카운트
        image_count = 0
        for root, _, files in os.walk(source_dir):
            image_count += len([f for f in files if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp'))])

        print("\n" + "=" * 76)
        print(" 🌐 multilingual_text_in_image_translation")
        print("=" * 76)
        print(f" 📂 [공통 인풋 폴더] : {source_dir}")
        print(f" 🖼️ [감지된 원본 이미지] : 총 {image_count}개")
        print("-" * 76)
        print(" 번역할 도착 언어를 선택하세요:")
        print("   [1] 🇺🇸 영어 (EN - Amazon / Shopee US 초월번역 + Montserrat)")
        print("   [2] 🇯🇵 일본어 (JP - Qoo10 Japan / 후생노동성 56종 약기법 준수)")
        print("   [3] 🇨🇳 중국어 간체 (CN - 중국 본토 신광고법 및 NMPA 규정 준수)")
        print("   [4] 🇹🇼 중국어 번체 (TW - 대만/홍콩 TFDA 규정 준수)")
        print("   [5] 🌐 전체 언어 일괄 번역 (EN -> JP -> CN -> TW 순차 실행)")
        print("   [Q] 종료 (Quit)")
        print("=" * 76)

        while True:
            choice = input(" 👉 번호를 입력하세요 (1/2/3/4/5/Q): ").strip().upper()
            if choice == "1":
                chosen_lang = "EN"
                break
            elif choice == "2":
                chosen_lang = "JP"
                break
            elif choice == "3":
                chosen_lang = "CN"
                break
            elif choice == "4":
                chosen_lang = "TW"
                break
            elif choice == "5":
                chosen_lang = "ALL"
                break
            elif choice in ["Q", "QUIT", "EXIT"]:
                print("번역 작업을 취소하고 종료합니다.")
                sys.exit(0)
            else:
                print(" ⚠️ 잘못된 입력입니다. 1, 2, 3, 4, 5 또는 Q를 입력하세요.")

    client = load_credentials()

    if chosen_lang == "ALL":
        for lang in ["EN", "JP", "CN", "TW"]:
            run_translation_batch(client, source_dir, lang)
    else:
        run_translation_batch(client, source_dir, chosen_lang)


if __name__ == "__main__":
    main()
