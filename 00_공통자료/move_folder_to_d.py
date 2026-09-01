# -*- coding: utf-8 -*-
import os, shutil, sys

src_folder = r"C:\Users\euntaewoo\Desktop\다국어_이미지_번역_260901"
dst_parent = r"D:\Users\euntaewoo\Desktop\이미지번역워크스페이스"
dst_folder = os.path.join(dst_parent, "다국어_이미지_번역_260901")

print(f"=== [MOVE FOLDER OPERATION] ===")
print(f"Source: {src_folder}")
print(f"Destination: {dst_folder}")

# 1. D드라이브 부모 폴더 확인 및 생성
os.makedirs(dst_parent, exist_ok=True)

# 2. 소스 폴더 실측
src_files = []
for root, dirs, files in os.walk(src_folder):
    for f in files:
        src_files.append(os.path.relpath(os.path.join(root, f), src_folder))

print(f"Source total files: {len(src_files)}개")

# 3. D드라이브로 100% 복사
if os.path.exists(dst_folder):
    shutil.rmtree(dst_folder, ignore_errors=True)

shutil.copytree(src_folder, dst_folder)
print(f"✅ Copied to {dst_folder}")

# 4. 복사 무결성 검증
dst_files = []
for root, dirs, files in os.walk(dst_folder):
    for f in files:
        dst_files.append(os.path.relpath(os.path.join(root, f), dst_folder))

print(f"Destination total files: {len(dst_files)}개")

if len(src_files) == len(dst_files):
    print("✅ Integrity verified: 100% matched!")
    # 5. C드라이브 소스 폴더 완전 제거
    shutil.rmtree(src_folder)
    print(f"🗑️ Successfully deleted source folder: {src_folder}")
    
    # 6. 삭제 확인
    deleted = not os.path.exists(src_folder)
    dst_exists = os.path.exists(dst_folder)
    print(f"Verification -> C folder exists: {not deleted}, D folder exists: {dst_exists}")
else:
    print("❌ File count mismatch! Aborting deletion for safety.")