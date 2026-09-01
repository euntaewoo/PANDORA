# -*- coding: utf-8 -*-
import os, shutil, stat

src_folder = r"C:\Users\euntaewoo\Desktop\다국어_이미지_번역_260901"
dst_folder = r"D:\Users\euntaewoo\Desktop\이미지번역워크스페이스\다국어_이미지_번역_260901"

def remove_readonly(func, path, exc_info):
    try:
        os.chmod(path, stat.S_IWRITE)
        func(path)
    except Exception as e:
        pass

# 1. D드라이브 존재 확인
dst_exists = os.path.exists(dst_folder)
dst_file_count = 0
if dst_exists:
    for root, dirs, files in os.walk(dst_folder):
        dst_file_count += len(files)

print(f"D Drive Folder Exists: {dst_exists} (Total files: {dst_file_count}개)")

# 2. C드라이브 완전 삭제 (읽기전용 핸들러 포함)
if os.path.exists(src_folder):
    shutil.rmtree(src_folder, onerror=remove_readonly)
    print(f"Removed C folder: {src_folder}")

# 3. 최종 확인
src_exists = os.path.exists(src_folder)
print(f"Final Verification -> C folder exists: {src_exists}, D folder exists: {dst_exists}")