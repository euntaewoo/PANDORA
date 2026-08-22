# 🇰🇷 한국어 상품정보제공고시(Notice Table) 표준 렌더링 규격서

> **모듈 파일명**: `render_notice_table_korean.py`  
> **AI 지능형 엔진**: `gemini-3.1-pro-preview` (Google Cloud Vertex AI, `location="global"`)  
> **초고정밀 OCR 엔진**: `Google Cloud Vision API` (`DOCUMENT_TEXT_DETECTION`)  
> **표준 폰트**: `Pretendard` (Bold, Regular)  
> **기반 엔진**: Headless Chromium (Playwright HTML5/CSS3 Vector Snapshot)  
> **통합 기준**: 국내 이커머스 최적화 및 글로벌 다국어 고시표의 원본(Source of Truth) 통일 규격 (2026-08 최종 확정)

---

## 🤖 1. 지능형 듀얼 인풋 (Dual Ingestion) 아키텍처

한국어 고시표 렌더러는 **[모드 A: 디지털 문서]**와 **[모드 B: 기존 이미지/사진]**의 2가지 입력 방식을 모두 지원합니다.

1. **모드 A: 디지털 문서 직접 입력 (Fast Lossless Mode)**:
   - `010_PDP_상품상세정보.docx` 등 워드 문서 인입 시, `python-docx`가 XML 노드를 직접 읽어 오타 0%, 누락 0%로 0.001초 만에 추출.
2. **모드 B: 기존 상세페이지 이미지 / 단상자 사진 입력 (Vision OCR + Gemini 3.1 Pro Reconstruct Mode)**:
   - 워드 파일이 없고 과거 제작된 이미지(PNG/JPG)나 패키지 사진만 있는 경우,
   - **Google Cloud Vision API (`DOCUMENT_TEXT_DETECTION`)**가 깨알 같은 6pt 전성분/주의사항 텍스트를 99.8% 정밀도로 스캔.
   - 스캔된 Raw 텍스트를 **`gemini-3.1-pro-preview`**가 수신하여 KCID/INCI 표준 명칭 교정, 1열/2열 분리, 소프트 하이픈(`&shy;`) 삽입 후 완벽한 테이블 구조로 복원.
3. **통합 인증 프로토콜 (Single Key Shared Auth)**:
   - `00_공통자료\APIs_KEY\인증키_및_계정\김차장_vertex api_key\vertex_ai_auth_key.json` 하나로 Vertex AI와 Cloud Vision API를 동시 인증.

---

## 📐 2. 캔버스 및 레이아웃 표준 규격

| 항목 | 표준 수치 / 설정 | 비고 |
| :--- | :--- | :--- |
| **캔버스 가로 너비** | **`860px` 고정** | 국내 이커머스 상세페이지 최적 표준 너비 (스크린샷 Bounding Box 860px) |
| **캔버스 세로 높이** | **`Auto-Fit` (내용 기반 자동 맞춤)** | 하단 여백 및 캔버스 패딩(상단 15px, 하단 20px, 좌우 20px) 포함 |
| **단일 페이지 최대 한도** | **`2,580px` 이하** | 1장 이미지 수납 원칙 |
| **2페이지 자동 분할 규칙** | **초과 시 1차 행간/패딩 압축(Squeeze), 실패 시 분할** | 2,580px 초과 시 `line-height: 1.25` 및 셀 패딩 `22px`로 압축하여 1페이지 수납을 재시도하며, 그래도 초과할 경우에만 `Part 1`, `Part 2` 자동 분할 렌더링 |
| **테이블 폭 (Table Width)** | **`820px` (table-layout: fixed)** | 860px 캔버스 내 좌우 안전 마진 각 `20px` 적용 |
| **Box Model 기준** | **`* { box-sizing: border-box; }` 의무화** | 패딩으로 인한 테이블 및 열 폭 팽창 원천 방지 |

---

## 🔤 3. 타이포그래피 및 서체 스타일

- **기본 폰트**: `Pretendard`, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif
- **기본 행간 (Line-Height)**: `1.45` (압축 시 `1.25`)
- **자간 (Letter-Spacing)**: `-0.5px`

### 1) 상단 타이틀 (`상품 상세 정보` / `상품정보제공고시`)
- **폰트 크기**: **`60px` (Bold)**
- **정렬 / 색상**: 중앙 정렬 (`text-align: center`), `#111111`
- **여백**: 상단 `15px`, 하단 `30px`

### 2) 테이블 1열 (항목명 라벨 열 / `<th>`)
- **열 너비**: **`295px` 고정폭 (타이트 핏)** | `width: 295px; word-break: break-word; overflow-wrap: break-word;`
- **텍스트 정렬**: **좌측 중앙정렬** (`text-align: left; vertical-align: middle;`)
- **폰트 크기**: **`30px` (Bold)**
- **배경색 / 글자색**: `#F8F9FA` / `#333333`
- **패딩**: 상하 `24px` (압축 시 `22px`), 좌우 `20px` (총 좌우 여백 `40px`)
- **단문 라벨 1줄 유지 원칙**: 10자 미만 라벨(`용량`, `사용방법`, `소비자상담`)은 1줄 강제 유지, 10자 이상 복합 라벨만 2줄 분할.
- **우측 테두리**: `1px solid #EAEAEA`

### 3) 테이블 2열 (본문 내용 열 / `<td>`)
- **열 너비**: **`525px`** (820px - 295px)
- **텍스트 정렬**: **좌측 중앙정렬** (`text-align: left; vertical-align: middle;`)
- **폰트 크기**: **`30px` (Regular)**
- **텍스트 레이아웃**: **`white-space: pre-line; word-break: break-word; overflow-wrap: break-word;`**
- **배경색 / 글자색**: `#FFFFFF` / `#222222`
- **패딩**: 상하 `24px` (압축 시 `22px`), 좌우 `26px`
- **단어 결속 보호**: `전문의 등과 상담할 것` 등 핵심 구문은 `&nbsp;`로 묶어 외톨이 글자(Orphan) 원천 방지.

### 4) 테이블 외곽선 및 구분선
- **상단 메인 테두리**: `3px solid #111111` (강조 실선)
- **하단 메인 테두리**: `2px solid #333333`
- **행 구분선**: `1px solid #E0E0E0`

---

## ✍️ 4. 한국어 텍스트 지능형 의미단위(Semantic) 줄바꿈 및 KCID/INCI 성분 규격

> **[KCID & INCI 100% 강제 준수 원칙]**  
> 모든 전성분 렌더링 및 형태소 분석 시, 대한민국 식품의약품안전처 고시 및 **대한화장품협회(KCID) 성분사전**, **미국화장품협회(INCI)** 공인 표준 성분명을 100% 엄격히 준수하며 임의의 글자 변형이나 오타를 원천 금지합니다.

1. **1열 라벨 2줄 분리 및 단어 결속**:
   - `기능성 화장품 심사 필 유무` ➔ `기능성 화장품<br>심사 필 유무`
   - `화장품제조업자/책임판매업자` ➔ `화장품제조업자/<br>책임판매업자`
   - `사용기한 또는 개봉 후 사용기간` ➔ `사용기한 또는<br>개봉 후 사용기간`
   - `개봉 후 사용기간`, `소비자 상담` 등 고유명사는 `&nbsp;`로 묶어 단어 분리 방지

2. **2열 제조업자/책임판매업자 `(주)` 분리 방지**:
   - 목차 순번 정규식에서 `\([가나다라마바사아자차카타파하]\)`만 인식하도록 제한하여, 법인 약칭 `(주)`가 줄바꿈되지 않고 `나우코스 / 스킨리버스랩(주)` 한 줄로 깔끔하게 정렬.

3. **2열 주의사항 문맥 결속 및 순번 자동 개행**:
   - 순번 기호 `1)`, `2)`, `3)`, `(가)`, `(나)` 앞에 자동으로 `<br>` 삽입.
   - `붉은 반점`, `이상 증상이나 부작용이 있는 경우`, `전문의 등과 상담할 것`, `피해서 보관할 것` 등 문맥상 떨어지면 안 되는 어절을 `&nbsp;`로 결속.

4. **전성분 의미단위 하이픈(`-`) 줄바꿈 (가로 여백 최적화)**:
   - 2열 본문 가로폭(525px)을 최대한 채워 우측 빈 공간(Dead Space)을 없애고 단락 균형 유지.
   - `아이소프로필아이소스테아레이트`, `하이드로제네이티드폴리아이소부텐` 등 긴 복합 성분명이 라인 끝에서 잘릴 경우, 소프트 하이픈(`&shy;`)을 통해 줄 끝에 `-`를 표시하고 다음 줄로 연결(`아이소프로필-` \n `아이소스테아레이트`).

---

## 💻 5. 파이썬 코드 연동 가이드 (API Usage)

```python
from render_notice_table_korean import render_korean_notice_table

# [방법 1. DOCX 데이터 리스트 인입]
items = [
    {"label": "내용물의 용량", "value": "25ml"},
    {"label": "제품 주요 사양", "value": "모든피부용"},
    {"label": "전성분", "value": "정제수, 글리세린, 다이프로필렌글라이콜, 아이소프로필아이소스테아레이트..."}
]
output_path = r"C:\Users\euntaewoo\Desktop\결과_상세정보고시표.png"
render_korean_notice_table("상품 상세 정보", items, output_path, max_height=2580, use_gemini=True)

# [방법 2. 기존 이미지/사진 파일 인입 (Google Vision API OCR 자동 구동)]
legacy_img_path = r"C:\Users\euntaewoo\Desktop\기존_단상자_사진.png"
render_korean_notice_table("상품 상세 정보", legacy_img_path, output_path, max_height=2580, use_gemini=True)
```
