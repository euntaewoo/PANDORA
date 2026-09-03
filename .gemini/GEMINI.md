# 절대 금지 행위 (HARD STOP)

- 사용자 명시적 승인 없이 파일 삭제 금지
- 소스 코드에 API 키 하드코딩 금지
- 존재하지 않는 경로·파일명 추측하여 사용 금지
- 테스트 없이 프로덕션 코드 직접 수정 금지
- 한 번에 10개 이상 파일 동시 수정 금지

## 전역 운영 핵심 원칙 6가지

| 원칙 | 내용 |
| --- | --- |
| `[ZERO-GUESSING]` | 추측 금지. 모르면 즉시 질문하고 실제 파일 근거로만 판단 |
| `[GRAPHIFY-FIRST]` | 아키텍처/구조 질문 전 `graphify-out/GRAPH_REPORT.md` 먼저 참조 |
| `[SINGLE-SOURCE]` | 파일 복제 금지. 메인 파일 직접 수정 |
| `[API-SECURITY]` | API 키는 `api_keys.json` 또는 `.env` 에서만 로드 |
| `[LANGUAGE]` | 사용자와의 모든 커뮤니케이션은 한국어로 |
| `[OS]` | Windows 기준. 백슬래시 경로 사용 |

## 작업 완료 전 필수 검증

- `[VERIFY-BEFORE-REPORT]` 완료 보고 전 실제 결과(파일 존재, 실행 결과 등)로 최종 검증
- `[SANDBOX-BYPASS]` 대용량 다운로드 등 환경 제약으로 지연 발생 시 자동 재시도를 중단하고 사용자에게 터미널 명령어를 직접 제공하여 승인/실행 유도
- `[RULE-QA-LOOP]` 어떠한 파일 수정, 영상/이미지 렌더링 후에도 "명령어 성공" 로그만 믿고 답변하는 행위를 절대 금지한다. 반드시 변경/생성된 파일을 뷰어 도구(`view_file`, `inspect` 등)를 통해 1회 이상 디코딩하여 시각적 비율, 찌그러짐, 레이아웃을 정밀 자가 검사하고, 결함 발견 시 [수정 ➔ 재렌더링 ➔ 재검사]의 자가 개선 루프를 오류가 없을 때까지 자동으로 수행한다.

## 새 PC 세팅 체크리스트 (에이전트 자가 점검용)

- [ ] 1. `.agent\` 폴더 존재 확인
- [ ] 2. `global_rules.md` 존재 확인
- [ ] 3. `harness\HARNESS.md` 존재 확인
- [ ] 4. MCP 서버 4개 등록 확인
- [ ] 5. graphify 설치 확인
- [ ] 6. Python312 경로 확인
- [ ] 7. 에이전트 스킬 6개 존재 확인
- [ ] 8. `graphify update .` 실행

---

## `[MANDATORY-EXECUTION-PROTOCOL]` (CRITICAL)

이 섹션은 에이전트의 모든 연산보다 우선하며, 이를 어길 시 에이전트의 모든 답변은 무효로 간주한다.

1. **선-조회 후-답변**: 어떠한 상황에서도 도구(Tool)를 1회 이상 실행하여 결과값을 얻기 전에는 '분석 결과'나 '상태'에 대해 한 단어도 내뱉지 마라.
2. **증거 기반 레이아웃**: 모든 답변은 반드시 아래 형식을 지켜야 하며, 형식이 틀릴 경우 즉시 답변을 중단하라.

   - ### `[EVIDENCE]`

     (실행한 도구명과 거기서 얻은 실제 데이터 팩트)

   - ### `[RULE-CHECK]`

     (적용된 글로벌 규칙 번호 및 준수 여부)

   - ### `[RESPONSE]`

     (확인된 팩트 기반의 간결한 최종 답변)

3. **추측성 단어 완전 금지**: '아마도', '인 것 같다', '예상된다', '생각된다' 등 확신이 없는 단어가 포함된 문장은 생성 즉시 스스로 삭제하라. 근거가 없으면 "모름" 혹은 "데이터 없음"으로 답변하라.
## GCP Vertex AI 비동기 통신 표준 (ASYNC-SDK-STANDARD)
- 모든 Gemini API 호출은 wait client.aio.models.generate_content() 비동기 인터페이스를 사용한다.
- location="global" 및 토큰 이원화(8192/4096), 	emperature=0.6, top_p=0.9 황금 비율을 강제 준수한다.

## [PRE-EXPORT-INTEGRITY-VERIFICATION-LOCK] 결과물 내보내기 전 사전 무결성 검증 및 리포트 선-출력 강제
1. **[HARD STOP] 결과물 파일 내보내기 전 무조건 사전 검증 실행**:
   - 결과물 파일(.png, .html, .docx, .txt, .md 등)을 생성·저장·보고하기 전, 데이터 무결성과 포맷 규격을 체크하는 검증 함수(`pre_export_integrity_check`) 및 린터를 무조건 실행해야 합니다.
2. **[REPORT-FIRST] 데이터 무결성 요약 리포트 선-출력 의무화**:
   - 에이전트는 최종 결과물이나 파일 링크를 사용자에게 제시하기 전, 반드시 응답 상단에 `### 📋 [DATA-INTEGRITY-SUMMARY-REPORT]` 요약 리포트 표(포맷 무결성, 콩글리시/금지어 0건 여부, 수치 일치성, 4종 파일 생성 여부)를 먼저 출력하여 검증 결과를 입증해야 합니다. 이 리포트 출력이 누락된 답변은 즉시 무효로 간주합니다.
3. **[GLOBAL-COMPLIANCE] 영미권/글로벌 뷰티 표준 명칭 강제**:
   - 무자극/저자극: 한국 성적서 0.00 직역투 배제 -> `Hypoallergenic & Dermatologist-tested for sensitive skin` 표준 강제.
   - 피부톤 케어: 'Tone Care / Dark Spot & Tone Care' 콩글리시 배제 -> `Dark Spot & Discoloration Defense` 표준 강제.
