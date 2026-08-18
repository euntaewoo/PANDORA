# multilingual_text_in_image_translation

한국어 원본 상세페이지/제품 이미지를 공통 폴더(`01_번역대상_원본`)에 넣고, 도착 언어(영어, 일본어, 중국어 간체/번체)를 선택하면 각 국가별 법률 및 폰트 규정에 맞추어 원클릭으로 일괄 번역·렌더링하는 통합 시스템입니다.

---

## 📁 주요 문서 링크
- 📊 **[워크플로우 차트 다이어그램](file:///C:/Users/euntaewoo/Desktop/다국어_이미지_번역/multilingual_text_in_image_translation/워크플로우_차트_다이어그램.md)**: 전체 시스템 아키텍처 및 5단계 처리 흐름도
- 📖 **[3가지 실행 방법 가이드](file:///C:/Users/euntaewoo/Desktop/다국어_이미지_번역/multilingual_text_in_image_translation/실행_방법_가이드.md)**: 안티그래비티 대화 요청 / CLI / BAT 실행 상세 가이드
- 🧬 **[기술적 기초 및 계승 내역 레퍼런스](file:///C:/Users/euntaewoo/Desktop/다국어_이미지_번역/multilingual_text_in_image_translation/기술적_기초_및_계승_내역_레퍼런스.md)**: 프로토/영어/일본어/중국어 엔진의 핵심 기술 융합 내역

---

## 📊 워크플로우 차트 다이어그램 (System Architecture)

```mermaid
flowchart TD
    subgraph S1["1. 단일 공통 인풋"]
        IN["📂 01_번역대상_원본<br/>(한국어 원본 이미지 일괄 수납)"]
    end

    subgraph S2["2. 실행 진입점 (User Execution Trigger)"]
        AGENT["🤖 [최우선] 안티그래비티 채팅창 대화 요청<br/>(예: '영어 번역해줘', '일본어 번역 시작해')"]
        P_MAIN["🥇 [터미널 직접 실행]<br/>multilingual_text_in_image_translation.py"]
        BAT_SUB["🥈 [보조 차선책]<br/>다국어_통합번역_원클릭실행.bat"]
        
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

    subgraph S5["5. 상품별·언어별 자동 서브폴더 분류 저장"]
        OUT["📂 02_번역결과_최종/"]
        OUT1["📁 [상품명]_영어/"]
        OUT2["📁 [상품명]_일본어/"]
        OUT3["📁 [상품명]_중국어_간체/"]
        OUT4["📁 [상품명]_중국어_번체/"]
        
        OUT --> OUT1 & OUT2 & OUT3 & OUT4
    end

    IN --> AGENT & P_MAIN & BAT_SUB
    PROMPT -->|EN 모드| EN
    PROMPT -->|JP 모드| JP
    PROMPT -->|CN 모드| CN
    PROMPT -->|TW 모드| TW
    PROMPT -->|ALL 모드| EN & JP & CN & TW

    EN & JP & CN & TW --> P1
    HTML & P2 --> OUT1 & OUT2 & OUT3 & OUT4
```

---

## 🚀 빠른 시작 가이드

### 💬 [방법 1: 최우선 권장] 안티그래비티 대화창 요청
- *"01_번역대상_원본에 이미지 넣었어, 영어로 번역해줘"*
- *"일본어 약기법 번역 시작해줘"*
- *"중국어 간체로 번역해줘"*
- *"전체 언어로 일괄 번역해줘"*

### 💻 [방법 2] 터미널에서 실행
```bash
# 상위 프로젝트 루트 기준
.venv\Scripts\python.exe multilingual_text_in_image_translation\multilingual_text_in_image_translation.py
```

### 🖱️ [방법 3: 차선책] 더블클릭 실행
- `다국어_통합번역_원클릭실행.bat` 더블클릭
