## **Google Cloud AI & Data 서비스 구조 및 API 연동 가이드** 

### **—--------------------------------------------------------------------**

## **구글 클라우드 핵심 AI / 데이터 서비스 카테고리**

┌───────────────────────────────────────────────────────────   ──────────────┐  
 │                        Google Cloud Platform                            │  
 ├──────────────────┬──────────────────┬──────────────────┬────────────────┤  
 │   1\. 생성형 AI    │    2\. 예측/분석   │  3\. 사전학습 AI  │ 4\. 데이터/DB   │  
 │   (Generative)   │  (Predictive)    │   (Pre-trained)  │  (Data & DB)   │  
 └──────────────────┴──────────────────┴──────────────────┴────────────────┘

### ---

**1\. API 키(JSON) 하나로 공통 사용이 가능한가요?**

**네, 가능합니다.**

구글 클라우드의 **서비스 계정(Service Account) JSON 키**는 일종의 "신분증(인증서)" 역할을 합니다.

* 하나의 JSON 키 파일로 **Vertex AI(생성형 AI)**, **Vision AI(분석)**, **BigQuery(빅데이터)** 등 프로젝트 내 모든 서비스에 동일하게 인증을 거칠 수 있습니다.  
* 단, 해당 서비스 계정에 적절한 권한(IAM Role, 예: Vertex AI User, Storage Object Viewer 등)이 부여되어 있어야 합니다.

### ---

**2\. 각 카테고리별로 API를 각각 활성화해야 하나요?**

**네, 반드시 각 서비스의 API를 개별적으로 \[사용 설정(Enable)\]하셔야 합니다.**

구글 클라우드는 보안 및 비용 관리 차원에서 **모든 API가 기본적으로 비활성화**되어 있습니다. 따라서 공통 JSON 키를 가지고 있더라도, 호출하려는 백엔드 API가 꺼져 있으면 403 API Not Enabled 에러가 발생합니다.

#### **💡 카테고리별 활성화해야 하는 대표 API 예시**

| 사용하려는 카테고리 / 기능 | 구글 클라우드에서 활성화해야 할 API 명칭 |
| :---- | :---- |
| **생성형 AI (Gemini, Imagen 4 등)** | **Vertex AI API** (aiplatform.googleapis.com) |
| **이미지/문서 분석 (OCR, 사물 인식)** | **Cloud Vision API** (vision.googleapis.com) |
| **음성 인식 / 음성 합성** | **Cloud Speech-to-Text API** / **Text-to-Speech API** |
| **빅데이터 분석 및 저장소** | **BigQuery API**, **Cloud Storage API** |

> **실무 팁:**

> Vertex AI API 하나만 켜두면 Vertex AI 카테고리 안에 있는 \*\*Gemini(텍스트/멀티모달)\*\*와 \*\*Imagen 4(이미지 생성/편집)\*\*는 모두 함께 호출해서 사용할 수 있습니다. 하지만 \*\*Vision AI(OCR/분석)\*\*로 넘어갈 때는 Cloud Vision API를 콘솔에서 별도로 \[사용\] 상태로 켜주셔야 합니다.

### ---

**3\. Google Cloud의 서비스 카테고리 분류가 더 있나요?**

질문하신 대로 앞서 설명해 드린 4개 주요 분류 외에도 구글 클라우드 전체에는 개발 목적에 따른 카테고리 분류가 더 존재합니다. 전체 구도를 이해하시기 쉽게 정리해 드립니다.

1. **생성형 AI (Generative AI):** Vertex AI (Gemini, Imagen, Veo 등)  
2. **사전학습/분석형 AI (Pre-trained AI):** Vision AI, Speech AI, Translation AI  
3. **데이터 & 데이터베이스 (Data & DB):** BigQuery, Cloud Storage, Firestore  
4. **인프라 & 연산 (Compute & Core):** Compute Engine (구글 VM 서버), Cloud Run, Kubernetes (GKE)  
5. **네트워킹 & 보안 (Networking & Security):** Cloud DNS, IAM (권한 관리), Secret Manager

### ---

**📌 요약 및 최종 정리**

1. **인증 키:** 서비스 계정에서 발급받은 **JSON 키 1개만** 프로젝트 전체 코드에서 공통 인증용으로 사용하시면 됩니다.  
2. **API 활성화:** 코드를 실행하기 전에 구글 클라우드 콘솔 상단 검색창에서 사용하려는 기능(예: Vertex AI API, Cloud Vision API)을 검색하여 **\[사용(Enable)\]** 버튼을 각각 눌러두셔야 호출이 정상 작동합니다.