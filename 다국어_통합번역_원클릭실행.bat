@echo off
chcp 65001 > nul
title multilingual_text_in_image_translation

echo ========================================================================
echo  🌐 multilingual_text_in_image_translation 가동
echo ========================================================================
echo.

cd /d "%~dp0"

if exist ".venv\Scripts\python.exe" (
    ".venv\Scripts\python.exe" multilingual_text_in_image_translation\multilingual_text_in_image_translation.py
) else (
    python multilingual_text_in_image_translation\multilingual_text_in_image_translation.py
)

echo.
echo ========================================================================
echo  작업이 완료되었습니다. 아무 키나 누르면 창을 닫습니다.
echo ========================================================================
pause > nul
