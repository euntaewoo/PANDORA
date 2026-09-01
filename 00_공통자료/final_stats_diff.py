# -*- coding: utf-8 -*-
import os

dir1 = r"C:\Users\euntaewoo\Desktop\multilingual_text_in_image_translatio_agy_sdk_uv-version"
dir2 = r"C:\Users\euntaewoo\Desktop\다국어_이미지_번역"

def get_stats(d):
    file_count = 0
    dir_count = 0
    total_size = 0
    for root, dirs, files in os.walk(d):
        dirs[:] = [x for x in dirs if x not in ['.git', '.venv', '__pycache__', 'cache']]
        dir_count += len(dirs)
        for f in files:
            if not f.startswith("~$"):
                file_count += 1
                try:
                    total_size += os.path.getsize(os.path.join(root, f))
                except Exception:
                    pass
    return dir_count, file_count, total_size

d1, f1, s1 = get_stats(dir1)
d2, f2, s2 = get_stats(dir2)

print(f"=== [최종 실측 대조표] ===")
print(f"1. uv-version: 폴더 {d1}개, 파일 {f1}개, 총 용량 {s1 / (1024*1024):.2f} MB")
print(f"2. 다국어_이미지_번역: 폴더 {d2}개, 파일 {f2}개, 총 용량 {s2 / (1024*1024):.2f} MB")