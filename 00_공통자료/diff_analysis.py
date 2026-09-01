# -*- coding: utf-8 -*-
import os

dir1 = r"C:\Users\euntaewoo\Desktop\multilingual_text_in_image_translatio_agy_sdk_uv-version"
dir2 = r"C:\Users\euntaewoo\Desktop\다국어_이미지_번역"

def check_feature(dpath, rel_path):
    full = os.path.join(dpath, rel_path)
    return os.path.exists(full)

print("=== 비교 분석 실측 데이터 ===")
print("1. 04_번역교정 폴더:")
print("   - uv-version:", check_feature(dir1, "04_번역교정"))
print("   - 다국어_이미지_번역:", check_feature(dir2, "04_번역교정"))

print("2. compliance_lexicons (4개국 법령 DB):")
print("   - uv-version:", check_feature(dir1, "00_공통자료/compliance_lexicons"))
print("   - 다국어_이미지_번역:", check_feature(dir2, "00_공통자료/compliance_lexicons"))

print("3. sync_regulatory_lexicon.py:")
print("   - uv-version:", check_feature(dir1, "00_공통자료/sync_regulatory_lexicon.py"))
print("   - 다국어_이미지_번역:", check_feature(dir2, "00_공통자료/sync_regulatory_lexicon.py"))

print("4. pyproject.toml / uv 환경 관리:")
print("   - uv-version:", check_feature(dir1, "pyproject.toml") or check_feature(dir1, "uv.lock"))
print("   - 다국어_이미지_번역:", check_feature(dir2, "pyproject.toml") or check_feature(dir2, "uv.lock"))

print("5. 메인 엔진 파일명:")
print("   - uv-version:", [f for f in os.listdir(dir1) if "multilingual" in f.lower()])
print("   - 다국어_이미지_번역:", [f for f in os.listdir(dir2) if "multilingual" in f.lower()])

# 비교분석표 문서가 있다면 확인
comp_doc = os.path.join(dir2, "다국어_이미지_번역_3대_프로그램_아키텍처_비교분석표.md")
if os.path.exists(comp_doc):
    with open(comp_doc, "r", encoding="utf-8") as f:
        print("\n=== 다국어_이미지_번역_3대_프로그램_아키텍처_비교분석표.md 발췌 ===")
        print(f.read()[:1000])