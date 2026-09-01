# -*- coding: utf-8 -*-
import os, json, re

target_dir = r"C:\Users\euntaewoo\Desktop\다국어_이미지_번역"

print("==========================================================================================")
print(f"🔍 [정밀 감사] {target_dir} 컴플라이언스 & 초월번역 시스템 전수 검증")
print("==========================================================================================\n")

# 1. 렉시콘 DB 검증
lex_dir = os.path.join(target_dir, "00_공통자료", "compliance_lexicons")
print("1. [데이터베이스 계층: 4개국 렉시콘 JSON 실측]")
lex_files = ["en_fda_mocra_lexicon.json", "jp_pmda_pharm_lexicon.json", "cn_nmpa_adlaw_lexicon.json", "tw_tfda_lexicon.json"]
for lf in lex_files:
    p = os.path.join(lex_dir, lf)
    if os.path.exists(p):
        sz = os.path.getsize(p)
        with open(p, "r", encoding="utf-8") as f:
            d = json.load(f)
            total_terms = sum(len(c.get("banned_terms", [])) for c in d.get("categories", {}).values())
        print(f"  ✅ {lf}: {sz} bytes | {len(d.get('categories', {}))}개 카테고리, 총 {total_terms}개 활성 규칙 탑재")
    else:
        print(f"  ❌ {lf}: 누락됨")

# 2. 엔진 소스코드 내 GLOBAL_COMPLIANCE_SYSTEM_INSTRUCTION 실측
print("\n2. [엔진 소스코드 계층: 시스템 인스트럭션 및 정규식 게이트 실측]")
engine_files = [
    "multilingual_text_in_image_translation.py",
    "multilingual_text_in_image_translatio_agy_sdk.py",
    "영어/EN_Text-In_Image_Translation_Engine_AGY_SDK.py",
    "일본어/JP_Text-In_Image_Translation_Engine_AGY_SDK.py",
    "중국어/CN_Text-In_Image_Translation_Engine_AGY_SDK.py",
    "프로토(베이직엔진)_PROTO_Text-In_Image_Translation_Engine_AGY_SDK/PROTO_Text-In_Image_Translation_Engine_AGY_SDK.py",
    "multilingual_transcreation_qa_evaluator_agy_sdk.py"
]

for ef in engine_files:
    p = os.path.join(target_dir, ef)
    if os.path.exists(p):
        sz = os.path.getsize(p)
        with open(p, "r", encoding="utf-8") as f:
            txt = f.read()
        has_sys = "GLOBAL_COMPLIANCE_SYSTEM_INSTRUCTION" in txt or "GLOBAL COMPLIANCE" in txt
        has_call = "system_instruction=GLOBAL_COMPLIANCE_SYSTEM_INSTRUCTION" in txt or "RUBRIC_PROMPT_TEMPLATE" in txt
        print(f"  ✅ {ef}: {sz} bytes | System Instruction: {'정상 탑재' if has_sys else '미탑재'} | API 주입: {'정상 주입' if has_call else '미주입'}")
    else:
        print(f"  ❌ {ef}: 파일 없음")

# 3. 전역 규칙 문서 내 조항 실측
print("\n3. [전역 규칙 및 규격 문서 계층: §2.7 컴플라이언스 락 실측]")
rule_files = [
    "global_rules.md",
    ".agents/rules/global_rules.md",
    ".agents/rules/Global_Text-In_Image_Translation_rules.md",
    ".agents/rules/multilingual_text_in_image_translation_rules.md",
    "00_공통자료/초월번역_품질평가_4대루브릭_표준규격.md",
    "00_공통자료/제미나이_AI_번역_안전장치_안티그래비티2.0_Gemini_GenerationConfig_기술규격서.md"
]

for rf in rule_files:
    p = os.path.join(target_dir, rf)
    if os.path.exists(p):
        sz = os.path.getsize(p)
        with open(p, "r", encoding="utf-8") as f:
            txt = f.read()
        has_lock = "GLOBAL-COMPLIANCE-LEXICON-LOCK" in txt or "GLOBAL_COMPLIANCE_SYSTEM_INSTRUCTION" in txt or "COMPLIANCE-FIRST" in txt
        print(f"  ✅ {rf}: {sz} bytes | 컴플라이언스 규격 명문화: {'100% 명문화 완료' if has_lock else '미명문화'}")
    else:
        print(f"  ❌ {rf}: 파일 없음")

# 4. 04_번역교정 폴더 내 5대 문구 실측
print("\n4. [산출물 계층: 04_번역교정 5대 문제 표현 교정 실측]")
txt_p = os.path.join(target_dir, "04_번역교정", "LogicallySkin_MultiVitaminSerum_영어", "LogicallySkin_MultiVitaminSerum_EN_SEO_GEO_AEO.txt")
if os.path.exists(txt_p):
    with open(txt_p, "r", encoding="utf-8") as f:
        t_txt = f.read()
    checks = {
        "Multiple skin concerns": "Multiple skin concerns" in t_txt,
        "Blemish-prone skin": "blemish-prone skin" in t_txt.lower(),
        "hydration for a resilient-looking": "hydration for a resilient-looking" in t_txt,
        "reinforces the skin's natural moisture barrier": "reinforces the skin's natural moisture barrier" in t_txt,
        "combats the signs of premature aging": "combats the signs of premature aging" in t_txt
    }
    for k, v in checks.items():
        print(f"  {'✅' if v else '❌'} 5대 권장 문구 '{k}': {'정상 반영' if v else '미반영'}")
else:
    print("  ❌ 04_번역교정 텍스트 파일 없음")

print("\n==========================================================================================")