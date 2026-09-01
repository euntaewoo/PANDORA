# -*- coding: utf-8 -*-
import os, filecmp

src_dir = r"C:\Users\euntaewoo\Desktop\multilingual_text_in_image_translatio_agy_sdk_uv-version"
dst_dir = r"C:\Users\euntaewoo\Desktop\다국어_이미지_번역"

def scan_all(base_dir):
    file_map = {}
    for root, dirs, files in os.walk(base_dir):
        dirs[:] = [d for d in dirs if d not in ['.git', '.venv', '__pycache__', 'cache', '.pytest_cache']]
        for f in files:
            full = os.path.join(root, f)
            rel = os.path.relpath(full, base_dir)
            try:
                sz = os.path.getsize(full)
            except Exception:
                sz = -1
            file_map[rel] = sz
    return file_map

src_files = scan_all(src_dir)
dst_files = scan_all(dst_dir)

missing_in_dst = []
diff_files = []

for rel, sz in src_files.items():
    if rel not in dst_files:
        missing_in_dst.append(rel)
    else:
        if sz != dst_files[rel]:
            diff_files.append((rel, sz, dst_files[rel]))

print("=== [AUDIT REPORT: 다국어_이미지_번역 미동기화 전수 감사] ===")
print(f"1. src 총 파일: {len(src_files)}개 | dst 총 파일: {len(dst_files)}개")
print(f"2. dst에 누락된 파일 수: {len(missing_in_dst)}개")
print(f"3. 내용/크기가 다른 파일 수: {len(diff_files)}개")

print("\n--- [A. 누락된 파일 목록 (상위 30개)] ---")
for f in missing_in_dst[:30]:
    print(f"  ❌ [MISSING] {f} ({src_files[f]} bytes)")

print("\n--- [B. 크기/내용이 다른 파일 목록] ---")
for f, s_sz, d_sz in diff_files:
    print(f"  ⚠️ [DIFF] {f} -> src: {s_sz} bytes vs dst: {d_sz} bytes")