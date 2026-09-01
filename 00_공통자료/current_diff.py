# -*- coding: utf-8 -*-
import os

dir1 = r"C:\Users\euntaewoo\Desktop\multilingual_text_in_image_translatio_agy_sdk_uv-version"
dir2 = r"C:\Users\euntaewoo\Desktop\다국어_이미지_번역"

def get_files(d):
    res = set()
    for root, dirs, files in os.walk(d):
        dirs[:] = [x for x in dirs if x not in ['.git', '.venv', '__pycache__', 'cache']]
        for f in files:
            if not f.startswith("~$"):
                res.add(os.path.relpath(os.path.join(root, f), d))
    return res

f1 = get_files(dir1)
f2 = get_files(dir2)

print("=== 현 시점 실측 비교 ===")
print(f"1. uv-version 파일 수: {len(f1)}개")
print(f"2. 다국어_이미지_번역 파일 수: {len(f2)}개")

only_in_1 = f1 - f2
only_in_2 = f2 - f1

print(f"3. uv-version에만 있는 파일: {len(only_in_1)}개 -> {only_in_1}")
print(f"4. 다국어_이미지_번역에만 있는 파일 (과거 이력 파일): {len(only_in_2)}개")
for x in sorted(list(only_in_2)):
    print(f"   - {x}")