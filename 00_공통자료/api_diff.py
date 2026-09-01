# -*- coding: utf-8 -*-
import os, re

f1 = r"C:\Users\euntaewoo\Desktop\multilingual_text_in_image_translatio_agy_sdk_uv-version\multilingual_text_in_image_translatio_agy_sdk.py"
f2 = r"C:\Users\euntaewoo\Desktop\다국어_이미지_번역\multilingual_text_in_image_translation.py"

with open(f1, "r", encoding="utf-8") as file1:
    code1 = file1.read()

with open(f2, "r", encoding="utf-8") as file2:
    code2 = file2.read()

print("=== [비교 1: SDK Import 및 클라이언트 초기화] ===")
for line in code1.splitlines()[:40]:
    if "import" in line or "genai.Client" in line or "location" in line:
        print("  [uv-version]:", line)

print("\n---")
for line in code2.splitlines()[:40]:
    if "import" in line or "genai.Client" in line or "location" in line:
        print("  [legacy]:    ", line)

print("\n=== [비교 2: API 호출 방식 (generate_content 검색)] ===")
m1 = re.findall(r"(?:await\s+)?client\.(?:aio\.)?models\.generate_content\([^)]+\)", code1, re.DOTALL)
m2 = re.findall(r"(?:await\s+)?client\.(?:aio\.)?models\.generate_content\([^)]+\)", code2, re.DOTALL)

print(f"uv-version 호출부 개수: {len(m1)}")
if m1:
    print("uv-version 대표 호출부:\n", m1[0][:300])

print(f"\nlegacy 호출부 개수: {len(m2)}")
if m2:
    print("legacy 대표 호출부:\n", m2[0][:300])