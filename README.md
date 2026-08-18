# PANDORA - Multi-lingual_Text-In_Image_Translation_Engine

한국어 원본 상세페이지/제품 이미지를 단일 공통 폴더에 넣고, 도착 언어(영어, 일본어, 중국어 간체/번체)를 선택하면 각 국가별 법률 및 폰트 규정에 맞추어 원클릭으로 일괄 번역·렌더링하는 통합 시스템입니다.

---

## 📊 워크플로우 차트 다이어그램 (System Architecture)

```mermaid
flowchart TD
    subgraph S1["1. 단일 공통 인풋"]
        IN["📂 01_번역대상_원본<br/>(한국어 원본 이미지 일괄 수납)"]
    end

    subgraph S2["2. 실행 진입점 (User Execution Trigger)"]
        AGENT["🤖 [최우선] 안티그래비티 채팅창 대화 요청<br/>(예: '영어 번역해줘', '일본어 번역 시작해')"]
        P_MAIN["🥇 [터미널 직접 실행] Multi-lingual_Text-In_Image_Translation_Engine.py<br/>(파이썬 명령어로 직접 구동)"]
        BAT_SUB["🥈 [보조 차선책] 다국어_통합번역_원클릭실행.bat<br/>(탐색기 더블클릭 런처)"]
        
        AGENT -->|에이전트가 자동 실행| P_MAIN
        P_MAIN --> PROMPT{"도착 언어 자동 분기 / 선택<br/>(EN / JP / CN / TW / ALL)"}
        BAT_SUB -.->|대화형 질의응답| PROMPT
    end

    subgraph S3["3. 국가별 규정 및 톤앤매너 자동 분기"]
        EN["🇺🇸 영어 (EN)<br/>• Amazon/Shopee US 초월번역<br/>• Montserrat 단일 서체 강제"]
        JP["🇯🇵 일본어 (JP)<br/>• 후생노동성 56종 약기법 포지티브 리스트<br/>• Noto Sans JP 서체"]
        CN["🇨🇳 중국어 간체 (CN)<br/>• 중국 신광고법 8대 절대화 금지어 순화<br/>• Noto Sans SC (思源黑体) 서체"]
        TW["🇹🇼 중국어 번체 (TW)<br/>• 대만/홍콩 TFDA 규정 준수<br/>• Noto Sans TC 서체"]
    end

    subgraph S4["4. 하이브리드 투패스 렌더링 엔진"]
        P1["🔍 Pass 1: gemini-3.1-pro-preview<br/>(텍스트 전수 스캔, 번역, 법률 필터링, 표 감지)"]
        DECIDE{"이미지 속성 판별"}
        
        HTML["📊 고시정보표 (테이블)<br/>Headless HTML 표준 렌더러<br/>(860px 고정, 100% 벡터 선명도)"]
        P2["🎨 일반 상세페이지 (인페인팅)<br/>Pass 2: gemini-3.1-flash-image<br/>(배경 텍스처 복원, 1:1 종횡비 잠금)"]
        
        P1 --> DECIDE
        DECIDE -->|고시표 / 성분표| HTML
        DECIDE -->|일반 디자인 이미지| P2
    end

    subgraph S5["5. 언어별 결과 폴더 자동 분류 저장"]
        OUT_EN["📂 02_번역결과_최종/영어"]
        OUT_JP["📂 02_번역결과_최종/일본어"]
        OUT_CN["📂 02_번역결과_최종/중국어_간체"]
        OUT_TW["📂 02_번역결과_최종/중국어_번체"]
    end

    IN --> AGENT & P_MAIN & BAT_SUB
    PROMPT -->|EN 모드| EN
    PROMPT -->|JP 모드| JP
    PROMPT -->|CN 모드| CN
    PROMPT -->|TW 모드| TW
    PROMPT -->|ALL 모드| EN & JP & CN & TW

    EN & JP & CN & TW --> P1
    HTML & P2 --> OUT_EN & OUT_JP & OUT_CN & OUT_TW
```

---

## 🚀 빠른 시작 (사용자 표준 실행법)

### 💬 [방법 1: 최우선] 안티그래비티 창에서 말로 요청하기 (가장 편리)
1. `01_번역대상_원본` 폴더에 번역할 한국어 이미지를 넣습니다.
2. 안티그래비티 채팅창에 아래와 같이 말씀하시면 제가 즉시 번역을 수행하고 품질을 검수하여 보고합니다:
   - *"01_번역대상_원본에 이미지 넣었어, 영어로 번역해줘"*
   - *"일본어 약기법 번역 시작해줘"*
   - *"중국어 간체로 번역해줘"*
   - *"전체 언어로 일괄 번역해줘"*

### 💻 [방법 2] 터미널에서 직접 실행
- **대화형 선택 모드**:
  ```bash
  .venv\Scripts\python.exe Multi-lingual_Text-In_Image_Translation_Engine.py
  ```
- **특정 언어 즉시 실행 모드**:
  ```bash
  .venv\Scripts\python.exe Multi-lingual_Text-In_Image_Translation_Engine.py --lang EN   # 영어
  .venv\Scripts\python.exe Multi-lingual_Text-In_Image_Translation_Engine.py --lang JP   # 일본어
  .venv\Scripts\python.exe Multi-lingual_Text-In_Image_Translation_Engine.py --lang CN   # 중국어 간체
  .venv\Scripts\python.exe Multi-lingual_Text-In_Image_Translation_Engine.py --lang TW   # 중국어 번체
  .venv\Scripts\python.exe Multi-lingual_Text-In_Image_Translation_Engine.py --lang ALL  # 전체 일괄
  ```

### 🖱️ [방법 3: 차선책] 탐색기 더블클릭 런처
- `다국어_통합번역_원클릭실행.bat` 더블클릭 ➔ 콘솔에서 숫자(1~5) 입력

---

## ⚙️ 엔진 핵심 아키텍처 및 특징

- **Two-Pass 신경망 인페인팅**:
  - **Pass 1 (`gemini-3.1-pro-preview`)**: 텍스트 추출, 마케팅 초월번역, 국가별 광고법/약기법(일본 후생노동성 56종, 중국 신광고법) 자동 필터링.
  - **Pass 2 (`gemini-3.1-flash-image`)**: 배경 보존 및 자연스러운 시각적 텍스트 식자 인페인팅.
- **고시정보표(테이블) 자동 분기**:
  - 제품 고시표/성분표 레이아웃 감지 시 HTML 표준 헤드리스 렌더러로 자동 분기하여 100% 칼같은 선명도 유지.
- **1:1 비율 보존**: 원본 해상도와 종횡비(Aspect Ratio)를 엄격히 동기화.
