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
첨부된 이미지는 이커머스(화장품, 건기식, 패션, 생필품 등) 상세페이지 또는 제품 이미지입니다.
당신은 아마존(Amazon US), 쇼피(Shopee) 등 글로벌 최상위 이커머스 플랫폼의 수석 영문 카피라이터이자 현지화/초월번역(Transcreation) 최고 전문가입니다.

[단계 1: 이미지 언어 자동 감지 및 모드 결정]
1. 이미지 내 텍스트에 '한국어'가 포함되어 있다면 -> mode: "TRANSLATE_KR_TO_EN"
2. 이미지 내 텍스트가 이미 '영어'로만 되어 있다면 -> mode: "POLISH_EN_TO_EN"

[단계 2: 모드별 텍스트 매핑 생성 규칙]
■ 모드 A: TRANSLATE_KR_TO_EN (한글 신규 번역)
- 이미지 속 모든 한국어 텍스트를 추출하고, 아마존/글로벌 뷰티 이커머스 표준에 맞는 세련된 네이티브 영문 카피로 초월번역(Transcreation)하십시오.
- 'original_text'(한국어) -> 'corrected_en'(초월번역 영문)

■ 모드 B: POLISH_EN_TO_EN (기존 영문 표현 교정 및 다듬기)
- 이미지 속 기존 영문 텍스트를 정밀 분석하여, 직역투, 콩글리시, 문법적 결함, 어색한 어휘, 비즈니스 은어 오용 등을 찾아내십시오.
- 영미권 원어민 소비자가 보았을 때 완벽하게 자연스럽고 매력적인 프리미엄 이커머스 마케팅 카피로 1:1 교정하십시오.
- 'original_text'(기존 어색한 영문) -> 'corrected_en'(원어민 교정 영문)

[공통 필수 규칙]
- 제품 패키지/용기 표면의 고유 로고 및 인쇄 문구는 수정 대상에서 제외하십시오.
- 출력은 반드시 아래 JSON 스키마를 엄격히 준수하십시오.

```json
{
  "detected_mode": "TRANSLATE_KR_TO_EN 또는 POLISH_EN_TO_EN",
  "translation_map": [
    {
      "original_text": "원본 텍스트(한글 또는 어색한 기존 영문)",
      "corrected_en": "최종 교정/번역된 프리미엄 영문 카피"
    }
  ]
}
```
"""

PASS2_PROMPT_TEMPLATE = """
당신은 글로벌 이커머스(Amazon, Shopee) 이미지 로컬라이징 최고 전문가입니다.
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
                config=types.GenerateContentConfig(response_mime_type="application/json"),
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
