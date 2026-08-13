import os
import io
import sys
import time
import json
import argparse
import re
from google import genai
from google.genai import types
from PIL import Image

sys.stdout.reconfigure(encoding='utf-8')

# 커맨드라인 파라미터 파싱
parser = argparse.ArgumentParser(description="Global Text-In_Image Translation Engine")
parser.add_argument("source_dir", nargs='?', default=r"C:\Users\euntaewoo\Desktop\이미지번역워크스페이스\변역대상", help="Source directory containing images")
parser.add_argument("target_dir", nargs='?', default=r"C:\Users\euntaewoo\Desktop\이미지번역워크스페이스\변역결과_Global", help="Target directory for output images")
parser.add_argument("--lang", required=True, choices=['EN', 'JP'], help="Target translation language (EN or JP)")
args = parser.parse_args()

TARGET_LANG = args.lang
source_dir = args.source_dir
base_target_dir = args.target_dir

# 로컬 상대경로의 .env 파일 탐색 및 키 추출
script_dir = os.path.dirname(os.path.abspath(__file__))
lang_folder_name = "영어" if TARGET_LANG == "EN" else "일본어"
env_path = os.path.join(script_dir, lang_folder_name, ".env")
api_key = os.environ.get("GEMINI_API_KEY")
gcp_json_key = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")

if not api_key:
    api_key = os.environ.get("GEMINI_API_KEY")
if not gcp_json_key:
    gcp_json_key = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")

if not api_key and not gcp_json_key and os.path.exists(env_path):
    with open(env_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line.startswith("#"):
                continue
            if line.startswith("GEMINI_API_KEY="):
                api_key = line.split("=", 1)[1].strip()
            elif line.startswith("GOOGLE_APPLICATION_CREDENTIALS="):
                gcp_json_key = line.split("=", 1)[1].strip().strip('"').strip("'")

if gcp_json_key and os.path.exists(gcp_json_key):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = gcp_json_key
    print(f"[INFO] Vertex AI 서비스 계정 JSON 키가 감지되었습니다: {gcp_json_key}")
    with open(gcp_json_key, 'r', encoding='utf-8') as f:
        key_data = json.load(f)
        project_id = key_data.get('project_id')
    client = genai.Client(vertexai=True, project=project_id, location="us-central1")
elif api_key:
    if api_key.startswith("AQ."):
        print("[INFO] Agent Platform API 키(AQ...)가 감지되었습니다. Vertex AI 모드로 전환합니다.")
        client = genai.Client(vertexai=True, api_key=api_key)
    else:
        client = genai.Client(api_key=api_key)
else:
    print("[ERROR] GEMINI_API_KEY 또는 GOOGLE_APPLICATION_CREDENTIALS가 설정되지 않았습니다.")
    sys.exit(1)

print("[SUCCESS] API Key 인증 체계가 다중 계층(google-genai 최신 SDK)으로 복구되었습니다.")

# 모델 세팅
MODEL_PRO = "gemini-3.1-pro-preview"
MODEL_FLASH_IMAGE = "gemini-3.1-flash-image"

# ==========================
# 플러그인 팩(Rule) 로드
# ==========================
rules_path = os.path.join(script_dir, "config", f"{TARGET_LANG}_translation_rules.json")
if not os.path.exists(rules_path):
    print(f"[ERROR] 룰 파일이 존재하지 않습니다: {rules_path}")
    sys.exit(1)

with open(rules_path, "r", encoding="utf-8") as f:
    rules = json.load(f)

font_rules = rules.get("font_requirements", {})
censorship_rules = rules.get("censorship_rules", {})
translation_tone = rules.get("translation_tone", {})

forbidden_patterns = censorship_rules.get("forbidden_regex_patterns", {})
apply_medical_law = censorship_rules.get("apply_medical_efficacy_law_56", False)

efficacy_list_str = ""
if apply_medical_law:
    efficacy_json_path = os.path.join(script_dir, "일본어", "cosmetics_efficacy_56.json")
    if os.path.exists(efficacy_json_path):
        with open(efficacy_json_path, "r", encoding="utf-8") as ef:
            efficacy_data = json.load(ef)
            efficacy_list_str = "\n".join([f"{item['id']}. {item['claim_jp']} ({item['claim_ko']})" for item in efficacy_data])
            print(f"[INFO] 56종 허용 효능 규격 로드 완료 ({len(efficacy_data)}종)")

# 폴더 설정 (껍데기 하위 폴더 생성 금지, 다이렉트 안착)
target_dir = base_target_dir
os.makedirs(target_dir, exist_ok=True)

# [Pass 1] 약기법 및 번역 매핑 프롬프트
pass1_prompt = f"""
첨부된 이미지는 화장품 상세페이지 또는 제품 패키지입니다.
이미지 내의 모든 한국어 텍스트를 스캔하고, 아래 [번역 지침]을 100% 반영하여 
'원본 한국어'와 '번역된 {TARGET_LANG}' 쌍을 포함하는 JSON 형식의 매핑 데이터를 생성하세요.

[번역 지침 (Tone & Manner)]
{translation_tone.get('directive', '')}

"""

if apply_medical_law:
    pass1_prompt += f"""
[후생노동성 공인 56종 허용 효능 목록 (Positive List)]
{efficacy_list_str}

[약기법 필수 준수 지침]
1. 일본 화장품법은 포지티브 리스트 방식입니다. '치료/효능'이 아닌 '세정/관리/느낌' 위주로 순화하세요.
2. '자극 없이', '무자극' -> '저자극 처방(低刺激処方)'.
3. '재생', '치료', '디톡스', '해독' 절대 금지 -> '피부를 정돈하다(肌を整える)' 등으로 대체.
4. '미백' -> '수분을 주어 투명감 있는 피부로 케어'.
"""

pass1_prompt += """
14. [중요] 제품 패키지/용기에 적힌 영문 텍스트는 절대 번역하거나 매핑 딕셔너리에 포함시키지 마세요.
16. [엄격 주의] 이미지 내의 모든 한국어 텍스트는 단 하나도 빠짐없이 100% 추출하여 번역 매핑에 포함시켜야 합니다.
17. [안전망 규칙] 이미지 내에 정보 고시 표나 복잡한 표(테이블) 레이아웃이 포함된 경우, 본 V6/V7 인페인팅 방식으로 렌더링하지 마십시오.

출력은 반드시 JSON 형식으로 아래 스키마를 엄격히 따르세요. 어떠한 마크다운 코드 블록도 쓰지 마세요.
{
  "translation_map": [
    {
      "kor": "한국어 원문", 
      "rule_check_reasoning": "번역 검열 사고 과정",
      "target_lang": "검열 및 가이드가 반영된 최종 번역문",
      "violation_reason": "수정 사유 (수정한 경우에만 기재, 아니면 빈 문자열)"
    }
  ]
}
"""

# [Pass 2] 렌더링 지시 프롬프트 템플릿
pass2_prompt_template = f"""
당신은 정밀한 시각적 로컬라이제이션을 수행하는 이미지 인페인팅 AI입니다.
아래에 제공된 [번역 매핑 데이터 JSON]을 바탕으로 다음 규칙을 엄격히 적용하여 단일 이미지를 생성하세요.

[시각적 렌더링 엄격 규칙]
1. (KOR ERASING) 원본의 한국어 텍스트는 원래 자리에 남겨두지 말고 배경색으로 덮어써서 100% 지울 것. 
2. (JSON APPLY) 지워진 그 자리에 오직 [번역 매핑 데이터 JSON]의 'target_lang' 텍스트만 렌더링할 것.
3. (FULL REGENERATION) 번역 검수 결과 텍스트 뭉개짐이나 번역 오류가 발생하더라도, **절대 오류가 발생한 부분만 오려서 수정(Patching)하지 마세요.** 반드시 캔버스 전체를 새롭게 다시 시작하여 1픽셀의 이질감도 없는 완벽한 하나의 이미지를 처음부터 끝까지 새로 그려야(Full Regeneration) 합니다.
4. (FONT DIRECTIVE) {font_rules.get('style_directive', '')} (지정 폰트: {font_rules.get('primary_font', '')})
5. (PACKAGE PRESERVATION) 본품(용기) 표면에 인쇄된 영문 텍스트는 100% 완벽하게 보존해야 합니다.
9. (HTML TO PNG RULE) 표 레이아웃이 감지되면 어떠한 텍스트 덮어쓰기 작업도 강행하지 마세요.

[번역 매핑 데이터 JSON]
{{json_data}}
"""

print(f"[START] Global Text-In_Image Translation Engine ({TARGET_LANG} Mode) 가동...")
print(f"[INFO] 타겟 스캔 폴더: {source_dir}")

targets = [f for f in os.listdir(source_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

if not targets:
    print(f"[WARNING] '{source_dir}' 폴더에 처리할 이미지가 없습니다.")
    sys.exit(0)

all_translations = []

for filename in targets:
    time.sleep(22)
    if f'_{TARGET_LANG}_' in filename:
        continue
        
    in_path = os.path.join(source_dir, filename)
    out_name = f"{os.path.splitext(filename)[0]}_{TARGET_LANG}_Global_Translated.png"
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
    # PASS 1: 텍스트 추출 및 번역
    # ==========================
    print("  -> [PASS 1] 텍스트 매핑 생성 중...")
    try:
        response_p1 = client.models.generate_content(
            model=MODEL_PRO,
            contents=[original_image, pass1_prompt]
        )
        mapping_data_str = response_p1.text
        
        # [안전망] 마크다운 클리닝 처리 (에러 튕김 방지)
        mapping_data_str = mapping_data_str.strip()
        if mapping_data_str.startswith("```json"):
            mapping_data_str = mapping_data_str[7:]
        elif mapping_data_str.startswith("```"):
            mapping_data_str = mapping_data_str[3:]
        if mapping_data_str.endswith("```"):
            mapping_data_str = mapping_data_str[:-3]
        mapping_data_str = mapping_data_str.strip()

        parsed_json = json.loads(mapping_data_str)
        if "translation_map" in parsed_json:
            for item in parsed_json["translation_map"]:
                translated_text = item.get("target_lang", "")
                
                # Python 하드 필터링 (JSON 팩 설정 기반 동적 적용)
                if forbidden_patterns:
                    for pattern, safe_word in forbidden_patterns.items():
                        if re.search(pattern, translated_text):
                            print(f"      [Regex Filter] 금지어 감지: '{pattern}' -> '{safe_word}' 치환")
                            translated_text = re.sub(pattern, safe_word, translated_text)
                            item["violation_reason"] = item.get("violation_reason", "") + f" (Filter: {pattern})"
                            
                item["target_lang"] = translated_text
                item["source_file"] = filename
            all_translations.extend(parsed_json["translation_map"])
            
        # JSON 덤프 후 Pass2에 넘길 문자열 재생성 (클리닝 및 Regex 필터링 반영본)
        mapping_data_str = json.dumps(parsed_json, ensure_ascii=False)
        print("  -> [PASS 1 SUCCESS] 매핑 데이터 생성 완료.")
    except Exception as e:
        print(f"  -> [PASS 1 ERROR] 매핑 실패 (JSON 파싱 에러 등): {e}")
        continue

    # ==========================
    # PASS 2: 이미지 렌더링
    # ==========================
    print("  -> [PASS 2] 이미지 인페인팅 렌더링 중...")
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
                            
        if img_saved:
            print(f"  -> [SUCCESS] {out_name} 최종 저장 완료!")
        else:
            print("  -> [FAILED] Pass 2에서 이미지 데이터를 반환받지 못했습니다.")
            
    except Exception as e:
        print(f"  -> [PASS 2 ERROR] 렌더링 실패: {e}")
    
    time.sleep(8)

if all_translations:
    report_path = os.path.join(target_dir, f"{TARGET_LANG}_번역_비교표.txt")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(f"=== Global Translation Engine [{TARGET_LANG}] Report ===\n\n")
        for t in all_translations:
            kor = t.get("kor", "").replace("\n", " ")
            tgt = t.get("target_lang", "").replace("\n", " ")
            reason = t.get("violation_reason", "")
            f.write(f"- 원본: {kor}\n- 번역: {tgt}\n- 검열/수정사유: {reason}\n\n")

print(f"\n[FINISH] Global Text-In_Image Translation Engine ({TARGET_LANG}) 완료!")
