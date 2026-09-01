# -*- coding: utf-8 -*-
import os

dir1 = r"C:\Users\euntaewoo\Desktop\multilingual_text_in_image_translatio_agy_sdk_uv-version"
dir2 = r"C:\Users\euntaewoo\Desktop\다국어_이미지_번역"

print(f"=== DIR 1: {dir1} ===")
print("Exists:", os.path.exists(dir1))

print(f"\n=== DIR 2: {dir2} ===")
print("Exists:", os.path.exists(dir2))
if os.path.exists(dir2):
    items = os.listdir(dir2)
    print(f"Items count: {len(items)}")
    for it in items:
        full = os.path.join(dir2, it)
        is_d = os.path.isdir(full)
        sz = os.path.getsize(full) if not is_d else 0
        tag = "[DIR]" if is_d else "[FILE]"
        print(f"  - {tag} {it} ({sz} bytes)")