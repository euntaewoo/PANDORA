# 🇨🇳 중국어(간체/번체) 이미지 번역 엔진 개발 계획 및 아키텍처 정의서

> **엔진 명칭**: `CN_Text-In_Image_Translation_Engine_AGY_SDK.py`  
> **기반 아키텍처**: Two-Pass Multimodal Neural Inpainting Architecture (Gemini 3.1 Pro + Flash-Image)  
> **지원 권역**: 중국 본토(간체자 `zh-CN`), 대만(번체자 `zh-TW`), 홍콩(번체자 `zh-HK`)  
> **표준 폰트**: Noto Sans SC (스위안헤이티 / 思源黑体 / Source Han Sans SC)

---


---

## ⚙️ 엔진 하이퍼파라미터 및 토큰 제원 (Hyperparameters & Token Limits)
- **4대 핵심 하이퍼파라미터 (GenerationConfig)**:
  - `temperature`: **0.6** (해외 광고법 준수 안전선 유지 및 럭셔리 초월번역 밸런스 확보)
  - `top_p`: **0.9** (하위 10% 투박한 직역 표현 배제 및 정제된 백화점 뷰티 어휘 필터링)
- **토큰 한도 이원화 (Token Limit Dualization)**:
  - **대용량 데이터 추출 및 고시표 번역 (Pass 1 & Table Render)**: `max_output_tokens=8192` (전성분 등 방대한 화학 명칭 및 JSON 구조 유실 방지)
  - **마케팅 카피 및 SEO 생성 (SEO/GEO/AEO)**: `max_output_tokens=4096` (불필요한 장황한 설명 차단 및 API 비용 최적화)

> 💡 **[Temperature 0.6 공학적·수학적 배경 및 실측 제원 주석]**
> - **수학적 작동 원리 (Softmax 연산식)**: $P(w_i) = \frac{\exp(z_i / T)}{\sum_j \exp(z_j / T)}$
>   - $T$ (Temperature)는 다음 단어를 샘플링할 때 확률 분포의 평탄화(Flatness) 정도를 제어하는 조절 매개변수임.
> - **실측 동작 특성 비교**:
>   - `T = 0.5`: 상위 1~2개 고확률 단어에 선택이 집중되어 결정론적/보수적 연산 수행 (문장이 딱딱한 기계 직역으로 고착됨).
>   - `T = 0.7`: 하위 확률 단어의 채택 가능성이 높아져 무작위성 및 창의성은 증가하나, 원문에 없는 과장/절대화 금지어 환각 및 광고법 위반 리스크 급증.
>   - `T = 0.6`: 해외 화장품 광고법(미국 MoCRA, 대만 TFDA, 일본 약기법, 중국 NMPA) 위반 리스크 차단과 백화점·세포라급 럭셔리 초월번역(Transcreation) 감성 품질 간의 **최적 균형점(황금 비율)**.


---

## 📊 1. 엔진 작업 동작 흐름 플로우차트 (Workflow Diagram)

> 💡 **[아키텍처 주석]**: 본 플로우차트와 엔진(`CN_Text-In_Image_Translation_Engine_AGY_SDK.py`)은 **프로토 베이직 엔진(`PROTO_Text-In_Image_Translation_Engine_AGY_SDK.py`)의 Two-Pass 코어를 기반으로 중국어권(본토/대만/홍콩) 특화 번역엔진으로 개발**되었습니다.

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
        P2_Erase --> P2_Font["2. Noto Sans SC(스위안헤이티 / 思源黑体) 벡터 식자"]
        P2_Font --> P2_Package["3. 본품 패키지 영문/로고 100% 무손실 보존"]
    end

    Pass2_Detail --> PostProc["📐 후처리: Pillow LANCZOS<br>(원본 가로/세로 해상도 1:1 보존 복원)"]
    
    PostProc --> TableCheck{"📋 고시정보 표(Notice Table) 여부"}
    TableCheck -- "일반 상세페이지 이미지" --> SaveImg["💾 최종 번역 이미지 PNG 저장"]
    TableCheck -- "고시정보 표 이미지" --> TableRenderer["🖥️ 860px 고시표 Headless Edge 렌더러<br>(Noto Sans SC, 타이틀 52px, 본문 26px, 1열 275px 기준,<br>복합항목 의미단위 개행, max 2580px 이하 1장 수납)"]
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
| **3. Font Engine**| 표준 타이포그래피 | **`NotoSansSC`** | Noto Sans SC (Regular, Medium, Bold) 식자 |
| **4. Legal Filter**| 광고법 자동 정제 | **`Python Regex + OpenCC`** | 중국 신광고법 절대화 금지어(`最`, `第一`, `顶级` 등) 원천 차단 및 간/번체 정규화 |
| **5. Post-Proc** | 해상도/비율 보존 | **`Pillow (PIL - LANCZOS)`** | 원본 종횡비(Aspect Ratio) 및 가로/세로 픽셀 1:1 강제 일치 복원 |
| **6. Notice Spec** | 고시정보 표 렌더링 | **`Headless Edge + Noto Sans SC/TC`**| 가로 `전체 860px (컨테이너 820px)` 고정, 세로 `Auto-Fit` (최대 2,580px 이하, 초과 시 1차 행간 유동 압축(Squeeze), 실패 시 2페이지 분할)<br> - 폰트 규격: 글자가 뚱뚱해지는 한자(방괴자) 특성 고려 타 언어 대비 축소 적용 (타이틀 **52px**, 본문 **26px**, 1열 폭 **중화권(간체/번체) 270px**, 좌우 여백 **30px**)<br> - 1열 라벨 규격: `width: 270px; padding: 20px 15px; word-break: break-word; overflow-wrap: break-word; text-align: left; vertical-align: middle;`<br> - 2열 본문 규격: `word-break: break-word; overflow-wrap: break-word;` (긴 화학물질 텍스트 오버플로우 방지 및 지능형 줄바꿈, 순수 본문 폭 520px 확보)<br> - 지능형 줄바꿈: 10자 미만 단문 1줄 강제 유지, 10자 이상 복합어 기준 `<br>` 자동 분할<br> - **[2열 심사 효능 줄바꿈]**: 특수용도/기능성 심사 2열 본문에서 기관 심사 결과 뒤의 괄호 효능 설명(`(美白...)`, `(미백...)`) 앞 100% 강제 개행(`<br>`) 주입<br> - **[핵심] 중화권 번역 표준 명칭 (NMPA / TFDA 매핑)**:<br>   > **간체(CN)**: 용량(`净含量`), 피부타입(`适用肤质`), 기한(`使用期限`), 사용법(`使用方法`), 성분(`全成分`)<br>   > **번체(TW)**: 용량(`淨含量`), 피부타입(`適用膚質`), 기한(`保存期限`), 사용법(`使用方法`), 성분(`全成分`) |
| **7. DevOps** | 형상 관리 | **`Git / GitHub (PANDORA)`** | 코드 및 결과 문서 변경 시 원격 저장소(`main` 브랜치) 실시간 자동 커밋/푸시 |
| **8. SEO/AEO** | 검색 최적화 자동 생성 | **`Dynamic {product_name} Prompting`** | 타겟 폴더의 상품명(`{product_name}`)을 실시간 동적 감지 및 매핑하여, 특정 제품(예: 아쿠아타이드)에 고정되지 않은 100% 맞춤형 사용법 및 5대 핵심 FAQ 자동 생성 |

---

## 💡 3. 중국어 엔진 핵심 5대 개발 특징

1. **중국 신(新) 광고법 100% 원천 차단 (Ad-Law Compliance Engine)**:
   - 중국 시장에서 벌금 및 상품 삭제 위험이 있는 8대 절대화 표현(`最`, `第一`, `顶级`, `极品`, `永久`, `彻底`, `万能`, `根除`)을 프롬프트와 파이썬 정규식 필터 이중 안전망으로 완벽 차단 및 순화(`卓越`, `优异`, `精心` 등으로 대체).

2. **3대 권역 지능형 분기 (Tri-Region Targeting)**:
   - `CN`: 중국 본토 타오바오/티몰/샤오홍슈/더우인 최적화 간체자(`zh-CN`)
   - `TW`: 대만 쇼피(Shopee TW)/momo 최적화 번체자(`zh-TW`)
   - `HK`: 홍콩 HKTVmall/Watsons HK 최적화 번체자(`zh-HK`)

3. **구글 공식 Noto Sans SC 폰트 파이프라인 (Google Noto Sans SC)**:
   - 중화권 이커머스 표준 서체인 알리바바 푸후이체 5종 웨이트를 완벽 연동하여 벡터 텍스트의 선명도와 가독성을 보장.

4. **완전 재생성 원칙 (Full Regeneration Rule)**:
   - 부분 덧칠(Patching)을 금지하고 캔버스 전체를 완전히 새롭게 렌더링하여 1픽셀의 이질감도 없는 최상의 퀄리티 유지.

5. **상품 패키지 포장 원본 보존 (Package Logo Protection)**:
   - 화장품 용기, 튜브, 패키지 상자에 인쇄된 원본 로고와 영문 텍스트는 인페인팅 대상에서 완벽히 제외하여 제품 고유 형태 보존.

6. **대만/홍콩 번체자 간체 획수 유출(Drift) 방지 및 번체 글리프 잠금 (Absolute Traditional Glyph Lock)**:
   - AI 인페인팅 모델의 간체자 쏠림을 원천 차단하기 위해, Pass 2 프롬프트에 `養(O) vs 养(X)`, `對(O) vs 对(X)`, `護(O) vs 护(X)` 등 획수 단위 네거티브 제약(Negative Glyph Constraint)을 주입하여 외부 비전 OCR에서도 100% 정체자로 판정되는 무결점 번체자 출력 보장.

7. **글로벌 럭셔리 뷰티 초월번역 및 규제 준수 표준 규격 (Global Luxury Beauty Transcreation & Compliance Automator)**:
   - **페르소나**: 에스티로더, 랑콤, 시슬리, SK-II 등 하이엔드 럭셔리 코스메틱 10년 차 수석 CD 및 엘리트 카피라이터 페르소나 적용.
   - **직역 부사 금지**: `确实/確實`, `真正`, `非常`, `绝对/絕對` 등 딱딱한 기계적 직역 부사 전면 금지 ➔ 럭셔리 뷰티 전문 어휘로 세련되게 재창조.
   - **성분 구문 결속**: "10% LiftDerm" 등 활성 성분 수치가 문맥과 단절되지 않고 제품 효능 서사로 매끄럽게 연결되도록 문장 구조화.
   - **4대 바이오 뷰티 전문 어휘 사전**:
     * 피부 속/기저층: [ZH-CN] `肌底深处` / [ZH-TW] `肌底`
     * 토탈 케어/멀티 코렉티브: [ZH-CN] `多效修护` / [ZH-TW] `多效修護`
     * 탄력 복원/강화: [ZH-CN] `赋活肌底弹力` / [ZH-TW] `賦活肌底彈力`
     * 눈가 잔주름/건조주름: [ZH-CN] `细纹・干纹` / [ZH-TW] `細紋・乾紋`
   - **절대적/과대 표현 전면 금지 (Ban on Absolute Claims)**: `全球首创/全球首創`, `第一`, `最佳`, `终极对策/終極對策` 등 검증 불가능한 절대 표현 전면 금지 ➔ `创新科技/創新科技`, `高端多效/頂級多效`, `精准修护/精準修護` 등 프리미엄 혁신 표현으로 순화.
   - **의료 시술 오인 금지 및 4대 안전 동사 (Compliance-Safe Verbs)**: 보톡스/필러 등 의료 시술 연상 및 '주름 박멸' 과장 표현 전면 배제 ➔ 반드시 **`抚平/撫平` (Smooth)**, **`淡化` (Diminish)**, **`舒缓/舒緩` (Alleviate)**, **`修护/修護` (Care/Repair)** 4대 컴플라이언스 안전 동사 사용.

8. **지능형 문맥 의미 단위 고시표 렌더링 및 1열 300px 황금비율 표준 (Semantic Notice Table Standard)**:
   - **1열 표준 너비**: `width: 300px`, `padding: 20px 15px` (좌우 여백 총 30px, 순수 글자 영역 270px).
   - **외톨이 글자(Orphan) 원천 방지**: `特殊用途化妆品<br>审查状态`, `化妆品生产企业 /<br>责任销售商` 등 10글자 이상 긴 복합 법정 라벨에 대해 의미 단위 2줄 황금 분할 개행을 파이썬 렌더러에서 자동 주입.
   - **글자 침범 방지**: `word-break: break-word; overflow-wrap: break-word;` 및 `text-align: left; vertical-align: middle;` 영구 적용.

---

## 🌐 4. 중화권 및 동남아 권역별 중국어 표기 및 이커머스 최적화 기준

| 권역 구분 | 해당 국가/지역 | 공식 표기 문자 | 번역 타겟 엔진 모드 | 이커머스 / 비즈니스 최적화 가이드 |
| :--- | :--- | :--- | :--- | :--- |
| **중국 본토** | 중국 (Mainland China) | 🟥 **간체자 (Simplified)** | `--target=CN` (`zh-CN`) | 표준어(푸통화) 어휘 기준, 글로벌 표준 간체의 핵심, 중국 신광고법 8대 금지어 필터링 필수 |
| **정통 번체권** | 대만 (Taiwan) | 🟦 **번체자 (Traditional)** | `--target=TW` (`zh-TW`) | 독자적인 대만식 뷰티 어휘 발달, 간체자 노출 시 거부감 매우 큼, 단순 간➡️번 변환 금지(SEO 파괴 방지) |
| **특별행정구** | 홍콩 (Hong Kong), 마카오 | ⭐️ **번체자 (Traditional)** | `--target=HK` (`zh-HK`) | 구어는 광동어 기반 어휘, 영어 병기 시 신뢰도 급상승, 브랜드명/스펙 영어 원문 노출 권장 |
| **동남아 주요국** | 싱가포르, 말레이시아 | 🟥 **간체자 (Simplified)** | `--target=CN` (`zh-CN/SG`) | 학교/미디어 간체자 사용, 본토식 정치용어/신조어 배제, 이커머스 주 언어는 영어(간체자는 보조) |
| **기타 동남아** | 태국, 베트남, 인도네시아 등 | 🚫 **중국어 불필요** | 현지어 / 영어 전용 | 화교 사회가 있으나 현지화됨, 국가별 현지어 또는 영어 상세페이지 필수 |



- 💡 **[2026-08 CSS 버그 픽스]**: 긴 단어에 의한 표 폭 팽창(이미지 우측 여백 발생 및 타이틀 좌측 쏠림 현상)을 방지하기 위해 공통적으로 `table-layout: fixed;` 속성을 강제 적용함.


---

## 🏆 초월번역(Transcreation) 품질 자동 평가 4대 루브릭 (100점 만점)
- **① 현지 카테고리 어휘 적합성 (30점)**: 콩글리시/직역투 배제, 현지 뷰티 플랫폼 네이티브 어휘 채택
- **② 국가별 광고법 무결성 (30점)**: 미국 MoCRA, 일본 약기법, 중국 NMPA/신광고법 위반 표현 100% 차단
- **③ 브랜드 감성 및 초월번역 완성도 (25점)**: 백화점·세포라급 하이엔드 뷰티 톤앤매너 및 구매 전환 설득력
- **④ 시각적 레이아웃 및 가독성 (15점)**: 텍스트 박스 침범 방지 및 간결한 문장 구조
- **[합격 기준 및 자가치유]**: **90점 이상 & 위반 0건 합격**, 미달 시 피드백 기반 **최대 2회 자동 재렌더링 및 `Transcreation_QA_Report.html` 발행**

