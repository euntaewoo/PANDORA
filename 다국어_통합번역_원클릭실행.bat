@echo off
chcp 65001 > nul
title PANDORA 다국어 원클릭 이미지 번역 엔진

echo ========================================================================
echo  🌐 PANDORA 다국어 원클릭 이미지 번역 엔진 가동
echo ========================================================================
echo.

cd /d "%~dp0"

if exist ".venv\Scripts\python.exe" (
    ".venv\Scripts\python.exe" Universal_Translation_Engine.py
) else (
    python Universal_Translation_Engine.py
)

echo.
echo ========================================================================
echo  작업이 완료되었습니다. 아무 키나 누르면 창을 닫습니다.
echo ========================================================================
pause > nul
