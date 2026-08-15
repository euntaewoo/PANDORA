# 🇨🇳 CN_Text-In_Image_Translation_Engine (중국어 이미지 번역 아키텍처)

본 문서는 중화권(중국 본토, 대만, 홍콩) 이커머스 상세페이지 이미지 번역 엔진의 표준 규격서입니다.

---

## 🌟 핵심 운영 원칙 (Core Rules)

### 1. 타겟 권역 사전 확인 의무 규칙 (`[RULE 8]`)
- 사용자가 중국어 번역을 요청할 때, 타겟 권역이 명시되지 않은 경우 에이전트는 절대 임의로 추측(`[ZERO-GUESSING]`)하지 않고 반드시 아래의 표준 질문을 먼저 제시합니다:
  > **"중국 본토(간체자)와 대만/홍콩(번체자) 중 어느 시장을 타겟으로 제작할까요?"**

---

## 🏗️ Two-Pass 아키텍처 및 권역별 특화 규격

```text
[입력 이미지]
     │
     ▼
[Pass 1: Gemini 3.1 Pro] ➔ 텍스트 추출 및 권역별 법률/톤앤매너 매핑 JSON 생성
     │
     ├─ 중국 본토 (CN): 간체자(zh-CN) + 중국 신광고법 절대화 표현(最, 第一 등) 검열
     └─ 대만/홍콩 (TW/HK): 번체자(zh-TW/HK) + 대만/홍콩 현지 뷰티 용어(鎖水, 爽膚水 등)
     │
     ▼
[Pass 2: Gemini 3.1 Flash Image] ➔ 한글 완벽 제거 및 알리바바 푸후이체 식자 인페인팅
     │
     ▼
[후처리: Pillow LANCZOS] ➔ 원본 해상도 및 종횡비(Aspect Ratio) 1:1 보존 복원
```

---

## 🔤 표준 폰트 규격

- **적용 폰트**: **알리바바 푸후이체 (阿里巴巴普惠体 / Alibaba PuHuiTi)**
  - `Alibaba-PuHuiTi-Regular.ttf` (본문, 표 내용)
  - `Alibaba-PuHuiTi-Medium.ttf` (서브 타이틀, 표 항목 라벨)
  - `Alibaba-PuHuiTi-Bold.ttf` (메인 타이틀 64px, 핵심 카피)
  - `Alibaba-PuHuiTi-Heavy.ttf` (프로모션 배너, 대형 숫자)
  - `Alibaba-PuHuiTi-Light.ttf` (주석, 법적 캡션)

---

## 📋 상품 정보 고시 표(Notice Table) 렌더링 규격
- **캔버스 규격**: 가로 **`860px` 고정**, 세로 **`Auto-Fit` (최대 허용치 `2,580px` 이하, 초과 시 2페이지 분할)**
- **폰트 크기**:
  - 상단 타이틀 (商品基本信息 등): **`64px` (Bold)**
  - 테이블 좌측 항목명 (라벨 열): **`32px`**
  - 테이블 우측 본문 내용 (값 열): **`32px`**
- **공통 렌더러**: `00_공통자료/render_notice_table_standard.py`
