# -*- coding: utf-8 -*-
import os, subprocess, time

src_folder = r"C:\Users\euntaewoo\Desktop\다국어_이미지_번역_260901"

# PowerShell을 통한 강제 삭제 재시도
subprocess.run(["cmd", "/c", f'takeown /F "{src_folder}" /R /D Y && icacls "{src_folder}" /grant Everyone:F /T && rmdir /s /q "{src_folder}"'], capture_output=True, text=True)

time.sleep(1)
exists = os.path.exists(src_folder)
print(f"C Folder Exists: {exists}")