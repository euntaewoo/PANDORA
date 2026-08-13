# 🔒 Antigravity Harness Engineering System
# 마스터 제어 명세서 (Master Control Specification)
# 버전: v1.3 | 작성일: 2026-05-10 | 기준 PC: 테스트탑 (C드라이브)

---

## ■ 하네스란 무엇인가

하네스(Harness)는 AI 에이전트의 **환각(Hallucination)을 방지**하고
**행동 범위를 제어**하기 위한 시스템 레벨의 가드레일(Guardrail)이다.

강력한 말(AI 모델)을 기수(사용자)가 원하는 방향으로 이끄는 "고삐"와 같다.

---

## ■ 1. 가드레일 (Guardrails) - 행동 제약 규칙

에이전트가 반드시 지켜야 할 불변의 원칙. 위반 시 즉시 작업 중단.

### 1-1. 절대 금지 행위 (HARD STOP)
- 사용자 명시적 승인 없이 파일 삭제 금지
- 소스 코드에 API 키 하드코딩 금지
- 존재하지 않는 경로·파일명 추측하여 사용 금지
- 테스트 없이 프로덕션 코드 직접 수정 금지
- 한 번에 10개 이상 파일 동시 수정 금지 (범위 폭발 방지)

### 1-2. 행동 전 필수 확인 사항 (PRE-ACTION CHECK)
- 파일 수정 전: 현재 파일 내용 먼저 읽기
- API 호출 전: api_keys.json 또는 .env 파일 존재 여부 확인
- 코드 실행 전: 실행 환경(Python 경로, Node 경로) 확인
- 외부 URL 참조 전: 접근 가능 여부 확인

### 1-3. 환각 방지 규칙 (HALLUCINATION PREVENTION)
- [ZERO-GUESSING]: 모르면 추측하지 말고 즉시 사용자에게 질문
- [GRAPHIFY-FIRST]: 구조 파악은 반드시 graphify-out/GRAPH_REPORT.md 먼저
- [VERIFY-BEFORE-REPORT]: 완료 보고 전 실제 파일/실행 결과로 검증
- [RULE-QA-LOOP]: 완료 보고 전, 뷰어 도구(view_file, inspect 등)를 사용하여 생성/수정된 모든 결과물 파일의 레이아웃, 종횡비 왜곡, 빌드 오류를 눈으로 정밀 자가 검사하고, 오류 발견 시 자가 개선 루프 자동 가동

---

## ■ 2. 도구 연결 (Tool Connections)

| 도구 | 역할 | 환각 방지 효과 |
|---|---|---|
| **filesystem** | 파일 읽기·쓰기·탐색 | 경로 추측 → 실제 확인으로 교정 |
| **puppeteer** | 브라우저 자동화 | UI 추측 → 실제 화면으로 교정 |
| **github** | 리포지토리 연동 | 코드 추측 → 실제 저장소로 교정 |
| **graphify** | 지식 그래프 쿼리 | 구조 추측 → 분석 데이터로 교정 |

GitHub 참조: PANDORA 리포지토리 (euntaewoo)

---

## ■ 3. 에이전트 레지스트리 (Agent Registry)

### [전역 등록 에이전트]
| 에이전트 | 스킬 경로 | 권한 범위 |
|---|---|---|
| **Graphify** | .agent/skills/graphify/ | 읽기 전용 (분석) |

### [로컬 등록 에이전트] - 웹상세페이지 프로젝트
| 에이전트 | 역할 | 관련 스킬 경로 |
|---|---|---|
| **MAESTRO** | 전체 조율·관리 | `01_Maestro/` |
| **CREW** | 코드 직접 작성·수정 | `01_Maestro/`, `04_UI_Frontend_Design/` |
| **DESIGNER** | 디자인 시스템/패턴 설계 | `01_UI_StyleSeed/`, `02_UI_Taste_Skill/` |
| **FRONTEND** | shadcn 및 고성능 UI 구현 | `03_UI_shadcn_Specialist/`, `04_UI_Frontend_Design/` |
| **UX_PLANNER** | 인터랙션 및 UX 오딧 | `05_UI_UX_Principles/` |
| **EVALUATOR** | 품질 검수 | `01_Maestro/SOP_Dev_Quality_Gate.md`, `02_UI_Taste_Skill/` |

---

## ■ 4. 피드백 루프 (Feedback Loop)

```
에이전트 작업
    ↓
EVALUATOR 검수 → PASS → 최종 결과 보고
    ↓ FAIL
피드백 → CREW 자동 수정 → 다시 검수 (100% PASS까지 반복)
```

---

## ■ 5. 설정 로드 우선순위

```
1순위: .agent/rules/global_rules.md
2순위: .agent/harness/HARNESS.md
3순위: [프로젝트]/.agent/rules/agents.md
4순위: [프로젝트]/.agent/workflows/maestro.md
5순위: graphify-out/GRAPH_REPORT.md
```

---

## ■ 변경 이력

| 날짜 | 버전 | 내용 |
|---|---|---|
| 2026-05-08 | v1.0 | 최초 작성 |
| 2026-05-10 | v1.3 | UI/UX 핵심 스킬 및 에이전트 역할 업데이트 |
| 2026-05-27 | v1.4 | 16:9 찌그러짐 이슈 대응 자동 품질 검증 루프(RULE-QA-LOOP) 추가 및 연관 파일 전면 동기화 |

---
*로컬 경로: C:\Users\euntaewoo\.agent\harness\HARNESS.md*
*자동 동기화: harness_sync.py 실행 또는 Windows 작업 스케줄러*