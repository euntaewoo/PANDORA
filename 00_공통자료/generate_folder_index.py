# -*- coding: utf-8 -*-
import os
import datetime

PROJECT_ROOT = r"C:\Users\euntaewoo\Desktop\이미지_다국어_번역_agy_sdk_uv_version"
output_file = os.path.join(PROJECT_ROOT, "폴더구조_인덱스.txt")
gen_script_target = os.path.join(PROJECT_ROOT, "00_공통자료", "generate_folder_index.py")

# 무시할 디렉토리/파일 패턴
IGNORE_DIRS = {'.git', '.venv', '__pycache__', '.pytest_cache', 'cache'}

lines = []
now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
lines.append("==========================================================================================")
lines.append("📁 이미지_다국어_번역_agy_sdk_uv_version 전체 디렉토리 및 파일 인덱스")
lines.append(f"📍 루트 경로: {PROJECT_ROOT}")
lines.append(f"🕒 최종 갱신 일시: {now_str}")
lines.append("==========================================================================================\n")

total_dirs = 0
total_files = 0

def format_size(size_bytes):
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    else:
        return f"{size_bytes / (1024 * 1024):.2f} MB"

def build_tree(dir_path, prefix=""):
    global total_dirs, total_files
    try:
        entries = os.listdir(dir_path)
    except PermissionError:
        return
    
    dirs = []
    files = []
    for e in entries:
        if e in IGNORE_DIRS:
            continue
        full = os.path.join(dir_path, e)
        if os.path.isdir(full):
            dirs.append(e)
        else:
            files.append(e)
            
    dirs.sort(key=lambda s: s.lower())
    files.sort(key=lambda s: s.lower())
    
    all_items = dirs + files
    count = len(all_items)
    
    for i, item in enumerate(all_items):
        is_last = (i == count - 1)
        connector = "└── " if is_last else "├── "
        full_path = os.path.join(dir_path, item)
        
        if os.path.isdir(full_path):
            total_dirs += 1
            lines.append(f"{prefix}{connector}📁 {item}/")
            new_prefix = prefix + ("    " if is_last else "│   ")
            build_tree(full_path, new_prefix)
        else:
            total_files += 1
            try:
                sz = os.path.getsize(full_path)
                sz_str = f" ({format_size(sz)})"
            except Exception:
                sz_str = ""
            lines.append(f"{prefix}{connector}📄 {item}{sz_str}")

build_tree(PROJECT_ROOT)

lines.append("\n==========================================================================================")
lines.append(f"📊 [통계 요약] 총 디렉토리 수: {total_dirs:,} 개 | 총 파일 수: {total_files:,} 개")
lines.append("==========================================================================================")

with open(output_file, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print(f"✅ [인덱스 생성 완료] 경로: {output_file}")
print(f"📊 총 디렉토리: {total_dirs:,} 개, 총 파일: {total_files:,} 개")
