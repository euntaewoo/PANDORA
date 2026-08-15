import os
import io
import sys
import time
import json
import re
import argparse
from google import genai
from google.genai import types
from PIL import Image

sys.stdout.reconfigure(encoding='utf-8')

# ==========================================
# 0. 경로 및 Google Cloud 인증키 설정
# ==========================================
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, ".."))

# .env 탐색
env_path = os.path.join(project_root, ".env")
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

# 루트 폴더 기준 인증키 fallback 탐색
if not gcp_json_key or not os.path.exists(gcp_json_key):
    fallback_key_path = os.path.join(project_root, "00_공통자료", "인증키_및_계정", "김차장_vertex api_key", "vertex_ai_auth_key.json")
    if os.path.exists(fallback_key_path):
        gcp_json_key = fallback_key_path

if gcp_json_key and os.path.exists(gcp_json_key):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = gcp_json_key
    print(f"[INFO] Vertex AI 서비스 계정 JSON 키 감지: {gcp_json_key}")
    with open(gcp_json_key, 'r', encoding='utf-8') as f:
        key_data = json.load(f)
        project_id = key_data.get('project_id')
    client = genai.Client(vertexai=True, project=project_id, location="global")
elif api_key:
    if api_key.startswith("AQ."):
        print("[INFO] Agent Platform API 키(AQ...) 감지. Vertex AI 모드로 전환합니다.")
        client = genai.Client(vertexai=True, api_key=api_key)
    else:
        client = genai.Client(api_key=api_key)
else:
    print("[ERROR] GEMINI_API_KEY 또는 GOOGLE_APPLICATION_CREDENTIALS가 설정되지 않았습니다.")
    sys.exit(1)

# ==========================================
# 1. 모델 및 파라미터 설정
# ==========================================
MODEL_PRO = "gemini-3.1-pro-preview"       # Pass 1: 텍스트 추출 및 중국 광고법 검열 번역
MODEL_FLASH_IMAGE = "gemini-3.1-flash-image" # Pass 2: 시각적 인페인팅 및 알리바바 푸후이체 식자

# 커맨드라인 인자 파싱
parser = argparse.ArgumentParser(description="CN Text-In-Image Translation Engine V1")
parser.add_argument("source_dir", nargs="?", default=os.path.join(project_root, "01_번역대상_원본"), help="원본 이미지 디렉터리")
parser.add_argument("target_dir", nargs="?", default=None, help="결과물 저장 디렉터리")
parser.add_argument("--target", choices=["CN", "TW", "HK"], default="CN", help="타겟 권역 (CN: 중국본토 간체, TW: 대만 번체, HK: 홍콩 번체)")

args = parser.parse_args()

source_dir = os.path.abspath(args.source_dir)
target_region = args.target.upper()

# 디렉터리명이나 파일명에서 자동 권역 힌트 감지
dir_name_lower = os.path.basename(source_dir).lower()
if "대만" in dir_name_lower or "tw" in dir_name_lower or "번체" in dir_name_lower:
    target_region = "TW"
elif "홍콩" in dir_name_lower or "hk" in dir_name_lower:
    target_region = "HK"
elif "중국" in dir_name_lower or "본토" in dir_name_lower or "간체" in dir_name_lower:
    target_region = "CN"

if args.target_dir:
    target_dir = os.path.abspath(args.target_dir)
else:
    folder_name = os.path.basename(source_dir)
    target_dir = os.path.join(project_root, "02_번역결과_최종", f"{folder_name}_CN_{target_region}_Translated")

os.makedirs(target_dir, exist_ok=True)

print(f"[START] CN_Text-In_Image_Translation_Engine_V1 (Two-Pass Architecture) 가동...")
print(f"[CONFIG] 타겟 권역 모드: {target_region} ({'🇨🇳 중국 본토 간체자 (zh-CN)' if target_region == 'CN' else '🇹🇼 대만 번체자 (zh-TW)' if target_region == 'TW' else '🇭🇰 홍콩 번체자 (zh-HK)'})")
print(f"[CONFIG] 입력 폴더: {source_dir}")
print(f"[CONFIG] 출력 폴더: {target_dir}")

# ==========================================
# 2. 중국 신광고법 및 NMPA 화장품 규정 필터링 정의
# ==========================================
# 중국 신광고법 8대 절대화 금지어 및 화장품 위반 어휘 -> 합법적 순화어 매핑
CN_AD_LAW_FILTERS = {
    r"最": "优",
    r"第一": "前沿",
    r"顶级": "高端",
    r"极品": "优选",
    r"永久": "持久",
    r"彻底": "深层",
    r"万能": "多效",
    r"根除": "改善",
    r"消炎": "舒缓",
    r"镇静": "舒缓修护",
    r"抗衰老": "紧致淡纹",
    r"去皱": "抚平细纹",
    r"再生": "赋活",
    r"无刺激": "温和低敏",
    r"100%安全": "温和配方",
    r"排毒": "净澈肌肤",
    r"美白": "焕亮透光"
}

# ==========================================
# 3. [Pass 1] 권역별 프롬프트 정의
# ==========================================
if target_region == "CN":
    lang_name = "Simplified Chinese (简体中文, zh-CN)"
    region_guidelines = """
[중국 본토 (간체자) 신광고법 및 이커머스 필수 지침]
1. [간체자 강제] 모든 번역문은 반드시 순수 간체자(Simplified Chinese)로 작성하십시오. 번체자 절대 혼용 금지.
2. [중국 신(新) 광고법 절대화 표현 전면 금지]
   - '최고/제일/최상급' 표현 절대 불가: 最, 第一, 顶级, 极品, 极致, 独家 등 금지 -> '卓越', '优异', '高端', '精心' 등으로 순화.
   - '영구/완벽/완전' 표현 금지: 永久, 彻底, 根除, 100%, 零刺激 -> '持久', '深层改善', '温和低敏' 등으로 순화.
3. [NMPA 화장품 효능 표기 가이드]
   - '치료/의약적 효능' 오인 표현 절대 금지: 治疗, 消炎, 镇静, 修复疤痕 -> '舒缓', '修护', '净澈', '维持肌肤稳定' 등으로 대체.
   - '안티에이징/주름제거' -> '紧致淡纹', '改善干纹', '丰盈饱满'.
   - '미백/잡티제거' -> '焕亮肌肤', '改善暗沉', '提亮肤色'.
4. [이커머스 표준 용어 (타오바오/티몰/샤오홍슈)]
   - 수분/보습: 补水 / 保湿
   - 탄력/리프팅: 紧致 / 提拉 / 弹润
   - 진정/피부장벽: 舒缓 / 屏障修护
"""
elif target_region == "TW":
    lang_name = "Traditional Chinese for Taiwan (台灣繁體中文, zh-TW)"
    region_guidelines = """
[대만 번체자 (zh-TW) TFDA 화장품법 및 이커머스 지침]
1. [대만 표준 번체자] 모든 번역문은 반드시 대만 정체자(Traditional Chinese, zh-TW)로 작성하십시오. 간체자 혼용 절대 금지.
2. [대만 뷰티 전문 용어 (Shopee TW / momo 최적화)]
   - 토너/스킨: 化妝水
   - 수분잠금/보습: 鎖水 / 保濕 / 補水
   - 에센스/앰플: 精華液 / 安瓶
   - 피부 탄력: 緊緻 / 澎潤 / 彈力
   - 진정/피부결: 舒緩修護 / 調理肌膚
   - 물광/윤광: 水光肌 / 透亮光澤
3. [TFDA 규정 준수] 의학적 치료, 영구 재생 등 과대광고 표현을 배제하고 부드럽고 신뢰도 높은 어조 적용.
"""
else: # HK
    lang_name = "Traditional Chinese for Hong Kong (香港繁體中文, zh-HK)"
    region_guidelines = """
[홍콩 번체자 (zh-HK) 이커머스 지침]
1. [홍콩 표준 번체자] 모든 번역문은 홍콩 번체자(Traditional Chinese, zh-HK)로 작성하십시오.
2. [홍콩 뷰티 전문 용어 (HKTVmall / Mannings 최적화)]
   - 토너/스킨: 爽膚水
   - 보습/수분: 補濕 / 保濕
   - 에센스/세럼: 精華素 / 精華
   - 클렌징워터: 卸妝水 / 落妝水
   - 피부결: 提亮 / 緊緻 / 舒緩
3. 직관적이고 세련된 홍콩 이커머스 마케팅 톤앤매너 적용.
"""

pass1_prompt = f"""
첨부된 이미지는 화장품/뷰티 상품 상세페이지 또는 제품 패키지입니다.
당신은 중화권 이커머스 마케팅 번역 및 광고법 규제 전문가입니다.
이미지 속의 모든 한국어 텍스트를 정밀하게 추출하고, 아래 [권역별 필수 지침]을 100% 준수하여
'원본 한국어'와 '중국어 번역문' 쌍을 포함하는 JSON 형식의 매핑 데이터를 생성하세요.

[목표 언어]: {lang_name}

{region_guidelines}

[절대 불변 원칙]
1. [패키지 영문/로고 100% 보존] 제품 본품(용기, 튜브, 단상자 등)에 인쇄된 영문 텍스트(예: LOGICALLY SKIN, 제품 영문명 등)와 브랜드 로고는 절대 번역 매핑에 넣지 마세요. 원본 픽셀을 그대로 유지해야 합니다.
2. [전수 추출] 이미지 내의 모든 한국어 텍스트는 단 하나도 빠짐없이 100% 추출하여 번역 매핑에 포함시키십시오.

출력은 반드시 JSON 형식으로 아래 스키마를 엄격히 따르세요:
{{
  "translation_map": [
    {{
      "kor": "한국어 원문",
      "chn": "광고법 준수 중국어 번역문",
      "violation_reason": "광고법/규제 순화 사유 (수정한 경우 기재, 없으면 빈 문자열)"
    }}
  ],
  "required_footnotes": [
    "필요한 법적 주석 문자열 (없으면 빈 배열)"
  ]
}}
"""

# ==========================================
# 4. [Pass 2] 렌더링 지시 프롬프트 템플릿
# ==========================================
pass2_prompt_template = f"""
당신은 정밀한 시각적 로컬라이제이션을 수행하는 이미지 인페인팅 AI입니다.
첨부된 원본 이미지 속의 텍스트 위치, 배경 텍스처, 제품 누끼, 디자인 레이아웃을 1픽셀의 왜곡 없이 그대로 유지하세요.
아래에 제공된 [번역 매핑 데이터 JSON]을 바탕으로 다음 규칙을 엄격히 적용하여 단일 이미지를 생성하세요.

[시각적 렌더링 엄격 규칙]
1. (KOR ERASING) 원본의 한국어 텍스트는 원래 자리에 남겨두지 말고 배경색/텍스처로 완벽하게 덮어써서 100% 지울 것. 병기 절대 금지.
2. (JSON APPLY) 지워진 그 자리에 오직 [번역 매핑 데이터 JSON]의 'chn' 텍스트만 렌더링할 것. 모델 임의로 글자를 누락하거나 수정하지 말 것.
3. (FONT STYLE) 폰트는 중화권 표준 서체인 '알리바바 푸후이체(Alibaba PuHuiTi)' 스타일의 깔끔한 산세리프로 선명하게 렌더링할 것.
4. (FULL INPAINTING NO PATCHING) 텍스트 수정 시 오류 부분만 오려내어 덧칠(Patching)하지 말고, 캔버스 전체를 완전히 새롭게 렌더링(Full Inpainting)하여 1픽셀의 이질감도 없는 완벽한 하나의 이미지를 생성할 것.
5. (PACKAGE PRESERVATION) 제품 본품(용기, 튜브, 박스 등) 표면에 인쇄된 영문 텍스트(예: LOGICALLY SKIN 등) 및 브랜드 로고는 절대 다시 그리거나 훼손하지 말고 100% 완벽하게 보존할 것.
6. (LAYOUT STRICTNESS) 원본 텍스트의 정렬축(좌/우/중앙), 폰트 두께감, 단락 간격을 정확하게 유지할 것.
7. (NO EXTRA NOISE) 번역과 무관한 AI 주석이나 영어 설명, 괄호를 이미지에 임의로 추가하지 말 것.

[번역 매핑 데이터 JSON]
{{json_data}}
"""

# ==========================================
# 5. 이미지 일괄 번역 루프
# ==========================================
targets = [f for f in os.listdir(source_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.jfif', '.webp'))]

if not targets:
    print(f"[WARNING] '{source_dir}' 폴더에 처리할 이미지가 없습니다.")
    sys.exit(0)

all_translations = []

for filename in targets:
    # 이미 번역된 파일 또는 고시표 텍스트 파일 등 스킵
    if '_CN_' in filename or '_JP_' in filename or '_EN_' in filename:
        continue

    in_path = os.path.join(source_dir, filename)
    out_name = f"{os.path.splitext(filename)[0]}_CN_{target_region}_v1.png"
    out_path = os.path.join(target_dir, out_name)

    if os.path.exists(out_path):
        print(f"\n[SKIP] 이미 번역 완료된 파일입니다: {filename}")
        continue

    print(f"\n[RENDER] 변환 시작: {filename}")

    try:
        original_image = Image.open(in_path)
        original_image.load()
    except Exception as e:
        print(f"  -> [ERROR] 이미지 로드 실패: {e}")
        continue

    # ==========================
    # PASS 1: OCR & 번역 매핑 (Pro 모델)
    # ==========================
    print(f"  -> [PASS 1] 텍스트 매핑 및 {target_region} 권역 규제 검열 중...")
    mapping_data_str = None
    for attempt in range(3):
        try:
            response_p1 = client.models.generate_content(
                model=MODEL_PRO,
                contents=[original_image, pass1_prompt],
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                )
            )
            mapping_data_str = response_p1.text
            break
        except Exception as e:
            if "429" in str(e) or "ResourceExhausted" in str(e):
                wait_time = 25 * (attempt + 1)
                print(f"  -> [RATE LIMIT] 429 감지. {wait_time}초 대기 후 재시도... ({attempt+1}/3)")
                time.sleep(wait_time)
            else:
                print(f"  -> [PASS 1 ERROR] {e}")
                break

    if not mapping_data_str:
        print("  -> [PASS 1 FAILED] 번역 매핑 데이터 생성 실패.")
        continue

    # Python 하드 필터링 (중국 본토 모드일 때 신광고법 추가 검열)
    try:
        parsed_json = json.loads(mapping_data_str)
        if "translation_map" in parsed_json:
            for item in parsed_json["translation_map"]:
                chn_text = item.get("chn", "")
                if target_region == "CN":
                    for pattern, safe_word in CN_AD_LAW_FILTERS.items():
                        if re.search(pattern, chn_text):
                            print(f"      [Python Regex Filter] 신광고법 금지어 감지: '{pattern}' -> '{safe_word}' 로 강제 치환")
                            chn_text = re.sub(pattern, safe_word, chn_text)
                            item["violation_reason"] = item.get("violation_reason", "") + f" (Python 정규식 치환: {pattern})"
                item["chn"] = chn_text
                item["source_file"] = filename
            all_translations.extend(parsed_json["translation_map"])
            mapping_data_str = json.dumps(parsed_json, ensure_ascii=False, indent=2)
        print("  -> [PASS 1 SUCCESS] 매핑 데이터 생성 및 검열 완료.")
    except Exception as e:
        print(f"  -> [WARNING] JSON 파싱 경고: {e}")

    # ==========================
    # PASS 2: 이미지 인페인팅 렌더링 (Flash-Image 모델)
    # ==========================
    print("  -> [PASS 2] 이미지 인페인팅 및 알리바바 푸후이체 식자 렌더링 중...")
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
            print(f"  -> [SUCCESS] {out_name} 최종 저장 완료! (해상도: {original_image.size[0]}x{original_image.size[1]} px)")
        else:
            print("  -> [FAILED] Pass 2에서 이미지 데이터를 반환받지 못했습니다.")

    except Exception as e:
        print(f"  -> [PASS 2 ERROR] 렌더링 실패: {e}")

    # 429 방지를 위한 8초 안전 대기
    time.sleep(8)

# ==========================================
# 6. 중국 광고법 준수 및 번역 비교표 리포트 생성
# ==========================================
if all_translations:
    print("\n[REPORT] 중국 광고법 준수 및 번역 비교표 TXT 리포트 생성 중...")
    report_path = os.path.join(target_dir, f"중국어_{target_region}_번역_비교표.txt")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("==================================================\n")
        f.write(f"🇨🇳 CN_Text-In_Image_Translation_Engine_V1 ({target_region} 모드)\n")
        f.write("중국 신(新) 광고법 준수 및 번역 대조표 리포트\n")
        f.write("==================================================\n")
        f.write(f"타겟 권역: {target_region} ({'중국 본토 간체자 zh-CN' if target_region == 'CN' else '대만 번체자 zh-TW' if target_region == 'TW' else '홍콩 번체자 zh-HK'})\n")
        f.write(f"표준 폰트: 알리바바 푸후이체 3.0 (Alibaba PuHuiTi)\n\n")
        for t in all_translations:
            kor = t.get("kor", "").replace("\n", " ")
            chn = t.get("chn", "").replace("\n", " ")
            reason = t.get("violation_reason", "").strip()
            src = t.get("source_file", "")
            f.write("--------------------------------------------------\n")
            f.write(f"[파일명]: {src}\n")
            f.write(f"[한국어 원문]: {kor}\n")
            if reason:
                f.write(f"[광고법/규제 수정 사유]: {reason}\n")
            f.write(f"[중국어 번역]: {chn}\n")
        f.write("--------------------------------------------------\n")
    print(f"  -> [SUCCESS] 비교표 저장 완료: {report_path}")

print(f"\n[FINISH] CN_Text-In_Image_Translation_Engine_V1 모든 작업 완료!")
