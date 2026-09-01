# -*- coding: utf-8 -*-
import os, subprocess, time

src_folder = r"C:\Users\euntaewoo\Desktop\다국어_이미지_번역_260901"

# 파이썬 프로세스 중 해당 폴더의 venv를 참조하지 않는 상태에서 재시도
time.sleep(2)
try:
    for root, dirs, files in os.walk(src_folder, topdown=False):
        for f in files:
            fp = os.path.join(root, f)
            try:
                os.remove(fp)
            except Exception:
                # 이름 변경 후 삭제 시도
                try:
                    tmp = fp + ".tmp"
                    os.rename(fp, tmp)
                    os.remove(tmp)
                except Exception:
                    pass
        for d in dirs:
            dp = os.path.join(root, d)
            try:
                os.rmdir(dp)
            except Exception:
                pass
    os.rmdir(src_folder)
except Exception as e:
    pass

exists = os.path.exists(src_folder)
print(f"C Folder Exists: {exists}")