"""
===================================================================================
🇺🇸 EN_Text-In_Image_Translation_Engine_V1.py
-----------------------------------------------------------------------------------
• Purpose: Two-Pass Multimodal Neural Inpainting Engine for English E-Commerce (Amazon/Shopee)
• Core Models:
    - Pass 1: gemini-3.1-pro-preview (Dual Mode: Transcreation KR->EN / Polishing EN->EN)
    - Pass 2: gemini-3.1-flash-image (Visual Inpainting & Typography Rendering)
• Standard Fonts:
    - Detail Page Main Images: 100% Montserrat (몬세라트 단일 서체 강제)
    - Notice Tables (고시정보표): Pretendard (render_notice_table_standard.py 독립 분리)
• Resolution: Aspect Ratio Lock via Pillow LANCZOS Resampling (1:1 픽셀 동기화)
• Location: Google Cloud Vertex AI (location="global") Serverless Standard
===================================================================================
"""

import io
import json
import os
import re
import sys
import time
from typing import Any, Dict, List, Optional, Tuple

from google import genai
from google.genai import types
from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")

# =================================================================================
# 1. 환경 설정 및 클라우드 인증 초기화
# =================================================================================
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))

MODEL_PRO = "gemini-3.1-pro-preview"
MODEL_FLASH_IMAGE = "gemini-3.1-flash-image"


def load_credentials() -> genai.Client:
    """Vertex AI 서비스 계정 키 및 API 키를 탐색하여 genai.Client를 초기화합니다."""
    env_paths = [
        os.path.join(SCRIPT_DIR, ".env"),
        os.path.join(PROJECT_ROOT, ".env"),
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
                    if line.startswith("GEMINI_API_KEY="):
                        api_key = line.split("=", 1)[1].strip()
                    elif line.startswith("GOOGLE_APPLICATION_CREDENTIALS="):
                        gcp_json_key = line.split("=", 1)[1].strip().strip('"').strip("'")

    key_candidates = [
        gcp_json_key,
        os.path.join(PROJECT_ROOT, "00_공통자료", "APIs_KEY", "인증키_및_계정", "김차장_vertex api_key", "vertex_ai_auth_key.json"),
        os.path.join(PROJECT_ROOT, "00_공통자료", "인증키_및_계정", "김차장_vertex api_key", "vertex_ai_auth_key.json"),
    ]

    for kpath in key_candidates:
        if kpath and os.path.exists(kpath) and kpath.endswith(".json"):
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = kpath
            print(f"[AUTH] Vertex AI 서비스 계정 키 감지: {kpath}")
            with open(kpath, "r", encoding="utf-8") as f:
                key_data = json.load(f)
                project_id = key_data.get("project_id")
            client = genai.Client(vertexai=True, project=project_id, location="global")
            print(f"[AUTH SUCCESS] Vertex AI Client 연결 완료 (Project: {project_id}, Location: global)")
            return client

    if api_key:
        if api_key.startswith("AQ."):
            print("[AUTH] Agent Platform API 키 감지 -> Vertex AI 모드로 전환")
            return genai.Client(vertexai=True, api_key=api_key)
        print("[AUTH] Gemini API 키 인증 모드 연결")
        return genai.Client(api_key=api_key)

    print("[ERROR] GEMINI_API_KEY 또는 GOOGLE_APPLICATION_CREDENTIALS가 설정되지 않았습니다.")
    sys.exit(1)


# =================================================================================
# 2. Pass 1 & Pass 2 프롬프트 정의
# =================================================================================
PASS1_PROMPT = """
[SYSTEM PROMPT] Global Luxury Beauty Transcreation & Compliance Expert (English Engine)

## 1. 시스템 역할 및 콘셉트 (Role & Context)
당신은 에스티로더, 랑콤, 시슬리, SK-II 등 글로벌 하이엔드 코스메틱 브랜드의 해외 진출을 총괄하는 10년 차 수석 크리에이티브 디렉터이자 세포라(Sephora) 전문 엘리트 카피라이터입니다.
단순 직역을 배제하고, 미국 및 글로벌 프레스티지 뷰티 고객의 구매 심리를 사로잡는 세련된 '초월번역(Transcreation)'을 수행하세요.

## 2. 단계별 모드 자동 감지
1. 이미지 내 텍스트에 '한국어'가 포함되어 있다면 -> mode: "TRANSLATE_KR_TO_EN"
2. 이미지 내 텍스트가 이미 '영어'로만 되어 있다면 -> mode: "POLISH_EN_TO_EN"

## 3. 초월번역 및 교정 핵심 원칙
1. [기계적 직역 및 부사 금지]
   - 'Definitely', 'Truly', 'Really', 'Certainly' 등 어색한 감정 부사 직역을 전면 금지하고, 럭셔리 뷰티 전문 능동태 동사/형용사로 재창조하십시오.
2. [자연스러운 구문 결속 및 활성 성분 연결]
   - "10% LiftDerm" 등 활성 성분 수치가 문맥과 끊기지 않고 제품 효능 및 서사로 매끄럽게 연결되도록 문장 구조를 재조정하십시오.
3. [4대 기능성 뷰티 전문 어휘 사전]
   - 피부 속/기저층: Deep within the skin layers / Deep within the dermal matrix
   - 토탈 케어/멀티 코렉티브: Multi-Corrective Repair / Total Revitalizing Care
   - 탄력 복원/강화: Rebuilding skin elasticity / Restoring visible firmness
   - 눈가 잔주름/건조주름: Fine lines and wrinkles / Micro-creases
4. [독자 성분명 영문 보존]
   - 'LiftDerm', 'Lifting Logic for eye' 등 글로벌 독자 성분명/브랜드명은 영문 그대로 유지하되 문맥과 완벽히 융합하십시오.
   - 제품 본품 용기/단상자 표면 인쇄 영문/로고는 수정 대상에서 제외하십시오.

## 4. 광고 법규 및 규제 준수 (Regulatory Compliance & Guardrails)
1. [절대적/과대 표현 전면 금지 (Ban on Absolute Claims)]
   - 'World's First', 'No.1', 'Best', 'The Ultimate' 등 입증되지 않은 절대적 표현 사용 전면 금지.
   - 반드시 'Innovative formula engineered for delicate eye areas', 'Advanced Multi-Corrective Solution', 'Targeted Precision Care' 등 프리미엄 혁신 표현으로 순화하십시오.
2. [의료 시술 오인 금지 및 4대 안전 동사 (Compliance-Safe Verbs)]
   - '주름 완전 박멸(Wrinkle-free)', '보톡스/필러 효과' 등 의료 시술 연상 및 세포 치료/재생 오인 단어 전면 배제.
   - 반드시 **`Smooth` (抚平/撫平)**, **`Diminish` (淡化)**, **`Alleviate` (舒缓/舒緩)**, **`Care / Repair` (修护/修護)** 4대 컴플라이언스 안전 동사를 사용하여 표현하십시오.

## 5. 고시정보 표 강제 표준 매핑
만약 이미지 내용이 '고시정보(Notice Table, Product Specifications)' 표라면, 다음의 표준 명칭으로 강제 매핑하십시오:
1) 용량 또는 중량 -> Size / Net Wt.
2) 제품 주요 사양 -> Skin Type
3) 사용기한 또는 개봉 후 사용기간 -> Shelf Life / PAO
4) 사용방법 -> Directions
5) 화장품제조업자 및 책임판매업자 -> Manufacturer / Distributed by
6) 제조국 -> Country of Origin
7) 전성분 -> Ingredients

출력은 반드시 아래 JSON 스키마를 엄격히 준수하십시오:
```json
{
  "detected_mode": "TRANSLATE_KR_TO_EN 또는 POLISH_EN_TO_EN",
  "translation_map": [
    {
      "original_text": "원본 텍스트(한글 또는 어색한 기존 영문)",
      "corrected_en": "최종 교정/초월번역된 프리미엄 영문 카피"
    }
  ]
}
```
"""

PASS2_PROMPT_TEMPLATE = """
당신은 글로벌 럭셔리 뷰티(Sephora, Amazon US) 이미지 로컬라이징 최고 전문가입니다.
첨부된 원본 이미지에서 기존의 원본 텍스트를 감쪽같이 지우고, 교정/번역된 영문 데이터를 바탕으로 완벽하게 재렌더링하세요.

[시각적 렌더링 엄격 규칙]
1. (TEXT ERASING) 원본의 기존 텍스트('original_text')를 원래 배경색과 완벽히 블렌딩하여 지울 것.
2. (NEW COPY RENDERING) 지워진 그 자리에 [매핑 데이터 JSON]의 'corrected_en' 영문 텍스트만 정확한 위치에 렌더링할 것.
3. (FONT & TYPOGRAPHY) 모든 영문 텍스트는 100% 오직 'Montserrat (몬세라트)' 폰트만을 유일한 표준 서체로 적용하여 렌더링할 것. (Montserrat 단일 서체 강제 / 타 서체 혼용 절대 금지)
4. (FULL INPAINTING NO PATCHING) 전체 이미지를 매끄럽게 재렌더링하여 원본과 동일한 해상도/비율을 100% 유지할 것.
5. (PACKAGE PRESERVATION) 제품 본품 용기/패키지에 인쇄된 로고 및 문구는 100% 원본 유지할 것.

[매핑 데이터 JSON]
{json_data}
"""


# =================================================================================
# 3. 헬퍼 함수
# =================================================================================
def natural_sort_key(s: str) -> List[Any]:
    """파일명 내부의 숫자를 자연스럽게 인식하여 정렬하는 키 함수입니다."""
    return [int(text) if text.isdigit() else text.lower() for text in re.split(r"(\d+)", s)]


def parse_arguments() -> Tuple[str, str]:
    """커맨드라인 파라미터를 파싱하여 입력 및 출력 디렉토리를 반환합니다."""
    if len(sys.argv) > 1:
        src = sys.argv[1]
        if len(sys.argv) > 2:
            tgt = sys.argv[2]
        else:
            tgt = os.path.join(
                os.path.dirname(src),
                os.path.normpath(src).split(os.sep)[-1] + "_EN_Translated",
            )
    else:
        src = os.path.join(SCRIPT_DIR, "input")
        tgt = os.path.join(SCRIPT_DIR, "output")

    os.makedirs(src, exist_ok=True)
    os.makedirs(tgt, exist_ok=True)
    return src, tgt


def extract_image_bytes(response: Any) -> Optional[bytes]:
    """Gemini API 응답 객체에서 렌더링된 이미지 바이트를 안전하게 추출합니다."""
    if not hasattr(response, "candidates") or not response.candidates:
        return None

    for cand in response.candidates:
        if hasattr(cand, "content") and hasattr(cand.content, "parts"):
            for part in cand.content.parts:
                if hasattr(part, "inline_data") and part.inline_data and part.inline_data.data:
                    return part.inline_data.data
                if hasattr(part, "image") and part.image and part.image.image_bytes:
                    return part.image.image_bytes
    return None


# =================================================================================
# 4. 메인 엔진 파이프라인
# =================================================================================
def run_engine():
    client = load_credentials()
    source_dir, target_dir = parse_arguments()

    print("\n=======================================================")
    print("🇺🇸 EN_Text-In_Image_Translation_Engine_V1 가동")
    print(f"• 입력 경로: {source_dir}")
    print(f"• 출력 경로: {target_dir}")
    print(f"• 메인 폰트: Montserrat (100% 단일 서체 강제)")
    print("=======================================================\n")

    valid_extensions = (".png", ".jpg", ".jpeg", ".jfif", ".gif", ".webp")
    raw_files = [f for f in os.listdir(source_dir) if f.lower().endswith(valid_extensions)]
    targets = sorted(raw_files, key=natural_sort_key)

    if not targets:
        print(f"[WARNING] '{source_dir}' 폴더에 처리할 이미지가 없습니다.")
        return

    all_translations = []

    for filename in targets:
        if "_수정번역" in filename or filename.endswith(".txt") or filename.endswith(".md"):
            continue

        in_path = os.path.join(source_dir, filename)
        out_name = f"{os.path.splitext(filename)[0]}_수정번역.png"
        out_path = os.path.join(target_dir, out_name)

        if os.path.exists(out_path):
            print(f"[SKIP] 이미 완료된 파일입니다: {filename}")
            continue

        print(f"\n[RENDER] 처리 시작: {filename}")

        try:
            original_image = Image.open(in_path)
            original_image.load()
            orig_w, orig_h = original_image.size
        except Exception as e:
            print(f"  -> [ERROR] 이미지 로드 실패 ({filename}): {e}")
            continue

        # -------------------------------------------------------------
        # PASS 1: 언어 자동 감지 및 초월번역 / 교정 매핑 생성 (Pro 모델)
        # -------------------------------------------------------------
        print("  -> [PASS 1] 텍스트 OCR 및 언어 감지, 영문 초월번역 생성 중...")
        mapping_data_str = ""
        try:
            response_p1 = client.models.generate_content(
                model=MODEL_PRO,
                contents=[original_image, PASS1_PROMPT],
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    temperature=0.6,
                    top_p=0.9,
                    max_output_tokens=2048
                ),
            )
            mapping_data_str = response_p1.text.strip()
            parsed_json = json.loads(mapping_data_str)
            mode = parsed_json.get("detected_mode", "UNKNOWN")
            map_count = len(parsed_json.get("translation_map", []))
            print(f"  -> [PASS 1 SUCCESS] 감지 모드: {mode} (매핑 항목: {map_count}개)")

            if "translation_map" in parsed_json:
                for item in parsed_json["translation_map"]:
                    item["source_file"] = filename
                    item["mode"] = mode
                all_translations.extend(parsed_json["translation_map"])
        except Exception as e:
            print(f"  -> [PASS 1 ERROR] 매핑 생성 실패: {e}")
            continue

        # -------------------------------------------------------------
        # PASS 2: 영문 이미지 인페인팅 렌더링 (Flash-Image 모델)
        # -------------------------------------------------------------
        print("  -> [PASS 2] Montserrat 영문 타이포그래피 인페인팅 렌더링 중...")
        max_retries = 3
        final_prompt = PASS2_PROMPT_TEMPLATE.replace("{json_data}", mapping_data_str)

        for attempt in range(max_retries):
            try:
                response_p2 = client.models.generate_content(
                    model=MODEL_FLASH_IMAGE,
                    contents=[final_prompt, original_image],
                )

                img_bytes = extract_image_bytes(response_p2)
                if img_bytes:
                    img = Image.open(io.BytesIO(img_bytes))
                    # 원본 해상도 1:1 강제 일치 (Aspect Ratio Lock)
                    img = img.resize((orig_w, orig_h), Image.Resampling.LANCZOS)
                    img.save(out_path, format="PNG")
                    print(f"  -> [PASS 2 SUCCESS] {out_name} 저장 완료 ({orig_w}x{orig_h}px)!")
                    break
                else:
                    print("  -> [RETRY] Pass 2 이미지 응답 없음, 10초 대기 후 재시도...")
                    time.sleep(10)
            except Exception as e:
                print(f"  -> [PASS 2 ERROR] 렌더링 에러 (시도 {attempt+1}/{max_retries}): {e}")
                if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
                    wait_sec = 25 * (attempt + 1)
                    print(f"  -> [QUOTA WAIT] 429 쿼터 대기 ({wait_sec}초)...")
                    time.sleep(wait_sec)
                else:
                    time.sleep(10)

        time.sleep(12)

    # -----------------------------------------------------------------
    # 최종 번역/교정 대조 리포트 발행
    # -----------------------------------------------------------------
    if all_translations:
        print("\n[REPORT] 영문 번역/교정 대조 리포트 생성 중...")
        report_path = os.path.join(target_dir, "EN_Translation_Polish_Report.txt")
        with open(report_path, "w", encoding="utf-8") as f:
            f.write("==============================================================\n")
            f.write("🇺🇸 EN V1 엔진: 국문 원본 vs 최종 영문(Montserrat) 매핑 리포트\n")
            f.write("==============================================================\n\n")
            for t in all_translations:
                orig = t.get("original_text", "").replace("\n", " ")
                corr = t.get("corrected_en", "").replace("\n", " ")
                src = t.get("source_file", "")
                mode = t.get("mode", "")
                f.write("--------------------------------------------------------------\n")
                f.write(f"[파일명]: {src} | [모드]: {mode}\n")
                f.write(f"[원본 텍스트]: {orig}\n")
                f.write(f"[교정 영문]: {corr}\n")
            f.write("--------------------------------------------------------------\n")
        print(f"  -> [REPORT SUCCESS] 리포트 저장 완료: {report_path}")

    print("\n[FINISH] EN_Text-In_Image_Translation_Engine_V1 영문 이미지 처리 파이프라인 종료!")


if __name__ == "__main__":
    run_engine()
