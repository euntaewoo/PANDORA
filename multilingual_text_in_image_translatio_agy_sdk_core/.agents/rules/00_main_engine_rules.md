---
description: "다국어 이미지 번역 메인 엔진 폴더(multilingual_text_in_image_translation) 전역 행동 수칙"
priority: "CRITICAL"
---

# [HARD STOP] 다국어 이미지 번역 메인 엔진 전역 행동 수칙

이 폴더(multilingual_text_in_image_translation) 내에서 '고시정보표 작성', '이미지 번역', '렌더링' 등의 작업을 사용자로부터 지시받은 모든 AI 에이전트는, **작업 착수 전 아래 3대 수칙을 무조건 선-조회 및 강제 적용**해야 합니다. 이를 어길 시 AI의 모든 결과물은 무효로 간주됩니다.

## 1. [ZERO-GUESSING] 즉흥적 코드 작성 및 바퀴의 재발명 금지
- 사용자가 고시정보표 렌더링을 지시했다고 해서 백지 상태에서 새로운 파이썬 렌더링 스크립트를 즉흥적으로 짜지 마십시오.
- **반드시 공용 모듈을 재사용하십시오.**
  - 다국어 표준 렌더러: ../00_공통자료/render_notice_table_standard.py (영문 전용 padding: 14px 12px / 가용폭 271px / word-break: keep-all 강제)
  - 한국어 원본 렌더러: render_notice_table_korean.py

## 2. [DOCS-FIRST] 메인 기획 문서 최우선 열람 및 필수 스펙 강제 적용
- 작업 착수 전, 반드시 아래 2개의 아키텍처 기획 문서를 정독하고 그 안의 스펙(해상도, 1열 고정폭 295px, padding: 14px 12px, 2580px 분할 룰 등)을 100% 준수하십시오.
- **[CRITICAL] 전성분 번역 시, 국제화장품원료집(ICID/INCI) 및 한국화장품성분사전(KCID) 표준 명칭과 해당 국가 표기법을 100% 적용하십시오. 렌더링 시에는 의미 단위 줄바꿈(`word-break: keep-all; overflow-wrap: break-word;`)을 적용하여 전문성과 가독성을 모두 확보해야 합니다.**
  1. SEO_GEO_AEO_Pipeline_Architecture.md
  2. 기술적_기초_및_계승_내역_레퍼런스.md

## 3. [GLOBAL-MAPPING] 글로벌 뷰티 표준 명칭 1:1 강제 매핑 준수
- 영어(Amazon), 일본어(약기법), 대만 번체(TFDA), 중국 간체(NMPA) 번역 시 기획 문서에 정의된 '현지 이커머스 표준 명칭'을 무조건 강제 적용(1:1 매핑)하십시오. 임의의 직역을 엄격히 금지합니다.
