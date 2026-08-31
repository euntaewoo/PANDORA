# 이미지번역-프로젝트-전역규칙 (Global Rules)

본 문서는 모든 에이전트가 최우선으로 준수해야 하는 전역(Global) 룰북입니다.

## 0. 인터페이스 및 환경 원칙 (Interface Lock)
- **[TERMINAL-INTERFACE-LOCK]**: Antigravity IDE 2.0 환경에서는 사용자에게 터미널 명령어 요청 시 PowerShell 문법을 절대 금지하며, 무조건 **Windows 표준 CMD(명령 프롬프트) 문법으로 100% 단일화**한다.
- **[AGENT-UNATTENDED-EXECUTION]**: 파일 수정, 생성, 복구, 테스트 실행 등 모든 작업은 사용자 수동 입력을 배제하고 **에이전트가 자체 도구로 무인 자동 처리**한다.
- **[4-IN-1 ATOMIC-COMMIT-GATE] (4단계 원자적 일괄 완결 게이트 전역 강제)**:
  - 소스 코드(`*.py`)를 수정하거나 신규 기능을 추가할 때, 다음 4개 단계를 분리할 수 없는 **단일 원자적 실행 단위(Atomic Transaction)**로 100% 일괄 완결해야 하며, 1단계만 마치고 턴을 종료하는 '조기 완료 보고'를 전면 영구 금지한다:
    - **1단계 (엔진 소스코드 수정)**: 메인 파이썬 엔진(`*.py`) 코드 수정 및 자체 구동 검증.
    - **2단계 (기술 문서 명세화)**: 해당 폴더 `README.md` / `TechStack.md`에 파라미터, 입출력, 동작 원리 공식 명세화.
    - **3단계 (전역 룰북/스킬 잠금)**: 공통 표준 기능일 경우 `global_rules.md` 및 `config\skills\` 에이전트 스킬 명세 동기화.
    - **4단계 (Git 형상 관리 완결)**: 코드와 문서를 100% 일치시킨 상태로 `git add` 및 버전 커밋 완결.
  - **[HARD STOP - 조기 종료 및 누락 무효화]**: 2~4단계가 누락된 모든 보고는 시스템 무효로 간주하며, 모든 작업 완료 보고 시 `[4-STAGE-SYNC-AUDIT]` 실측 체크리스트를 의무 출력해야 한다.
- **[ISOLATED-FAST-PATH-AND-PROACTIVE-SYNC] (2단계 분리 운영 및 전역 동기화 능동적 제안 표준)**:
  - **1단계 (단일 파일 핀포인트 초고속 작업)**: 사용자가 특정 결과물 파일의 오류/수정/재작업을 요청할 때, 무관한 전역 문서(`global_rules.md`, `SKILL.md` 등) 및 전체 구동 엔진 조회를 일체 배제하고 **오직 지정된 해당 파일만 직접 수정 ➔ 렌더링 ➔ 결과물 1회 시각 검수 ➔ 즉시 저장 완료 보고**로 초고속 처리한다.
  - **2단계 (전역 동기화 능동적 제안 - Proactive Confirmation)**: 1단계 완료 보고 시, 에이전트는 무단으로 전역 엔진을 수정하지 않고 사용자에게 *"이번 작업에 적용된 [수정 사항/기능]을 전체 구동 엔진(`render_notice_table_standard.py` 등) 및 전역 규칙 문서(`global_rules.md`)에도 일괄 업데이트 동기화할까요?"*라고 능동적으로 확인 질문을 제시한다.
  - **3단계 (승인 기반 전역 동기화 실행)**: 사용자가 명시적으로 승인("응, 반영해줘")할 때에만 전역 렌더링 스크립트, 전역 규칙 문서, 스킬 명세서를 일괄 업데이트하고 Git 버전 관리를 완결한다. (사용자가 "아니오/이번만 써"라고 하면 추가 작업 없이 즉시 종료)

## 1. 오류 복구 원칙 (Full Regeneration Rule)
- 텍스트 번역이나 이미지 렌더링 과정에서 오류(글자 뭉개짐, 403/429 등 통신 에러, 레이아웃 깨짐)가 발생할 경우, **절대로 오류가 발생한 부분만 임의로 수정(Patching, 덧칠 등)하지 마십시오.**
- 오류 발생 시 무조건 **전체 작업을 새롭게 다시 시작(Full Regeneration)**하여 하나의 완벽한 캔버스를 처음부터 끝까지 새로 생성해야 합니다.

## 2. 1.5 & 2.5 구형/레거시 모델 금지 및 언급 완전 배제 (3.1 플래그십 라인업 전역 강제)
- **[HARD STOP]** 어떠한 상황에서도 `gemini-1.5-*` 및 `gemini-2.5-*` (`gemini-2.5-pro`, `gemini-2.5-flash`, `gemini-2.5-flash-image` 등) 구형/중간 레거시 모델의 사용, 언급, 제안, 및 코드로의 다운그레이드를 전면 영구 금지합니다.
- 이미지 번역 및 인페인팅, OCR, SEO 생성 파이프라인 전역에서 오직 최신의 **`gemini-3.1-pro-preview`** (PASS 1 OCR/초월번역/SEO) 및 **`gemini-3.1-flash-image`** (PASS 2 신경망 이미지 인페인팅) 플래그십 라인업만 100% 단일화하여 사용하고 설명해야 합니다.


### 2.1 4대 핵심 하이퍼파라미터 및 토큰 이원화 전역 강제 조항 (GenerationConfig & Token Limits Lock)
- **[HYPERPARAMETER-LOCK]**: Gemini API를 호출하는 모든 엔진 및 파이프라인에서 다음의 황금 비율 하이퍼파라미터를 전역 강제 적용한다:
  - `temperature`: **0.6** (해외 광고법 준수 안전선 유지 및 럭셔리 초월번역 밸런스 확보)
  - `top_p`: **0.9** (하위 10% 투박한 직역 표현 배제 및 정제된 백화점 뷰티 어휘 필터링)
- **[TOKEN-LIMIT-DUALIZATION-LOCK]**: 토큰 한도는 작업 목적에 따라 이원화하여 전역 강제한다:
  - **대용량 데이터 추출 및 고시표 번역 (Pass 1 & Table Render)**: `max_output_tokens=8192` (전성분 등 방대한 화학 명칭 및 JSON 구조 유실 방지)
  - **마케팅 카피 및 SEO 생성 (SEO/GEO/AEO)**: `max_output_tokens=8192` (불필요한 장황한 설명 차단 및 API 비용 최적화)

> 💡 **[Temperature 0.6 공학적·수학적 배경 및 실측 제원 주석]**
> - **수학적 작동 원리 (Softmax 연산식)**: $P(w_i) = \frac{\exp(z_i / T)}{\sum_j \exp(z_j / T)}$
>   - $T$ (Temperature)는 다음 단어를 샘플링할 때 확률 분포의 평탄화(Flatness) 정도를 제어하는 조절 매개변수임.
> - **실측 동작 특성 비교**:
>   - `T = 0.5`: 상위 1~2개 고확률 단어에 선택이 집중되어 결정론적/보수적 연산 수행 (문장이 딱딱한 기계 직역으로 고착됨).
>   - `T = 0.7`: 하위 확률 단어의 채택 가능성이 높아져 무작위성 및 창의성은 증가하나, 원문에 없는 과장/절대화 금지어 환각 및 광고법 위반 리스크 급증.
>   - `T = 0.6`: 해외 화장품 광고법(미국 MoCRA, 대만 TFDA, 일본 약기법, 중국 NMPA) 위반 리스크 차단과 백화점·세포라급 럭셔리 초월번역(Transcreation) 감성 품질 간의 **최적 균형점(황금 비율)**.

### 2.2 HTML 뷰어 다국어 소제목 자동 삽입 표준 (HTML-VIEWER-SECTION-HEADING-LOCK)
- **[HEADING-AUTO-INCLUSION]**: `_SEO_GEO_AEO_VIEWER.html` 및 클립보드 복사 영역 생성 시, 해외 쇼핑몰 등록 편의를 위해 다음 규격을 전역 강제한다:
  - **섹터 1 (공식 상품명)**: 카드 외관 한글 헤더 유지 + 본문 `textarea`에는 순수 상품명만 수납 (타이틀 태그 중복 방지).
  - **섹터 2 (5줄 마이크로 요약)**: 본문 `textarea` 및 HTML 코드 최상단에 **번역 도착어 공식 소제목(예: `2. Core Value & Active Ingredient Summary`)**을 필수 자동 삽입.
  - **섹터 3 (5대 핵심 FAQ)**: 본문 `textarea` 및 HTML 코드 최상단에 **번역 도착어 공식 소제목(예: `3. Product Usage Guide & Frequently Asked Questions (FAQ)`)**을 필수 자동 삽입.
  - **외관 헤더 UI**: 카드 상단 헤더 바는 관리자 직관성을 위해 한글 명칭(`📌 1. 공식 상품명`, `🔬 2. 핵심 가치...`, `💬 3. 5대 핵심 FAQ...`)을 100% 유지.

### 2.3 03_번역품질평가 전용 2-Subfolder 격리 표준 (QUALITY-EVAL-DIRECTORY-LOCK)
- **[EVAL-DIRECTORY-ISOLATION]**: 기존 번역 상세페이지(영문/일문/중문 등)의 품질 진단 및 4단 가치대조 리포트 발행은 루트 디렉토리 오염을 방지하기 위해 `03_번역품질평가` 마스터 폴더 내 2-Subfolder 규격을 전역 강제한다:
  - **인풋 경로**: `03_번역품질평가\01_평가대상_원본\[제품폴더]\` (순수 원본 이미지/문서만 수납, 100% 무오염 보존)
  - **아웃풋 경로**: `03_번역품질평가\02_진단결과\[제품폴더]\` (`Transcreation_QA_Report.html` 및 JSON 단독 저장)
  - **초고속 무렌더링 가동**: 이미지 재렌더링을 생략하고 3초 만에 4대 루브릭 100점 채점 및 4단 가치대조표 발행.

### 2.4 1단계 QA 진단 결과 번역 엔진 2중 강제 주입 표준 (QA-FEEDBACK-INJECTION-LOCK)
- **[DUAL-LAYER-QA-INJECTION]**: 1단계 QA 진단 리포트(`Transcreation_QA_Report.json`)에 기록된 `correction_feedbacks`(오타 교정표) 및 `transcreation_comparisons`(초월번역 확정 문안)은 번역 파이프라인에서 누락 없이 100% 반영되어야 하며, 다음 2중 안전망을 강제한다:
  - **1계층 (프롬프트 주입)**: Pass 1 실행 시 진단 리포트의 교정 목록을 `[MANDATORY QA OVERRIDE]` 최우선 섹션으로 시스템 프롬프트에 자동 주입한다.
  - **2계층 (결정론적 보정 게이트)**: Pass 1 번역 완료 후, Python 정규식 및 치환 규칙(`apply_deterministic_qa_overrides`)을 통해 7대 핵심 오타(`enurgy`, `deley`, `ocne`, `metabailism`, `LIGHTWEGHT`, `Cosmetis`, `Pynidoxine`) 및 MoCRA 금지어(`Prescribe`, `Bio-Immunity`)를 100% 검증·보정하여 Pass 2 렌더러로 전달한다.
  - **가이드 파일 자동 동봉**: 번역 대상 폴더 배치 시 `transcreation_guide.json`을 자동 복사·동봉하여 독립 실행 무결성을 보장한다.

### 2.5 5단계 QA 최종 재검증 시 개선 조치 이행 검증 대조표 표준 (DEFECT-RESOLUTION-DELTA-CHECKLIST)
- **[DELTA-VERIFICATION-MATRIX]**: 5단계 최종 QA 재검증 리포트(`Transcreation_QA_Report.html`) 최상단(제1섹터)에는 단순 번역 대조표와 별개로, 1단계에서 지적된 문제점들의 실제 개선 조치 이행 여부를 판정하는 **`1단계 지적사항 이행 및 결함 해결 검증 대조표(Defect Resolution & Delta Checklist)`**를 필수 렌더링해야 한다:
  - **5대 필수 대조 열(Columns)**:
    1. `① 지적 항목 및 결함 유형`: 1단계 검출 결함(스펠링 오타, MoCRA 위반 등)
    2. `② 수정 전 기존 문안 (Before)`: 결함이 존재했던 원문/기존 번역 구문
    3. `③ 1단계 권고 교정안 (Target)`: 사전 진단 시 확정된 표준 초월번역 목표치
    4. `④ 5단계 최종 렌더링 결과 (After)`: 실제 재렌더링된 이미지/문서 내 최종 영문 텍스트
    5. `⑤ 이행 판정 (Status)`: `✅ 정상 반영` (100% 교정 완료) 또는 `❌ 미반영` (미결함)
  - **종합 합격 승인 요건**: 점수 90점 이상 달성 및 1단계 지적 사항의 `이행 판정`이 **100% `✅ 정상 반영`**으로 완결되어야만 `[PASSED (초월번역 승인)]` 뱃지를 발급한다.

### 2.6 4대 마스터 폴더 체계 및 3대 워크플로우별 결과표 차별화 표준 규격 (4-MASTER-FOLDERS-AND-3-TRACK-STANDARDS)
- **[4-MASTER-FOLDER-LIFECYCLE-LOCK]**: 파이프라인의 데이터 오염 방지(Pipeline Isolation) 및 업무 생명주기(Lifecycle) 관리를 위해 다음 **4대 마스터 폴더 체계**를 전역 강제한다:
  - **`01_번역대상_원본`**: [신규 인풋] 순수 한국어 원본 이미지 및 DOCX 수납.
  - **`02_번역결과_최종`**: [Track 1 신규 아웃풋] 신규 다국어 번역 상세페이지 + SEO + VIEWER 수납.
  - **`03_번역품질평가`**: [Track 2 감사/진단] `01_평가대상_원본`(기존 다국어본) ➔ `02_진단결과`(진단 리포트).
  - **`04_번역교정`**: [Track 3 교정 완결 아웃풋] 1단계 진단 결함(오타 7종, MoCRA 위반 등)을 100% 치료한 최종 교정본 수납.
- **[WORKFLOW-TABLE-DIFFERENTIATION]**: 초월번역 시스템은 업무 성격에 따라 3대 워크플로우로 명확히 분리되며, 각 결과표는 다음 차별화 규격을 전역 강제한다:
  - **1. [워크플로우 1] 신규 상품 다국어 런칭 (New Production - `01` ➔ `02`)**:
    - 처음부터 기계 직역을 전면 배제하고 최고급 초월번역을 직접 생성하므로, 인위적인 기계번역 열을 일체 생성하지 않는다.
    - **표준 결과표**: **`💎 3단 순수 초월번역 가치표`** (`① 한국어 원문 ➔ ② 확정 초월번역 ➔ ③ 글로벌 마케팅 가치 및 규정 분석`)
  - **2. [워크플로우 2] 기존 상세페이지 품질 진단/감사 (Pre-Audit - `03/01` ➔ `03/02`)**:
    - 타사/기존 번역물이 실제로 존재하는 경우에 한하여 기계직역/기존본의 결함을 대조 분석한다.
    - **표준 결과표**: **`📊 4단 품질 진단 대조표`** (`① 한국어 원문 ➔ ② 실제 기존 타사 번역본 ➔ ③ 권고 초월번역안 ➔ ④ 결함 및 개선점 분석`)
  - **3. [워크플로우 3] 결함 교정 및 재검증 (Closed-Loop Remediation - `03` ➔ `04`)**:
    - 1단계 진단 피드백을 주입하여 재렌더링 후 결함 해결 여부를 1:1로 확증하여 **`04_번역교정`**에 수납한다.
    - **표준 결과표**: **`🎯 5단 개선 조치 이행 검증표 (Delta Matrix)`** (`① 지적 항목 ➔ ② 수정 전 기존(Before) ➔ ③ 목표 권고안 ➔ ④ 최종 렌더링(After) ➔ ⑤ 이행 판정`)

## 3. 원본 비율 및 해상도 절대 보존 (Aspect Ratio Lock)
- 렌더링 결과물은 Pillow 라이브러리의 LANCZOS 알고리즘 등을 통해 원본 이미지의 픽셀 비율(Aspect Ratio)과 해상도에 100% 강제 동기화되어야 하며, 정사각형(1:1) 등으로 임의 크롭되는 것을 절대 금지합니다.

## 4. 상품 패키지 포장 원본 보존 규칙 (Product Package Text & Logo Protection)
- 이미지 속 제품이나 상품의 패키지 박스 원본에 포함된 텍스트 및 브랜드 로고는 상품 패키지 박스 포장 원본 형태를 그대로 유지하며, 패키지 상의 글자 및 로고에 대한 번역/수정/수평 덧칠 행위를 엄격히 금지합니다.

## 5. 구글 클라우드 공식 가이드 참조 및 비동기 API 통신 규격 강제 규칙 (Official Docs, Location & Async SDK Lock)
- **[ASYNC-SDK-LOCK]**: 모든 Gemini API 호출 시 rom google import genai 공식 SDK를 사용하며, 동기 호출을 전면 금지하고 **wait client.aio.models.generate_content() 비동기 코루틴 호출 규격을 100% 강제**한다.
- **[TOKEN-LIMIT-DUALIZATION-LOCK]**: 토큰 한도는 목적에 따라 이원화하여 전역 강제한다:
  - **대용량 데이터 추출 및 고시표 번역 (Pass 1 & Table Render)**: max_output_tokens=8192 (화학 성분 및 복합 JSON 누락 방지)
  - **마케팅 카피 및 SEO 생성 (SEO/GEO/AEO)**: max_output_tokens=8192 (비용 최적화 및 3대 섹션 안정 수납)

- 모든 Gemini 3.1+ 모델 호출 시, 추측성 리전 변경을 엄격히 금지하며 무조건 프로젝트 내 구글 공식 가이드(`00_공통자료/.../Vertex_AI_Model_Garden_공식가이드_및_모델선택규칙.md`)의 **`location="global"` (Serverless 관리형 규격)**을 100% 강제 적용합니다.
- 어떠한 상황에서도 공식 기술 문서의 규격을 이탈하여 `us-central1` 등 임의의 리전으로 단독 변경하는 행위를 절대 금지합니다.
- **[공식 문서 주기적 체크 필수]**: 구글 클라우드 에이전트 플랫폼(Google Cloud Agent Platform) 및 Vertex AI Model Garden 공식 가이드와 신규 업데이트 내용을 작업 전/주기적으로 반드시 탐색·체크하여 최신 API 표준 및 리전 정책을 차질 없이 반영합니다.
- **[HARD STOP — load_credentials() 의무 사용 규칙]**: 에이전트가 Gemini API를 호출하는 모든 스크립트(임시 스크래치 파일 포함)에서 `genai.Client(vertexai=True, project=..., location=...)` 를 **직접 작성하는 행위를 전면 절대 금지**합니다. 반드시 `multilingual_text_in_image_translatio_agy_sdk_core.py` 내 `load_credentials()` 함수를 `import`하여 호출해야 합니다. 이 함수가 `location="global"` 을 포함한 모든 인증 및 리전 규칙을 정확히 보장합니다.
  ```python
  # 【유일하게 허용되는 클라이언트 초기화 패턴】
  import sys
  sys.path.insert(0, r"C:\Users\euntaewoo\Desktop\multilingual_text_in_image_translatio_agy_sdk\multilingual_text_in_image_translatio_agy_sdk_core")
  from multilingual_text_in_image_translatio_agy_sdk_core import load_credentials
  client = load_credentials()  # location="global" 자동 보장
  ```

## 6. 깃허브 자동 버전 관리 및 실시간 푸시 규칙 (Automatic GitHub Sync & Push)
- 모든 작업 진행 시, 소스코드 수정, 문서 개정, 신규 기능 추가가 일어날 때마다 무조건 깃허브 저장소(`https://github.com/euntaewoo/PANDORA.git`)로 자동 커밋 및 푸시(Auto Commit & Push)를 수행하여 버전 관리를 실시간 유지해야 합니다.
- API 키 및 인증 파일은 `.gitignore`로 안전하게 제외 처리한 후 커밋합니다.

## 7. 상품 정보 고시 표(Notice Table) 고해상도 HTML 렌더링 표준 규격 (Notice Table Rendering Standard)
- **[해상도 규격]**:
  - 가로 폭: **`860px` 고정**
  - 세로 높이: **`Auto-Fit` 적용 (단, 최대 허용 높이는 `2,580px` 이하 엄격 준수)**
  - **[2페이지 분할 룰]**: 전성분 등 본문 내용이 길어져 세로 높이가 **`2,580px`를 초과할 경우 무조건 2페이지(Part 1, Part 2)로 분할 작성**하여 개별 이미지로 렌더링할 것.
- **[언어별 표준 폰트 적용 및 철저한 격리 원칙 (Font Isolation Standard)]**:
  - **영문(EN)**:
    - **메인 이미지 및 상세페이지 본문/카피**: **`Montserrat (몬세라트)` 100% 단일 서체 강제** (AI 인페인팅 엔진 렌더링 시 타 폰트 혼용 절대 금지).
    - **상품상세정보(고시정보) 테이블**: **`Pretendard` 전용 분리 적용** (오직 독립 Headless HTML 렌더러 `render_notice_table_standard.py`에만 국한).
  - **일본어(JP)**: **`Noto Sans JP`** (NotoSansJP-Bold / NotoSansJP-Regular)
  - **중국어(CN / TW / HK)**: **`Noto Sans SC (스위안헤이티 / 思源黑体)`** (NotoSansSC-Bold / NotoSansSC-Regular)
  - 기타 언어: 해당 국가 및 상품 카테고리에서 가장 빈도가 높고 가독성이 검증된 표준 산세리프 서체 적용.
- **[타이포그래피 폰트 크기 규격]**:
  - **영문(EN) / 일본어(JP)**:
    - **상단 타이틀**: **`64px`** (Bold)
    - **테이블 좌측 항목명 (항목 라벨 열)**: **`32px`** (Bold)
    - **테이블 우측 본문 내용 (값 열)**: **`32px`** (Regular)
  - **중국어(CN / TW / HK)**:
    - **상단 타이틀**: **`52px`** (Bold)
    - **테이블 좌측 항목명 (항목 라벨 열)**: **`26px`** (Bold)
    - **테이블 우측 본문 내용 (값 열)**: **`26px`** (Regular)
- **[1열 항목명 가로 폭 및 줄바꿈 전역 공통 규칙 (Column 1 Layout Standard)]**:
  - **1열 가로 너비 기준점 (Max Label Width Base)**: 1열의 가로 너비는 해당 언어의 고시정보 항목 중 **"가장 긴 단일 항목(불필요한 공백이나 줄바꿈 없이 1줄로 딱 맞게 수납되는 최대 단일 항목)"의 텍스트 길이를 기준점**으로 산정하여 최적화한다.
    - 예시 (중국어): `特殊用途化妆品审查` (9글자)를 기준으로 `width: 275px` 최적화.
    - 예시 (영문/일본어): `Country of Origin`, `製造販売業者` 등 각 언어별 최대 단일 라벨 기준 폭 최적화.
  - **복합 기술 항목의 의미 단위 줄바꿈 (Semantic Line-Break)**: 1열 항목명이 2개 이상의 복합적 의미로 길게 기술된 항목(예: `제조업자 및 책임판매업자`, `化妆品生产企业及责任销售商`, `Manufacturer & Distributor`)은 1열 너비를 억지로 늘리지 않고 **그 의미 단위로 자연스럽게 줄바꿈(`<br>`)하여 표기**한다.
    - 예시: `化妆品生产企业及`<br>`责任销售商`, `제조업자 및`<br>`책임판매업자`
  - **[2열 본문 기능성/특수용도 심사 효능 괄호 앞 줄바꿈 규칙 (Functional Cosmetics Semantic Line-Break)]**: 기능성 및 특수용도 심사 항목의 2열 본문에서 기관 심사 결과와 효능 부가설명 괄호 구문(`(미백...)`, `(美白...)`)은 서로 다른 의미 단위이므로, 괄호 `(` 또는 `（` 앞에서 파이썬/HTML 렌더러가 100% 무조건 강제 개행(`<br>`)을 주입하여 가독성을 보장한다.
    - 예시 (중국어 간체): `已完成韩国食品药品安全处审查`<br>`(美白、改善皱纹双重功效)`
    - 예시 (중국어 번체): `已完成韓國食品藥物安全處審查`<br>`(美白、改善皺紋雙重功效)`
    - 예시 (한국어): `식품의약품안전처 심사 필 완료`<br>`(미백, 주름개선 2중 기능성화장품)`
- **[렌더링 엔진]**: AI 생성형 뭉개짐을 배제하고 칼같은 벡터 텍스트 선명도를 위해 Headless Chromium/Edge 기반 초고해상도 렌더링 파이프라인을 의무 적용할 것.



## 8. 중국어 번역 타겟 권역 사전 확인 의무 규칙 (Mandatory Region Check for Chinese Translation)
- 사용자가 중국어 번역을 요청할 때, 명시적인 권역(간체자 vs 번체자)이나 특정 플랫폼/지역이 명시되지 않은 경우, 에이전트는 절대 임의로 추측(`[ZERO-GUESSING]`)하여 작업을 진행하지 마십시오.
- 작업 착수 전 반드시 아래의 표준 질문을 사용자에게 먼저 제시하고, 사용자의 선택/답변을 확인한 후 해당 권역 규격에 맞추어 작업을 진행해야 합니다:
  > **"중국 본토(간체자)와 대만/홍콩(번체자) 중 어느 시장을 타겟으로 제작할까요?"**
- **권역별 표준 규격**:
  - **중국 본토 (간체자, zh-CN)**: 간체자 출력, 중국 신(新) 광고법 절대화 표현 필터링, 타오바오/티몰 톤앤매너, Noto Sans SC (스위안헤이티 / 思源黑体) 렌더링.
  - **대만/홍콩 (번체자, zh-TW / zh-HK)**: 번체자 출력, 대만 TFDA 규정 및 현지 이커머스 어휘(鎖水, 水光肌 등), Noto Sans TC 렌더링.
- **[8.1 번체자(대만/홍콩) AI 인페인팅 간체 획수 유출(Drift) 원천 차단 규칙 (Absolute Traditional Glyph Lock)]**:
  - 확산 이미지 인페인팅 모델(`gemini-3.1-flash-image`)은 사전 학습 데이터셋 특성상 번체자 렌더링 시 간체자 획수로 쏠리는 현상(Glyph Drift)이 발생할 수 있으므로, 번체자(TW/HK) 모드에서는 Pass 2 프롬프트에 **"간체자 획수 렌더링 절대 금지 및 획수 단위 정체자 고정 규칙(Negative Glyph Constraint)"**을 100% 의무 주입한다.
  - **필수 교정 한자 리스트**:
    - `養(O) vs 养(X)` (보양/영양/조리), `對(O) vs 对(X)` (대책/침대), `護(O) vs 护(X)` (수호/호리), `創(O) vs 创(X)` (수창/창조)
    - `變(O) vs 变(X)`, `顯(O) vs 显(X)`, `實(O) vs 实(X)`, `體(O) vs 体(X)`, `驗(O) vs 验(X)`
    - `緊(O) vs 紧(X)`, `緻(O) vs 致(X)`, `膚(O) vs 肤(X)`, `雙(O) vs 双(X)`, `氣(O) vs 气(X)`
    - `隊(O) vs 队(X)`, `劃(O) vs 划(X)`, `歲(O) vs 岁(X)`, `乾(O) vs 干(X)`, `華(O) vs 华(X)`
    - `濕(O) vs 湿(X)`, `鎖(O) vs 锁(X)`, `膠(O) vs 胶(X)`, `纖(O) vs 纤(X)`

## 9. 중국어 이커머스 상세페이지 렌더링 3대 실전 팁 규칙 (Chinese E-commerce Layout Optimization)
- 중국어 한자(간체자/번체자)는 정사각 Em-box를 꽉 채우는 특성으로 인해 한국어 대비 시각적 부피가 크므로, 레이아웃 붕괴를 방지하기 위해 다음 3대 실전 팁을 강제 적용합니다:
  1. **본문 폰트 크기 슬림화 (Font Size Reduction)**: 한국어 원본 대비 폰트 크기를 약 10~15% 작게 설정하여 원본 디자인의 시각적 여백과 균형(Balance)을 유지할 것.
  2. **행간(Line Height) 15~20% 확장**: 한자가 상하로 빽빽하게 붙어 가독성이 저하되는 것을 방지하기 위해 한국어 대비 행간을 15~20% 더 넓게 (`line-height: 1.6 ~ 1.7`) 설정할 것.
  3. **자간(Letter Spacing) 여유 확보**: 답답하고 빽빽한 느낌을 줄이고 럭셔리/프리미엄 뷰티 상세페이지 느낌을 극대화하기 위해 자간을 미세하게 확장(`letter-spacing: +0.5px ~ +1.0px` / `+50~+100`)할 것.

## 10. 글로벌 럭셔리 뷰티 초월번역 및 규제 준수 표준 규격 (Global Luxury Beauty Transcreation & Compliance Automator)
- **1. 시스템 역할 (Role & Persona)**: 에스티로더, 랑콤, 시슬리, SK-II 등 글로벌 하이엔드 코스메틱 10년 차 수석 CD 및 엘리트 카피라이터 페르소나 적용. 단순 직역을 배제하고 초월번역(Transcreation) 수행.
- **2. 번역투 및 1:1 직역 부사 전면 금지 (Eliminate Translationese)**: `Definitely`, `Truly`, `確実に`, `本当に`, `确实`, `真正`, `확실히`, `진짜` 등 어색한 감정 부사 직역을 전면 차단하고, 프리미엄 동사/형용사로 세련되게 재창조.
- **3. 구문 결속 및 활성 성분 연결 (Natural Sentence Flow)**: "10% LiftDerm" 등 성분 비율 수치가 문맥과 단절되지 않고 제품명 및 효능 서사로 자연스럽게 흘러가도록 문장 구조 재조정.
- **4. 4대 기능성 바이오 뷰티 전문 어휘 사전 (Premium Terminology)**:
  - **피부 속/기저층**: [EN] `Deep within the skin layers` / [JA] `肌の奥・角質層のすみずみ` / [ZH-CN] `肌底深处` / [ZH-TW] `肌底`
  - **토탈 케어/멀티 코렉티브**: [EN] `Multi-Corrective Repair` / [JA] `高機能トータルリペア` / [ZH-CN] `多效修护` / [ZH-TW] `多效修護`
  - **탄력 복원/강화**: [EN] `Rebuilding skin elasticity` / [JA] `ハリ・弾力を呼び覚ます` / [ZH-CN] `赋活肌底弹力` / [ZH-TW] `賦活肌底彈力`
  - **눈가 잔주름/건조주름**: [EN] `Fine lines and wrinkles` / [JA] `目元の小ジワ・乾燥ジワ` / [ZH-CN] `细纹・干纹` / [ZH-TW] `細紋・乾紋`
- **5. 독자 성분명, 브랜드명 및 전역 용어집(Brand & Key Ingredient Glossary Standard)**:
  - **브랜드명(Brand Name)**: 고유 영문 명칭인 **`Logicall Skin`**을 100% 원형 유지하며, 임의 한자/가타카나 번역을 금지한다.
  - **상품명 및 FAQ 동적 렌더링 (Dynamic Product Name Mapping)**:
    * 과거 특정 상품(예: `阿夸肽修护精华液 (Aquatide Resurface Serum)`)으로 템플릿이 하드코딩되었던 방식을 폐기하고, 현재 번역 파이프라인에서 구동 중인 타겟 폴더의 상품명(`{product_name}`)을 실시간 동적 감지하여 제품 정식 명칭 및 5대 핵심 맞춤형 FAQ를 똑똑하게 자동 생성하도록 100% 동기화한다.
  - **글로벌 독자 성분명 보존**: `LiftDerm`, `Lifting Logic for eye`, `Aquatide 5000` 등 글로벌 독자 성분명은 영문 원형을 보존한다.
  - **제품 본품 인쇄 무손실 보존**: 제품 본품(용기 표면)에 인쇄된 영문 텍스트 및 로고는 1픽셀 왜곡 없이 100% 보존한다.
- **6. 절대적/검증불가 표현 전면 금지 (Ban on Absolute & Unverifiable Claims)**:
  - `全球首創`(세계최초), `第一`(제1), `最佳`(최고), `終極對策`(종극대책) 등 절대적 수식어 전면 차단.
  - 반드시 `專為...研發의 創新科技`(혁신기술), `頂級多效`(프리미엄케어), `精準修護`(어드밴스드 포뮬러)로 의무 순화.
- **7. 의료/임상 오인 금지 및 4대 안전 동사 강제 (Compliance-Safe Verbs)**:
  - 보톡스/필러 등 의료 시술 연상 및 '주름 박멸/영구 삭제' 표현 전면 배제.
  - 반드시 **`撫平` (Smooth), `淡化` (Diminish), `舒緩` (Alleviate), `修護` (Care)** 4대 컴플라이언스 안전 동사 사용.
- **8. 권역별 로컬라이징 전략**:
  - **EN**: 세포라(Sephora) 및 최고급 백화점 톤 (능동적, 결과 중심적, 임상적 신뢰도)
  - **JA**: @cosme 정중하고 섬세한 제형/효능 감성 묘사, 56종 약기법 포지티브 리스트 100% 준수
  - **ZH-CN**: 중국 신광고법 8대 절대화 금지어 차단, NMPA 준수, 간체자
  - **ZH-TW**: 대만/홍콩 우아한 메디컬 더마 톤, TFDA 규정 준수, 절대표현 순화, 대만 정체자 및 23개 한자 글리프 잠금
- **9. 생성 AI 하이퍼파라미터 표준**:
  - `temperature`: 0.6, `topP`: 0.9, `maxOutputTokens`: 2048 (JSON 무결성 및 전수 텍스트 블록 보호).
  - 📖 **상세 기술 규격서**: [`00_공통자료/제미나이_AI_번역_안전장치_안티그래비티2.0_Gemini_GenerationConfig_기술규격서.md`](file:///C:/Users/euntaewoo/Desktop/multilingual_text_in_image_translatio_agy_sdk/00_공통자료/제미나이_AI_번역_안전장치_안티그래비티2.0_Gemini_GenerationConfig_기술규격서.md) 참조.

## 11. 다국어 고시정보표(Notice Table) 타이포그래피 및 레이아웃 표준 규격
- **1. 1열 라벨 너비 및 폰트 크기 (Width & Font Size)**:
  - **한국어(KO)**: `width: 295px` (Pretendard 30px, padding: `24px 20px`, val_padding: `24px 26px` 기준, 긴 한국어 라벨 '화장품제조업자 및 책임판매업자' 2줄 황금비율).
  - **영어(EN)**: `width: 295px` (Pretendard 30px, padding: **`14px 12px`**, val_padding: **`14px 16px`**, letter-spacing: **`-0.8px`** 기준. 순수 가용폭 **`271px`** 확보로 `Customer Service`, `Country of Origin`, `Precautions for Use` 등 16~19자 주요 라벨 100% 1줄 안착 및 'Quality Assurance Standard' 2줄 대칭 보장).
  - **중화권 (중국어 간체 CN / 중국어 번체 TW·HK)**: `width: 250px` (Noto Sans SC/TC 26px 기준, 좌우 여백 총 30px(15px+15px), 2열 순수 본문 폭 570px 극대화 황금비율).
  - **일본어(JA)**: `width: 280px` (Noto Sans JP 32px 기준).
- **2. 줄바꿈 및 오버플로우 방지 (Word Break & Overflow Wrap)**:
  - **필수 속성**: **`word-break: keep-all; overflow-wrap: break-word;`** (영문 단어가 중간에 찢어지는 `Origin` ➔ `Or`/`igin`, `Standard` ➔ `St and`/`ard` 결함 100% 원천 차단).
  - **동작 원리**: 1열 라벨은 `keep-all`을 통해 어절(단어) 단위로만 줄바꿈되며, 2열 본문은 `overflow-wrap: break-word`를 통해 긴 전성분이나 URL이 영역을 벗어나지 않도록 방어.
  - **정규식 단어 경계(`\b`)**: 정규식 접속사 매칭 시 `\band\b|\bor\b` 단어 경계를 강제하여 `Origin`, `Standard` 등 단어 내부 알파벳 오인 분절 원천 방지.
- **3. 정렬 및 가독성 (Alignment & Padding)**:
  - **필수 속성**: **`text-align: left; vertical-align: middle;`** (EN: `padding: 14px 12px; letter-spacing: -0.8px;`, KO/JP: `padding: 24px 20px`, CN/TW: `padding: 20px 15px`).
- **4. 언어별 독립 샌드박스화 문맥 의미 단위 줄바꿈 (Language-Specific Sandboxed Semantic Breaker)**:
  - **단문 라벨 1줄 강제 유지**: `Skin Type`, `Directions`, `Ingredients`, `Country of Origin`, `Precautions for Use`, `Customer Service` ➔ 100% 1줄 강제 유지.
  - **10자 이상 긴 라벨 분할**:
    * **EN 샌드박스**: 글로벌 FDA/MoCRA 규격 (`Country of<br>Origin`, `Quality Assurance<br>Standard`, `Precautions<br>for Use`, `Manufacturer /<br>Distributed by`, `Functional Cosmetics<br>Review Status`, `Shelf Life /<br>Period After Opening`).
    * **CN 샌드박스**: 중국 신광고법 및 NMPA 표준 규격 (`特殊用途化妆品<br>审查状态`, `化妆品生产企业 /<br>责任销售商`, `使用期限或<br>开封后使用期限`).
    * **TW/HK 샌드박스**: 대만 TFDA 표준 규격 (`特殊用途化妝品<br>審查狀態`, `化妝品生產企業 /<br>責任銷售商`, `保存期限或<br>開封後保存期限`).
    * **JP 샌드박스**: 일본 약기법 및 @cosme 표준 (`製造販売業者及び<br>製造業者`, `使用期限又は<br>開封後の使用期間`, `医薬部外品・薬用<br>審査済み`).
    * **KO 샌드박스**: 식약처 고시 표준 (`기능성 화장품<br>심사 필 유무`, `화장품제조업자 및<br>책임판매업자`, `사용기한 또는<br>개봉 후 사용기간`).
  - **2열 본문 상품명/영문 병기 스마트 의미 단위 줄바꿈 (Smart Semantic Line-Break for Bilingual Product Names)**:
    * 2열 본문의 상품명(제품명)이 1줄 가로폭(`570px`)에 온전히 들어가는 짧은 품명은 **1줄 자연 안착을 유지**한다.
    * 한자/한글 품명과 영문 병기를 합친 길이가 2열 안전 가로폭(`520px`)을 초과하여 영문 단어 도중 어정쩡하게 줄바꿈 결함이 발생하는 경우에는, **괄호 앞(`(` 또는 `（`)에 `<br>`을 자동 주입하여 `한자 품명` / `(영문 병기)` 형태로 완벽한 의미 단위 2줄 분리 안착**을 강제 적용한다.
  - **2열 본문 단어 결속 보호**: 전문의 상담 어휘(`专业医生`, `专业医师`, `전문의 등과 상담할 것`) 등 핵심 구문은 `<span style="white-space: nowrap">` 또는 `\u00A0`로 묶어 1글자 낙오 원천 차단.
  - **2열 본문 기능성화장품 심사필 초월번역 의무화 (Functional Cosmetics Value Transcreation)**:
    * 원문의 `Y (미백, 주름개선 등)`, `해당있음`, `심사필` 등 단순 기계적 `Y` 알파벳 출력을 전면 금지한다.
    * **영어 (EN)**: **`MFDS-Certified Functional Cosmetic (Brightening, Wrinkle Improvement, UV Protection)`** (또는 해당 기능성 공식 인증 명칭)으로 글로벌 신뢰도 문구 승격 의무화.
    * **중국어 (CN/TW)**: **`已完成特殊用途化妆品审查 (美白、改善皱纹双重功效)`** (또는 `已完成特定用途化粧品審查`)으로 NMPA/TFDA 공인 표현 강제.
    * **일본어 (JP)**: **`機能性化粧品審査済（美白・シワ改善・紫外線カット等）`** 약기법 표준 표기 강제.
- **5. 고시정보표 전담 프론트엔드 QA 서브에이전트 (`notice_table_frontend_qa_agent`) 4대 핵심 업무 및 자동 검수 의무화**:
  - **1) 시각적 이미지 실측 검수 (`view_file` 정밀 디코딩 의무)**: 고시정보표 렌더링 완료 즉시, 에이전트는 무조건 `view_file` 도구를 실행하여 `Part1.png`, `Part2.png` 이미지를 직접 시각 디코딩 검수한다. 로그 성공 메시지만 보고 통과시키는 행위를 엄격히 금지한다.
  - **2) 타이포그래피 및 줄바꿈 품질 감독**: 10자 미만 단문 라벨의 1줄 강제 안착 여부 및 긴 복합 라벨(`Country of Origin`, `Quality Assurance Standard`)의 의미 단위 대칭 2줄 분할, 단어 쪼개짐 여부를 전수 검사한다.
  - **3) 2열 본문 외톨이 글자(Orphan Word) 및 침범 차단**: 문장 끝 1~2글자 낙오 방지 및 2열 본문 영역 침범 여부를 실측 검증한다.
  - **4) 무인 자가 수술 및 재렌더링 자가개선 루프 (Self-Healing QA Loop)**: 검수 중 레이아웃 결함 감지 시, `render_notice_table_standard.py`의 CSS/정규식을 즉시 자체 수정 ➔ 재렌더링 ➔ 재검수 통과 후 최종 저장 및 Git 커밋을 완결한다.

---

## 12. 다국어 이커머스 SEO/GEO/AEO 마이크로-써머리(DOCX + TXT + HTML Viewer) 작성 및 광고법 준수 표준 규격
- **1. [HARD STOP] 산출물 문서 포맷 (DOCX + TXT + HTML 3중 동시 생성)**:
  - **MS Word (`.docx`)**: 굵은 제목(Bold), 문단 간격, 불릿 기호 등 시각적 타이포그래피가 완벽히 보존된 서식 문서로 자동 생성하여 눈으로 확인하고 부위별로 발췌/복사하기 용이하게 제공.
  - **서식형 텍스트 (`.txt`)**: 문장 단위 자동 개행(`\r\n`)과 명확한 닫는 괄호 번호(`1)`, `2)`)를 적용하여 메모장이나 웹 폼 입력 시 가로 1줄로 길게 늘어지는 현상을 원천 방지.
  - **다국어 이커머스 원클릭 복사 뷰어 (`_VIEWER.html`)**: 스마트스토어, 쿠팡, 지마켓/옥션(ESM Plus), 11번가, 타오바오/티몰, 쇼피, 아마존 등 **국내외 모든 전자상거래 플랫폼 에디터에 100% 줄바꿈과 문단 여백이 자동 보존**되는 순수 텍스트 및 서식 복사 도구 제공.
- **2. [HARD STOP] AI 부연 설명 및 글자수 카운트 메타 주석 일체 출력 금지 (Zero Meta Commentary)**:
  - 사용자가 오픈마켓(아마존, 쇼피, 타오바오/티몰, 징둥, 라쿠텐, 스마트스토어 등) 상품 등록 시 즉각 **100% 원클릭 복사-붙여넣기(Copy & Paste)**할 수 있는 순수 최종 문안만 출력한다.
  - `注：本标题共计49个字符...`, `*(Character Count: 85)*`, `글자수: 45자` 등 글자수 카운트 주석, 해설, 마크다운 코드블록 메타 태그의 출력을 전면 금지한다.
- **3. 각 국가별 전자상거래 및 광고법(Ad-Law) 사전 준수 의무**:
  - **중국/중화권 (CN/TW)**: 중국 신광고법 및 NMPA 규정에 따라 외국 정부 '인증(认证)' 등의 표현을 금지하고 '심사 완료(通过审查 / 审查完毕)'로 표기하며, 절대화 금지어(`最`, `第一`, `顶级` 등) 사용을 엄격히 배제.
  - **미국/글로벌 (EN)**: FDA 화장품 규정(MoCRA)에 따라 의약품적 치료 효능(`cure`, `treat`) 표현을 배제하고 기능성 뷰티 표현(`helps improve the appearance of wrinkles`, `deeply hydrates`) 준수.
  - **일본 (JP)**: 일본 의약품의료기기등법(약기법) 56개 표방 가능 효능 범위를 준수하여 허위/과장 광고 차단.
  - **한국 (KO)**: 화장품 표시·광고 실증에 관한 규정에 맞춘 기능성 화장품 표기 준수.
- **4. 쇼핑몰 상품등록 표준 실무 매뉴얼 동기화**:
  - `00_공통자료/쇼핑몰_상품등록_원클릭_복사_실무가이드.md` 문서에 지마켓/옥션(ESM Plus), 스마트스토어, 쿠팡, 타오바오 등 탭별 원클릭 복사 실무 프로세스를 영구 보존.

---

## 13. 영문 번역 시 미국 FDA FD&C Act 및 MoCRA 의약품 오인성(Drug Claim) 원천 금지 및 럭셔리 초월번역 표준 규격
- **1. [HARD STOP] 화장품 효능 표제 내 의약품성 단어 사용 원천 금지**:
  - 미국 연방 식품의약품화장품법(FD&C Act 201(g)) 및 화장품 규제 현대화법(MoCRA)에 따라, 화장품 상세페이지의 메인 카피나 표제구에서 질병/증상 치료를 연상시키는 의약품성 용어 사용을 전면 금지한다.
- **2. 의약품 오인성 금지어 ➔ 럭셔리 뷰티 초월번역 매핑 강제**:
  - `Wrinkle Treatment` (주름 치료) ➔ **`Advanced Wrinkle Care` / `Targeted Wrinkle Solution` / `Age-Defying Ritual`**
  - `Treatment` (단독/치료 표기) ➔ **`Care` / `Solution` / `Formula` / `Ritual`**
  - `Whitening` (미백/탈색 오인) ➔ **`Brightening` / `Radiance` / `Illuminating`**
  - `Trouble / Skin Trouble` ➔ **`Blemish` / `Sensitive Skin Concerns` / `Visible Irritation`**
  - `Cure / Heal / Repair tissue` ➔ **`Soothe` / `Comfort` / `Fortify skin barrier` / `Visible Renewal`**
  - `Bulk up / Build up` (피트니스 은어) ➔ **`Volumizing Skin Density Matrix` / `Triple Firming Architecture`**
- **3. 원본 텍스트 무비판적 계승(Carryover) 원천 차단**:
  - 영문 원본이나 한국어 직역 텍스트에 상기 금지어가 존재하더라도, Pass 1 OCR/초월번역 단계에서 100% 필터링하여 글로벌 프레스티지 스킨케어(Sephora/Amazon US) 규격 카피로만 출력한다.








---

## 14. 다국어 이커머스 초월번역(Transcreation) 품질 자동 평가 및 자가개선 루프 표준 규격 (Transcreation Self-Healing QA Standard)
- **1. [HARD STOP] 4대 정밀 평가 루브릭 (100점 만점) 및 합격 기준**:
  - **① 도메인/카테고리 어휘 적합성 (30점)**: 뷰티/스킨케어 전문 용어의 현지화 수준 (Konglish, 직역투 배제)
  - **② 국가별 광고법 무결성 (30점)**: 미국 MoCRA, 일본 약기법 56종, 중국 신광고법/NMPA 8대 절대화 금지어 100% 준수
  - **③ 브랜드 감성 및 초월번역 완성도 (25점)**: 세포라, @cosme, 샤오홍슈 최상위 뷰티 브랜드 톤앤매너 구현
  - **④ 시각 레이아웃 및 텍스트 밸런스 (15점)**: 텍스트 오버플로우 방지 및 간결한 문장 구조
  - **[합격 기준]**: **종합 점수 90점 이상 & 법률 위반 0건 (PASS)**
- **2. [자가 치유 루프 (Self-Healing Loop) 의무화]**:
  - 번역 결과물이 90점 미만이거나 광고법 위반 표현이 검출될 경우, 평가 모듈의 교정 피드백(`correction_feedbacks`)을 Pass 1 프롬프트에 자동 주입하여 **최대 2회 무인 재렌더링(Full Regeneration)**을 실행한다.
- **3. [3중 품질 리포트 자동 발행]**:
  - 번역 완료 시 각 언어별 결과 폴더(`02_번역결과_최종/`) 내에 **`Transcreation_QA_Report.html`** (원클릭 시각 뷰어) 및 **`Transcreation_QA_Report.json`**을 의무 생성하여 보관한다.

---

## 15. Antigravity UI 및 시스템 조작 표준 (UI-SOURCE-VERIFICATION-LOCK)
- **1. [UI-SOURCE-FIRST]**: Antigravity 2.0 및 IDE 환경의 UI 조작/설정 관련 질의 시 일반론이나 추측성 답변을 전면 금지하며, 반드시 로컬 설치 렌더러 소스코드(`jetskiAgent/main.js` 등)를 직접 실측하여 확인된 단일 정답만 1회에 즉시 안내한다.
- **2. [PROJECT-REMOVAL-STANDARD]**: Antigravity 2.0 화면(사이드바)에서 프로젝트 폴더를 삭제/제거할 때는 실제 PC 파일 삭제가 아닌 UI 상의 프로젝트 해제 표준 경로를 안내한다:
  - **공식 표준 경로**: 프로젝트 우측 `⋮` (세로 점 3개) ➔ `Project Settings` ➔ 화면 최하단 `Danger Zone` ➔ `Delete Project` (실제 원본 파일 100% 보존, UI 화면 목록에서만 완전 삭제).

---

## 16. 전수 파일 이관 및 무결성 1:1 대조 프로토콜 (Anti-Hallucination Sync Rule)
- **1. 기계적 스캔 및 추측 금지**: 대규모 폴더나 파일을 다른 프로젝트로 복제/이관/마이그레이션할 때, 에이전트는 절대 list_dir이나 눈대중으로 파악하고 "다 옮겨졌다"고 추측(Guessing) 및 허위 보고(Hallucination)하는 것을 전면 영구 금지한다.
- **2. [VERIFY-BEFORE-REPORT] (강제 1:1 바이트 및 개수 대조)**: 복사 작업 후 완료를 보고하기 전에, 반드시 PowerShell의 Compare-Object나 Measure-Object 등을 활용하여 양쪽 폴더의 순수 프로젝트 자산(예: .venv, __pycache__, .git 제외)의 "파일 개수 총합"이 1:1로 100% 일치하는지 터미널 명령어 수준에서 수치로 증명(물리적 실측)해야 한다.
- **3. 물리적 증거(숫자) 기반 보고**: 사용자에게 완료를 보고할 때는 에이전트의 주관적 텍스트 서술이 아닌, 1:1로 일치된 [파일 개수 수치]와 [터미널 출력 로그]를 팩트 증거(EVIDENCE)로 직접 제시해야만 정상적인 작업 완료로 인정받는다.

---

## 17. 입력 폴더 트리(하위 폴더) 자동 인식 및 병합 처리 규정 (Recursive Directory Scan)
- **1. 지원 규격**: 번역 대상 원본 이미지를 투입하는 입력 폴더(01_번역대상_원본)에 낱개 파일을 직투입하는 방식뿐만 아니라, 상품별/카테고리별로 서브 폴더(예: \세럼\, \크림\)를 무한 Depth로 생성하여 분류해 넣어도 엔진이 모든 하위 폴더를 자동으로 뚫고 들어가 재귀 탐색(os.walk)하여 100% 인식한다.
- **2. 코드 명세 보장**: 향후 구동 엔진 업데이트 시, 이미지 스캔 로직은 반드시 단일 폴더 스캔(os.listdir)을 배제하고 하위 폴더 추적 래퍼 함수(get_recursive_files 또는 os.walk) 체제를 100% 영구 유지해야 한다.

## 18. [3단계 철벽 코드 검증 표준] (3-Stage Ironclad Code Verification Standard)
에이전트는 어떠한 파이썬 스크립트 수정 후에도 아래 3단계를 의무 실행하여 무결성을 증명해야 한다:
1. **1단계 (py_compile)**: python -m py_compile <파일경로> 가동으로 문법/들여쓰기 100% 무결성 검증.
2. **2단계 (정규식/보안 린트)**: client.aio 비동기 규격, 토큰 8192 안전천장, 정규식 문법 오류( * 등) 0건 스캔.
3. **3단계 (RULE-QA-LOOP)**: view_file 도구로 최종 산출물(이미지/표)을 뷰어로 열어 시각적 무결성 실측 검수.
