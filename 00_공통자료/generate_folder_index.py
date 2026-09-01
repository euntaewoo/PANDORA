# -*- coding: utf-8 -*-
import os

root_dir = r"C:\Users\euntaewoo\Desktop\multilingual_text_in_image_translatio_agy_sdk_uv-version"
output_file = os.path.join(root_dir, "폴더구조_인덱스.txt")

# 무시할 디렉토리/파일 패턴 (선택사항, 하지만 전체 인덱스이므로 깔끔하게 정돈)
IGNORE_DIRS = {'.git', '.venv', '__pycache__', '.pytest_cache', 'cache'}

lines = []
lines.append("==========================================================================================")
lines.append("📁 multilingual_text_in_image_translatio_agy_sdk_uv-version 전체 디렉토리 및 파일 인덱스")
lines.append(f"📍 루트 경로: {root_dir}")
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
    
    # 디렉토리와 파일 분리 및 정렬
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
                sz_str = format_size(sz)
            except Exception:
                sz_str = "N/A"
            lines.append(f"{prefix}{connector}📄 {item} ({sz_str})")

build_tree(root_dir)

lines.append("\n" + "=" * 90)
lines.append(f"📊 [총계] 총 폴더 수: {total_dirs}개 | 총 파일 수: {total_files}개")
lines.append("=" * 90)

content = "\n".join(lines)
with open(output_file, "w", encoding="utf-8") as f:
    f.write(content)

print(f"SUCCESS: Generated {output_file}")
print(f"Total Dirs: {total_dirs}, Total Files: {total_files}")