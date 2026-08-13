@echo off
chcp 65001
echo ===========================================================
echo [EN] Global Text-In_Image Translation Engine 가동 (영어 모드)
echo ===========================================================
echo.
echo 루트 디렉토리의 통합 코어 엔진을 호출합니다...
echo.

set SOURCE_DIR=%~dp0input
set TARGET_DIR=%~dp0output

if not exist "%TARGET_DIR%" mkdir "%TARGET_DIR%"

python "%~dp0..\Global_Text-In_Image_Translation_Engine.py" "%SOURCE_DIR%" "%TARGET_DIR%" --lang EN

echo.
echo ===========================================================
echo 작업이 완료되었습니다.
pause
