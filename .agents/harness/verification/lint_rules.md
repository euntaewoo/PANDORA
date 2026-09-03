# 🛡️ [3단계 철벽 코드 검증 표준] (Lint & Verification Rules)

에이전트가 코드를 1줄이라도 수정하거나 생성한 후, 사용자에게 보고하기 전 **반드시 거쳐야 하는 3중 필수 방어막**.

---

### 1단계: py_compile 정적 문법 검사 (Syntax & Indentation Lock)
- 실행 명령어: python -m py_compile <파일경로>
- 검증 대상:
  - [x] 문법 오타(SyntaxError), 비동기 async/await 누락 완전 박멸
  - [x] 들여쓰기 꼬임(IndentationError) 0건 확인
  - [x] 유령 바이트(U+FEFF BOM) 찌꺼기 0건 확인

### 2단계: 정규식 및 보안 규격 린트 검사 (Security & Regex Lock)
- 실행 명령어: `uv run python 00_공통자료/lint_workspace_rules.py`
- 검증 대상:
  - [x] **전역 워크스페이스 무결성 전수 린터 100% PASS (Exit Code 0 필수)**: 5대 파이썬 엔진(루트/코어/영어/일본어/중국어), 렉시콘 JSON, MD 문서 전반의 규정 누락 0건 확인
  - [x] API 키 하드코딩 여부 스캔 (환경변수/.env 로드 강제)
  - [x] 구형 동기식 호출(client.models.generate_content) 잔여 0건 확인 (비동기 SDK 강제)
  - [x] 정규식 문법 오류( * 등 수량자 오류) 전수 스캔
  - [x] 토큰 한도 안전천장(전역 8192) 준수 확인

### 3단계: view_file 자가 시각 실측 검증 ([RULE-QA-LOOP])
- 검증 대상:
  - [x] 생성된 PNG 이미지를  iew_file 뷰어로 직접 디코딩하여 시각 검수
  - [x] 1:1 픽셀 비율(Aspect Ratio Lock) 및 자간/행간 왜곡 여부 확인
  - [x] 고시정보표(860px Pretendard, +82-2-6743-3206) 및 몬세라트 영문 서체 정합성 육안 확인

---

## 🎯 PASS 기준
- 1, 2, 3단계 100% 통과 시에만 [EVIDENCE]와 함께 작업 완료 보고를 허용한다.

## 11. [PRE-EXPORT-INTEGRITY-VERIFICATION-LOCK] 결과물 내보내기 전 사전 무결성 검증 및 리포트 강제
1. **[HARD STOP] 결과물 파일 내보내기 전 무조건 사전 검증 실행**:
   - 결과물 파일(.png, .html, .docx, .txt, .md 등)을 생성·저장·보고하기 전, 데이터 무결성과 포맷 규격을 체크하는 검증 함수(`pre_export_integrity_check`) 및 린터를 무조건 실행해야 합니다.
2. **[REPORT-FIRST] 데이터 무결성 요약 리포트 선-출력 의무화**:
   - 에이전트는 최종 결과물이나 파일 링크를 사용자에게 제시하기 전, 반드시 응답 상단에 `### 📋 [DATA-INTEGRITY-SUMMARY-REPORT]` 요약 리포트 표(포맷 무결성, 콩글리시/금지어 0건 여부, 수치 일치성, 4종 파일 생성 여부)를 먼저 출력하여 검증 결과를 입증해야 합니다. 이 리포트 출력이 누락된 답변은 즉시 무효로 간주합니다.

## [GLOBAL-COMPLIANCE-STANDARDS] 영미권/글로벌 뷰티 표준 용어 및 콩글리시 배제 규격
1. **무자극/저자극 공인 표준 표기**: 한국 인체적용시험 성적서의 '피부자극지수 0.00' 직역투를 엄격히 금지하고 반드시 `Hypoallergenic & Dermatologist-tested for sensitive skin` 또는 `Dermatologist-tested & clinically proven hypoallergenic`으로 표기합니다.
2. **피부톤 케어 표준 표기**: 'Tone Care / Dark Spot & Tone Care' 등 콩글리시 단순 단어 조합을 배제하고 `Dark Spot & Discoloration Defense` 또는 `Evening Skin Tone & Discoloration Care` 표준 명칭을 강제합니다.
