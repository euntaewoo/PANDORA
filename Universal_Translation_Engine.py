"""
===================================================================================
🌐 Multi-lingual_Text-In_Image_Translation_Engine.py (Universal_Translation_Engine.py)
-----------------------------------------------------------------------------------
• Purpose: Multi-lingual_Text-In_Image_Translation_Engine
• Features:
    1. 단일 공통 인풋 폴더(01_번역대상_원본) 기준 구동
    2. 실행 시 도착 언어(EN, JP, CN, TW, ALL) 대화형 질의응답 선택
    3. 도착어별 규정/법률(영어 초월번역, 일본 약기법 56종, 중국 신광고법) 자동 적용
    4. 표(고시표/성분표) 자동 감지 시 HTML 표준 헤드리스 렌더러로 고선명 분기 처리
    5. 결과물을 02_번역결과_최종/[언어명] 폴더로 자동 분류 저장
• Models:
    - Pass 1: gemini-3.1-pro-preview (추론, 번역, 법률 필터링)
    - Pass 2: gemini-3.1-flash-image (시각적 신경망 인페인팅 렌더링)
• API Standard: Google Cloud Vertex AI (location="global")
===================================================================================
"""

import os
import sys
import subprocess

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
MAIN_ENGINE = os.path.join(SCRIPT_DIR, "Multi-lingual_Text-In_Image_Translation_Engine.py")

if __name__ == "__main__":
    cmd = [sys.executable, MAIN_ENGINE] + sys.argv[1:]
    sys.exit(subprocess.run(cmd).returncode)
