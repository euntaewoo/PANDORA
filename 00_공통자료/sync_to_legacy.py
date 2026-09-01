# -*- coding: utf-8 -*-
import os, shutil, sys

src_dir = r"C:\Users\euntaewoo\Desktop\multilingual_text_in_image_translatio_agy_sdk_uv-version"
dst_dir = r"C:\Users\euntaewoo\Desktop\다국어_이미지_번역"

print(f"=== [START SYNC] {src_dir} -> {dst_dir} ===")

# 1. 00_공통자료/compliance_lexicons 복사
src_lex = os.path.join(src_dir, "00_공통자료", "compliance_lexicons")
dst_lex = os.path.join(dst_dir, "00_공통자료", "compliance_lexicons")
os.makedirs(dst_lex, exist_ok=True)
for f in os.listdir(src_lex):
    shutil.copy2(os.path.join(src_lex, f), os.path.join(dst_lex, f))
    print(f"  [SYNC] 00_공통자료/compliance_lexicons/{f}")

# 2. 전용 자율 감사 도구 및 동기화 엔진 복사
sync_tools = [
    ("00_공통자료/sync_regulatory_lexicon.py", "00_공통자료/sync_regulatory_lexicon.py"),
    ("00_공통자료/verify_pipeline.py", "00_공통자료/verify_pipeline.py"),
    ("00_공통자료/render_notice_table_standard.py", "00_공통자료/render_notice_table_standard.py"),
    ("00_공통자료/render_notice_table_korean.py", "00_공통자료/render_notice_table_korean.py"),
    ("00_공통자료/초월번역_품질평가_4대루브릭_표준규격.md", "00_공통자료/초월번역_품질평가_4대루브릭_표준규격.md"),
    ("00_공통자료/제미나이_AI_번역_안전장치_안티그래비티2.0_Gemini_GenerationConfig_기술규격서.md", "00_공통자료/제미나이_AI_번역_안전장치_안티그래비티2.0_Gemini_GenerationConfig_기술규격서.md"),
    ("make_qa_report.py", "make_qa_report.py"),
    ("evaluate_transcreation_quality.py", "evaluate_transcreation_quality.py"),
    ("docx_to_html.py", "docx_to_html.py"),
    ("global_rules.md", "global_rules.md"),
    ("제미나이_AI_번역_안전장치_안티그래비티2.0_Gemini_GenerationConfig_기술규격서.md", "제미나이_AI_번역_안전장치_안티그래비티2.0_Gemini_GenerationConfig_기술규격서.md"),
]

for s_rel, d_rel in sync_tools:
    s_full = os.path.join(src_dir, s_rel)
    d_full = os.path.join(dst_dir, d_rel)
    if os.path.exists(s_full):
        os.makedirs(os.path.dirname(d_full), exist_ok=True)
        shutil.copy2(s_full, d_full)
        print(f"  [SYNC] {d_rel}")

# 3. .agents/rules/ 전역 규칙 문서 동기화
src_rules = os.path.join(src_dir, ".agents", "rules")
dst_rules = os.path.join(dst_dir, ".agents", "rules")
os.makedirs(dst_rules, exist_ok=True)
for f in os.listdir(src_rules):
    shutil.copy2(os.path.join(src_rules, f), os.path.join(dst_rules, f))
    print(f"  [SYNC] .agents/rules/{f}")

# 4. 코어 번역 엔진 및 루트 엔진 동기화
shutil.copy2(
    os.path.join(src_dir, "multilingual_text_in_image_translatio_agy_sdk_core", "multilingual_text_in_image_translation.py"),
    os.path.join(dst_dir, "multilingual_text_in_image_translation.py")
)
print("  [SYNC] multilingual_text_in_image_translation.py (Core & Root)")

# 코어 평가기 동기화
if os.path.exists(os.path.join(src_dir, "multilingual_text_in_image_translatio_agy_sdk_core", "multilingual_transcreation_qa_evaluator_agy_sdk.py")):
    shutil.copy2(
        os.path.join(src_dir, "multilingual_text_in_image_translatio_agy_sdk_core", "multilingual_transcreation_qa_evaluator_agy_sdk.py"),
        os.path.join(dst_dir, "multilingual_transcreation_qa_evaluator_agy_sdk.py")
    )
    print("  [SYNC] multilingual_transcreation_qa_evaluator_agy_sdk.py")

# 5. 각 언어별 독립 엔진 동기화
lang_engines = [
    ("영어/EN_Text-In_Image_Translation_Engine_AGY_SDK.py", "영어/EN_Text-In_Image_Translation_Engine_AGY_SDK.py"),
    ("일본어/JP_Text-In_Image_Translation_Engine_AGY_SDK.py", "일본어/JP_Text-In_Image_Translation_Engine_AGY_SDK.py"),
    ("중국어/CN_Text-In_Image_Translation_Engine_AGY_SDK.py", "중국어/CN_Text-In_Image_Translation_Engine_AGY_SDK.py"),
    ("프로토(베이직엔진)_PROTO_Text-In_Image_Translation_Engine_AGY_SDK/PROTO_Text-In_Image_Translation_Engine_AGY_SDK.py", "프로토(베이직엔진)_PROTO_Text-In_Image_Translation_Engine_V0/PROTO_Text-In_Image_Translation_Engine_V0.py"),
    ("일본어/README.md", "일본어/README.md"),
    ("중국어/README.md", "중국어/README.md"),
]

for s_rel, d_rel in lang_engines:
    s_full = os.path.join(src_dir, s_rel)
    d_full = os.path.join(dst_dir, d_rel)
    if os.path.exists(s_full):
        os.makedirs(os.path.dirname(d_full), exist_ok=True)
        shutil.copy2(s_full, d_full)
        print(f"  [SYNC] {d_rel}")

# 6. 04_번역교정 폴더 통째로 동기화
src_04 = os.path.join(src_dir, "04_번역교정")
dst_04 = os.path.join(dst_dir, "04_번역교정")
if os.path.exists(src_04):
    if os.path.exists(dst_04):
        shutil.rmtree(dst_04)
    shutil.copytree(src_04, dst_04)
    print("  [SYNC] 04_번역교정/ 폴더 전수 동기화 완료")

print("\n🎉 ALL COMPONENTS SUCCESSFULLY SYNCED TO C:\\Users\\euntaewoo\\Desktop\\다국어_이미지_번역")