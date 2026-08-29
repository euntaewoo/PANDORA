@echo off
chcp 65001 > nul
echo ===========================================================
echo [EN] EN_Text-In_Image_Translation_Engine_V1 가동 (영어 모드)
echo ===========================================================
echo.

set SCRIPT_DIR=%~dp0
set VENV_PYTHON=%SCRIPT_DIR%..\.venv\Scripts\python.exe
set SOURCE_DIR=%SCRIPT_DIR%input
set TARGET_DIR=%SCRIPT_DIR%output

if not exist "%TARGET_DIR%" mkdir "%TARGET_DIR%"

if exist "%VENV_PYTHON%" (
    "%VENV_PYTHON%" "%SCRIPT_DIR%EN_Text-In_Image_Translation_Engine_V1.py" "%SOURCE_DIR%" "%TARGET_DIR%"
) else (
    python "%SCRIPT_DIR%EN_Text-In_Image_Translation_Engine_V1.py" "%SOURCE_DIR%" "%TARGET_DIR%"
)

echo.
echo ===========================================================
echo 영문 이미지 번역 작업이 완료되었습니다.
echo ===========================================================
pause
