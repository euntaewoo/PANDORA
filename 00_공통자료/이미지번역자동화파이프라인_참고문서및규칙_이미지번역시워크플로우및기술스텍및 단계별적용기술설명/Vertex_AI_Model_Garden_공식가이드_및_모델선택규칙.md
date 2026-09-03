# Vertex AI Model Garden 공식 가이드 및 V7 이미지 번역 엔진 규칙

## 1. 개요 (Overview)
Google Cloud Vertex AI (Gemini Enterprise Agent Platform)의 **Model Garden**은 Google 및 파트너사의 다양한 AI 모델을 탐색, 맞춤설정, 배포할 수 있는 공식 라이브러리입니다.

본 문서는 배포 방식에 따른 **리전(Location) 설정 기준**과 **이미지 생성 특화 모델 4종 라인업 선택 지침**을 정의합니다.

---

## 2. 모델 배포/호출 방식에 따른 리전(Location) 설정 정밀 표준

### 🟢 (1) Serverless (구글 관리형 API 호출 방식)
* **해당 모델**: `gemini-3.1-pro-preview`, `gemini-3.1-flash-image` (별도 엔드포인트 배포 없이 기본 API 호출 시)
* **특징**: 구글이 직접 전 세계 인프라에서 서버리스로 제공하는 방식입니다.
* **리전 규칙**: 프리뷰 파운데이션 API 호출 시 **`location="global"`**을 지정합니다. (`us-central1` 지정 시 404 NOT_FOUND 발생)
* **⛔ [HARD STOP] 직접 `genai.Client()` 작성 절대 금지**: 에이전트가 작성하는 모든 스크립트(임시 스크래치 포함)에서 `genai.Client(vertexai=True, project=..., location=...)` 를 직접 기입하는 행위를 전면 금지합니다. 반드시 아래 유일한 허용 패턴을 사용할 것:

```python
# 【유일하게 허용되는 클라이언트 초기화 패턴】
import sys
sys.path.insert(0, r"C:\Users\euntaewoo\Desktop\multilingual_text_in_image_translatio_agy_sdk\multilingual_text_in_image_translatio_agy_sdk_core")
from multilingual_text_in_image_translatio_agy_sdk_core import load_credentials
client = load_credentials()  # location="global" + 인증 자동 보장
```

### 🔴 (2) Self-deployed (사용자 전용 엔드포인트 직접 배포 방식)
* **해당 모델**: `gemini-3.1-flash-image`, Gemma, Llama 등 Model Garden에서 사용자가 특정 가상 인프라에 직접 배포(Deploy)한 모델.
* **특징**: 사용자가 특정 지역의 가상 서버(GPU/TPU)를 직접 할당받아 엔드포인트를 생성한 방식입니다.
* **리전 규칙**: `global`이 아닌 **사용자가 직접 인프라를 배포한 특정 지역 리전**(`us-central1`, `asia-northeast3` 등)을 정확히 지정해야 엔드포인트 통신이 가능합니다.

```python
# [Self-deployed 엔드포인트 호출 규격 예시]
client = genai.Client(
    vertexai=True,
    project=project_id,
    location="us-central1"  # 사용자가 직접 배포한 인프라 지역 지정
)
```

---

## 3. 🎨 Vertex AI 이미지 생성 전용 모델 4종 라인업 비교 및 채택 표준

버텍스 AI Model Garden의 이미지 생성 전용 모델 라인업(Pro, Flash, Lite, Preview) 기준에 따른 목적별 최적 모델 분류 지침입니다.

### 🏆 1. 가장 고성능 (최고 품질 특화): `Gemini 3 Pro Image`
* **특징**: 'Pro' 라인업은 복잡한 프롬프트 이해력, 정교한 디테일 표현, 고해상도 출력이 최우선인 최상위 모델입니다. 예술성과 퀄리티가 최우선일 때 선택합니다.
* **단점**: 연산량이 많아 속도가 느리며, Self-deployed 적용 시 고사양 GPU 인프라 요구로 유지 비용이 가장 높습니다.

### ⚡ 2. 상용화 최적화 (품질 + 속도 균형): `Gemini 3.1 Flash Image` ⭐ [V7 엔진 채택]
* **특징**: 'Flash' 라인업은 Pro 모델에 근접하는 우수한 퀄리티를 유지하면서 응답 지연 시간(Latency)이 짧고 리소스 소모가 적습니다.
* **장점**: 대량의 API 호출이 발생하는 e-커머스 상세페이지 자동 번역/인페인팅 상용화 환경에서 **가성비와 속도, 안정성을 모두 확보하는 최적의 상용 모델**입니다.

### 💡 3. 극가성비/단순 작업용 (참고 모델): `Gemini 3.1 Flash Lite Image`
* **특징**: Flash보다 더 빠르고 가볍지만, 디테일 품질이 다소 떨어질 수 있어 아주 단순한 썸네일/아이콘 작업에만 제한적으로 사용합니다.

### 🧪 4. 최신 기능 테스트용 (참고 모델): `Gemini 3.1 Flash Image Preview`
* **특징**: 최신 미공개 기능이 적용된 실험용 버전으로, 안정성이 최우선인 프로덕션(Production) 상용 서비스에는 권장하지 않습니다.

---

## 4. V7 이미지 번역 엔진 모드별 호출 규격 (Two-Pass Architecture)

| 구분 | 적용 모델명 | 호출 모드 | 지정 리전 | 비고 및 설정 기준 |
| --- | --- | --- | --- | --- |
| **Pass 1 (텍스트 매핑 & 약기법 검열)** | `gemini-3.1-pro-preview` | Serverless | `global` | 멀티모달 텍스트 추출, 약기법 56종 우회 번역 |
| **Pass 2 (이미지 렌더링 - 기본)** | `gemini-3.1-flash-image` | Serverless | `global` | 상용 최적화 Flash 모델로 고화질 인페인팅 |
| **Pass 2 (이미지 렌더링 - 엔드포인트)** | `gemini-3.1-flash-image` | Self-deployed | `배포 지역 (예: us-central1)` | 사용자가 Model Garden에서 자체 엔드포인트 배포 시 |

---

## 5. 인증 및 보안 규칙 (Security & Credentials)
1. **인증 방식**: GCP 서비스 계정 JSON 키(`vertex_ai_auth_key.json`) 기반 버텍스 AI 인증.
2. **환경 변수**: `.env` 파일 내 `GOOGLE_APPLICATION_CREDENTIALS` 경로 참조.

---

## 6. 변경 이력
* **2026-07-30**: Vertex AI 이미지 생성 전용 모델 4종(Pro Image, Flash Image, Flash Lite Image, Flash Image Preview) 라인업 비교 및 V7 상용화 채택 지침 명시화.

## [PRE-EXPORT-INTEGRITY-VERIFICATION-LOCK] 결과물 내보내기 전 사전 무결성 검증 및 리포트 선-출력 강제
1. **[HARD STOP] 결과물 파일 내보내기 전 무조건 사전 검증 실행**:
   - 결과물 파일(.png, .html, .docx, .txt, .md 등)을 생성·저장·보고하기 전, 데이터 무결성과 포맷 규격을 체크하는 검증 함수(`pre_export_integrity_check`) 및 린터를 무조건 실행해야 합니다.
2. **[REPORT-FIRST] 데이터 무결성 요약 리포트 선-출력 의무화**:
   - 에이전트는 최종 결과물이나 파일 링크를 사용자에게 제시하기 전, 반드시 응답 상단에 `### 📋 [DATA-INTEGRITY-SUMMARY-REPORT]` 요약 리포트 표(포맷 무결성, 콩글리시/금지어 0건 여부, 수치 일치성, 4종 파일 생성 여부)를 먼저 출력하여 검증 결과를 입증해야 합니다. 이 리포트 출력이 누락된 답변은 즉시 무효로 간주합니다.
3. **[GLOBAL-COMPLIANCE] 영미권/글로벌 뷰티 표준 명칭 강제**:
   - 무자극/저자극: 한국 성적서 0.00 직역투 배제 -> `Hypoallergenic & Dermatologist-tested for sensitive skin` 표준 강제.
   - 피부톤 케어: 'Tone Care / Dark Spot & Tone Care' 콩글리시 배제 -> `Dark Spot & Discoloration Defense` 표준 강제.
