# 🚀 JP_Text-In_Image_Translation_Engine_V7 (단일 통합 메인 시스템)

본 문서는 일본 이커머스(Qoo10 Japan / Amazon Japan 등) 상세페이지 이미지 번역 및 인페인팅을 수행하는 **V7 단일 통합 메인 엔진(`JP_Text-In_Image_Translation_Engine_AGY_SDK.py`)의 표준 기술 명세서**입니다.

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

## 🌟 V7 핵심 운영 원칙 (Strict Rules)

1. **단일 메인 엔진 원칙 (Single Core Engine Lock)**
   - 일본어 번역 및 렌더링 파이프라인은 오직 `JP_Text-In_Image_Translation_Engine_AGY_SDK.py` 단일 메인 엔진으로 100% 완결되며, 임시 덧칠용 파편화 스크립트 사용을 전면 배제합니다.
2. **일본 후생노동성 약기법 56종 강제 준수 (PMDA Compliance)**
   - AI의 환각(Hallucination)을 원천 차단하기 위해, 프롬프트 지시뿐만 아니라 파이썬 정규식 필터(`forbidden_patterns`)를 엔진 코어에 탑재하여 위반 단어(배출, 디톡스, 재생, 무자극, 주름개선 등)를 100% 강제 차단 및 안전 표현(`肌を整える`, `ハリを与える` 등)으로 자동 치환합니다.
3. **부분 덧칠 금지 및 완전 재생성 (Full Regeneration Rule)**
   - 텍스트 수정 발생 시 국소 덧칠(Patching)을 금지하고, 첨부된 원본 이미지를 기반으로 캔버스 전체를 완전히 새롭게 렌더링(Full Inpainting)하여 1픽셀의 이질감도 없는 무결점 퀄리티를 유지합니다.
4. **원본 종횡비 및 해상도 1:1 보존 (Aspect Ratio Lock)**
   - Pillow의 `LANCZOS` 리샘플링 알고리즘을 통해 원본 이미지의 가로/세로 해상도 및 종횡비를 100% 강제 일치시킵니다.
5. **글로벌 럭셔리 뷰티 초월번역 (Luxury Beauty Transcreation)**
   - 일본 프레스티지 뷰티(@cosme, 시슬리, SK-II 톤앤매너) 전문 카피라이터 페르소나를 적용하여 직역 부사(`確実に`, `本当に` 등)를 배제하고 고급 뷰티 어휘(`肌の奥`, `高機能トータルリペア`, `ハリを呼び覚ます`)를 사용합니다.

---

## 🏗️ Two-Pass 아키텍처 흐름

```text
[원본 입력 이미지]
      │
      ▼
[Pass 1: Gemini 3.1 Pro Preview] (max_output_tokens=8192, temp=0.6, top_p=0.9)
      ├─ 고정밀 멀티모달 OCR 스캔
      ├─ 일본 후생노동성 약기법 56종 허용 표현 대조 및 검열
      └─ 파이썬 정규식 하드 필터링 (최후의 보루 안전망)
      │
      ▼
[Pass 2: Gemini 3.1 Flash-Image] (IMAGE modality, temp=0.6, top_p=0.9)
      ├─ 원본 한국어 텍스트 완전 제거 (Seamless Erasing)
      ├─ 일본어 Noto Sans JP 표준 서체 재식자
      └─ 본품 패키지/용기 영문 로고 100% 무손실 보존
      │
      ▼
[후처리: Pillow LANCZOS] ➔ 원본 해상도 1:1 복원 및 최종 이미지 저장
      │
      ▼
[SEO/AEO 자동 생성: Gemini 3.1 Pro]
      └─ 타겟 폴더의 상품명(`{product_name}`)을 실시간 동적 매핑하여, 특정 제품에 고정되지 않은 100% 맞춤형 Qoo10/Amazon 검색 최적화 문서 5대 FAQ 자동 생성
```

---

## 📋 상품 정보 고시 표(Notice Table) 표준 규격
- **캔버스 규격**: 가로 **전체 `860px` 고정 (컨테이너 820px)**, 세로 **`Auto-Fit` (최대 허용치 `2,580px` 이하, 초과 시 2페이지 자동 분할)**
- **표준 폰트**: **`Noto Sans JP`** (Bold 700 / Regular 400)
- **타이포그래피**: 타이틀 `64px` (Bold), 항목 라벨 `32px` (Bold), 본문 `32px` (Regular)
- **공통 렌더러**: `00_공통자료/render_notice_table_standard.py`

---

## 🏆 초월번역(Transcreation) 품질 자동 평가 4대 루브릭 (100점 만점)
- **① 현지 카테고리 어휘 적합성 (30점)**: 콩글리시/직역투 배제, 현지 뷰티 플랫폼 네이티브 어휘 채택
- **② 국가별 광고법 무결성 (30점)**: 미국 MoCRA, 일본 약기법, 중국 NMPA/신광고법 위반 표현 100% 차단
- **③ 브랜드 감성 및 초월번역 완성도 (25점)**: 백화점·세포라급 하이엔드 뷰티 톤앤매너 및 구매 전환 설득력
- **④ 시각적 레이아웃 및 가독성 (15점)**: 텍스트 박스 침범 방지 및 간결한 문장 구조
- **[합격 기준 및 자가치유]**: **90점 이상 & 위반 0건 합격**, 미달 시 피드백 기반 **최대 2회 자동 재렌더링 및 `Transcreation_QA_Report.html` 발행**


## 4. 고시정보표 표준 규격 (MFDS 식약처 심사필)
- 기능성화장품 심사: `韓国化粧品法に基づき韓国食品医薬品安全処(MFDS)の機能性化粧品審査(または報告)済`
- 공정위 품질보증기준 및 +82 고객상담실 표준화 적용.


## ⚖️ 글로벌 컴플라이언스(법무) & 럭셔리 초월번역 시스템 연동 명세
- **System Instruction**: `GLOBAL_COMPLIANCE_SYSTEM_INSTRUCTION` (다국어 법무 감사관 + 럭셔리 마케터 페르소나 및 원천 법리 영구 장착)
- **표준 렉시콘 DB**: `00_공통자료/compliance_lexicons/*.json` 실시간 동적 바인딩
- **하이퍼파라미터 전역 고정**: `temperature: 0.6`, `top_p: 0.9`, `max_output_tokens: 8192`
- **안전망**: Python 정규식(`apply_deterministic_qa_overrides`) 100% 강제 치환 게이트 연동
