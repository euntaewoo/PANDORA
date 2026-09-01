# -*- coding: utf-8 -*-
import os, sys, re

# 1. EN Engine Update
en_file = r"C:\Users\euntaewoo\Desktop\multilingual_text_in_image_translatio_agy_sdk_uv-version\영어\EN_Text-In_Image_Translation_Engine_AGY_SDK.py"
with open(en_file, "r", encoding="utf-8") as f:
    en_content = f.read()

# 렉시콘 로더 추가
en_lex_code = '''
# =================================================================================
# 1-1. 글로벌 컴플라이언스(법무) & 렉시콘 로더
# =================================================================================
GLOBAL_COMPLIANCE_SYSTEM_INSTRUCTION = """[SYSTEM INSTRUCTION: Global Cross-Border E-Commerce Compliance & Prestige Beauty Transcreation Expert]
당신은 미국 FDA(MoCRA), 일본 후생노동성(약기법), 중국 NMPA/신광고법, 대만 TFDA 규정을 완벽히 준수하는 15년 차 글로벌 뷰티 법무 감사관이자, 세포라(Sephora)·백화점 럭셔리 브랜드의 수석 카피라이터입니다.

[엄격 실행 4대 대원칙]
1. [의약품 오인 원천 차단]: 인체 구조, 생리적 기능, 세포(Cellular) 단위 클레임(cellular vitality, cellular resilience 등)을 100% 차단하고 피부 표면 미용적 개선(-looking, moisture barrier)으로 우회.
2. [타겟 권역 문화적 어댑테이션]: K-뷰티 콩글리시('Complex skin issues' -> 'Multiple skin concerns', 'Troubled skin' -> 'Blemish-prone skin') 전면 배제. 노화 서술 시 'combats the signs of premature aging'으로 징후 한정.
3. [디자인 & 레이아웃 최적화]: 백화점 럭셔리 브랜드 수준의 세련된 어휘로 초월번역.
4. [하이퍼파라미터 전역 고정]: temperature: 0.6, top_p: 0.9 유지.
"""

def load_en_compliance_lexicon() -> Dict[str, str]:
    fpath = os.path.join(PROJECT_ROOT, "00_공통자료", "compliance_lexicons", "en_fda_mocra_lexicon.json")
    replacements = {
        r"\\bComplex skin issues\\b": "Multiple skin concerns",
        r"\\bcomplex skin issues\\b": "multiple skin concerns",
        r"\\bTroubled skin\\b": "Blemish-prone skin",
        r"\\btroubled skin\\b": "blemish-prone skin",
        r"\\bnutrients for cellular vitality\\b": "hydration for a resilient-looking complexion",
        r"\\bcellular vitality\\b": "resilient-looking complexion",
        r"\\breinforces cellular resilience\\b": "reinforces the skin's natural moisture barrier",
        r"\\bcellular resilience\\b": "skin's natural moisture barrier",
        r"\\bcombats premature aging\\b": "combats the signs of premature aging",
        r"\\bcombats aging\\b": "combats the signs of aging",
        r"\\bPrescribe\\b": "Targeted Solution for",
        r"\\bBio-Immunity\\b": "Skin Defense",
        r"\\bfed directly\\b": "infused daily",
        r"\\bKyel-Tan-Tone\\b": "Texture, Elasticity & Luminosity",
    }
    if os.path.exists(fpath):
        try:
            with open(fpath, "r", encoding="utf-8") as f:
                data = json.load(f)
                for cat in data.get("categories", {}).values():
                    for it in cat.get("banned_terms", []):
                        b, p = it.get("banned", ""), it.get("preferred", "")
                        if b and p:
                            replacements[rf"\\b{re.escape(b)}\\b"] = p
        except Exception:
            pass
    return replacements
'''

if "GLOBAL_COMPLIANCE_SYSTEM_INSTRUCTION" not in en_content:
    en_content = en_content.replace('MODEL_FLASH_IMAGE = "gemini-3.1-flash-image"', 'MODEL_FLASH_IMAGE = "gemini-3.1-flash-image"\n' + en_lex_code)

# Pass 1 프롬프트 내에 5대 금지어 명시 강화
old_pass1 = 'PASS1_PROMPT = """'
new_pass1 = '''PASS1_PROMPT = """
[MANDATORY COMPLIANCE HARD RULES - 5대 금지 표현 강제 대체]
1. 'Complex skin issues' -> MUST USE: 'Multiple skin concerns'
2. 'Troubled skin' -> MUST USE: 'Blemish-prone skin'
3. 'cellular vitality / nutrients for cellular vitality' -> MUST USE: 'hydration for a resilient-looking complexion'
4. 'cellular resilience / reinforces cellular resilience' -> MUST USE: 'reinforces the skin's natural moisture barrier'
5. 'combats premature aging' -> MUST USE: 'combats the signs of premature aging'
'''
if "[MANDATORY COMPLIANCE HARD RULES" not in en_content:
    en_content = en_content.replace(old_pass1, new_pass1)

# GenerateContentConfig 호출부에 system_instruction 주입 및 후처리 게이트 연동
en_content = en_content.replace(
    '                    config=types.GenerateContentConfig(\n                        response_mime_type="application/json",\n                        temperature=0.6,\n                        top_p=0.9,\n                        max_output_tokens=8192\n                    ),',
    '                    config=types.GenerateContentConfig(\n                        system_instruction=GLOBAL_COMPLIANCE_SYSTEM_INSTRUCTION,\n                        response_mime_type="application/json",\n                        temperature=0.6,\n                        top_p=0.9,\n                        max_output_tokens=8192\n                    ),'
)

# 후처리 게이트 추가
old_p1_save = '                if "translation_map" in parsed_json:\n                    for item in parsed_json["translation_map"]:\n                        item["source_file"] = filename\n                        item["mode"] = mode'
new_p1_save = '''                if "translation_map" in parsed_json:
                    en_reps = load_en_compliance_lexicon()
                    for item in parsed_json["translation_map"]:
                        item["source_file"] = filename
                        item["mode"] = mode
                        cor_en = item.get("corrected_en", "")
                        orig_cor = cor_en
                        for pat, rep in en_reps.items():
                            cor_en = re.sub(pat, rep, cor_en, flags=re.IGNORECASE)
                        if cor_en != orig_cor:
                            item["corrected_en"] = cor_en
                            print(f"     ⚡ [EN 법규 자동 보정] `{orig_cor[:35]}` ➔ `{cor_en[:35]}`")'''

en_content = en_content.replace(old_p1_save, new_p1_save)

with open(en_file, "w", encoding="utf-8") as f:
    f.write(en_content)
print("SUCCESS: Updated EN Engine.")

# 2. QA Evaluator Update
qa_eval_file = r"C:\Users\euntaewoo\Desktop\multilingual_text_in_image_translatio_agy_sdk_uv-version\multilingual_text_in_image_translatio_agy_sdk_core\multilingual_transcreation_qa_evaluator_agy_sdk.py"
with open(qa_eval_file, "r", encoding="utf-8") as f:
    qa_content = f.read()

# 루브릭 프롬프트 내에 5대 금지어 감점 및 교정 룰 추가
old_rubric_rule = '2. [국가별 광고법 무결성 (30점)]: 미국 MoCRA(치료 오인어 배제), 일본 약기법 56종, 중국 신광고법 8대 절대화 금지어 준수.'
new_rubric_rule = '''2. [국가별 광고법 무결성 (30점)]: 미국 MoCRA(세포/생리기능 cellular vitality/cellular resilience 클레임 엄격 금지, 노화는 반드시 signs of aging으로 한정), 일본 약기법 56종, 중국 신광고법 8대 절대화 금지어 준수.
   - [필수 교정 감점 대상]: 'Complex skin issues'(-> Multiple skin concerns), 'Troubled skin'(-> Blemish-prone skin), 'cellular vitality'(-> resilient-looking complexion), 'cellular resilience'(-> skin's natural moisture barrier), 'combats premature aging'(-> combats the signs of premature aging) 미준수 시 ad_law_compliance 즉시 감점 및 correction_feedbacks 필수 생성.'''

if "[필수 교정 감점 대상]" not in qa_content:
    qa_content = qa_content.replace(old_rubric_rule, new_rubric_rule)

with open(qa_eval_file, "w", encoding="utf-8") as f:
    f.write(qa_content)
print("SUCCESS: Updated QA Evaluator.")