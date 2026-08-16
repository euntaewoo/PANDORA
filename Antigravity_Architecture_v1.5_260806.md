# Antigravity 멀티에이전트 시스템 표준 아키텍처 정의서

> **버전**: v1.5 (v1.4 100% 완전 보존 및 2026-08-06 개정 통합판) | **작성일**: 2026-08-06 | **기준 PC**: 메인컴퓨터 (Windows 11) | **기준 드라이브**: C드라이브

---

## 📌 문서 목적

이 문서는 Antigravity AI 에이전트 시스템의 **전역(Global) / 로컬(Local) 디렉토리 구조 표준**과 **하네스(Harness) 엔지니어링 설계**를 정의하고, 향후 PC 교체 또는 환경 재세팅 시 동일한 구조를 빠르게 복원하기 위한 기준 문서입니다.

---

## PART 1. 시스템 아키텍처 구조

### 핵심 개념 정의

| 구분 | 위치 | 의미 | 기준 |
| --- | --- | --- | --- |
| **전역 설정 (Global)** | `C:\Users\euntaewoo\.agent\` | 모든 프로젝트에 항상 적용되는 공통 원칙 및 범용 도구 | "이 규칙은 모든 작업에서 항상 지켜야 한다" |
| **로컬 설정 (Local)** | `프로젝트폴더\.agent\` | 특정 프로젝트 안에서만 적용되는 전용 에이전트 및 SOP | "이 에이전트/규칙은 이 프로젝트에서만 쓰인다" |
| **Antigravity 시스템 규칙** | `C:\Users\euntaewoo\.gemini\antigravity\` | GEMINI.md: 시스템 전역 규칙 및 프로토콜 최종 저장소 | **[중요]** 에이전트 하드닝 시 직접 수정 |

---

### 완성된 C드라이브 표준 디렉토리 구조

```text
C:\Users\euntaewoo\
│
├── AppData\Local\                                   ← [유형 1: 독립 구동 바이너리 에이전트 (.exe Engine)]
│     ├── hermes\                                    ← Hermes Agent v0.20.0 (.env, OpenRouter 무료 연동)
│     ├── Antigravity\                               ← Antigravity 2.0 메인 엔진
│     └── agy\bin\agy.exe                            ← Antigravity CLI 바이너리
│
├── .agent\                                          ← [전역 독립 에이전트 & 규칙 보관소]
│     ├── instructions.md
│     ├── harness\                                   ← ★ 하네스 엔지니어링 (환각 방지 시스템)
│     │     ├── HARNESS.md
│     │     ├── harness_sync.py                     ← GitHub 다운로드(Pull) 스크립트
│     │     ├── harness_push.bat                    ← GitHub 업로드(Push) 자동화 스크립트
│     │     ├── sync_log.txt
│     │     └── verification\
│     │           ├── lint_rules.md
│     │           └── test_checklist.md
│     ├── rules\
│     │     ├── global_rules.md
│     │     └── graphify.md
│     ├── workflows\
│     │     ├── graphify.md
│     │     └── rule_update_protocol.md             ← 규칙 자동 전파 SOP 워크플로우
│     └── skills\                                    ← ★ [유형 2: 안티그래비티 의존 독립 에이전트 보관소]
│           ├── graphify\                            ← 지식 그래프 분석 독립 에이전트
│           └── pdp-generator\                       ← ★ 웹 상품 상세페이지 제작 전문 독립 에이전트
│
├── Projects\                                        ← [로컬 실무 작업 공장 (Local Workspace)]
│     ├── 웹상세페이지\                               ← ★ pdp-generator 전용 11인 실무 에이전트 공장
│     │     ├── input\                               ← 원본 파싱 에셋 투입
│     │     ├── output\                              ← 최종 가로 860px 압축 이미지 출력
│     │     └── .agent\
│     │           ├── rules\
│     │           │     ├── agents.md
│     │           │     └── Typography_Design_System.md ← ★ 황금비(1.618) 타이포그래피 표준
│     │           ├── workflows\
│     │           │     └── maestro.md
│     │           └── skills\                        ← ★ 11인 서브에이전트 실무 스킬 보관소
│     │                 ├── 01_Maestro\              ← 🕵️ MAESTRO (총괄 지휘)
│     │                 ├── 01_UI_StyleSeed\          ← 🌱 DESIGNER (패턴 토큰)
│     │                 ├── 02_UI_Taste_Skill\        ← 👁️ EVALUATOR (감성 검수)
│     │                 ├── 02_WebPlanning_Design\    ← 🎨 DESIGNER (웹 디자인)
│     │                 ├── 03_Localization\          ← 🌐 NANOBANANA (이미지 번역)
│     │                 ├── 03_UI_shadcn_Specialist\  ← 🧩 FRONTEND (shadcn UI)
│     │                 ├── 04_UI_Frontend_Design\    ← 💻 FRONTEND/CREW (HTML/CSS 코딩)
│     │                 ├── 04_Marketing_CX\          ← 📈 MARKETER/CS (마케팅 & Q&A)
│     │                 ├── 05_DevOps_Security\       ← 🛡️ DevOps 보안
│     │                 ├── 05_UI_UX_Principles\      ← 🔀 UX_PLANNER (UX 흐름)
│     │                 └── 06_Researcher\            ← 🔍 BROWSER (레퍼런스 크롤링)
│     └── 홍보영상제작\
│           ├── input\
│           ├── output\
│           └── .agent\
│                 └── skills\
│                       └── 04_Marketing_CX\          ← ★ 홍보 영상 기획 및 퍼포먼스 마케팅 스킬
│
└── .gemini\                                         ← [유형 3: 전역 업무 지침 서재]
      ├── config\skills\                             ← 전역 44개 레시피 스킬 지침
      └── config\rules\                              ← 본 아키텍처 정의서 (Antigravity_Architecture_v1.5)
```

---

## PART 2. 하네스 엔지니어링 (Harness Engineering)

> 하네스(Harness)는 AI 에이전트의 **환각(Hallucination)을 방지**하고 **행동 범위를 제어**하기 위한 시스템 레벨의 가드레일(Guardrail)이다.

**저장 위치**: `C:\Users\euntaewoo\.agent\harness\`

### 구성 1: 가드레일 (Guardrails)

#### 절대 금지 행위 (HARD STOP)

- 사용자 명시적 승인 없이 파일 삭제 금지
- 소스 코드에 API 키 하드코딩 금지
- 존재하지 않는 경로·파일명 추측하여 사용 금지
- 테스트 없이 프로덕션 코드 직접 수정 금지
- 한 번에 10개 이상 파일 동시 수정 금지

#### 환각 방지 규칙

- `[ZERO-GUESSING]` 모르면 즉시 사용자에게 질문
- `[GRAPHIFY-FIRST]` 구조 파악은 `graphify-out/GRAPH_REPORT.md` 먼저
- `[VERIFY-BEFORE-REPORT]` 완료 보고 전 실제 결과로 검증
- `[SANDBOX-BYPASS]` 샌드박스 규제 제약 시 무한 다운로드 재시도 금지 및 사용자 터미널 명령어 직접 제공

#### 증거 기반 답변 강제 (MANDATORY-PROTOCOL) - [v1.4 추가]

- **선-조회 후-답변**: 도구(Tool) 실행 전 분석 결과 발언 금지
- **증거 기반 레이아웃**: `[EVIDENCE]`, `[RULE-CHECK]`, `[RESPONSE]` 형식 강제
- **치명적 오류(Fatal Error)**: 프로토콜 위반 시 에이전트 답변 무효화 및 중단

### 구성 2: 도구 연결 (Tool Connections)

| 도구 | 역할 | 환각 방지 효과 |
| --- | --- | --- |
| **filesystem** | 파일 읽기·쓰기·탐색 | 경로 추측 → 실제 확인으로 교정 |
| **puppeteer** | 브라우저 자동화 | UI 추측 → 실제 화면으로 교정 |
| **github** | 리포지토리 연동 | 코드 추측 → 실제 저장소로 교정 |
| **graphify** | 지식 그래프 쿼리 | 구조 추측 → 분석 데이터로 교정 |

### 구성 3: 에이전트 레지스트리 (UI/UX 최적화)

| 에이전트 | 역할 | 관련 스킬 경로 | pdp-generator 내 담당 단계 |
| --- | --- | --- | --- |
| **MAESTRO** | 전체 조율·관리 | `01_Maestro/` | **[1단계]** 오케스트레이션 및 산출물 감지 |
| **CREW** | 코드 직접 작성·수정 | `01_Maestro/`, `04_UI_Frontend_Design/` | **[4단계]** 불합격 시 자가 치유 수정 |
| **DESIGNER** | 디자인 시스템/패턴 설계 | `01_UI_StyleSeed/`, `02_UI_Taste_Skill/` | **[2단계]** 토스 감성 design_tokens 설계 |
| **MARKETER** | 영상 기획/대본 및 마케팅 전략 | `04_Marketing_CX/` | **[2단계]** USP 소구점 및 카피 구조화 |
| **FRONTEND** | shadcn 및 고성능 UI 구현 | `03_UI_shadcn_Specialist/`, `04_UI_Frontend_Design/` | **[3단계]** 860px HTML/CSS 코딩 & 렌더링 |
| **UX_PLANNER** | 인터랙션 및 UX 오딧 | `05_UI_UX_Principles/` | **[4단계]** CVR 구매전환 스크롤 동선 점검 |
| **EVALUATOR** | 품질 검수 (감성/기능/성능) | `01_Maestro/SOP_Dev_Quality_Gate.md`, `02_UI_Taste_Skill/` | **[4단계]** 품질 채점 및 PASS 승인 피드백 |
| **NANOBANANA** | 이미지 OCR·번역·합성 | `03_Localization/` | **[3단계]** 해외 텍스트 번역 및 이미지 합성 |
| **V-DALE** | 이미지 결함 감지·보정 QA | `02_WebPlanning_Design/v-dale-engine/` | **[4단계]** 누끼/해상도 시각적 결함 QA |
| **BROWSER** | 외부 웹 정보 수집 | `06_Researcher/` | **[1단계]** 경쟁사 레퍼런스 수집 |
| **CS** | 고객 자동 대응 | `04_Marketing_CX/cs-automation-logic/` | **[5단계]** 자주 묻는 질문 Q&A 자동 결합 |

### 구성 4: 피드백 루프

```text
에이전트 작업 → EVALUATOR 검수 → PASS → 최종 결과 보고
                      ↓ FAIL
              피드백 → CREW 자동 수정 → 재검수 (100% PASS까지 반복)
```

### 구성 5: 설정 로드 우선순위

```text
1순위: .agent\rules\global_rules.md
2순위: .agent\harness\HARNESS.md
3순위: [프로젝트]\.agent\rules\skill_sync_policy.md (신규 추가)
4순위: [프로젝트]\.agent\rules\agents.md
5순위: [프로젝트]\.agent\rules\Typography_Design_System.md
6순위: [프로젝트]\.agent\workflows\maestro.md
7순위: graphify-out\GRAPH_REPORT.md
```

### GitHub 자동 동기화

| 항목 | 내용 |
| --- | --- |
| **스크립트** | `C:\Users\euntaewoo\.agent\harness\harness_sync.py` |
| **작업명** | `Antigravity-HarnessSync` |
| **실행 시점** | PC 시작 시 + 매일 오전 9시 |
| **로그** | `sync_log.txt` |

---

## PART 3. 로컬 프로젝트 전용 규칙

### 황금비 타이포그래피 디자인 시스템 (웹상세페이지 전용)

#### 캔버스 설정

| 항목 | 값 |
| --- | --- |
| **너비** | `860px` 고정 |
| **높이** | `Auto` |
| **배치** | Auto Layout 강제 적용 |
| **기본 폰트** | 영문: Montserrat 100% (메인 이미지 단일 강제) / 일본어: Noto Sans JP / 중국어: Noto Sans SC (단, 영문 고시정보 표는 Pretendard 분리 적용) |

#### 황금비(1.618) 폰트 스케일

| 계층 | 권장 크기 | 줄간격 |
| --- | --- | --- |
| **메인 타이틀 (H1)** | `40px ~ 48px` | `1.2 ~ 1.4배` |
| **서브 타이틀 (H2)** | `24px ~ 30px` | `1.2 ~ 1.4배` |
| **본문 (Body)** | `16px ~ 18px` | `1.6 ~ 1.8배` |

#### 단락 간격

| 상황 | 기준 |
| --- | --- |
| **섹션 간** | H1 크기의 2배 이상 |
| **타이틀~본문** | 해당 폰트 크기의 1배 |
| **본문 단락 간** | 해당 폰트 크기의 0.5~0.8배 |

#### 상품 정보 고시 표(Notice Table) 표준 규격 [2026-08 신설]

| 항목 | 기준 규격 | 세부 로직 |
| --- | --- | --- |
| **캔버스 규격** | 가로 **`860px` 고정**, 세로 **`Auto-Fit`** | 최대 허용 세로 높이 **`2,580px` 이하** 엄격 준수 |
| **2페이지 분할 룰** | **`2,580px` 초과 시 자동 분할** | 본문이 길 경우 강제로 줄이지 않고 **Part 1, Part 2로 2페이지 분할 렌더링** |
| **언어별 표준 폰트** | 영문: **`Pretendard`** (메인 이미지는 100% **`Montserrat`** 단일 강제) / 일본어: **`Noto Sans JP`** / 중국어: **`Noto Sans SC`** | 100% 벡터 폰트 스크린샷 파이프라인 적용 |
| **타이포그래피 크기** | **타이틀 `64px` (Bold) / 항목명 `32px` / 본문 `32px`** | 가독성 극대화 및 황금비 밸런스 유지 |
| **렌더링 모듈** | `00_공통자료/render_notice_table_standard.py` | Headless Edge 초고해상도 렌더러 파이프라인 |

#### 중국어 번역 타겟 권역 사전 확인 의무 규칙 (`[RULE 8]`)
- 사용자가 중국어 번역을 요청할 때, 명시적인 권역(간체 vs 번체) 지정이 없는 경우 에이전트는 절대 임의로 추측(`[ZERO-GUESSING]`)하지 않고 반드시 아래 표준 질문을 먼저 제시하여 확인 후 작업에 착수합니다:
  > **"중국 본토(간체자)와 대만/홍콩(번체자) 중 어느 시장을 타겟으로 제작할까요?"**

> [!NOTE]
> **독립 서비스 참조**: 일본어 이미지 번역 전용 엔진 및 관련 폰트/타이포그래피 설정은 독립 시스템인 `C:\Users\euntaewoo\Desktop\이미지번역워크스페이스\JP_Ecom_Visual_Localizer_V7_이미지번역메인시스템엔진\` 폴더에서 전적으로 관리·구동됩니다.


---

## PART 4. 공통 설정 정보

### 전역 운영 핵심 원칙 6가지

| 원칙 | 내용 |
| --- | --- |
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
| --- | --- |
| `D:\...\AppData\Roaming\antigravity\config\` | 원본 SOP 전체 |
| `D:\...\Desktop\JP_Ecom_Visual_Localizer_V3\` | 실전 프로젝트 원본 |
| `D:\...\Documents\Antigravity_Projects\` | 타이포그래피 등 기획 문서 |

---

## PART 5. 2026-08-06 신규 개정 시스템 (3대 에이전트 분류 및 pdp-generator 11인 구조 매핑)

### 🏗️ 1. 에이전트 & 스킬 3대 분류 체계 (개념 및 저장 위치 정의)

```text
========================================================================================================
 구분                             핵심 정의 및 파일 형태                                물리적 저장 디렉터리 경로
========================================================================================================
[유형 1]                         • 자체 파이썬 런타임과 C/C++ 실행 파일(.exe)을 구비하여   C:\Users\euntaewoo\AppData\Local\<에이전트명>\
독립 구동 바이너리 에이전트            컴퓨터 윈도우 OS 위에서 단독 프로세스로 구동되는         (예: AppData\Local\hermes\)
(Standalone Executable Agent)    대형 AI 소프트웨어 엔진
--------------------------------------------------------------------------------------------------------
[유형 2]                         • 안티그래비티 2.0 엔진 위에서 백그라운드 멀티스레드로   C:\Users\euntaewoo\.agent\skills\<에이전트명>\
안티그래비티 의존 독립 에이전트        독립 대화 맥락(Context)을 생성하고 5단계 자동화       (예: .agent\skills\pdp-generator\)
(Antigravity-dependent Agent)    파이프라인을 자율 구동하는 전문 에이전트
--------------------------------------------------------------------------------------------------------
[유형 3]                         • 에이전트가 추론하고 행동할 때 읽고 따르는             C:\Users\euntaewoo\.gemini\config\skills\
업무 지침 스킬                    업무 매뉴얼 / 가이드라인 문서 (.md)                   (전역 44개 스킬 모음)
(Skill Instructions)
========================================================================================================
```

---

### 📂 2. pdp-generator 독립 에이전트와 11인 서브에이전트 간 통합 구조 설계

#### 🎨 pdp-generator (웹 상품 상세페이지 제작 전문 독립 에이전트)
- **저장 디렉터리**: `C:\Users\euntaewoo\.agent\skills\pdp-generator\SKILL.md`
- **통합 설계 팩트**: `pdp-generator`는 11인의 UI/UX 서브에이전트 레지스트리(MAESTRO, CREW, DESIGNER, MARKETER, FRONTEND, UX_PLANNER, EVALUATOR, NANOBANANA, V-DALE, BROWSER, CS)를 하위 실무 오퍼레이션 조직으로 상시 구동하는 **하이브리드 독립 파이프라인 엔진**으로 최종 정의·설계되었습니다.

#### 🤖 Hermes Agent v0.20.0 (헤르메스 에이전트)
- **저장 디렉터리**: `C:\Users\euntaewoo\AppData\Local\hermes\`
- **실행 바이너리**: `C:\Users\euntaewoo\AppData\Local\hermes\hermes-agent\venv\Scripts\hermes.exe`
- **주요 역할**: 무인 스케줄러(Cron) 구동, 세션 초월 장기 기억(`USER.md`), OpenRouter 무료 라우터 기반 단독 구동.

---

### 🌳 3. 최종 정리된 아키텍처 체계 (pdp-generator 11인 오퍼레이션 조직도)

```text
[독립 에이전트 엔진]
    └── pdp-generator (웹 상품 상세페이지 제작 전문 독립 에이전트)
           │
           ├── 🕵️ MAESTRO       (총괄 지휘 / 오케스트레이션 및 산출물 감지)
           ├── 🔍 BROWSER       (경쟁사 상세페이지 조사 및 레퍼런스 크롤링)
           ├── 📈 MARKETER      (상품 USP 소구점 기획 & 카피라이팅 구조 작성)
           ├── 🎨 DESIGNER      (황금비 1.618 폰트 & design_tokens 레이아웃)
           ├── 💻 FRONTEND      (가로 860px 반응형 HTML/CSS 코딩 & 렌더링)
           ├── 🛠️ CREW          (EVALUATOR 불합격 시 자가 치유 코드 수정)
           ├── 🌐 NANOBANANA    (해외 상품 원물 OCR & 이미지 번역 합성)
           ├── 🖼️ V-DALE        (이미지 누끼 타점 & 해상도 시각 결함 QA)
           ├── 👁️ EVALUATOR     (품질 검수 & 100% PASS 피드백 루프 주도)
           ├── 🔀 UX_PLANNER    (고객 구매 전환 CVR 최적화 동선 점검)
           └── 💬 CS            (상세페이지 하단 Q&A 대화형 로직 배포)
```

---

## 변경 이력

| 날짜 | 버전 | 내용 |
| --- | --- | --- |
| 2026-05-08 | v1.0 | 최초 작성 |
| 2026-05-08 | v1.1 | 하네스 엔지니어링 추가 |
| 2026-05-08 | v1.2 | 황금비 타이포그래피 디자인 시스템 추가 / MD 형식 변환 |
| 2026-05-10 | v1.3 | UI/UX 핵심 스킬 라이브러리(5종) 및 에이전트 역할 업데이트 |
| 2026-05-11 | v1.4 | [MANDATORY-PROTOCOL] 도입 및 시스템 규칙(GEMINI.md) 하드닝 반영 |
| **2026-08-06** | **v1.5** | **pdp-generator 전역 의존 독립 에이전트 경로(C:\Users\euntaewoo\.agent\skills\pdp-generator\) C드라이브 표준 아스키 트리, PART 5 통합 및 2026-08 고시정보 표 표준 규격 반영 판** |
