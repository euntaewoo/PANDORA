# -*- coding: utf-8 -*-
import os, ctypes

MOVEFILE_DELAY_UNTIL_REBOOT = 0x00000004
MoveFileExW = ctypes.windll.kernel32.MoveFileExW

src_folder = r"C:\Users\euntaewoo\Desktop\다국어_이미지_번역_260901"

for root, dirs, files in os.walk(src_folder, topdown=False):
    for f in files:
        fp = os.path.join(root, f)
        MoveFileExW(fp, None, MOVEFILE_DELAY_UNTIL_REBOOT)
    for d in dirs:
        dp = os.path.join(root, d)
        MoveFileExW(dp, None, MOVEFILE_DELAY_UNTIL_REBOOT)

MoveFileExW(src_folder, None, MOVEFILE_DELAY_UNTIL_REBOOT)
print("Registered MOVEFILE_DELAY_UNTIL_REBOOT for any remaining locked handles.")