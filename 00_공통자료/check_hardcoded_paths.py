# -*- coding: utf-8 -*-
import os, re

base_dir = r"C:\Users\euntaewoo\Desktop\multilingual_text_in_image_translatio_agy_sdk_uv-version"
target_str = "multilingual_text_in_image_translatio_agy_sdk_uv-version"

hardcoded_files = []

for root, dirs, files in os.walk(base_dir):
    dirs[:] = [d for d in dirs if d not in ['.git', '.venv', '__pycache__', 'cache']]
    for f in files:
        if f.endswith(('.py', '.json', '.toml', '.bat', '.sh', '.md', '.txt')):
            fp = os.path.join(root, f)
            try:
                with open(fp, "r", encoding="utf-8") as file:
                    content = file.read()
                    if target_str in content:
                        rel = os.path.relpath(fp, base_dir)
                        # 몇 번째 줄에 있는지 확인
                        lines = [i+1 for i, line in enumerate(content.splitlines()) if target_str in line]
                        hardcoded_files.append((rel, lines))
            except Exception:
                pass

print(f"=== [하드코딩 폴더명 검색 결과: 총 {len(hardcoded_files)}개 파일 검출] ===")
for f, lines in hardcoded_files:
    print(f"  📄 {f} (Lines: {lines})")