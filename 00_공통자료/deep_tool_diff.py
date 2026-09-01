# -*- coding: utf-8 -*-
import os, filecmp

dir1 = r"C:\Users\euntaewoo\Desktop\multilingual_text_in_image_translatio_agy_sdk_uv-version"
dir2 = r"C:\Users\euntaewoo\Desktop\다국어_이미지_번역"

def get_all_relative_files(base_dir):
    res = {}
    for root, dirs, files in os.walk(base_dir):
        # 무시할 폴더
        dirs[:] = [d for d in dirs if d not in ['.git', '.venv', '__pycache__', 'cache']]
        for f in files:
            full = os.path.join(root, f)
            rel = os.path.relpath(full, base_dir)
            try:
                sz = os.path.getsize(full)
            except Exception:
                sz = -1
            res[rel] = sz
    return res

files1 = get_all_relative_files(dir1)
files2 = get_all_relative_files(dir2)

only_in_1 = sorted(list(set(files1.keys()) - set(files2.keys())))
only_in_2 = sorted(list(set(files2.keys()) - set(files1.keys())))
common = sorted(list(set(files1.keys()) & set(files2.keys())))

print(f"=== 파일 수 비교 ===")
print(f"uv-version 총 파일 수: {len(files1)}개")
print(f"다국어_이미지_번역 총 파일 수: {len(files2)}개")
print(f"uv-version에만 존재하는 파일 수: {len(only_in_1)}개")
print(f"다국어_이미지_번역에만 존재하는 파일 수: {len(only_in_2)}개")
print(f"공통 파일 수: {len(common)}개")

print("\n=== 1. uv-version에만 존재하는 주요 도구 및 기능 파일 ===")
for f in only_in_1:
    if f.endswith(('.py', '.html', '.json', '.md', '.txt')) and not f.startswith(('01_', '02_', '03_', '04_')):
        print(f"  + [NEW TOOL/DOC] {f} ({files1[f]} bytes)")

print("\n=== 2. 다국어_이미지_번역에만 존재하는 구형/잔재 파일 ===")
for f in only_in_2:
    if f.endswith(('.py', '.html', '.json', '.md', '.txt')) and not f.startswith(('01_', '02_', '03_', '04_')):
        print(f"  - [LEGACY ONLY] {f} ({files2[f]} bytes)")

print("\n=== 3. 공통 파일 중 크기가 다른 주요 스크립트 비교 ===")
diff_scripts = []
for f in common:
    if f.endswith('.py'):
        if files1[f] != files2[f]:
            print(f"  * [DIFF] {f} -> uv-version: {files1[f]} bytes vs legacy: {files2[f]} bytes")
            diff_scripts.append(f)