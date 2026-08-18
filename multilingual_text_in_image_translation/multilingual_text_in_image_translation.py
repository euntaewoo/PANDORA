"""
===================================================================================
🌐 multilingual_text_in_image_translation.py
-----------------------------------------------------------------------------------
• Purpose: multilingual_text_in_image_translation
• Location: multilingual_text_in_image_translation/multilingual_text_in_image_translation.py
• Features:
    1. 단일 공통 인풋 폴더(01_번역대상_원본) 기준 구동
    2. 실행 시 도착 언어(EN, JP, CN, TW, ALL) 대화형 질의응답 선택
    3. 도착어별 규정/법률(영어 초월번역, 일본 약기법 56종, 중국 신광고법) 자동 적용
    4. 표(고시표/성분표) 자동 감지 시 HTML 표준 헤드리스 렌더러로 고선명 분기 처리
    5. 결과물을 02_번역결과_최종/[언어명] 폴더로 자동 분류 저장
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
# 서브폴더 안에 위치하므로 상위 폴더를 PROJECT_ROOT로 탐색
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
    return "1. 肌を整える\n2. 肌荒れを防ぐ\n3. 皮膚에うるおいを与える 등 56종"


# =================================================================================
# 3. 언어별 프롬프트 생성기 (Pass 1 & Pass 2)
# =================================================================================
def build_prompts(lang_code: str) -> Tuple[str, str]:
    if lang_code == "EN":
        pass1 = """
첨부된 이미지는 이커머스 상세페이지 또는 제품 이미지입니다.
당신은 아마존(Amazon US), 쇼피(Shopee) 등 글로벌 최상위 이커머스 플랫폼의 수석 영문 카피라이터이자 현지화/초월번역(Transcreation) 최고 전문가입니다.

[번역 지침]
1. 단순 1:1 직역을 금지하고, 미국/글로벌 소비자가 읽었을 때 극도로 자연스럽고 매력적인 프리미엄 영문 카피로 초월번역(Transcreation)하세요.
2. 제품 본품(용기, 튜브, 박스)에 적힌 영문 텍스트(예: 브랜드명, 제품 영문명)는 번역 매핑에 넣지 마세요.
3. 이미지 내의 모든 한국어 텍스트는 단 하나도 빠짐없이 100% 추출하세요.
4. 만약 이미지가 고시정보표(Product Details/Specifications 테이블)인 경우, table_mode: true로 설정하고 표 안의 각 행(label과 value)을 정확히 분리 추출하세요.

출력은 반드시 순수 JSON이어야 합니다:
{
  "is_table": false,
  "translation_map": [
    {
      "kor": "한국어 원문",
      "target_text": "세련된 프리미엄 영문 번역문",
      "reasoning": "초월번역 및 카피라이팅 근거"
    }
  ]
}
"""
        pass2_tmpl = """
당신은 정밀한 시각적 로컬라이제이션을 수행하는 이미지 인페인팅 AI입니다.
첨부된 원본 이미지의 배경, 텍스처, 제품 누끼, 색상 톤을 1픽셀의 왜곡 없이 보존하세요.
아래 [번역 매핑 데이터 JSON]을 바탕으로 단일 이미지를 생성하세요.

[엄격 렌더링 규칙]
1. (KOR ERASING) 원본 한국어 텍스트는 배경색/텍스처로 완벽히 덮어써서 100% 제거할 것.
2. (JSON APPLY) 지워진 그 자리에 오직 [번역 매핑 데이터 JSON]의 'target_text'만 렌더링할 것.
3. (FONT DIRECTIVE) 세련된 프리미엄 산세리프(Montserrat / Inter 스타일)로 깔끔하고 가독성 높게 렌더링할 것.
4. (FULL REGENERATION) 패칭(덧칠)하지 말고 전체 캔버스를 완벽하게 새로 렌더링할 것.
5. (PACKAGE PRESERVATION) 제품 본품(용기 표면)의 영문 및 로고는 100% 완벽 보존할 것.

[번역 매핑 데이터 JSON]
{json_data}
"""
    elif lang_code == "JP":
        efficacy_str = load_jp_efficacy_list()
        pass1 = f"""
첨부된 이미지는 화장품 상세페이지 또는 제품 패키지입니다.
당신은 일본 후생노동성 약기법(약사법) 및 Qoo10 Japan 화장품 광고 규정 최고 전문가입니다.
이미지 내 모든 한국어 텍스트를 추출하고 일본 약기법 및 56종 허용 효능 목록을 100% 준수하여 번역 매핑 JSON을 생성하세요.

[일본 후생노동성 공인 56종 허용 효능 목록]
{efficacy_str}

[약기법 필수 지침]
1. '치료/재생/소염' 등 의학적 효능 표현 절대 금지 -> '피부를 정돈하다(肌を整える)', '피부결 정돈' 등으로 순화.
2. '무자극/자극없이' -> '저자극 처방(低刺激処方)'.
3. '미백' -> '수분을 주어 맑고 투명감 있는 피부로 케어'.
4. 제품 본품 표면 영문은 번역 매핑에 넣지 마세요.
5. 만약 표(고시정보표) 레이아웃인 경우 is_table: true 로 설정하세요.

출력은 반드시 순수 JSON이어야 합니다:
{{
  "is_table": false,
  "translation_map": [
    {{
      "kor": "한국어 원문",
      "target_text": "약기법 준수 일본어 번역문",
      "reasoning": "약기법 검열 및 순화 사유"
    }}
  ]
}}
"""
        pass2_tmpl = """
당신은 정밀한 시각적 로컬라이제이션을 수행하는 이미지 인페인팅 AI입니다.
첨부된 원본 이미지의 디자인 레이아웃과 제품을 그대로 유지하세요.
아래 [번역 매핑 데이터 JSON]을 바탕으로 단일 이미지를 생성하세요.

[엄격 렌더링 규칙]
1. (KOR ERASING) 원본 한국어 텍스트는 배경으로 덮어써서 100% 지울 것.
2. (JSON APPLY) 지워진 자리에 오직 [번역 매핑 데이터 JSON]의 'target_text'만 렌더링할 것.
3. (FONT DIRECTIVE) 일본 최고급 표준 서체(Noto Sans JP / Gothic) 스타일로 단정하게 렌더링할 것.
4. (FULL REGENERATION) 전체 캔버스를 결점 없이 완벽히 새로 렌더링할 것.
5. (PACKAGE PRESERVATION) 제품 본품(용기)의 영문 및 로고는 100% 보존할 것.

[번역 매핑 데이터 JSON]
{json_data}
"""
    elif lang_code == "CN":
        pass1 = """
첨부된 이미지는 화장품 상세페이지 또는 제품 패키지입니다.
당신은 중국 본토 신(新)광고법 및 NMPA 화장품 효능 표기 규정 전문가입니다.
모든 한국어 텍스트를 추출하고 순수 간체자(zh-CN) 및 광고법 규정을 100% 준수하여 번역 매핑 JSON을 생성하세요.

[중국 신광고법 및 가이드]
1. '최고/제일(最, 第一, 顶级, 极品)' 절대 금지 -> '卓越', '优异', '高端' 등으로 대체.
2. '영구/완벽/완전/100%/무자극' 금지 -> '持久', '深层改善', '温和低敏' 등으로 대체.
3. '치료/소염/재생(治疗, 消炎, 修复疤痕)' 금지 -> '舒缓', '修护', '赋活' 등으로 대체.
4. 순수 간체자(Simplified Chinese)만 사용.
5. 표 레이아웃인 경우 is_table: true 설정.

출력은 반드시 순수 JSON이어야 합니다:
{
  "is_table": false,
  "translation_map": [
    {
      "kor": "한국어 원문",
      "target_text": "광고법 준수 중국어 간체 번역문",
      "reasoning": "광고법 순화 사유"
    }
  ]
}
"""
        pass2_tmpl = """
당신은 정밀한 시각적 로컬라이제이션을 수행하는 이미지 인페인팅 AI입니다.
첨부된 원본 이미지 레이아웃을 보존하며 아래 [번역 매핑 데이터 JSON]으로 단일 이미지를 생성하세요.

[엄격 렌더링 규칙]
1. (KOR ERASING) 원본 한국어 텍스트를 100% 지울 것.
2. (JSON APPLY) 오직 [번역 매핑 데이터 JSON]의 'target_text'만 렌더링할 것.
3. (FONT & LAYOUT) Noto Sans SC (思源黑体) 산세리프 스타일로 렌더링하되, 한자 특성을 고려하여 한국어 대비 폰트 크기 10% 축소, 행간 15% 확장 적용.
4. (PACKAGE PRESERVATION) 본품 표면 영문/로고 100% 보존.

[번역 매핑 데이터 JSON]
{json_data}
"""
    else:  # TW
        pass1 = """
첨부된 이미지는 화장품 상세페이지 또는 제품 패키지입니다.
당신은 대만(Taiwan, zh-TW) TFDA 화장품 규정 및 이커머스 번역 전문가입니다.
모든 한국어 텍스트를 추출하고 순수 대만 정체자(Traditional Chinese, zh-TW) 및 뷰티 표준 용어를 반영하여 번역 매핑 JSON을 생성하세요.

[대만 번체 가이드]
1. 대만 정체자(繁體中文) 필수 (간체자 혼용 절대 금지).
2. 대만 이커머스(Shopee TW, momo) 최적화: 化妝水, 保濕/鎖水, 精華液, 緊緻, 舒緩修護.
3. 의학적 치료/과대광고 배제.
4. 표 레이아웃인 경우 is_table: true 설정.

출력은 반드시 순수 JSON이어야 합니다:
{
  "is_table": false,
  "translation_map": [
    {
      "kor": "한국어 원문",
      "target_text": "대만 정체자 번역문",
      "reasoning": "대만 로컬라이징 사유"
    }
  ]
}
"""
        pass2_tmpl = """
당신은 정밀한 시각적 로컬라이제이션을 수행하는 이미지 인페인팅 AI입니다.
아래 [번역 매핑 데이터 JSON]을 바탕으로 단일 이미지를 생성하세요.

[엄격 렌더링 규칙]
1. (KOR ERASING) 원본 한국어 텍스트 100% 지울 것.
2. (JSON APPLY) 오직 'target_text'의 대만 정체자만 렌더링할 것.
3. (FONT & LAYOUT) Noto Sans TC / 思源黑體 스타일로 렌더링.
4. (PACKAGE PRESERVATION) 본품 표면 영문/로고 100% 보존.

[번역 매핑 데이터 JSON]
{json_data}
"""
    return pass1, pass2_tmpl


# =================================================================================
# 4. 고시정보 표 자동 HTML 렌더러 연동
# =================================================================================
def render_notice_table(mapping_data: Dict[str, Any], lang_code: str, out_path: str, orig_width: int = 860) -> bool:
    """render_notice_table_standard.py 모듈을 활용하여 고선명 표 이미지를 렌더링합니다."""
    std_script = os.path.join(PROJECT_ROOT, "00_공통자료", "render_notice_table_standard.py")
    if not os.path.exists(std_script):
        return False

    try:
        items = []
        for row in mapping_data.get("translation_map", []):
            kor = row.get("kor", "")
            tgt = row.get("target_text", "")
            if ":" in kor or "：" in kor:
                parts = re.split(r"[:：]", tgt, 1)
                lbl = parts[0].strip()
                val = parts[1].strip() if len(parts) > 1 else ""
            else:
                lbl = kor
                val = tgt
            items.append({"label": lbl, "value": val})

        tmp_json = os.path.join(PROJECT_ROOT, "00_공통자료", f"_tmp_table_{lang_code}.json")
        with open(tmp_json, "w", encoding="utf-8") as f:
            json.dump({"title": "PRODUCT DETAILS", "items": items, "lang": lang_code, "out_path": out_path, "width": orig_width}, f, ensure_ascii=False)

        cmd = [sys.executable, "-c", f"""
import sys, json, os
from PIL import Image
sys.path.insert(0, r'{os.path.join(PROJECT_ROOT, "00_공통자료")}')
import render_notice_table_standard as rnts

with open(r'{tmp_json}', 'r', encoding='utf-8') as f:
    cfg = json.load(f)

browser = rnts.get_browser_path()
html = rnts.build_notice_html(cfg['title'], cfg['items'], lang=cfg['lang'])
tmp_html = r'{tmp_json}.html'
with open(tmp_html, 'w', encoding='utf-8') as hf:
    hf.write(html)

ret = rnts.render_html_to_png(tmp_html, cfg['out_path'], browser_path=browser, target_width=cfg['width'])
if os.path.exists(tmp_html): os.remove(tmp_html)
sys.exit(0 if ret else 1)
"""]
        res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
        if os.path.exists(tmp_json):
            os.remove(tmp_json)
        return res.returncode == 0 and os.path.exists(out_path)
    except Exception as e:
        print(f"  -> [TABLE FALLBACK FAIL] 표 렌더러 예외: {e}")
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

    # PASS 1: 텍스트 추출 및 번역 매핑
    print(f"  🔍 [PASS 1] 텍스트 스캔 및 다국어 매핑 추출 중 ({MODEL_PRO})...", flush=True)
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
    except Exception as e:
        print(f"  ❌ [ERROR] PASS 1 매핑 생성 실패: {e}")
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

    # PASS 2: 신경망 인페인팅 렌더링
    print(f"  🎨 [PASS 2] 시각적 신경망 인페인팅 렌더링 가동 ({MODEL_FLASH_IMAGE})...", flush=True)
    clean_json_str = json.dumps(p1_json, ensure_ascii=False, indent=2)
    pass2_prompt = pass2_tmpl.format(json_data=clean_json_str)

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
            print(f"  ❌ [ERROR] PASS 2 이미지 데이터 반환 없음")
            return False

        img = Image.open(io.BytesIO(rendered_img_bytes))
        if img.size != (orig_w, orig_h):
            img = img.resize((orig_w, orig_h), Image.Resampling.LANCZOS)

        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        img.save(out_path, format="PNG", optimize=True)
        print(f"  🎉 [SUCCESS] 렌더링 완료 및 저장: {os.path.basename(out_path)} ({orig_w}x{orig_h})")
        return True

    except Exception as e:
        print(f"  ❌ [ERROR] PASS 2 렌더링 실패: {e}")
        return False


def run_translation_batch(client: genai.Client, source_dir: str, target_lang: str):
    config = LANG_CONFIGS[target_lang]
    target_dir = os.path.join(DEFAULT_OUTPUT_BASE, config["folder_name"])
    os.makedirs(target_dir, exist_ok=True)

    print(f"\n================================================================================")
    print(f"🚀 [{config['name']}] 일괄 번역 시작")
    print(f"📁 [입력 폴더] {source_dir}")
    print(f"📁 [출력 폴더] {target_dir}")
    print(f"================================================================================")

    targets = sorted(
        [f for f in os.listdir(source_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp'))],
        key=lambda x: [int(c) if c.isdigit() else c.lower() for c in re.split(r'(\d+)', x)]
    )

    if not targets:
        print(f"⚠️ [WARNING] '{source_dir}' 폴더에 처리할 이미지가 없습니다.")
        return

    total = len(targets)
    success_count = 0

    for idx, filename in enumerate(targets, 1):
        if config["tag"] in filename or "_Translated" in filename:
            print(f"[{idx}/{total}] ⏭️ [SKIP] 이미 번역된 파일: {filename}")
            continue

        in_path = os.path.join(source_dir, filename)
        base_name = os.path.splitext(filename)[0]
        out_name = f"{base_name}{config['tag']}"
        out_path = os.path.join(target_dir, out_name)

        if os.path.exists(out_path):
            print(f"[{idx}/{total}] ⏭️ [SKIP] 이미 결과물이 존재함: {out_name}")
            success_count += 1
            continue

        print(f"\n[{idx}/{total}] 작업 시작...")
        success = process_single_image(client, in_path, out_path, target_lang)
        if success:
            success_count += 1

        if idx < total:
            print("⏳ API 쿼터 안전 대기 (12초)...", flush=True)
            time.sleep(12)

    print(f"\n🏁 [{config['name']}] 번역 완료: 총 {total}개 중 {success_count}개 성공!")
    print(f"📂 저장 경로: {target_dir}\n")


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
        image_count = len([f for f in os.listdir(source_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp'))]) if os.path.exists(source_dir) else 0

        print("\n" + "=" * 76)
        print(" 🌐 multilingual_text_in_image_translation")
        print("=" * 76)
        print(f" 📂 [공통 인풋 폴더] : {source_dir}")
        print(f" 🖼️ [감지된 원본 이미지] : {image_count}개")
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
