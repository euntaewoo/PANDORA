# 🚀 PROTO_Text-In_Image_Translation_Engine_AGY_SDK (Two-Pass Core Architecture)

본 문서는 다국어 이미지 번역 시스템의 기초 토대가 되는 **프로토 비동기 베이직 엔진(AGY_SDK)**의 기술 명세서입니다.

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

## 🏗️ 2-Pass 아키텍처 흐름
1. **Pass 1 (Text & Multimodal)**: `gemini-3.1-pro-preview` (OCR 스캔, 규제 검열, 초월번역 JSON 매핑)
2. **Pass 2 (Image Generation)**: `gemini-3.1-flash-image` (한글 완전 삭제 및 시각적 인페인팅 렌더링)
3. **후처리 (Post-Processing)**: Pillow `LANCZOS` 알고리즘을 통한 원본 해상도 1:1 종횡비 보존 복원


---

## 🏆 초월번역(Transcreation) 품질 자동 평가 4대 루브릭 (100점 만점)
- **① 현지 카테고리 어휘 적합성 (30점)**: 콩글리시/직역투 배제, 현지 뷰티 플랫폼 네이티브 어휘 채택
- **② 국가별 광고법 무결성 (30점)**: 미국 MoCRA, 일본 약기법, 중국 NMPA/신광고법 위반 표현 100% 차단
- **③ 브랜드 감성 및 초월번역 완성도 (25점)**: 백화점·세포라급 하이엔드 뷰티 톤앤매너 및 구매 전환 설득력
- **④ 시각적 레이아웃 및 가독성 (15점)**: 텍스트 박스 침범 방지 및 간결한 문장 구조
- **[합격 기준 및 자가치유]**: **90점 이상 & 위반 0건 합격**, 미달 시 피드백 기반 **최대 2회 자동 재렌더링 및 `Transcreation_QA_Report.html` 발행**


## ⚡ 비동기 API 통신 규격
- wait client.aio.models.generate_content() 비동기 I/O 표준 100% 적용


## 📋 고시정보표 4대 법률 표준화 (MFDS 식약처 관할기관 명시)
- 기능성 심사필: `韓国化粧品法に基づき韓国食品医薬品安全処(MFDS)の機能性化粧品審査(または報告)済`
- 주의사항 3대 조항, 공정위 품질보증기준, 고객상담실(+82) 전역 표준 규격 적용.


## ⚖️ 글로벌 컴플라이언스(법무) & 럭셔리 초월번역 시스템 연동 명세
- **System Instruction**: `GLOBAL_COMPLIANCE_SYSTEM_INSTRUCTION` (다국어 법무 감사관 + 럭셔리 마케터 페르소나 및 원천 법리 영구 장착)
- **표준 렉시콘 DB**: `00_공통자료/compliance_lexicons/*.json` 실시간 동적 바인딩
- **하이퍼파라미터 전역 고정**: `temperature: 0.6`, `top_p: 0.9`, `max_output_tokens: 8192`
- **안전망**: Python 정규식(`apply_deterministic_qa_overrides`) 100% 강제 치환 게이트 연동


## 4-Core 검색 최적화(SEO/GEO/AEO) 및 하이브리드 인제스천 표준
- **4-Core 표준 구조**: 1. 공식 상품명 (100자 NPO) ➔ 2. 5줄 마이크로 요약 ➔ 3. 제품 상세 비교 스펙 테이블(HTML Table) ➔ 4. 5대 핵심 FAQ
- **하이브리드 듀얼 인제스천**: `url.txt` 웹 실시간 텍스트 스크래핑 및 미출시 신제품 4중 이미지 팩트 앵커링 지원
- **트리플 익스포트**: `.docx` (MS Word), `.html` (원클릭 복사 뷰어), `.txt` (가독성 개행), `.md` 4종 파일 일괄 동시 생성
- **Zero Meta Commentary**: 내부 개발/최적화 용어 일체 배제한 100% 고객 대면용 카피

## [PRE-EXPORT-INTEGRITY-VERIFICATION-LOCK] 결과물 내보내기 전 사전 무결성 검증 및 리포트 선-출력 강제
1. **[HARD STOP] 결과물 파일 내보내기 전 무조건 사전 검증 실행**:
   - 결과물 파일(.png, .html, .docx, .txt, .md 등)을 생성·저장·보고하기 전, 데이터 무결성과 포맷 규격을 체크하는 검증 함수(`pre_export_integrity_check`) 및 린터를 무조건 실행해야 합니다.
2. **[REPORT-FIRST] 데이터 무결성 요약 리포트 선-출력 의무화**:
   - 에이전트는 최종 결과물이나 파일 링크를 사용자에게 제시하기 전, 반드시 응답 상단에 `### 📋 [DATA-INTEGRITY-SUMMARY-REPORT]` 요약 리포트 표(포맷 무결성, 콩글리시/금지어 0건 여부, 수치 일치성, 4종 파일 생성 여부)를 먼저 출력하여 검증 결과를 입증해야 합니다. 이 리포트 출력이 누락된 답변은 즉시 무효로 간주합니다.

## [GLOBAL-COMPLIANCE-STANDARDS] 영미권/글로벌 뷰티 표준 용어 및 콩글리시 배제 규격
1. **무자극/저자극 공인 표준 표기**: 한국 인체적용시험 성적서의 '피부자극지수 0.00' 직역투를 엄격히 금지하고 반드시 `Hypoallergenic & Dermatologist-tested for sensitive skin` 또는 `Dermatologist-tested & clinically proven hypoallergenic`으로 표기합니다.
2. **피부톤 케어 표준 표기**: 'Tone Care / Dark Spot & Tone Care' 등 콩글리시 단순 단어 조합을 배제하고 `Dark Spot & Discoloration Defense` 또는 `Evening Skin Tone & Discoloration Care` 표준 명칭을 강제합니다.
---

## [PREVENT-SEMANTIC-DRIFT] 지시사항 누락 방지 및 출력 생성제어 4대 안전장치

1. **[LAZY-CODING-HARD-BAN]**: `// ... 기존 코드와 동일 ...`, `TODO:`, `...` 등 일체의 축약/생략 표현 전면 금지.
2. **[PRE-EXECUTION-CHECKLIST]**: 복합 요구사항 처리 시 지시사항 이행 매트릭스(표) 선행 검증 강제.
3. **[DIFF-FORMAT-STANDARD]**: 긴 코드/데이터 수정 시 불필요한 전체 재출력을 방지하여 토큰 버짓 보호.
4. **[THINKING-BUDGET-CONTROL]**: 추론(Thinking) 토큰의 본문 잠식을 차단하는 파라미터 규격화 (`max_output_tokens=8192`, 최신 `gemini-3.1-*` 플래그십 유지).
