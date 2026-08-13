@echo off
cd /d "%~dp0"
title JP Ecom Visual Localizer V5
echo =========================================================
echo    JP_Ecom_Visual_Localizer_V5 Engine
echo =========================================================
echo.
echo [*] Checking and installing required libraries...
python -m pip install -q requests numpy pillow opencv-python google-genai
echo.
echo [*] Starting JP_Ecom_Visual_Localizer_V5.py ...
echo.
python JP_Ecom_Visual_Localizer_V5.py %*
echo.
echo =========================================================
echo   Task Completed. Please check the output folder.
echo =========================================================
pause > nul
