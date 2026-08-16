# 글로벌 이미지 번역 통합 아키텍처 규칙 (Global Translation Rules)

이 문서는 루트 경로에 구축된 `Global_Text-In_Image_Translation_Engine.py` 엔진 시스템을 제어하는 최상위 시스템 룰 파일입니다. 에이전트는 다국어 이미지 번역 엔진을 다룰 때 이 문서의 규칙을 절대적으로 준수해야 합니다.

## 1. 아키텍처 원칙: 설정 주도형 플러그인 격리 (Configuration-Driven Pack)
- **하드코딩 금지**: 코어 엔진 스크립트(`Global_Text-In_Image_Translation_Engine.py`) 내에 특정 언어의 폰트 명칭, 규제 금지어, 약기법 등을 `if/else`로 하드코딩하는 것을 절대 금지합니다.
- **플러그인 로드**: 언어별 규칙은 반드시 `config/` 디렉토리 하위의 독립된 JSON 팩(예: `EN_translation_rules.json`, `JP_translation_rules.json`)에 분리하여 저장하고, 엔진 구동 시 `--lang` 파라미터에 따라 런타임에 동적으로 주입(로드)해야 합니다.

## 2. 언어별 렌더링 및 폰트 강제 원칙
- **일본어(JP)**: 후생노동성 기준 56종 약기법 금지어 정규식(Regex) 락을 가동하고, 렌더링 시 반드시 `NotoSansJP` 폰트를 지정합니다.
- **영어(EN)**: 규제 단어 강제 필터링 락을 해제하고 초월번역 톤앤매너를 지향하며, 렌더링 시 영미권 글로벌 프리미엄 지오메트릭 산세리프인 `Montserrat (몬세라트)` 폰트를 메인 서체로 강제 적용합니다. (단, 상품상세정보 고시정보 테이블 렌더링 시에만 `Pretendard` 적용).

## 3. 안정성 방어망 (Safety Nets)
- LLM(Gemini)이 JSON 결과 반환 시 ` ```json ` 과 같은 마크다운 코드 블록을 포함하여 응답할 경우, `JSONDecodeError`가 발생하여 튕기는 치명적 결함을 막기 위해 파이썬 단에서 `replace` 및 정제(Cleaning)하는 코드가 필수적으로 포함되어야 합니다.

## 4. 핵심 기술 스택 및 아키텍처 명세
- **AI Core (Google Gemini API)**: `gemini-pro-preview` 급 모델 (OCR, 텍스트 매핑, 약기법 1차 검열) 및 `gemini-flash-image` 급 모델 (시각적 밸런스 유지 100% 인페인팅 렌더링).
- **Backend & Image Processing**: Python, Pillow(PIL) (해상도 리사이징 및 바이너리 I/O).
- **Architecture Pattern**: 설정 주도형 플러그인(Configuration-Driven) 설계. 엔진 본체(`Global_Text-In_Image_Translation_Engine.py`)는 1개로 단일화하고, 언어별 폰트/규제 룰은 JSON 팩으로 분리 주입.

## 5. 클라우드 모델 신규 버전 즉각 반영 원칙 (최신성 유지)
- **버전 업데이트 강제**: Google Cloud Vertex AI 또는 Agent Platform에서 `gemini` 모델의 신규 버전(예: 향상된 Pro/Flash 버전 등)이 출시될 경우, 에이전트는 코어 스크립트에 하드코딩된 과거 모델명(`gemini-3.1-pro-preview` 등)에 얽매이지 말고 **가장 최신의, 성능이 가장 뛰어난 버전으로 즉각 코드를 갱신(반영)**하여 번역 및 렌더링 품질을 항상 최상위로 유지해야 합니다.

## 6. 오류 복구 및 렌더링 원칙 (Full Regeneration Rule)
- **부분 수정(Patching) 절대 금지**: 텍스트 매핑(Pro 모델)이나 이미지 인페인팅(Flash 모델) 단계에서 번역 오류, 글자 뭉개짐, 레이아웃 파괴 등의 오류가 감지된 경우, **절대로 오류가 발생한 부분(영역)만 오려서 덧칠하거나 부분 수정(Patching)하지 마십시오.**
- **전체 캔버스 새롭게 재생성**: 오류 발생 시 무조건 처음(백지/원본 이미지)으로 돌아가서 **전체 작업을 새롭게 다시 시작(Full Regeneration)**하여 하나의 완벽한 이미지를 처음부터 끝까지 새로 그려내야 합니다. 이는 픽셀 밸런스 붕괴를 막기 위한 최상위 절대 원칙입니다.

## 7. 원본 비율 및 해상도 절대 보존 원칙 (Aspect Ratio Lock)
- **비율 찌그러짐 절대 허용 불가**: AI(Flash 모델)가 전체 캔버스를 새롭게 렌더링하여 이미지를 배출하더라도, 파이썬 백엔드 코드 단에서 `Pillow (PIL)` 라이브러리의 고화질 `Image.Resampling.LANCZOS` 알고리즘을 강제 가동해야 합니다.
- **원본 100% 강제 맞춤**: 배출된 결과물은 저장되기 직전, 반드시 원본 이미지의 사이즈(`original_image.size`)와 픽셀 비율(Aspect Ratio)에 100% 똑같이 맞춰서 강제로 리사이징(Lock) 된 후 파일로 저장되어야 합니다. 원본 대비 비율이나 화질이 미세하게라도 변경되는 것을 원천 차단합니다.

## 8. [HARD STOP] 1.5 라인업 및 구형 모델 사용 절대 금지 (3.1+ 강제)
- 어떠한 에러(404, 권한 부족 등)나 테스트 상황에서도 gemini-1.5-pro, gemini-1.5-flash 등 1.5 라인업이나 그 이하의 구형 범용 모델을 대안으로 언급하거나 코드로 다운그레이드(적용)하는 것을 시스템적으로 엄격히 금지합니다.
- 엔진은 무조건 gemini-3.1-pro-preview / gemini-3.1-flash-image (또는 그 이상)의 초고성능 모델만을 고정적으로 사용해야 하며, 구동 실패 시 모델을 낮출 것이 아니라 인증키 환경이나 설정값 누락을 먼저 체크해야 합니다.
