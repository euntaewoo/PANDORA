# 🇨🇳 중국어 이미지 번역 엔진 CLI 명령어 가이드 (CLI Usage Guide)

> **엔진 파일**: `CN_Text-In_Image_Translation_Engine_AGY_SDK.py`  
> **엔진 위치**: `C:\Users\euntaewoo\Desktop\multilingual_text_in_image_translatio_agy_sdk\중국어\`  
> **기반 코어**: Two-Pass Multimodal Neural Inpainting Architecture (Gemini 3.1 Pro + Flash-Image)  
> **표준 폰트**: Noto Sans SC (스위안헤이티 / 思源黑体 / Source Han Sans SC)

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
>   - `T = 0.6`: 중화권 화장품 광고법(중국 본토 NMPA 신광고법 및 대만 TFDA 규정) 위반 리스크 차단과 티몰·샤오홍슈·모모급 럭셔리 초월번역(Transcreation) 감성 품질 간의 **최적 균형점(황금 비율)**.


---

## 📌 1. 기본 명령어 문법 (Syntax)

```bash
python C:\Users\euntaewoo\Desktop\multilingual_text_in_image_translatio_agy_sdk\중국어\CN_Text-In_Image_Translation_Engine_AGY_SDK.py [원본_이미지_폴더] [출력_폴더_옵션] --target={CN|TW|HK}
```

---

## 🎯 2. 타겟 권역별 실행 명령어

### 1) 🇨🇳 중국 본토 시장 (간체자, zh-CN) — 기본값
- **적용 규격**: 간체자 강제, 중국 신(新) 광고법 8대 절대화 표현(`最`, `第一`, `顶级` 등) 자동 순화, 타오바오/티몰/샤오홍슈 톤앤매너
```bash
python C:\Users\euntaewoo\Desktop\multilingual_text_in_image_translatio_agy_sdk\중국어\CN_Text-In_Image_Translation_Engine_AGY_SDK.py "C:\Users\euntaewoo\Desktop\multilingual_text_in_image_translatio_agy_sdk\01_번역대상_원본" --target=CN
```

### 2) 🇹🇼 대만 시장 (번체자, zh-TW)
- **적용 규격**: 대만 정체자(번체), 대만 TFDA 화장품법 준수, 대만 이커머스 어휘(`化妝水`, `鎖水`, `精華液`, `水光肌` 등)
```bash
python C:\Users\euntaewoo\Desktop\multilingual_text_in_image_translatio_agy_sdk\중국어\CN_Text-In_Image_Translation_Engine_AGY_SDK.py "C:\Users\euntaewoo\Desktop\multilingual_text_in_image_translatio_agy_sdk\01_번역대상_원본" --target=TW
```

### 3) 🇭🇰 홍콩 시장 (번체자, zh-HK)
- **적용 규격**: 홍콩 정체자(번체), 홍콩 이커머스 어휘(`爽膚水`, `補濕`, `精華素`, `HK$` 등), HKTVmall 톤앤매너
```bash
python C:\Users\euntaewoo\Desktop\multilingual_text_in_image_translatio_agy_sdk\중국어\CN_Text-In_Image_Translation_Engine_AGY_SDK.py "C:\Users\euntaewoo\Desktop\multilingual_text_in_image_translatio_agy_sdk\01_번역대상_원본" --target=HK
```

---

## 📂 3. 출력 폴더 직접 지정 시 명령어

출력 폴더 경로를 두 번째 인자로 전달하면 원하는 위치에 결과물이 저장됩니다:

```bash
python C:\Users\euntaewoo\Desktop\multilingual_text_in_image_translatio_agy_sdk\중국어\CN_Text-In_Image_Translation_Engine_AGY_SDK.py "C:\Users\euntaewoo\Desktop\multilingual_text_in_image_translatio_agy_sdk\01_번역대상_원본" "C:\Users\euntaewoo\Desktop\multilingual_text_in_image_translatio_agy_sdk\02_번역결과_최종\중국어_출력결과" --target=CN
```

---

## 📋 4. 상품 고시정보 표 렌더러 단독 실행 가이드

고시정보 표(Notice Table)를 가로 `860px`, 세로 `Auto-Fit`(타이틀 52px, 본문 26px, 1열 275px 기준, 복합항목 의미단위 개행, 최대 2,580px 이하 1장 단일 통합 페이지) 표준 규격으로 단독 렌더링할 때:

```bash
python C:\Users\euntaewoo\Desktop\multilingual_text_in_image_translatio_agy_sdk\00_공통자료\render_notice_table_standard.py
```



---

## ⚙️ 5. 주요 옵션 설명 (Options)

| 옵션 플래그 | 필수 여부 | 기본값 | 설명 |
| :--- | :---: | :---: | :--- |
| `source_dir` | 선택 | `..\01_번역대상_원본` | 번역할 한국어 원본 이미지가 위치한 디렉터리 경로 |
| `target_dir` | 선택 | `..\02_번역결과_최종\...` | 번역된 이미지를 저장할 디렉터리 경로 (미지정 시 자동 생성) |
| `--target` | 선택 | `CN` | 타겟 시장 권역 지정 (`CN`: 중국본토 간체, `TW`: 대만 번체, `HK`: 홍콩 번체) |
| `-h, --help` | 선택 | - | 도움말 및 사용법 출력 |

---

## 🛡️ 6. 작업 전 필수 체크리스트 (`[RULE 8]`)

> ⚠️ **주의**: 사용자가 중국어 번역을 요청할 때 타겟 권역을 지정하지 않은 경우, 에이전트는 절대 임의로 추측하지 않고 반드시 아래 표준 질문을 먼저 제시해야 합니다:
> 
> **"중국 본토(간체자)와 대만/홍콩(번체자) 중 어느 시장을 타겟으로 제작할까요?"**

---

## 🌐 7. 중화권 및 동남아 권역별 중국어 표기 기준 요약

1. **중국 본토 (`--target=CN`)**: 간체자 (`zh-CN`), 표준어(푸통화) 어휘 기준, 신광고법 8대 절대화 금지어 필터링.
2. **대만 번체권 (`--target=TW`)**: 정통 번체자 (`zh-TW`), 대만 전용 어휘(예: `智慧型手機`, `化妝水`, `精華液`, `水光肌`) 및 TFDA 규정 준수 (단순 간➡️번 변환 금지).
3. **홍콩 번체권 (`--target=HK`)**: 홍콩 번체자 (`zh-HK`), 구어 광동어 기반 어휘, 브랜드명/스펙 영어 원문 병기 권장.
4. **동남아 (싱가포르/말레이시아)**: 간체자 (`zh-CN/SG`) 사용하되 본토식 정치용어/신조어 배제, 이커머스 주 언어인 영어 상세페이지 기본에 간체자 보조 활용.
5. **기타 동남아 (태국, 베트남, 인니 등)**: 중국어 불필요 (현지어 또는 영어 상세페이지 제작 필수).



---

## 🏆 초월번역(Transcreation) 품질 자동 평가 4대 루브릭 (100점 만점)
- **① 현지 카테고리 어휘 적합성 (30점)**: 콩글리시/직역투 배제, 현지 뷰티 플랫폼 네이티브 어휘 채택
- **② 중화권 광고법 무결성 (30점)**: 중국 대륙 NMPA 신광고법 및 대만 TFDA 광고법 위반 표현 100% 차단
- **③ 브랜드 감성 및 초월번역 완성도 (25점)**: 백화점·세포라급 하이엔드 뷰티 톤앤매너 및 구매 전환 설득력
- **④ 시각적 레이아웃 및 가독성 (15점)**: 텍스트 박스 침범 방지 및 간결한 문장 구조
- **[합격 기준 및 자가치유]**: **90점 이상 & 위반 0건 합격**, 미달 시 피드백 기반 **최대 2회 자동 재렌더링 및 `Transcreation_QA_Report.html` 발행**

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
