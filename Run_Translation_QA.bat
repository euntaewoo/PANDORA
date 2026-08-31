@echo off
chcp 65001 > nul
echo ===============================================================================
echo  [03_번역품질평가] 초고속 무렌더링 QA 진단 및 HTML 리포터 원클릭 실행
echo ===============================================================================
cd /d "%~dp0"
if exist ".\.venv\Scripts\python.exe" (
    .\.venv\Scripts\python.exe evaluate_transcreation_quality.py
) else (
    python evaluate_transcreation_quality.py
)
pause
