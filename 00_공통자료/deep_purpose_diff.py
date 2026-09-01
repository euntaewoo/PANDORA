# -*- coding: utf-8 -*-
import os

f1_readme = r"C:\Users\euntaewoo\Desktop\multilingual_text_in_image_translatio_agy_sdk_uv-version\README.md"
f2_readme = r"C:\Users\euntaewoo\Desktop\다국어_이미지_번역\README.md"
f_arch = r"C:\Users\euntaewoo\Desktop\multilingual_text_in_image_translatio_agy_sdk_uv-version\multilingual_text_in_image_translatio_agy_sdk_core\SEO_GEO_AEO_Pipeline_Architecture.md"

print("=== [1. uv-version README 발췌] ===")
if os.path.exists(f1_readme):
    with open(f1_readme, "r", encoding="utf-8") as f:
        print(f.read()[:800])

print("\n=== [2. SEO_GEO_AEO_Pipeline_Architecture 발췌] ===")
if os.path.exists(f_arch):
    with open(f_arch, "r", encoding="utf-8") as f:
        print(f.read()[:800])