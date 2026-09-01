# -*- coding: utf-8 -*-
import os

target_folder = r"C:\Users\euntaewoo\Desktop\다국어_이미지_번역_260901"

print(f"=== [SCAN] {target_folder} ===")
print("Folder Exists:", os.path.exists(target_folder))

if os.path.exists(target_folder):
    for root, dirs, files in os.walk(target_folder):
        rel = os.path.relpath(root, target_folder)
        print(f"\n📁 Directory: {rel}")
        for f in files:
            full = os.path.join(root, f)
            sz = os.path.getsize(full)
            print(f"  - 📄 {f} ({sz} bytes)")