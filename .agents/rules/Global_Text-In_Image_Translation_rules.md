# multilingual_text_in_image_translation 시스템 규칙 (System Rules)

이 문서는 루트 경로에 구축된 `multilingual_text_in_image_translatio_agy_sdk.py` 엔진 시스템을 제어하는 최상위 시스템 룰 파일입니다. 에이전트는 다국어 이미지 번역 엔진을 다룰 때 이 문서의 규칙을 절대적으로 준수해야 합니다.

## 1. 아키텍처 원칙: 설정 주도형 플러그인 격리 (Configuration-Driven Pack)
- **하드코딩 금지**: 코어 엔진 스크립트(`multilingual_text_in_image_translatio_agy_sdk.py`) 내에 특정 언어의 폰트 명칭, 규제 금지어, 약기법 등을 `if/else`로 하드코딩하는 것을 절대 금지합니다.
- **표준 렉시콘 DB 연동**: 언어별 법률 규제 및 금지어/대체어는 반드시 `00_공통자료/compliance_lexicons/` 하위의 독립된 JSON 팩(예: `en_fda_mocra_lexicon.json`, `jp_pmda_pharm_lexicon.json`, `cn_nmpa_adlaw_lexicon.json`, `tw_tfda_lexicon.json`)에 분리 저장하고, 엔진 구동 시 `--lang` 파라미터에 따라 `load_dynamic_compliance_lexicon()`을 통해 런타임에 동적으로 주입(로드)해야 합니다.

## 2. 언어별 렌더링, 폰트 및 컴플라이언스 강제 원칙
- **영어(EN)**: 미국 FDA MoCRA 및 FTC 기준 의약품 오인(세포/생리기능 cellular vitality/resilience) 클레임 전면 차단, 노화는 반드시 `the signs of premature aging`으로 한정, K-뷰티 콩글리시(`Complex skin issues` -> `Multiple skin concerns`, `Troubled skin` -> `Blemish-prone skin`) 배제 및 럭셔리 초월번역 톤앤매너 강제. 렌더링 시 영미권 글로벌 프리미엄 지오메트릭 산세리프인 `Montserrat (몬세라트)` 폰트를 메인 서체로 100% 강제 적용합니다. (단, 고시정보 테이블 렌더링 시에만 `Pretendard` 적용).
- **일본어(JP)**: 후생노동성 기준 56종 약기법 포지티브 리스트(Positive List) 엄격 준수, 치료/재생 클레임 배제, 렌더링 시 반드시 `NotoSansJP` 폰트를 지정합니다.
- **중국어(CN/TW)**: 중국 신광고법 8대 절대화 금지어('最', '第一', '顶级' 등) 및 NMPA/TFDA 화장품 규정 필터링을 적용하며, 렌더링 시 `Noto Sans SC` (간체자) / `Noto Sans TC` (번체자) 폰트를 적용합니다.

## 2-1. [GLOBAL-COMPLIANCE] 전역 시스템 인스트럭션 & 원천 법리 (First Principles Heuristic)
- 모든 번역 엔진 호출 시 `GLOBAL_COMPLIANCE_SYSTEM_INSTRUCTION`을 최상위 시스템 지침으로 주입하여 '다국어 법무 감사관 + 럭셔리 카피라이터' 역할을 강제합니다.
- 사전에 등록되지 않은 신규 성분/어휘라도 인체 세포/생리기능에 직접 관여하는 뉘앙스가 있다면 무조건 '피부 표면의 미용적 외관 개선(-looking, appearance of, moisture barrier)'으로 안전하게 우회해야 합니다.

## 3. 안정성 방어망 (Safety Nets)
- LLM(Gemini)이 JSON 결과 반환 시 ` ```json ` 과 같은 마크다운 코드 블록을 포함하여 응답할 경우, `JSONDecodeError`가 발생하여 튕기는 치명적 결함을 막기 위해 파이썬 단에서 `replace` 및 정제(Cleaning)하는 코드가 필수적으로 포함되어야 합니다.

## 4. 핵심 기술 스택 및 아키텍처 명세
- **AI Core (Google Gemini API)**: `gemini-3.1-pro-preview` (OCR, 텍스트 매핑, 법률 검열) 및 `gemini-3.1-flash-image` (시각적 밸런스 유지 100% 인페인팅 렌더링).
- **Backend & Image Processing**: Python, Pillow(PIL) (해상도 리사이징 및 바이너리 I/O).
- **Architecture Pattern**: 단일 통합 코어(`multilingual_text_in_image_translatio_agy_sdk.py`) 기반 언어별 분기 및 고시표 HTML 자동 렌더링.

## 5. 클라우드 모델 신규 버전 즉각 반영 원칙 (최신성 유지)
- **버전 업데이트 강제**: Google Cloud Vertex AI 또는 Agent Platform에서 `gemini` 모델의 신규 버전이 출시될 경우, 코어 스크립트에 하드코딩된 과거 모델명에 얽매이지 말고 가장 최신의, 성능이 가장 뛰어난 버전으로 즉각 코드를 갱신하여 품질을 최상위로 유지해야 합니다.

## 6. 오류 복구 및 렌더링 원칙 (Full Regeneration Rule)
- **부분 수정(Patching) 절대 금지**: 오류 발생 시 절대로 부분 덧칠(Patching)하지 말고, 전체 캔버스를 새롭게 다시 렌더링(Full Regeneration)해야 합니다.

## 7. 원본 비율 및 해상도 절대 보존 원칙 (Aspect Ratio Lock)
- Pillow `Image.Resampling.LANCZOS` 알고리즘을 통해 원본 해상도 및 종횡비를 100% 강제 동기화합니다.

## 8. [HARD STOP] 1.5 라인업 및 구형 모델 사용 절대 금지 (3.1+ 강제)
- 어떠한 상황에서도 `gemini-1.5-pro`, `gemini-1.5-flash` 등 구형 레거시 모델로 다운그레이드하는 행위를 절대 금지합니다.

## [PRE-EXPORT-INTEGRITY-VERIFICATION-LOCK] 결과물 내보내기 전 사전 무결성 검증 및 리포트 선-출력 강제
1. **[HARD STOP] 결과물 파일 내보내기 전 무조건 사전 검증 실행**:
   - 결과물 파일(.png, .html, .docx, .txt, .md 등)을 생성·저장·보고하기 전, 데이터 무결성과 포맷 규격을 체크하는 검증 함수(`pre_export_integrity_check`) 및 린터를 무조건 실행해야 합니다.
2. **[REPORT-FIRST] 데이터 무결성 요약 리포트 선-출력 의무화**:
   - 에이전트는 최종 결과물이나 파일 링크를 사용자에게 제시하기 전, 반드시 응답 상단에 `### 📋 [DATA-INTEGRITY-SUMMARY-REPORT]` 요약 리포트 표(포맷 무결성, 콩글리시/금지어 0건 여부, 수치 일치성, 4종 파일 생성 여부)를 먼저 출력하여 검증 결과를 입증해야 합니다. 이 리포트 출력이 누락된 답변은 즉시 무효로 간주합니다.
3. **[GLOBAL-COMPLIANCE] 영미권/글로벌 뷰티 표준 명칭 강제**:
   - 무자극/저자극: 한국 성적서 0.00 직역투 배제 -> `Hypoallergenic & Dermatologist-tested for sensitive skin` 표준 강제.
   - 피부톤 케어: 'Tone Care / Dark Spot & Tone Care' 콩글리시 배제 -> `Dark Spot & Discoloration Defense` 표준 강제.
