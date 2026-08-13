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

# [Pass 1] 한국어 -> 영문 프리미엄 이커머스 초월번역(Transcreation) 매핑 프롬프트
pass1_prompt = """
첨부된 이미지는 이커머스(화장품, 건기식, 패션, 가전, 생필품 등) 상세페이지 또는 제품 패키지입니다.
당신은 아마존(Amazon US/Global), 쇼피(Shopee), 라자다(Lazada) 등 글로벌 최상위 이커머스 플랫폼의 수석 영문 카피라이터(Lead Ecommerce Copywriter)이자 초월번역(Transcreation) 전문가입니다.

이미지 내의 모든 한국어 텍스트를 정밀 스캔하고, 단순한 직역/어색한 의역을 엄격히 금지하며, 구글 Gemini의 강력한 "초월번역(Transcreation)" 기법을 적용해 아래 현지화 카피라이팅 원칙에 따라 영문 번역 매핑 데이터를 생성하세요.

[초월번역 (Transcreation) & 현지화 카피라이팅 원칙]
1. (CATEGORY-SPECIFIC TERMINOLOGY) 해당 제품 카테고리별 글로벌 프리미엄 이커머스 시장에서 실제로 통용되는 전문 용어 및 세련된 마케팅 어휘를 100% 적용할 것.
   - 뷰티/화장품 예시: '피부 진정' -> 'Soothing & Calming Support', '피부 장벽 강화' -> 'Skin Barrier Fortifying', '속건조 케어' -> 'Deep Moisture Lock', '순한 성분' -> 'Gentle & Mild Formula'
   - 건기식/헬스 예시: '피로 개선' -> 'Vitality & Energy Boost', '체지방 감소' -> 'Body Fat Management Support'
   - 생활/가전/기타 예시: '강력한' -> 'High-Performance', '편리한 세척' -> 'Effortless Maintenance'
2. (CONCISE & IMPACTFUL COPY) 이미지는 글자 배치 공간(Visual Area)이 한정되어 있습니다. 원문 문장이 길더라도 동일한 세련된 의미를 전하는 임팩트 있고 간결한 영문 표현으로 초월번역하십시오.
3. (NATIVE ECOMMERCE TONE) 영미권 현지 소비자가 보았을 때 한국어 직역 느낌이 전혀 나지 않는 100% 네이티브 프리미엄 이커머스 상세페이지 톤앤매너를 구현하십시오.
4. (PACKAGE PRESERVATION) 제품 본품(용기, 튜브, 패키지 상자 등) 표면에 이미 영문으로 인쇄된 브랜드명/영문 문구는 절대 다시 번역하거나 매핑에 포함시키지 마세요. 오직 '한국어' 텍스트만 추출 및 번역 대상으로 삼으세요.
5. (COMPLETE EXTRACTION) 이미지 내의 모든 한국어 텍스트는 단 하나도 빠짐없이 100% 추출하여 'kor'과 'eng' 페어로 매핑하세요.

출력은 반드시 JSON 형식으로 아래 스키마를 엄격히 따르세요:
{
  "translation_map": [
    {
      "kor": "한국어 원문", 
      "eng": "초월번역(Transcreation)이 적용된 글로벌 영문 카피 문구"
    }
  ]
}
"""

# [Pass 2] 영문 시각적 렌더링 프롬프트 템플릿
pass2_prompt_template = """
당신은 글로벌 이커머스(Amazon, Shopee, Lazada) 이미지 로컬라이징 최고 전문가입니다.
첨부된 원본 이미지에서 한국어 텍스트를 감쪽같이 지우고, 영문 번역 데이터를 바탕으로 완벽하게 재렌더링하세요.

[시각적 렌더링 엄격 규칙]
1. (KOR ERASING) 원본의 한국어 텍스트는 원래 자리에 남겨두지 말고 배경색으로 덮어써서 100% 지울 것. 병기(한글+영어) 절대 금지.
2. (JSON APPLY) 지워진 그 자리에 오직 [번역 매핑 데이터 JSON]의 'eng' 영문 텍스트만 렌더링할 것. 모델 임의로 번역을 수정하지 말 것.
3. (FONT & TYPOGRAPHY) 렌더링 시 영미권 프리미엄 모던 이커머스 표준 산세리프(Pretendard / Inter 스타일) 폰트를 적용하고, 자간과 행간을 시독성 높게 유지할 것.
4. (FULL INPAINTING NO PATCHING) 국소 덧칠(Patching) 금지. 캔버스 전체를 완전히 새롭게 렌더링(Full Inpainting)하여 이질감 없는 하나의 완성된 이미지를 생성하십시오.
5. (VISUAL BALANCE) 원본의 상단 텍스트와 하단 텍스트 간의 폰트 크기, 두께(Weight) 시각적 밸런스를 1:1로 통일하여 식자할 것.
6. (LAYOUT STRICTNESS) 원래 텍스트가 있던 단락의 정렬축(좌/우/중앙)과 여백 구도를 1픽셀 오차 없이 완벽하게 유지하십시오.
7. (PACKAGE PRESERVATION) 제품 본품 용기 표면에 인쇄된 기존 영문 텍스트(예: 브랜드명, 원본 영문 로고 등)는 절대 변경하거나 손대지 말고 100% 원본 픽셀 상태로 보존하십시오.
8. (NO EXTRA NOISE) 번역과 무관한 AI 주석이나 부연 설명 문구를 이미지에 추가하지 말 것.

[번역 매핑 데이터 JSON]
{json_data}
"""

print("[START] EN_Text-In_Image_Translation_Engine_V1 (Two-Pass Architecture) 엔진 가동...")
print(f"[INFO] 타겟 스캔 폴더: {source_dir}")
print(f"[INFO] 결과 저장 폴더: {target_dir}")

targets = [f for f in os.listdir(source_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.jfif', '.gif'))]

if not targets:
    print(f"[WARNING] '{source_dir}' 폴더에 처리할 이미지가 없습니다.")
    sys.exit(0)

all_translations = []

for filename in targets:
    if '_EN_' in filename:
        continue
        
    if filename.endswith('.txt'):
        continue
        
    in_path = os.path.join(source_dir, filename)
    out_name = f"{os.path.splitext(filename)[0]}_EN_Surgical_v0.png"
    out_path = os.path.join(target_dir, out_name)
    
    if os.path.exists(out_path):
        print(f"\n[SKIP] 이미 번역 완료된 파일입니다: {filename}")
        continue

    print(f"\n[RENDER] 영문 변환 시작: {filename}")
    
    try:
        original_image = Image.open(in_path)
        original_image.load()
    except Exception as e:
        print(f"  -> [ERROR] 이미지 로드 실패: {e}")
        continue

    # ==========================
    # PASS 1: 텍스트 추출 및 영문 번역 (pro 모델)
    # ==========================
    print("  -> [PASS 1] 한국어 추출 및 영문 매핑 생성 중...")
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
        if "translation_map" in parsed_json:
            for item in parsed_json["translation_map"]:
                item["source_file"] = filename
            all_translations.extend(parsed_json["translation_map"])
        print("  -> [PASS 1 SUCCESS] 영문 매핑 데이터 생성 완료.")
    except Exception as e:
        print(f"  -> [PASS 1 ERROR] 영문 매핑 실패: {e}")
        continue

    # ==========================
    # PASS 2: 이미지 렌더링 (flash-image 모델)
    # ==========================
    print("  -> [PASS 2] 영문 이미지 인페인팅 렌더링 중...")
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
            print(f"  -> [SUCCESS] {out_name} 최종 저장 완료!")
        else:
            print("  -> [FAILED] Pass 2에서 이미지 데이터를 반환받지 못했습니다.")
            
    except Exception as e:
        print(f"  -> [PASS 2 ERROR] 영문 렌더링 실패: {e}")
    
    time.sleep(8)

if all_translations:
    print("\n[REPORT] 영문 번역 결과 매핑 TXT 문서 생성 중...")
    report_path = os.path.join(target_dir, "EN_Translation_Report.txt")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("==================================================\n")
        f.write("🇺🇸 EN V0 엔진: 한국어 원문 vs 영문 번역 매핑 리포트\n")
        f.write("==================================================\n\n")
        for t in all_translations:
            kor = t.get("kor", "").replace("\n", " ")
            eng = t.get("eng", "").replace("\n", " ")
            src = t.get("source_file", "")
            f.write("--------------------------------------------------\n")
            f.write(f"[파일명]: {src}\n")
            f.write(f"[한국어 원문]: {kor}\n")
            f.write(f"[영문 번역문]: {eng}\n")
        f.write("--------------------------------------------------\n")
    print(f"  -> [SUCCESS] 번역 리포트 저장 완료: {report_path}")

print("\n[FINISH] EN_Text-In_Image_Translation_Engine_V1 영문 이미지 번역 완료!")
