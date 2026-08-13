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

```python
# [Serverless 관리형 API 호출 기본 규격]
client = genai.Client(
    vertexai=True,
    project=project_id,
    location="global"  # 관리형 Serverless 호출 시 global 필수
)
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
