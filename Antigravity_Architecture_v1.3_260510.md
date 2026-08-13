# Antigravity 멀티에이전트 시스템 표준 아키텍처 정의서

> **버전**: v1.3 | **작성일**: 2026-05-10 | **기준 PC**: 테스트탑 (신규 중고PC) | **기준 드라이브**: C드라이브

---

## 📌 문서 목적

이 문서는 Antigravity AI 에이전트 시스템의 **전역(Global) / 로컬(Local) 디렉토리 구조 표준**과 **하네스(Harness) 엔지니어링 설계**를 정의하고, 향후 PC 교체 또는 환경 재세팅 시 동일한 구조를 빠르게 복원하기 위한 기준 문서입니다.

---

## PART 1. 시스템 아키텍처 구조

### 핵심 개념 정의

| 구분 | 위치 | 의미 | 기준 |
|---|---|---|---|
| **전역 설정 (Global)** | `C:\Users\euntaewoo\.agent\` | 모든 프로젝트에 항상 적용되는 공통 원칙 및 범용 도구 | "이 규칙은 모든 작업에서 항상 지켜야 한다" |
| **로컬 설정 (Local)** | `프로젝트폴더\.agent\` | 특정 프로젝트 안에서만 적용되는 전용 에이전트 및 SOP | "이 에이전트/규칙은 이 프로젝트에서만 쓰인다" |
| **Antigravity 앱 데이터** | `C:\Users\euntaewoo\.gemini\antigravity\` | 앱이 자동으로 관리하는 대화 기록, 지식 저장소 | 사용자가 직접 건드리지 않음 |

---

### 완성된 C드라이브 표준 디렉토리 구조

```
C:\Users\euntaewoo\
│
├── .agent\                                    ← [전역] 모든 프로젝트 공통 적용
│     ├── instructions.md
│     ├── harness\                             ← ★ 하네스 엔지니어링 (환각 방지 시스템)
│     │     ├── HARNESS.md
│     │     ├── harness_sync.py               ← GitHub 자동 동기화 스크립트
│     │     ├── sync_log.txt
│     │     └── verification\
│     │           ├── lint_rules.md
│     │           └── test_checklist.md
│     ├── rules\
│     │     ├── global_rules.md
│     │     └── graphify.md
│     ├── workflows\
│     │     └── graphify.md
│     └── skills\
│           └── graphify\
│
├── Projects\
│     └── 웹상세페이지\
│           ├── input\
│           ├── output\
│           └── .agent\
│                 ├── rules\
│                 │     ├── agents.md
│                 │     └── Typography_Design_System.md ← ★ 황금비(1.618) 타이포그래피 표준
│                 ├── workflows\
│                 │     └── maestro.md
│                 ├── skills\
│                       ├── 01_Maestro\
│                       ├── 01_UI_StyleSeed\            ← ★ 토스(Toss) 디자인 시스템 기반 패턴
│                       ├── 02_UI_Taste_Skill\          ← ★ 프리미엄 UI 감성 및 안티 패턴 지침
│                       ├── 02_WebPlanning_Design\
│                       ├── 03_Localization\
│                       ├── 03_UI_shadcn_Specialist\    ← ★ shadcn/ui 표준 구현 가이드
│                       ├── 04_UI_Frontend_Design\      ← ★ 고성능 React/Next.js 아키텍처
│                       ├── 04_Marketing_CX\
│                       ├── 05_DevOps_Security\
│                       ├── 05_UI_UX_Principles\        ← ★ IA 설계 및 UX 오딧 원칙
│                       └── 06_Researcher\
│
└── .gemini\antigravity\                       ← [앱 자동관리] 건드리지 않음
```

---

## PART 2. 하네스 엔지니어링 (Harness Engineering)

> 하네스(Harness)는 AI 에이전트의 **환각(Hallucination)을 방지**하고 **행동 범위를 제어**하기 위한 시스템 레벨의 가드레일(Guardrail)이다.

**저장 위치**: `C:\Users\euntaewoo\.agent\harness\`

### 구성 1: 가드레일 (Guardrails)

**절대 금지 행위 (HARD STOP)**
- 사용자 명시적 승인 없이 파일 삭제 금지
- 소스 코드에 API 키 하드코딩 금지
- 존재하지 않는 경로·파일명 추측하여 사용 금지
- 테스트 없이 프로덕션 코드 직접 수정 금지
- 한 번에 10개 이상 파일 동시 수정 금지

**환각 방지 규칙**
- `[ZERO-GUESSING]` 모르면 즉시 사용자에게 질문
- `[GRAPHIFY-FIRST]` 구조 파악은 `graphify-out/GRAPH_REPORT.md` 먼저
- `[VERIFY-BEFORE-REPORT]` 완료 보고 전 실제 결과로 검증

### 구성 2: 도구 연결 (Tool Connections)

| 도구 | 역할 | 환각 방지 효과 |
|---|---|---|
| **filesystem** | 파일 읽기·쓰기·탐색 | 경로 추측 → 실제 확인으로 교정 |
| **puppeteer** | 브라우저 자동화 | UI 추측 → 실제 화면으로 교정 |
| **github** | 리포지토리 연동 | 코드 추측 → 실제 저장소로 교정 |
| **graphify** | 지식 그래프 쿼리 | 구조 추측 → 분석 데이터로 교정 |

### 구성 3: 에이전트 레지스트리 (UI/UX 최적화)

| 에이전트 | 역할 | 관련 스킬 경로 |
|---|---|---|
| **MAESTRO** | 전체 조율·관리 | `01_Maestro/` |
| **CREW** | 코드 직접 작성·수정 | `01_Maestro/`, `04_UI_Frontend_Design/` |
| **DESIGNER** | 디자인 시스템/패턴 설계 | `01_UI_StyleSeed/`, `02_UI_Taste_Skill/` |
| **FRONTEND** | shadcn 및 고성능 UI 구현 | `03_UI_shadcn_Specialist/`, `04_UI_Frontend_Design/` |
| **UX_PLANNER** | 인터랙션 및 UX 오딧 | `05_UI_UX_Principles/` |
| **EVALUATOR** | 품질 검수 (감성/기능/성능) | `01_Maestro/SOP_Dev_Quality_Gate.md`, `02_UI_Taste_Skill/` |
| **NANOBANANA** | 이미지 OCR·번역·합성 | `03_Localization/` |
| **V-DALE** | 이미지 결함 감지·보정 QA | `02_WebPlanning_Design/v-dale-engine/` |
| **BROWSER** | 외부 웹 정보 수집 | `06_Researcher/` |
| **CS** | 고객 자동 대응 | `04_Marketing_CX/cs-automation-logic/` |

---

## PART 3. 로컬 프로젝트 전용 규칙

### 황금비 타이포그래피 디자인 시스템 (웹상세페이지 전용)

#### 캔버스 설정
| 항목 | 값 |
|---|---|
| **너비** | `860px` 고정 |
| **높이** | `Auto` |
| **배치** | Auto Layout 강제 적용 |
| **기본 폰트** | Pretendard / 일본어: Noto Sans JP |

---

## 변경 이력

| 날짜 | 버전 | 내용 |
|---|---|---|
| 2026-05-08 | v1.0 | 최초 작성 |
| 2026-05-08 | v1.1 | 하네스 엔지니어링 추가 |
| 2026-05-08 | v1.2 | 황금비 타이포그래피 디자인 시스템 추가 |
| 2026-05-10 | v1.3 | UI/UX 핵심 스킬 라이브러리 및 에이전트 역할 업데이트 |
