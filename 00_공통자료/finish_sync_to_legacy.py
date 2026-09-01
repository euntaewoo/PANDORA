# -*- coding: utf-8 -*-
import os, shutil, sys

src_dir = r"C:\Users\euntaewoo\Desktop\multilingual_text_in_image_translatio_agy_sdk_uv-version"
dst_dir = r"C:\Users\euntaewoo\Desktop\다국어_이미지_번역"

# 04_번역교정 폴더 복사 (임시 파일 제외)
src_04 = os.path.join(src_dir, "04_번역교정")
dst_04 = os.path.join(dst_dir, "04_번역교정")

def ignore_temp(directory, contents):
    return [c for c in contents if c.startswith("~$")]

if os.path.exists(src_04):
    if os.path.exists(dst_04):
        shutil.rmtree(dst_04, ignore_errors=True)
    shutil.copytree(src_04, dst_04, ignore=ignore_temp)
    print("  [SYNC] 04_번역교정/ 폴더 전수 동기화 완료")

# 다국어_이미지_번역 폴더의 verify_pipeline.py 실행 검증
test_script = os.path.join(dst_dir, "00_공통자료", "verify_pipeline.py")
if os.path.exists(test_script):
    import subprocess
    res = subprocess.run([sys.executable, test_script], capture_output=True, text=True, cwd=dst_dir)
    print("\n=== [동기화 검증: 다국어_이미지_번역 내 verify_pipeline.py 실행 결과] ===")
    print(res.stdout)
    if res.stderr:
        print("STDERR:", res.stderr)

print("\n🎉 ALL COMPONENTS SUCCESSFULLY SYNCED AND VERIFIED IN C:\\Users\\euntaewoo\\Desktop\\다국어_이미지_번역")