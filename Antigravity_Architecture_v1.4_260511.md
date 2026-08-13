# Antigravity 멀티에이전트 시스템 표준 아키텍처 정의서

> **버전**: v1.4 | **작성일**: 2026-05-11 | **기준 PC**: 테스트탑 (신규 중고PC) | **기준 드라이브**: C드라이브

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
| **Antigravity 시스템 규칙** | `C:\Users\euntaewoo\.gemini\antigravity\` | GEMINI.md: 시스템 전역 규칙 및 프로토콜 최종 저장소 | **[중요]** 에이전트 하드닝 시 직접 수정 |

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
└── .gemini\antigravity\                       ← [시스템] GEMINI.md (전역 규칙 저장소)
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

**증거 기반 답변 강제 (MANDATORY-PROTOCOL) - [v1.4 추가]**
- **선-조회 후-답변**: 도구(Tool) 실행 전 분석 결과 발언 금지
- **증거 기반 레이아웃**: `[EVIDENCE]`, `[RULE-CHECK]`, `[RESPONSE]` 형식 강제
- **치명적 오류(Fatal Error)**: 프로토콜 위반 시 에이전트 답변 무효화 및 중단

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

### 구성 4: 피드백 루프

```
에이전트 작업 → EVALUATOR 검수 → PASS → 최종 결과 보고
                      ↓ FAIL
              피드백 → CREW 자동 수정 → 재검수 (100% PASS까지 반복)
```

### 구성 5: 설정 로드 우선순위

```
0순위: .gemini\antigravity\GEMINI.md (시스템 프롬프트 / 최상위 권위)
1순위: .agent\rules\global_rules.md
2순위: .agent\harness\HARNESS.md
3순위: [프로젝트]\.agent\rules\skill_sync_policy.md
4순위: [프로젝트]\.agent\rules\agents.md
5순위: [프로젝트]\.agent\rules\Typography_Design_System.md
6순위: [프로젝트]\.agent\workflows\maestro.md
7순위: graphify-out\GRAPH_REPORT.md
```

### GitHub 자동 동기화

| 항목 | 내용 |
|---|---|
| **스크립트** | `C:\Users\euntaewoo\.agent\harness\harness_sync.py` |
| **작업명** | `Antigravity-HarnessSync` |
| **실행 시점** | PC 시작 시 + 매일 오전 9시 |
| **로그** | `sync_log.txt` |

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

#### 황금비(1.618) 폰트 스케일

| 계층 | 권장 크기 | 줄간격 |
|---|---|---|
| **메인 타이틀 (H1)** | `40px ~ 48px` | `1.2 ~ 1.4배` |
| **서브 타이틀 (H2)** | `24px ~ 30px` | `1.2 ~ 1.4배` |
| **본문 (Body)** | `16px ~ 18px` | `1.6 ~ 1.8배` |

#### 단락 간격
| 상황 | 기준 |
|---|---|
| **섹션 간** | H1 크기의 2배 이상 |
| **타이틀~본문** | 해당 폰트 크기의 1배 |
| **본문 단락 간** | 해당 폰트 크기의 0.5~0.8배 |

#### 일본어 전용 설정 (JP Ecom)
```json
{
  "default_font": ["Noto Sans JP", "sans-serif"],
  "kerning": "-0.03em",
  "line_height": 1.6,
  "roles": {
    "title":  { "weight": 700, "size_ratio": 0.045, "color": "#000000" },
    "body":   { "weight": 400, "size_ratio": 0.025, "color": "#333333" },
    "legal":  { "weight": 400, "size_ratio": 0.012, "min_px": 24, "color": "#666666" },
    "badge":  { "weight": 700, "size_ratio": 0.020, "color": "#FFFFFF" }
  }
}
```

---

## PART 4. 공통 설정 정보

### 전역 운영 핵심 원칙 6가지

| 원칙 | 내용 |
|---|---|
| `[ZERO-GUESSING-POLICY]` | 추측 금지. 반드시 실제 파일 근거 확인 후 판단 |
| `[GRAPHIFY-FIRST]` | 아키텍처 질문 전 `GRAPH_REPORT.md` 먼저 참조 |
| `[SINGLE-SOURCE]` | 파일 복제 금지. 메인 파일 직접 수정 |
| `[API-SECURITY]` | API 키는 `api_keys.json` 또는 `.env` 에서만 로드 |
| `[LANGUAGE]` | 사용자와의 모든 커뮤니케이션은 한국어로 |
| `[OS]` | Windows 기준. 백슬래시 경로 사용 |

### 새 PC 세팅 체크리스트

- [ ] 1. `.agent\` 폴더 존재 확인
- [ ] 2. `global_rules.md` 존재 확인
- [ ] 3. `harness\HARNESS.md` 존재 확인
- [ ] 4. MCP 서버 4개 등록 확인
- [ ] 5. graphify 설치 확인
- [ ] 6. Python312 경로 확인
- [ ] 7. 에이전트 스킬 11개(기존 6개 + UI/UX 5개) 존재 확인
- [ ] 8. `graphify update .` 실행

### 이전 PC (D드라이브) 원본 보존 위치

| 경로 | 내용 |
|---|---|
| `D:\...\AppData\Roaming\antigravity\config\` | 원본 SOP 전체 |
| `D:\...\Desktop\JP_Ecom_Visual_Localizer_V3\` | 실전 프로젝트 원본 |
| `D:\...\Documents\Antigravity_Projects\` | 타이포그래피 등 기획 문서 |

---

## 변경 이력

| 날짜 | 버전 | 내용 |
|---|---|---|
| 2026-05-08 | v1.0 | 최초 작성 |
| 2026-05-08 | v1.1 | 하네스 엔지니어링 추가 |
| 2026-05-08 | v1.2 | 황금비 타이포그래피 디자인 시스템 추가 / MD 형식 변환 |
| 2026-05-10 | v1.3 | UI/UX 핵심 스킬 라이브러리(5종) 및 에이전트 역할 업데이트 |
| 2026-05-11 | v1.4 | [MANDATORY-PROTOCOL] 도입 및 시스템 규칙(GEMINI.md) 하드닝 반영 |
