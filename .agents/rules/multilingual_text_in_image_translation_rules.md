# multilingual_text_in_image_translation 시스템 규칙 (System Rules)

이 문서는 루트 경로에 구축된 `multilingual_text_in_image_translatio_agy_sdk.py` 엔진 시스템을 제어하는 최상위 시스템 룰 파일입니다. 에이전트는 다국어 이미지 번역 엔진을 다룰 때 이 문서의 규칙을 절대적으로 준수해야 합니다.

## 1. 아키텍처 원칙: 설정 주도형 플러그인 격리 (Configuration-Driven Pack)
- **하드코딩 금지**: 코어 엔진 스크립트(`multilingual_text_in_image_translatio_agy_sdk.py`) 내에 특정 언어의 폰트 명칭, 규제 금지어, 약기법 등을 `if/else`로 하드코딩하는 것을 절대 금지합니다.
- **플러그인 로드**: 언어별 규칙은 반드시 `config/` 디렉토리 하위의 독립된 JSON 팩(예: `EN_translation_rules.json`, `JP_translation_rules.json`)에 분리하여 저장하고, 엔진 구동 시 `--lang` 파라미터에 따라 런타임에 동적으로 주입(로드)해야 합니다.

## 2. 언어별 렌더링 및 폰트 강제 원칙
- **일본어(JP)**: 후생노동성 기준 56종 약기법 금지어 정규식(Regex) 락을 가동하고, 렌더링 시 반드시 `NotoSansJP` 폰트를 지정합니다.
- **영어(EN)**: 규제 단어 강제 필터링 락을 해제하고 초월번역 톤앤매너를 지향하며, 렌더링 시 영미권 글로벌 프리미엄 지오메트릭 산세리프인 `Montserrat (몬세라트)` 폰트를 메인 서체로 강제 적용합니다. (단, 상품상세정보 고시정보 테이블 렌더링 시에만 `Pretendard` 적용).
- **중국어(CN/TW)**: 중국 신광고법 및 NMPA 규정 필터링을 적용하며, 렌더링 시 `Noto Sans SC` (간체자) / `Noto Sans TC` (번체자) 폰트를 적용합니다.

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


## 9. [COMPLIANCE-FIRST] 글로벌 법무 & 럭셔리 마케팅 초월번역 표준 규격
1. **시스템 인스트럭션 전역 고정**: 모든 Pass 1 호출 시 `GLOBAL_COMPLIANCE_SYSTEM_INSTRUCTION` (다국어 법무팀 + 럭셔리 카피라이터) 주입 필수.
2. **동적 렉시콘 연동**: `00_공통자료/compliance_lexicons/*.json`에서 4개국 법령 DB를 실시간 동적 로드.
3. **5대 법적 리스크 & 콩글리시 100% 강제 치환**:
   - `Complex skin issues` ➔ `Multiple skin concerns`
   - `Troubled skin` ➔ `Blemish-prone skin`
   - `nutrients for cellular vitality` ➔ `hydration for a resilient-looking complexion`
   - `reinforces cellular resilience` ➔ `reinforces the skin's natural moisture barrier`
   - `combats premature aging` ➔ `combats the signs of premature aging`
4. **결정론적 후처리 게이트 (`apply_deterministic_qa_overrides`)**: Python 정규식 필터에서 금지어를 1ms 내에 전수 자동 교정.
