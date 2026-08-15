# 🇨🇳 중국어(간체/번체) 이미지 번역 엔진 개발 계획 및 아키텍처 정의서

> **엔진 명칭**: `CN_Text-In_Image_Translation_Engine_V1.py`  
> **기반 아키텍처**: Two-Pass Multimodal Neural Inpainting Architecture (Gemini 3.1 Pro + Flash-Image)  
> **지원 권역**: 중국 본토(간체자 `zh-CN`), 대만(번체자 `zh-TW`), 홍콩(번체자 `zh-HK`)  
> **표준 폰트**: 알리바바 푸후이체 (阿里巴巴普惠体 / Alibaba PuHuiTi 3.0)

---

## 📊 1. 엔진 작업 동작 흐름 플로우차트 (Workflow Diagram)

> 💡 **[아키텍처 주석]**: 본 플로우차트와 엔진(`CN_Text-In_Image_Translation_Engine_V1.py`)은 **프로토 베이직 엔진(`PROTO_Text-In_Image_Translation_Engine_V0.py`)의 Two-Pass 코어를 기반으로 중국어권(본토/대만/홍콩) 특화 번역엔진으로 개발**되었습니다.

```mermaid
flowchart TD
    %% [기초 엔진 주석]: 프로토엔진(PROTO_Engine_V0) 코어 기반 중국어권 특화 파생 모델
    Start(["🚀 원본 이미지 투입<br>(input_dir)"]) --> Auth["🔑 Google Cloud GenAI Client 인증<br>(Vertex AI global Serverless)"]
    Auth --> CheckRegion{"🌐 타겟 권역 확인<br>(Rule 8 적용)"}


    CheckRegion -- "권역 미지정 시" --> AskUser["❓ 사용자에게 타겟 질문<br>'중국 본토(간체) vs 대만/홍콩(번체)'"]
    AskUser --> Branch
    CheckRegion -- "권역 명시 시 (CN / TW / HK)" --> Branch["🎯 권역 분기 설정"]

    Branch --> ScanImages["🖼️ 대상 이미지 스캔 & Bounding Box 분석"]
    ScanImages --> Pass1["🧠 [Pass 1] Gemini 3.1 Pro<br>(고정밀 멀티모달 OCR & 번역 매핑)"]

    subgraph Pass1_Detail ["Pass 1 : 텍스트 추출 & 법률/용어 정제"]
        Pass1 --> P1_Prompt["프롬프트 주입:<br>• 중국 신광고법 8대 절대화 금지어 검열<br>• NMPA 화장품 효능 표기 가이드 준수<br>• 패키지 영문/로고 보존 지침"]
        P1_Prompt --> P1_Gen["JSON 매핑 데이터 생성<br>{kor, chn, violation_reason, footnote}"]
        P1_Gen --> P1_Regex["🛡️ 파이썬 정규식 하드 필터<br>(最, 第一, 顶级, 治疗, 永久 강제 치환)"]
    end

    P1_Regex --> Pass2["🎨 [Pass 2] Gemini 3.1 Flash-Image<br>(시각적 로컬라이제이션 & 인페인팅 렌더링)"]

    subgraph Pass2_Detail ["Pass 2 : 이미지 인페인팅 & 식자"]
        Pass2 --> P2_Erase["1. 원본 한국어 텍스트 완전 제거 (Full Inpainting)"]
        P2_Erase --> P2_Font["2. 알리바바 푸후이체(Alibaba-PuHuiTi) 벡터 식자"]
        P2_Font --> P2_Package["3. 본품 패키지 영문/로고 100% 무손실 보존"]
    end

    Pass2_Detail --> PostProc["📐 후처리: Pillow LANCZOS<br>(원본 가로/세로 해상도 1:1 보존 복원)"]
    
    PostProc --> TableCheck{"📋 고시정보 표(Notice Table) 여부"}
    TableCheck -- "일반 상세페이지 이미지" --> SaveImg["💾 최종 번역 이미지 PNG 저장"]
    TableCheck -- "고시정보 표 이미지" --> TableRenderer["🖥️ 860px 고시표 Headless Edge 렌더러<br>(Alibaba-PuHuiTi, 타이틀 64px, 본문 32px,<br>max 2580px 이하, 초과 시 2페이지 자동 분할)"]
    TableRenderer --> SaveImg

    SaveImg --> Report["📄 중국 광고법 준수 및 번역 비교표 TXT 리포트 생성"]
    Report --> GitSync["🔄 GitHub PANDORA 저장소 실시간 자동 커밋 & 푸시"]
    GitSync --> Finish(["🎉 변환 완료"])

    classDef passClass fill:#e3f2fd,stroke:#1565c0,stroke-width:2px;
    classDef checkClass fill:#fff3e0,stroke:#e65100,stroke-width:2px;
    classDef finishClass fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px;
    class Pass1,Pass2 passClass;
    class CheckRegion,TableCheck checkClass;
    class Finish finishClass;
```

---

## 🛠️ 2. 단계별 적용 기술 스택 (Tech Stack Summary)

| 단계 | 역할 및 목적 | 적용 기술 스택 | 세부 설명 |
| :--- | :--- | :--- | :--- |
| **1. AI Model** | OCR & 텍스트 검열 | **`gemini-3.1-pro-preview`** | 이미지 속 한글 100% 인식 및 중국 신광고법/NMPA 규제 준수 JSON 매핑 생성 |
| **2. Inpainting** | 이미지 인페인팅 식자 | **`gemini-3.1-flash-image`** | 한글 제거 후 알리바바 푸후이체로 자연스러운 무결점 인페인팅 렌더링 |
| **3. Font Engine**| 표준 타이포그래피 | **`Alibaba-PuHuiTi` (5 Weights)** | 알리바바 공식 푸후이체 3.0 (Regular, Medium, Bold, Heavy, Light) 식자 |
| **4. Legal Filter**| 광고법 자동 정제 | **`Python Regex + OpenCC`** | 중국 신광고법 절대화 금지어(`最`, `第一`, `顶级` 등) 원천 차단 및 간/번체 정규화 |
| **5. Post-Proc** | 해상도/비율 보존 | **`Pillow (PIL - LANCZOS)`** | 원본 종횡비(Aspect Ratio) 및 가로/세로 픽셀 1:1 강제 일치 복원 |
| **6. Notice Spec** | 고시정보 표 렌더링 | **`Headless Edge + Alibaba-PuHuiTi`**| 가로 `860px` 고정, 세로 `Auto-Fit` (최대 2,580px 이하, 초과 시 2페이지 분할), 타이틀 64px, 본문 32px |
| **7. DevOps** | 형상 관리 | **`Git / GitHub (PANDORA)`** | 코드 및 결과 문서 변경 시 원격 저장소(`main` 브랜치) 실시간 자동 커밋/푸시 |

---

## 💡 3. 중국어 엔진 핵심 5대 개발 특징

1. **중국 신(新) 광고법 100% 원천 차단 (Ad-Law Compliance Engine)**:
   - 중국 시장에서 벌금 및 상품 삭제 위험이 있는 8대 절대화 표현(`最`, `第一`, `顶级`, `极品`, `永久`, `彻底`, `万能`, `根除`)을 프롬프트와 파이썬 정규식 필터 이중 안전망으로 완벽 차단 및 순화(`卓越`, `优异`, `精心` 등으로 대체).

2. **3대 권역 지능형 분기 (Tri-Region Targeting)**:
   - `CN`: 중국 본토 타오바오/티몰/샤오홍슈/더우인 최적화 간체자(`zh-CN`)
   - `TW`: 대만 쇼피(Shopee TW)/momo 최적화 번체자(`zh-TW`)
   - `HK`: 홍콩 HKTVmall/Watsons HK 최적화 번체자(`zh-HK`)

3. **알리바바 푸후이체 공식 폰트 파이프라인 (Alibaba PuHuiTi 3.0)**:
   - 중화권 이커머스 표준 서체인 알리바바 푸후이체 5종 웨이트를 완벽 연동하여 벡터 텍스트의 선명도와 가독성을 보장.

4. **완전 재생성 원칙 (Full Regeneration Rule)**:
   - 부분 덧칠(Patching)을 금지하고 캔버스 전체를 완전히 새롭게 렌더링하여 1픽셀의 이질감도 없는 최상의 퀄리티 유지.

5. **상품 패키지 포장 원본 보존 (Package Logo Protection)**:
   - 화장품 용기, 튜브, 패키지 상자에 인쇄된 원본 로고와 영문 텍스트는 인페인팅 대상에서 완벽히 제외하여 제품 고유 형태 보존.
