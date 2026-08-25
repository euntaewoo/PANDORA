# 🌐 Antigravity 전역 운영 원칙 (Global Rules)

이 규칙은 **모든 프로젝트**에서 항상 적용됩니다.

---

## 0. 최우선 운영 원칙 (CRITICAL)

- **[ZERO-GUESSING-POLICY]**: 모든 판단은 반드시 현재 워크스페이스 내 실제 파일 경로나 확인된 번호를 근거로 명시하라. 근거를 찾을 수 없는 경우 추측하지 말고 즉시 '파일 없음'을 보고하고 사용자에게 질문하라.
- **[GRAPHIFY-FIRST]**: 아키텍처·코드베이스 질문에 답하기 전, `graphify-out/GRAPH_REPORT.md`를 최우선 참조한다.
- **[SINGLE-SOURCE]**: 파일 복제 금지. 메인 파일 직접 수정 후 주석 기록.

---

## 1. 환경 설정

- **OS**: Windows (백슬래시 경로 사용)
- **Python**: `C:\Users\euntaewoo\AppData\Local\Programs\Python\Python312\python.exe`
- **프로젝트 루트**: `C:\Users\euntaewoo\Projects\`

---

## 2. API 및 보안 원칙

- API 키는 반드시 `config/api_keys.json` 또는 `.env` 파일에서만 로드.
- 소스 코드에 API 키 하드코딩 **절대 금지**.

---

## 3. AI 모델 사용 원칙

- **[LANGUAGE]**: 사용자와의 모든 커뮤니케이션은 **한국어**로.
- **[REPORT]**: 작업 완료 후 간결한 결과 보고만 제공.

---

## 4. Graphify 도구 사용 원칙

- 코드 파일 수정 후 반드시 `graphify update .` 실행.
- `grep` 대신 `graphify query "<질문>"` 사용.

---

## 5. 자동 품질 검증 원칙 (RULE-QA-LOOP)

- **[ZERO-EXCEPTION-QA]**: 어떠한 파일 수정, 신규 파일 생성, 영상/이미지 렌더링 작업 후에도 "명령어가 성공했다"는 시스템 로그만 믿고 답변하는 행위를 절대 금지한다. 반드시 변경/생성된 결과물 파일을 직접 뷰어 도구(`view_file`, `inspect` 등)를 통해 1회 이상 디코딩하여 시각적 비율, 레이아웃, 오탈자, 찌그러짐을 정밀 검사한 뒤 보고하라.
- **[SELF-CORRECTION-LOOP]**: 품질 검증 단계에서 찌그러짐, 레이아웃 왜곡, 빌드 오류 등 결함이 발견될 경우 스스로 완료 보고를 유보하고 즉각 [수정 ➔ 재렌더링 ➔ 시각 캡처 ➔ 재검사]의 자가 개선 루프를 오류가 없을 때까지 자동으로 반복 수행하라.