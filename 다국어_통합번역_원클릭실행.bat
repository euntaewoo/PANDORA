@echo off
chcp 65001 > nul
title Multi-lingual_Text-In_Image_Translation_Engine

echo ========================================================================
echo  🌐 Multi-lingual_Text-In_Image_Translation_Engine 가동
echo ========================================================================
echo.

cd /d "%~dp0"

if exist ".venv\Scripts\python.exe" (
    ".venv\Scripts\python.exe" Multi-lingual_Text-In_Image_Translation_Engine.py
) else (
    python Multi-lingual_Text-In_Image_Translation_Engine.py
)

echo.
echo ========================================================================
echo  작업이 완료되었습니다. 아무 키나 누르면 창을 닫습니다.
echo ========================================================================
pause > nul
