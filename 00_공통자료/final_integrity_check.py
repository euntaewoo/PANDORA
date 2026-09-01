# -*- coding: utf-8 -*-
import os, json, subprocess, sys

dir1 = r"C:\Users\euntaewoo\Desktop\multilingual_text_in_image_translatio_agy_sdk_uv-version"
dir2 = r"C:\Users\euntaewoo\Desktop\다국어_이미지_번역"

print("==========================================================================================")
print("🛡️ [최종 무결성 전수 감사] 누락 작업 점검")
print("==========================================================================================\n")

# 1. verify_pipeline.py 실행 검증 (양쪽 모두)
print("1. [단위 테스트 자동 검증]")
for d_name, d_path in [("uv-version", dir1), ("다국어_이미지_번역", dir2)]:
    v_script = os.path.join(d_path, "00_공통자료", "verify_pipeline.py")
    if os.path.exists(v_script):
        res = subprocess.run(["uv", "run", "python", v_script], capture_output=True, text=True, cwd=d_path)
        passed = "[ALL TESTS PASSED]" in res.stdout
        print(f"  - {d_name}: {'✅ ALL TESTS PASSED' if passed else '❌ FAILED'}")
    else:
        print(f"  - {d_name}: ❌ verify_pipeline.py 없음")

# 2. 4개국 렉시콘 JSON 4종 검증
print("\n2. [4개국 렉시콘 JSON DB 검증]")
for d_name, d_path in [("uv-version", dir1), ("다국어_이미지_번역", dir2)]:
    lex_p = os.path.join(d_path, "00_공통자료", "compliance_lexicons")
    files = ["en_fda_mocra_lexicon.json", "jp_pmda_pharm_lexicon.json", "cn_nmpa_adlaw_lexicon.json", "tw_tfda_lexicon.json"]
    all_ok = True
    for f in files:
        if not os.path.exists(os.path.join(lex_p, f)):
            all_ok = False
            break
    print(f"  - {d_name} 4종 JSON DB: {'✅ 100% 정상 탑재' if all_ok else '❌ 누락'}")

# 3. 04_번역교정 5대 문제 표현 교정 검증
print("\n3. [04_번역교정 5대 문제 표현 교정 검증]")
for d_name, d_path in [("uv-version", dir1), ("다국어_이미지_번역", dir2)]:
    txt_p = os.path.join(d_path, "04_번역교정", "LogicallySkin_MultiVitaminSerum_영어", "LogicallySkin_MultiVitaminSerum_EN_SEO_GEO_AEO.txt")
    if os.path.exists(txt_p):
        with open(txt_p, "r", encoding="utf-8") as f:
            c = f.read()
        has_5 = ("Multiple skin concerns" in c and 
                 "blemish-prone skin" in c.lower() and 
                 "hydration for a resilient-looking" in c and 
                 "reinforces the skin's natural moisture barrier" in c and 
                 "combats the signs of premature aging" in c)
        print(f"  - {d_name} 5대 문구 교정: {'✅ 100% 교정 완료' if has_5 else '❌ 미교정'}")
    else:
        print(f"  - {d_name}: ❌ 파일 없음")

# 4. Git 상태 점검 (uv-version)
print("\n4. [Git 형상 관리 상태 점검]")
res_git = subprocess.run(["git", "status", "--short"], capture_output=True, text=True, cwd=dir1)
print(f"  - uv-version Git 변경사항:\n{res_git.stdout.strip() if res_git.stdout.strip() else '  (clean working tree)'}")

print("\n==========================================================================================")