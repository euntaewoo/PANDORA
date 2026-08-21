# multilingual_text_in_image_translation 워크플로우 차트 다이어그램

본 문서는 **`multilingual_text_in_image_translation`** 엔진의 전체 아키텍처 및 5단계 하이브리드 처리 흐름을 도식화한 공식 다이어그램 문서입니다.

---

## 📊 1. 시스템 워크플로우 아키텍처 다이어그램

```mermaid
flowchart TD
    subgraph S1["1. 단일 공통 인풋 (Input Stage)"]
        IN["📂 01_번역대상_원본<br/>(한국어 원본 상품별 폴더 또는 이미지 일괄 수납)"]
    end

    subgraph S2["2. 실행 진입점 (Execution Trigger)"]
        AGENT["🤖 [최우선] 안티그래비티 채팅창 대화 요청<br/>(예: '영어 번역해줘', '일본어 번역 시작해')"]
        P_MAIN["🥇 [터미널 직접 실행]<br/>multilingual_text_in_image_translation.py"]
        BAT_SUB["🥈 [보조 차선책]<br/>다국어_통합번역_원클릭실행.bat"]
        
        AGENT -->|에이전트가 자동 실행| P_MAIN
        P_MAIN --> PROMPT{"도착 언어 자동 분기 / 선택<br/>(EN / JP / CN / TW / ALL)"}
        BAT_SUB -.->|대화형 콘솔 질의응답| PROMPT
    end

    subgraph S3["3. 국가별 규정 및 톤앤매너 자동 분기 (Policy & Font Pack)"]
        EN["🇺🇸 영어 (EN)<br/>• Amazon/Shopee US 마케팅 초월번역<br/>• Montserrat 단일 서체 강제"]
        JP["🇯🇵 일본어 (JP)<br/>• 후생노동성 56종 약기법 포지티브 리스트 필터링<br/>• Noto Sans JP 서체"]
        CN["🇨🇳 중국어 간체 (CN)<br/>• 중국 신광고법 8대 절대화 금지어 순화<br/>• Noto Sans SC (思源黑体) 서체"]
        TW["🇹🇼 중국어 번체 (TW)<br/>• 대만/홍콩 TFDA 화장품 규정 준수<br/>• Noto Sans TC 서체"]
    end

    subgraph S4["4. 하이브리드 투패스 렌더링 엔진 (Two-Pass Neural Engine)"]
        P1["🔍 Pass 1: gemini-3.1-pro-preview<br/>(텍스트 전수 스캔, 번역, 법률 필터링, 표/DOCX 감지)"]
        DECIDE{"입력 속성 자동 판별"}
        
        HTML["📊 고시정보표 (테이블/DOCX)<br/>Headless HTML 표준 렌더러<br/>(860px 고정, 100% 벡터 선명도)"]
        P2["🎨 일반 상세페이지 (인페인팅)<br/>Pass 2: gemini-3.1-flash-image<br/>(지수 백오프 자동 복구, 1:1 종횡비 잠금)"]
        
        P1 --> DECIDE
        DECIDE -->|고시표 / 성분표 / DOCX 감지| HTML
        DECIDE -->|일반 디자인 이미지| P2
    end

    subgraph S5["5. 상품별·언어별 자동 서브폴더 분류 저장 (Output Stage)"]
        OUT["📂 02_번역결과_최종/"]
        OUT1["📁 [상품명]_영어/"]
        OUT2["📁 [상품명]_일본어/"]
        OUT3["📁 [상품명]_중국어_간체/"]
        OUT4["📁 [상품명]_중국어_번체/"]
        
        OUT --> OUT1 & OUT2 & OUT3 & OUT4
    end

    subgraph S6["6. 웹검색 최적화 메타데이터 생성 (SEO / GEO / AEO)"]
        TXT["📝 [상품명]_[언어]_SEO_GEO_AEO.txt<br/>• SEO 상품명 (공백 포함 100자 이내 엄격)<br/>• GEO (생성형 AI 모델 인용 최적화 브랜드/엔티티 서사)<br/>• AEO (AI Overviews/음성검색 5대 핵심 FAQ)"]
        OUT1 & OUT2 & OUT3 & OUT4 --> TXT
    end

    IN --> AGENT & P_MAIN & BAT_SUB
    PROMPT -->|1. EN 선택| EN
    PROMPT -->|2. JP 선택| JP
    PROMPT -->|3. CN 선택| CN
    PROMPT -->|4. TW 선택| TW
    PROMPT -->|5. ALL 선택| EN & JP & CN & TW

    EN & JP & CN & TW --> P1
    HTML & P2 --> OUT1 & OUT2 & OUT3 & OUT4
```

---

## 📌 2. 6단계 핵심 파이프라인 명세표

| 단계 | 단계명 | 적용 기술 및 수행 작업 | 주요 산출물 / 특징 |
| :--- | :--- | :--- | :--- |
| **1단계** | **단일 공통 인풋** | 상위 `01_번역대상_원본/` 폴더에 상품별 폴더 또는 파일 배치 | 언어별 폴더 복사 불필요 |
| **2단계** | **실행 진입점** | 안티그래비티 대화창 요청, Python CLI, BAT 런처 | 도착어 파라미터(`--lang`) 전달 |
| **3단계** | **규정/폰트 분기** | 국가별 광고법, 약기법(56종), 초월번역 지침 주입 | Noto Sans JP/SC/TC, Montserrat |
| **4단계** | **투패스 렌더링** | `Pass 1` (Pro 추론/OCR/표감지) ➔ `Pass 2` (Flash 인페인팅 / HTML 렌더러) | 1:1 비율 보존, 표 벡터 선명도 |
| **5단계** | **자동 분류 저장** | `02_번역결과_최종/[상품명]_[번역국가언어]/` 폴더 자동 생성 | **상품별·언어별 파일 혼재 100% 차단** |
| **6단계** | **SEO/GEO/AEO 생성** | `gemini-3.1-pro-preview` 기반 현지어 웹검색 최적화 메타데이터 추출 | **100자 이내 상품명 + AI 인용 서사 + 5대 FAQ TXT** |
