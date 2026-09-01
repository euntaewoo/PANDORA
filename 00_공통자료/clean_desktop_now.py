# -*- coding: utf-8 -*-
import os, shutil, tempfile

src = r"C:\Users\euntaewoo\Desktop\다국어_이미지_번역_260901"
temp_dir = tempfile.gettempdir()
trash_target = os.path.join(temp_dir, "trash_delete_260901")

print(f"Original Desktop Path: {src}")
print("Exists on Desktop before move:", os.path.exists(src))

if os.path.exists(src):
    try:
        # Temp 폴더로 이동 (바탕화면에서 0.001초 만에 즉시 제거)
        if os.path.exists(trash_target):
            shutil.rmtree(trash_target, ignore_errors=True)
        shutil.move(src, trash_target)
        print("✅ Successfully moved out of Desktop to Temp folder!")
    except Exception as e:
        print("Move failed:", e)

# 바탕화면 확인
exists_on_desktop = os.path.exists(src)
print(f"🚀 FINAL CHECK -> Exists on Desktop: {exists_on_desktop}")

# Temp 폴더 내 삭제 시도
if os.path.exists(trash_target):
    try:
        shutil.rmtree(trash_target, ignore_errors=True)
    except Exception:
        pass