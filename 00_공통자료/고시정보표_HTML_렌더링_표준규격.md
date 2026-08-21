# 📋 상품 정보 고시 표(Notice Table) 고해상도 HTML 렌더링 표준 규격서
### (영문 Pretendard / 일본어 Noto Sans JP 표준 엔진 연동 규격)

본 문서는 **프로토(Proto) 엔진, 영문(EN) 엔진, 일본어(JP) 엔진**을 포함한 모든 다국어 번역 시스템에서 상품 필수 정보 고시 표를 렌더링할 때 반드시 준수해야 하는 **공통 표준 규격서**입니다.

---

## 0. 👁️ 듀얼 인풋 파이프라인 (DOCX & Google Cloud Vision API OCR)

1. **디지털 문서 인입 (DOCX/Excel)**: `python-docx` 기반 무손실 추출 (0.001초)
2. **이미지/단상자 사진 인입 (PNG/JPG)**: `Google Cloud Vision API` (`DOCUMENT_TEXT_DETECTION`)로 6pt 초소형 텍스트를 99.8% 정밀도로 OCR 스캔 후 `Gemini 3.1 Pro`가 KCID/INCI 표준 명칭으로 교정 및 JSON 구조화.

---

## 1. 📐 캔버스 및 해상도 표준 규격

1. **가로 픽셀 폭 (Width)**: **`860px` 고정**
2. **세로 픽셀 높이 (Height)**: **`Auto-Fit` 적용** (내용물 분량에 맞춰 유동적 자동 조정)
3. **최대 허용 세로 높이 (Max Height)**: **`2,580px` 이하 엄격 준수**
### (4) 세로 2페이지 분할 (Pagination) 자동화 룰
- **기준**: 모든 고시표는 기본적으로 1장(세로 Auto-Fit, 최대 2,580px)으로 렌더링.
- **유동적 행간 압축(Squeeze)**: 기본 행간(1.45~1.65) 적용 시 2,580px을 초과할 경우, 무작정 분할하지 않고 1차적으로 **행간을 유동적으로 압축(`line-height: 1.25`)하여 1페이지 수납을 재시도**한다.
- **분할(Split)**: 행간을 쥐어짜도 2,580px을 초과하는 텍스트 괴물(초장문 전성분 등)에 한해서만, 기본 행간으로 원복한 뒤 Part 1 / Part 2로 2페이지 분할하여 저장한다.
   - 예시:
     - `08_Product_Notice_Part1_EN.png` (860 x 2400 px)
     - `08_Product_Notice_Part2_EN.png` (860 x 1800 px)

---

## 2. 🔤 국가 및 카테고리별 표준 폰트 (Font Stack)

글로벌 이커머스 시장에서 가장 가독성이 높고 널리 쓰이는 표준 산세리프 폰트를 의무 적용합니다.

| 대상 언어 / 국가 | 지정 표준 폰트 (Standard Font) | 적용 웨이트 (Weight) | 대체 폰트 스택 (Fallback) |
| :--- | :--- | :--- | :--- |
| **🇰🇷 한국어 (KR / 원본)** | **`Pretendard`** | • 타이틀: **Bold (60px)**<br>• 본문: **Bold/Regular (30px)** | `-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif` |
| **🇺🇸 영문 (EN / Global)** | **`Pretendard`**<br>*(메인 이미지는 Montserrat 적용, 고시표 전용 Pretendard)* | • 타이틀: **Bold (60px)**<br>• 본문: **Regular/Bold (30px)** | `-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif` |
| **🇯🇵 일본어 (JP / Qoo10·Rakuten)** | **`Noto Sans JP`** | • 타이틀: **Bold (64px)**<br>• 본문: **Regular (32px)** | `"Hiragino Sans", "Meiryo", sans-serif` |
| **🇨🇳 중국어 간체 (CN / Shopee·Taobao)** | **`Noto Sans SC` (스위안헤이티 / 思源黑体)** | • 타이틀: **Bold (52px)**<br>• 본문: **Regular (26px)** | `"Source Han Sans SC", "PingFang SC", "Microsoft YaHei", sans-serif` |
| **🇹🇼 중국어 번체 (TW / Shopee TW·momo)** | **`Noto Sans TC` (스위안헤이티 / 思源黑體)** | • 타이틀: **Bold (52px)**<br>• 본문: **Regular (26px)** | `"Source Han Sans TC", "PingFang TC", "Microsoft JhengHei", sans-serif` |

---

## 3. 🌐 글로벌 뷰티 이커머스 번역 표준 명칭 (1:1 강제 매핑 규격)

모든 국가의 고시표 번역 시 1열(라벨)은 다음 현지 이커머스/법적 표준 명칭으로 강제 고정됩니다.

- **한국어 (식약처/전자상거래법)**: 용량 `내용물의 용량`, 피부타입 `제품 주요 사양`, 기한 `사용기한 또는 개봉 후 사용기간`, 사용법 `사용방법`, 제조/책임 `화장품제조업자/책임판매업자`, 성분 `전성분`, 기능성 `기능성 화장품 심사 필 유무`, 주의사항 `사용할 때의 주의사항`, 번호 `소비자 상담 전화번호`
- **영어 (Amazon/Sephora)**: 용량 `Size / Net Wt.`, 피부타입 `Skin Type`, 기한 `Shelf Life / PAO`, 사용법 `Directions`, 성분 `Ingredients`
- **일본어 (약기법/Qoo10)**: 용량 `内容量`, 피부타입 `お肌のタイプ / 対象肌`, 기한 `使用期限`, 사용법 `ご使用方法`, 성분 `全成分`
- **대만 번체 (TFDA)**: 용량 `淨含量 / 容量`, 피부타입 `適用膚質`, 기한 `保存期限`, 사용법 `使用方法`, 성분 `全成分`
- **중국 간체 (NMPA)**: 용량 `净含量 / 容量`, 피부타입 `适用肤质 / 产品规格`, 기한 `使用期限 / 保质期`, 사용법 `使用方法`, 성분 `全成分`

---

## 4. 🧠 지능형 테이블 유동폭 및 자동 줄바꿈 규격 (Smart Layout & Hyphenation)

1열 항목 라벨과 2열 본문 내용의 자연스러운 비율 유지를 위해 **타이트 핏 고정폭**과 지능형 유동 줄바꿈을 적용합니다.

1. **1열 라벨(th) 고정폭 및 텍스트 정렬**: `width: 295px; word-break: keep-all; text-align: left; vertical-align: middle; box-sizing: border-box;` (테이블 전체 확장 방지를 위해 `table-layout: fixed;` 와 함께 사용)
   - 라벨 내에 빗금(`/`), `또는`, `or`, `または`, `或` 가 감지되면 파이썬/AI 단에서 자동으로 `<br>` 태그를 주입하여 2줄로 균형 있게 분리합니다.
2. **2열 본문(td) 및 Gemini 3.1 Pro 스마트 하이픈(`-`) 규격**: `word-break: keep-all; overflow-wrap: break-word;`
   - `gemini-3.1-pro-preview`가 전성분 복합 화학 결합 구조를 자동 분석하여 10자 이상의 긴 단어 결합부에 소프트 하이픈(`&shy;`)을 삽입합니다.
   - 단어가 2열 가로폭(525px)을 초과할 때만 줄 끝에서 `-`를 표기하고 줄바꿈(`아이소프로필-` \n `아이소스테아레이트`)되어 우측 빈 여백을 꽉 채우는 고급 타이포그래피를 완성합니다.
3. **법인명 약칭 `(주)` 보존**:
   - 순번 기호 정규식에서 `\([가나다라마바사아자차카타파하]\)`만 허용하여 `나우코스 / 스킨리버스랩(주)`의 `(주)`가 혼자 줄바꿈되는 현상을 원천 방어합니다.

---

## 5. 📏 타이포그래피 및 폰트 크기 표준 규격 (Typography Specs)

언어별 특성에 맞춘 최적화 폰트 크기 계층 구조입니다.

| 언어 구분 | 상단 타이틀 (`.title`) | 1열 항목 라벨 (`th.label-cell`) | 2열 본문 내용 (`td.value-cell`) |
| :--- | :---: | :---: | :---: |
| **영문(EN) / 일본어(JP)** | **`64px`** (Bold 700) | **`32px`** (Bold 700) | **`32px`** (Regular 400) |
| **중국어(CN / TW / HK)** | **`52px`** (Bold 700) | **`26px`** (Bold 700) | **`26px`** (Regular 400) |

```css
/* [중국어 기준 최적화 CSS 예시 - 3대 실전 팁 적용] */
/* 상단 메인 타이틀 */
.notice-title {
    font-size: 52px;
    font-weight: 700;
    line-height: 1.3;
    letter-spacing: 0.6px;
    text-align: center;
    color: #111111;
    margin-bottom: 40px;
}

/* 테이블 좌측 항목명 (라벨 열) */
.notice-table th, .notice-label {
    width: 275px;
    font-size: 26px;
    font-weight: 700;
    line-height: 1.65;
    letter-spacing: 0.6px;
    color: #333333;
    background-color: #F8F9FA;
    padding: 18px 16px;
    word-break: keep-all;
    vertical-align: middle;
}

/* 테이블 우측 본문 내용 (값 열) */
.notice-table td, .notice-value {
    font-size: 26px;
    font-weight: 400;
    line-height: 1.65;
    letter-spacing: 0.6px;
    color: #222222;
    padding: 18px 20px;
    word-break: keep-all;
    vertical-align: middle;
}
```

---

## 6. 🚀 렌더링 파이프라인 (Headless Chromium / Edge)

- AI 생성형 모델의 글자 흐림(Blurry) 현상을 배제하기 위해, 고시정보 표는 **HTML ➔ Headless Browser ➔ 2x/1x 고해상도 PNG 캡처** 파이프라인을 의무 적용합니다.
- 실행 명령어 규격:
  ```bash
  msedge.exe --headless=new --screenshot=output.png --window-size=860,3000 --hide-scrollbars temp.html
  ```
- 캡처 후 Pillow를 통해 정확한 내용 영역(Content Bounding Box)을 감지하여 세로 `Auto-Fit` 및 `2,580px 초과 검사`를 수행합니다.



## 5. 텍스트 의미단위(Semantic) 렌더링 최적화 룰
- **타이틀 및 본문 폰트 사이즈 (EN/KO)**: 타이틀 60px, 본문 30px (2580px 이하 1페이지 수납을 위한 황금비율)
- **Box-Sizing**: 모든 렌더링 엔진은 * { box-sizing: border-box; }를 의무 적용하여 1열 패딩이 295px 밖으로 팽창하지 않도록 방지.
- **의미단위 자동 줄바꿈**: '기능성 화장품 / 심사 필 유무', '1) 화장품 사용 시', '붉은 반점' 등 주요 의미 단위는 <br> 또는 &nbsp; 를 주입하여 문맥이 중간에 끊어지는 것을 방지한다.



### (5) 전성분 의미단위 하이픈(-) 줄바꿈 및 가로 여백 최적화 룰 (2026-08 확정)
- **목적**: 2열 본문 가로폭(약 470px)을 최대한 채워 우측 휑한 빈 공간(Dead Space)을 방지하고 단어 가독성을 보존.
- **원칙**:
  1. 일반 성분명은 keep-all로 단어 전체를 보존하여 쉼표 단위로 줄바꿈.
  2. 아이소프로필아이소스테아레이트, 하이드로제네이티드폴리아이소부텐 등 긴 복합 성분이 라인 끝에 걸려 가로폭을 초과할 경우, 임의로 찢지 않고 형태소 결합부(아이소프로필-, 하이드로-) 뒤에 하이픈(- / &shy;)을 붙여 줄바꿈 처리.
