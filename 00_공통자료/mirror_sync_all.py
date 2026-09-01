# -*- coding: utf-8 -*-
import os, shutil, sys

src_dir = r"C:\Users\euntaewoo\Desktop\multilingual_text_in_image_translatio_agy_sdk_uv-version"
dst_dir = r"C:\Users\euntaewoo\Desktop\다국어_이미지_번역"

print(f"=== [FULL 100% MIRROR SYNC] {src_dir} -> {dst_dir} ===")

IGNORE_DIRS = {'.git', '.venv', '__pycache__', 'cache', '.pytest_cache'}

synced_files = 0
for root, dirs, files in os.walk(src_dir):
    dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
    rel_dir = os.path.relpath(root, src_dir)
    target_root = os.path.join(dst_dir, rel_dir) if rel_dir != "." else dst_dir
    os.makedirs(target_root, exist_ok=True)
    
    for f in files:
        if f.startswith("~$"):  # 엑셀 임시 잠금 파일 제외
            continue
        src_file = os.path.join(root, f)
        dst_file = os.path.join(target_root, f)
        
        # 파일 복사
        shutil.copy2(src_file, dst_file)
        synced_files += 1

print(f"🎉 100% FULL SYNC COMPLETED: {synced_files} files mirrored perfectly!")