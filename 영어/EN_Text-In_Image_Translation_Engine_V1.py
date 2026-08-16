import os
import io
import sys
import time
import json
from google import genai
from google.genai import types
from PIL import Image

sys.stdout.reconfigure(encoding='utf-8')

# 로컬 상대경로의 .env 파일 탐색 및 키 추출
script_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(script_dir, ".env")
api_key = None
gcp_json_key = None

if os.path.exists(env_path):
    with open(env_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line.startswith("GEMINI_API_KEY="):
                api_key = line.split("=", 1)[1].strip()
            elif line.startswith("GOOGLE_APPLICATION_CREDENTIALS="):
                gcp_json_key = line.split("=", 1)[1].strip().strip('"').strip("'")

if not api_key:
    api_key = os.environ.get("GEMINI_API_KEY")
if not gcp_json_key:
    gcp_json_key = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")

if gcp_json_key and os.path.exists(gcp_json_key):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = gcp_json_key
    print(f"[INFO] Vertex AI 서비스 계정 JSON 키가 감지되었습니다: {gcp_json_key}")
    with open(gcp_json_key, 'r', encoding='utf-8') as f:
        key_data = json.load(f)
        project_id = key_data.get('project_id')
    client = genai.Client(vertexai=True, project=project_id, location="global")
elif api_key:
    if api_key.startswith("AQ."):
        print("[INFO] Agent Platform API 키(AQ...)가 감지되었습니다. Vertex AI 모드로 전환합니다.")
        client = genai.Client(vertexai=True, api_key=api_key)
    else:
        client = genai.Client(api_key=api_key)
else:
    print("[ERROR] GEMINI_API_KEY 또는 GOOGLE_APPLICATION_CREDENTIALS가 설정되지 않았습니다.")
    sys.exit(1)

# 코어 AI 모델 사양
MODEL_PRO = "gemini-3.1-pro-preview"
MODEL_FLASH_IMAGE = "gemini-3.1-flash-image"

# 커맨드라인 파라미터 파싱
if len(sys.argv) > 1:
    source_dir = sys.argv[1]
    if len(sys.argv) > 2:
        base_target_dir = sys.argv[2]
    else:
        base_target_dir = os.path.join(os.path.dirname(source_dir), os.path.normpath(source_dir).split(os.sep)[-1] + "_EN_Translated")
else:
    source_dir = r"C:\Users\euntaewoo\Desktop\다국어_이미지_번역\01_번역대상_원본"
    base_target_dir = r"C:\Users\euntaewoo\Desktop\다국어_이미지_번역\02_번역결과_최종"

if len(sys.argv) > 2:
    target_dir = base_target_dir
else:
    if len(sys.argv) == 1:
        target_dir = base_target_dir
    else:
        folder_name = os.path.normpath(source_dir).split(os.sep)[-1]
        target_dir = os.path.join(base_target_dir, folder_name)
os.makedirs(source_dir, exist_ok=True)
os.makedirs(target_dir, exist_ok=True)

# [Pass 1] 자동 언어 감지 및 듀얼 모드 (신규 번역 vs 영문 교정) 프롬프트
pass1_prompt = """
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

# [Pass 2] 영문 시각적 렌더링 프롬프트 템플릿
pass2_prompt_template = """
당신은 글로벌 이커머스(Amazon, Shopee) 이미지 로컬라이징 최고 전문가입니다.
첨부된 원본 이미지에서 기존의 원본 텍스트를 감쪽같이 지우고, 교정/번역된 영문 데이터를 바탕으로 완벽하게 재렌더링하세요.

[시각적 렌더링 엄격 규칙]
1. (TEXT ERASING) 원본의 기존 텍스트('original_text')를 원래 배경색과 완벽히 블렌딩하여 지울 것.
2. (NEW COPY RENDERING) 지워진 그 자리에 [매핑 데이터 JSON]의 'corrected_en' 영문 텍스트만 정확한 위치에 렌더링할 것.
3. (FONT & TYPOGRAPHY) 영미권 프리미엄 모던 이커머스 표준 산세리프(Pretendard / Inter 스타일) 폰트를 적용하고 자간/행간을 최적화할 것.
4. (FULL INPAINTING NO PATCHING) 전체 이미지를 매끄럽게 재렌더링하여 원본과 동일한 해상도/비율을 100% 유지할 것.
5. (PACKAGE PRESERVATION) 제품 본품 용기/패키지에 인쇄된 로고 및 문구는 100% 원본 유지할 것.

[매핑 데이터 JSON]
{json_data}
"""

print("[START] EN_Text-In_Image_Translation_Engine_V1 (Auto-Detect Dual Mode) 엔진 가동...")
print(f"[INFO] 타겟 스캔 폴더: {source_dir}")
print(f"[INFO] 결과 저장 폴더: {target_dir}")

targets = sorted(
    [f for f in os.listdir(source_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.jfif', '.gif'))],
    key=lambda x: [int(c) if c.isdigit() else c.lower() for c in __import__('re').split(r'(\d+)', x)]
)

if not targets:
    print(f"[WARNING] '{source_dir}' 폴더에 처리할 이미지가 없습니다.")
    sys.exit(0)

all_translations = []

for filename in targets:
    if '_수정번역' in filename or filename.endswith('.txt') or filename.endswith('.md'):
        continue
        
    in_path = os.path.join(source_dir, filename)
    out_name = f"{os.path.splitext(filename)[0]}_수정번역.png"
    out_path = os.path.join(target_dir, out_name)
    
    if os.path.exists(out_path):
        print(f"\n[SKIP] 이미 완료된 파일입니다: {filename}")
        continue

    print(f"\n[RENDER] 처리 시작: {filename}")
    
    try:
        original_image = Image.open(in_path)
        original_image.load()
    except Exception as e:
        print(f"  -> [ERROR] 이미지 로드 실패: {e}")
        continue

    # ==========================
    # PASS 1: 언어 자동 감지 및 텍스트 매핑 생성 (pro 모델)
    # ==========================
    print("  -> [PASS 1] 텍스트 및 언어 자동 감지, 영문 매핑 생성 중...")
    mapping_data_str = ""
    try:
        response_p1 = client.models.generate_content(
            model=MODEL_PRO,
            contents=[original_image, pass1_prompt],
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
            )
        )
        mapping_data_str = response_p1.text
        parsed_json = json.loads(mapping_data_str)
        mode = parsed_json.get("detected_mode", "UNKNOWN")
        print(f"  -> [PASS 1 SUCCESS] 감지된 모드: {mode} (매핑 항목: {len(parsed_json.get('translation_map', []))}개)")
        if "translation_map" in parsed_json:
            for item in parsed_json["translation_map"]:
                item["source_file"] = filename
                item["mode"] = mode
            all_translations.extend(parsed_json["translation_map"])
    except Exception as e:
        print(f"  -> [PASS 1 ERROR] 매핑 실패: {e}")
        continue

    # ==========================
    # PASS 2: 이미지 렌더링 (flash-image 모델, 재시도 로직 포함)
    # ==========================
    print("  -> [PASS 2] 영문 이미지 인페인팅 렌더링 중...")
    max_retries = 3
    for attempt in range(max_retries):
        try:
            final_prompt = pass2_prompt_template.replace("{json_data}", mapping_data_str)
            response_p2 = client.models.generate_content(
                model=MODEL_FLASH_IMAGE,
                contents=[final_prompt, original_image]
            )
            
            img_saved = False
            if hasattr(response_p2, 'candidates'):
                for cand in response_p2.candidates:
                    if hasattr(cand, 'content') and hasattr(cand.content, 'parts'):
                        for part in cand.content.parts:
                            if hasattr(part, 'inline_data') and part.inline_data:
                                img = Image.open(io.BytesIO(part.inline_data.data))
                                img = img.resize(original_image.size, Image.Resampling.LANCZOS)
                                img.save(out_path, format="PNG")
                                img_saved = True
                                break
                            elif hasattr(part, 'image') and part.image:
                                img = Image.open(io.BytesIO(part.image.image_bytes))
                                img = img.resize(original_image.size, Image.Resampling.LANCZOS)
                                img.save(out_path, format="PNG")
                                img_saved = True
                                break
                                
            if img_saved:
                print(f"  -> [SUCCESS] {out_name} 최종 저장 완료 (해상도: {original_image.size[0]}x{original_image.size[1]}px)!")
                break
            else:
                print("  -> [RETRY] Pass 2 이미지 반환 없음, 재시도 중...")
                time.sleep(10)
        except Exception as e:
            print(f"  -> [PASS 2 ERROR] 렌더링 에러: {e}")
            if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
                wait_sec = 25 * (attempt + 1)
                print(f"  -> [QUOTA WAIT] 429 쿼터 대기 ({wait_sec}초)...")
                time.sleep(wait_sec)
            else:
                time.sleep(10)
    
    time.sleep(15)

if all_translations:
    print("\n[REPORT] 영문 번역/교정 결과 리포트 생성 중...")
    report_path = os.path.join(target_dir, "EN_Translation_Polish_Report.txt")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("==================================================\n")
        f.write("🇺🇸 EN V1 엔진: 원본 텍스트 vs 최종 영문 매핑 리포트\n")
        f.write("==================================================\n\n")
        for t in all_translations:
            orig = t.get("original_text", "").replace("\n", " ")
            corr = t.get("corrected_en", "").replace("\n", " ")
            src = t.get("source_file", "")
            mode = t.get("mode", "")
            f.write("--------------------------------------------------\n")
            f.write(f"[파일명]: {src} | [모드]: {mode}\n")
            f.write(f"[원본 텍스트]: {orig}\n")
            f.write(f"[교정 영문]: {corr}\n")
        f.write("--------------------------------------------------\n")
    print(f"  -> [SUCCESS] 리포트 저장 완료: {report_path}")

print("\n[FINISH] EN_Text-In_Image_Translation_Engine_V1 영문 이미지 처리 완료!")
