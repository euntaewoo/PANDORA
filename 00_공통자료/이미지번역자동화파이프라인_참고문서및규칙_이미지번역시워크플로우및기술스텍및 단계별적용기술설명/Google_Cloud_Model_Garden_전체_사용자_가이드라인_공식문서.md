# Google Cloud Model Garden 전체 사용자 가이드라인 (공식 문서 전문)

> **공식 출처**: https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/model-garden/explore-models?hl=ko

---

Model Garden은 Google 및 Google 파트너의 모델 및 애셋을 검색, 테스트, 맞춤설정, 배포할 수 있게 도와주는 AI/ML 모델 라이브러리입니다.


## Model Garden의 이점

AI 모델 작업을 수행할 때 Model Garden은 다음과 같은 이점을 제공합니다.

* 사용 가능한 모델이 모두 단일 위치에 그룹화됩니다.
* Model Garden은 여러 유형의 모델에 대해 일관적인 배포 패턴을 제공합니다.
* Model Garden은 모델 조정, 평가, 서빙과 같은 Gemini Enterprise Agent Platform의 여러 부분에 대해 기본적으로 지원되는 통합 기능을 제공합니다.
* 생성형 AI 모델 서빙은 어려운 작업일 수 있습니다. Gemini Enterprise Agent Platform은 모델 배포 및 서빙을 자동으로 처리합니다.


## 모델 살펴보기

사용 가능한 Gemini Enterprise Agent Platform 및 오픈소스 파운데이션,
튜닝 가능한 모델, 작업별 모델의 목록을 보려면
Google Cloud 콘솔에서 Model Garden 페이지로 이동합니다.

Model Garden으로 이동

Model Garden에서 제공하는 모델 카테고리는 다음과 같습니다.

| 카테고리 | 설명 |
| 기반 모델 | Agent Studio, Agent Platform API, Agent Platform SDK를 사용하여 특정 태스크에 대해 조정하거나 맞춤설정할 수 있는 사전 학습된 멀티태스크 대규모 모델입니다. |
| 미세 조정 가능한 모델 | 커스텀 노트북 또는 파이프라인을 사용하여 미세 조정할 수 있는 모델입니다. |
| 태스크별 솔루션 | 이와 같이 사전 빌드된 모델은 대부분 즉시 사용 가능하며 자체 데이터를 사용하여 맞춤설정할 수 있는 경우가 많습니다. |

필터 창에서 모델을 필터링하려면 다음을 지정합니다.

* 태스크: 모델로 수행할 태스크를 클릭합니다.
* 모델 컬렉션: Google, 파트너 또는 개발자가 관리하는 모델을 선택하려면 클릭합니다.
* 제공업체: 모델 제공업체를 클릭합니다.
* 기능: 모델에서 지원하려는 기능을 클릭합니다.

각 모델에 대해 자세히 알아보려면 모델 카드를 클릭하세요.


## 모델 보안 스캔

Google은 Google에서 제공되는 모델 서빙 및 조정 컨테이너에 대해 철저한 테스트와 벤치마크를 수행합니다. 이러한 컨테이너 아티팩트에 대해서는 취약점 스캔도 적극적으로 수행합니다.

Model Garden은 포함된 파트너의 서드 파티 모델에 대해 모델 체크포인트 스캔을 수행하여 진위 여부를 확인합니다. HuggingFace Hub의 서드 파티 모델은 HuggingFace에서 직접 스캔되며서드 파트 스캐너를 사용하여 멀웨어, 피클 파일, Keras 람다 레이어, 보안 비밀을 확인합니다. 스캔 결과 모델이 안전하지 않다고 판단되면 HuggingFace에서 플래그를 지정하여 Model Garden에 배포할 수 없도록 차단됩니다. 의심스럽거나 원격 코드를 실행할 수 있는 것으로 표시된 모델은 Model Garden에 표시되더라도 여전히 배포할 수 있습니다. 하지만 Model Garden에서 이를 배포하기 전에 의심스러운 모델을 주의 깊게 검사하는 것이 좋습니다.


## 가격 책정

Model Garden의 오픈소스 모델의 경우 Gemini Enterprise Agent Platform에서 다음 항목의 사용에 따라 요금이 부과됩니다.

* 모델 미세 조정: 커스텀 학습과 동일한
요율로 사용되는 컴퓨팅 리소스에 대한 요금이 부과됩니다.커스텀 학습 가격 책정을 참조하세요.
* 모델 배포: 모델을 엔드포인트에 배포하는 데 사용되는 컴퓨팅 리소스에 대한 요금이 부과됩니다.예측 가격 책정을 참조하세요.
* Colab Enterprise:Colab Enterprise 가격 책정을 참고하세요.


## 특정 모델에 대한 액세스 제어

조직, 폴더 또는 프로젝트 수준에서Model Garden 조직 정책을 설정하여 Model Garden의 특정 모델에 대한 액세스를 제어할 수 있습니다. 예를 들어 검증된 특정 모델에 대한 액세스를 허용하고 다른 모든 모델에 대한 액세스를 거부할 수 있습니다.


## Model Garden 자세히 알아보기

Model Garden에서 모델에 수행할 수 있는 배포 옵션 및 맞춤설정에 대한 자세한 내용은 튜토리얼, 참조, 노트북, YouTube 동영상 링크가 포함된 다음 섹션의 리소스를 참조하세요.


### 배포 및 서빙

배포 및 고급 서빙 기능의 맞춤설정에 대해 자세히 알아보세요.

* Python SDK, CLI, REST API 또는 콘솔을 사용하여 오픈소스 모델 배포 및 서빙개발자 블로그: 새로운 Gemini Enterprise Agent Platform Model Garden CLI 및 SDK 소개SDK 튜토리얼 노트북을 사용하여 공개 모델 배포Gemini Enterprise Agent Platform Model Garden SDK 노트북 시작하기
* Model Garden에서 Gemma 3 배포 및 미세 조정 YouTube 동영상
* Gemma 배포 및 예측 수행
* Cloud TPU에서 Hex-LLM 컨테이너를 사용하여 오픈소스 모델 서빙
* Hex-LLM을 사용하여 Llama 모델 배포 튜토리얼 노트북
* Hex-LLM 또는 vLLM으로 프리픽스 캐싱 및 추측 디코딩 사용 튜토리얼 노트북
* Cloud GPU에서 vLLM을 사용하여 텍스트 전용 및 멀티모달 언어 모델 서빙텍스트 전용 모델 튜토리얼 노트북멀티모달 모델 튜토리얼 노트북
* 이미지 및 동영상 생성을 위한 xDiT GPU 서빙 컨테이너 사용
* PyTorch 추론을 위해 HuggingFace DLC를 사용하고 여러 LoRA 어댑터가 적용된 Gemma 2를 서빙하는 방법 Medium 튜토리얼
* PyTorch 추론을 위해 HuggingFace DLC를 사용하고 커스텀 핸들을 사용하여 이미지 캡셔닝을 위해 PaliGemma를 서빙하는 방법 LinkedIn 튜토리얼
* Spot VM 또는 Compute Engine 예약을 사용하는 모델 배포 및 서빙 튜토리얼 노트북
* Hugging Face 모델 배포 및 서빙

* 개발자 블로그: 새로운 Gemini Enterprise Agent Platform Model Garden CLI 및 SDK 소개
* SDK 튜토리얼 노트북을 사용하여 공개 모델 배포
* Gemini Enterprise Agent Platform Model Garden SDK 노트북 시작하기

* 텍스트 전용 모델 튜토리얼 노트북
* 멀티모달 모델 튜토리얼 노트북


### 조정

특정 사용 사례에 맞게 응답을 조정하려면 조정 모델에 대해 자세히 알아보세요.

* 워크벤치 미세 조정 튜토리얼 노트북
* 미세 조정 및 평가 튜토리얼 노트북
* Model Garden에서 Gemma 3 배포 및 미세 조정 YouTube 동영상


### 평가

Agent Platform을 사용하여 모델 응답에 액세스하는 방법을 자세히 알아보세요.

* 생성형 AI 평가 서비스로 Gemma 2 평가 YouTube 동영상


### 추가 리소스

* 모델 및 사용자 경험 관련 Model Garden 노트북
* Gemini Enterprise Agent Platform 오픈 모델 서빙, 미세 조정, 평가 노트북

## [PRE-EXPORT-INTEGRITY-VERIFICATION-LOCK] 결과물 내보내기 전 사전 무결성 검증 및 리포트 선-출력 강제
1. **[HARD STOP] 결과물 파일 내보내기 전 무조건 사전 검증 실행**:
   - 결과물 파일(.png, .html, .docx, .txt, .md 등)을 생성·저장·보고하기 전, 데이터 무결성과 포맷 규격을 체크하는 검증 함수(`pre_export_integrity_check`) 및 린터를 무조건 실행해야 합니다.
2. **[REPORT-FIRST] 데이터 무결성 요약 리포트 선-출력 의무화**:
   - 에이전트는 최종 결과물이나 파일 링크를 사용자에게 제시하기 전, 반드시 응답 상단에 `### 📋 [DATA-INTEGRITY-SUMMARY-REPORT]` 요약 리포트 표(포맷 무결성, 콩글리시/금지어 0건 여부, 수치 일치성, 4종 파일 생성 여부)를 먼저 출력하여 검증 결과를 입증해야 합니다. 이 리포트 출력이 누락된 답변은 즉시 무효로 간주합니다.
3. **[GLOBAL-COMPLIANCE] 영미권/글로벌 뷰티 표준 명칭 강제**:
   - 무자극/저자극: 한국 성적서 0.00 직역투 배제 -> `Hypoallergenic & Dermatologist-tested for sensitive skin` 표준 강제.
   - 피부톤 케어: 'Tone Care / Dark Spot & Tone Care' 콩글리시 배제 -> `Dark Spot & Discoloration Defense` 표준 강제.
