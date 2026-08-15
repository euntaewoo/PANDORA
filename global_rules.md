# 이미지번역-프로젝트-전역규칙 (Global Rules)

본 문서는 모든 에이전트가 최우선으로 준수해야 하는 전역(Global) 룰북입니다.

## 1. 오류 복구 원칙 (Full Regeneration Rule)
- 텍스트 번역이나 이미지 렌더링 과정에서 오류(글자 뭉개짐, 403/429 등 통신 에러, 레이아웃 깨짐)가 발생할 경우, **절대로 오류가 발생한 부분만 임의로 수정(Patching, 덧칠 등)하지 마십시오.**
- 오류 발생 시 무조건 **전체 작업을 새롭게 다시 시작(Full Regeneration)**하여 하나의 완벽한 캔버스를 처음부터 끝까지 새로 생성해야 합니다.

## 2. 1.5 Legacy Model 금지 (3.1+ 강제)
- 어떠한 상황에서도 `gemini-1.5-pro`, `gemini-1.5-flash` 등 구형 레거시 모델의 사용 및 언급을 절대 금지합니다.
- 엔진은 무조건 최신의 `gemini-3.1-pro-preview`, `gemini-3.1-flash-image` (또는 3.5 이상) 라인업으로만 구동되어야 합니다.

## 3. 원본 비율 및 해상도 절대 보존 (Aspect Ratio Lock)
- 렌더링 결과물은 Pillow 라이브러리의 LANCZOS 알고리즘 등을 통해 원본 이미지의 픽셀 비율(Aspect Ratio)과 해상도에 100% 강제 동기화되어야 하며, 정사각형(1:1) 등으로 임의 크롭되는 것을 절대 금지합니다.

## 4. 상품 패키지 포장 원본 보존 규칙 (Product Package Text & Logo Protection)
- 이미지 속 제품이나 상품의 패키지 박스 원본에 포함된 텍스트 및 브랜드 로고는 상품 패키지 박스 포장 원본 형태를 그대로 유지하며, 패키지 상의 글자 및 로고에 대한 번역/수정/수평 덧칠 행위를 엄격히 금지합니다.

## 5. 구글 클라우드 공식 가이드 참조 및 리전 강제 규칙 (Official Docs & Location Lock)
- 모든 Gemini 3.1+ 모델 호출 시, 추측성 리전 변경을 엄격히 금지하며 무조건 프로젝트 내 구글 공식 가이드(`00_공통자료/.../Vertex_AI_Model_Garden_공식가이드_및_모델선택규칙.md`)의 **`location="global"` (Serverless 관리형 규격)**을 100% 강제 적용합니다.
- 어떠한 상황에서도 공식 기술 문서의 규격을 이탈하여 `us-central1` 등 임의의 리전으로 단독 변경하는 행위를 절대 금지합니다.
- **[공식 문서 주기적 체크 필수]**: 구글 클라우드 에이전트 플랫폼(Google Cloud Agent Platform) 및 Vertex AI Model Garden 공식 가이드와 신규 업데이트 내용을 작업 전/주기적으로 반드시 탐색·체크하여 최신 API 표준 및 리전 정책을 차질 없이 반영합니다.

## 6. 깃허브 자동 버전 관리 및 실시간 푸시 규칙 (Automatic GitHub Sync & Push)
- 모든 작업 진행 시, 소스코드 수정, 문서 개정, 신규 기능 추가가 일어날 때마다 무조건 깃허브 저장소(`https://github.com/euntaewoo/PANDORA.git`)로 자동 커밋 및 푸시(Auto Commit & Push)를 수행하여 버전 관리를 실시간 유지해야 합니다.
- API 키 및 인증 파일은 `.gitignore`로 안전하게 제외 처리한 후 커밋합니다.

## 7. 상품 정보 고시 표(Notice Table) 고해상도 HTML 렌더링 표준 규격 (Notice Table Rendering Standard)
- **[해상도 규격]**:
  - 가로 폭: **`860px` 고정**
  - 세로 높이: **`Auto-Fit` 적용 (단, 최대 허용 높이는 `2,580px` 이하 엄격 준수)**
  - **[2페이지 분할 룰]**: 전성분 등 본문 내용이 길어져 세로 높이가 **`2,580px`를 초과할 경우 무조건 2페이지(Part 1, Part 2)로 분할 작성**하여 개별 이미지로 렌더링할 것.
- **[언어별 표준 폰트 적용]**:
  - **영문(EN)**: **`Pretendard`** (Pretendard-Bold / Pretendard-Regular)
  - **일본어(JP)**: **`Noto Sans JP`** (NotoSansJP-Bold / NotoSansJP-Regular)
  - 기타 언어: 해당 국가 및 상품 카테고리에서 가장 빈도가 높고 가독성이 검증된 표준 산세리프 서체 적용.
- **[타이포그래피 폰트 크기 규격]**:
  - **상단 타이틀 (PRODUCT DETAILS / 商品基本情報 등)**: **`64px`** (Bold)
  - **테이블 좌측 항목명 (항목 라벨 열)**: **`32px`**
  - **테이블 우측 본문 내용 (값 열)**: **`32px`**
- **[렌더링 엔진]**: AI 생성형 뭉개짐을 배제하고 칼같은 벡터 텍스트 선명도를 위해 Headless Chromium/Edge 기반 초고해상도 렌더링 파이프라인을 의무 적용할 것.

