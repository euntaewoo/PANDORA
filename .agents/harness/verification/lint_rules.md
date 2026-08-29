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
- 검증 대상:
  - [x] API 키 하드코딩 여부 스캔 (환경변수/.env 로드 강제)
  - [x] 구형 동기식 호출(client.models.generate_content) 잔여 0건 확인 (비동기 SDK 강제)
  - [x] 정규식 문법 오류(* 등 수량자 오류) 전수 스캔
  - [x] 토큰 한도 안전천장(전역 8192) 준수 확인

### 3단계: view_file 자가 시각 실측 검증 ([RULE-QA-LOOP])
- 검증 대상:
  - [x] 생성된 PNG 이미지를 iew_file 뷰어로 직접 디코딩하여 시각 검수
  - [x] 1:1 픽셀 비율(Aspect Ratio Lock) 및 자간/행간 왜곡 여부 확인
  - [x] 고시정보표(860px Pretendard, +82-2-6743-3206) 및 몬세라트 영문 서체 정합성 육안 확인

---

## 🎯 PASS 기준
- 1, 2, 3단계 100% 통과 시에만 [EVIDENCE]와 함께 작업 완료 보고를 허용한다.
