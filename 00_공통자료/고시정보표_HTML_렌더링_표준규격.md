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

1열 항목 라벨과 2열 본문 내용의 자연스러운 비율 유지를 위해 **언어별 최적화 너비**와 지능형 샌드박스 줄바꿈을 적용합니다.

1. **1열 라벨(th) 최적 너비 및 텍스트 정렬**:
   - **중국어 간체(CN)**: `width: 270px; padding: 20px 15px;` (좌우 여백 30px, 2열 순수 본문 폭 520px 극대화 황금비율)
   - **중국어 번체(TW/HK)**: `width: 300px; padding: 20px 15px;` (좌우 여백 30px, 방괴자 11자 복합 라벨 완벽 수용)
   - **한국어/영문(KO/EN)**: `width: 295px; padding: 24px 20px;` (Pretendard 긴 라벨 2줄 황금분할)
   - **일본어(JP)**: `width: 280px; padding: 24px 20px;` (Noto Sans JP 32px 기준)
   - **정렬 기준**: `text-align: left; vertical-align: middle; word-break: break-word; overflow-wrap: break-word;`
   - **단문 라벨 1줄 유지 원칙**: 10자 미만 라벨(`使用注意事项` 6자, `消费者咨询电话` 7자, `使用方法` 4자)은 절대 2줄로 쪼개지 않고 **100% 1줄 유지**.
   - **10자 이상 긴 라벨 분할**: `特殊用途化妆品<br>审查状态`, `化妆品生产企业 /<br>责任销售商` 등 의미 단위 2줄 황금 분할.
2. **2열 본문(td) 폭 확장 및 단어 결속 보호**:
   - 중국어 간체 기준 2열 순수 본문 폭을 **`520px`**로 확장 (`val_padding: 20px 15px`, `letter-spacing: 0px`).
   - 주의사항 1번 문단 등 장문 텍스트가 억지 개행 없이 정확히 3줄로 자연스럽게 안착.
   - 전문의 상담 어휘(`专业医生`, `专业医师`, `전문의 등과 상담할 것`) 등 문장 끝 핵심 구문은 `<span style="white-space: nowrap">` 또는 `&nbsp;`로 묶어 외톨이 글자(Orphan) 원천 차단.
3. **법인명 약칭 `(주)` 보존**:
   - 순번 기호 정규식에서 `\([가나다라마바사아자차카타파하]\)`만 허용하여 `나우코스 / 스킨리버스랩(주)`의 `(주)`가 혼자 줄바꿈되는 현상을 원천 방어합니다.
4. **기능성/특수용도 심사 본문 부가설명 괄호 `(...)` 앞 강제 줄바꿈 (Functional Cosmetics Semantic Line-Break)**:
   - 심사 기관의 심사 완료 상태 텍스트(예: `식품의약품안전처 심사 필 완료`, `已完成韩国食品药品安全处审查`, `已完成韓國食品藥物安全處審查`, `Completed review by MFDS`)와 효능 부가설명 괄호 구문(`(미백, 주름개선...)`, `(美白、改善皱纹...)`)은 서로 다른 의미 단위이므로, 괄호 `(` 또는 `（` 앞에서 파이썬/HTML 렌더러가 100% 무조건 강제 개행(`<br>`)을 주입하여 가독성을 보장합니다.
5. **고시정보표 전담 프론트엔드 QA 서브에이전트 연동**:
   - 1차 렌더링 직후 `notice_table_frontend_qa_agent`가 PNG 산출물을 `view_file`로 자동 디코딩하여 1열 라벨 규격, 10자 미만 1줄 유지, 외톨이 글자 유무를 픽셀 단위로 자가 검수하고 결함 발견 시 자동 교정.

---

## 5. 📏 타이포그래피 및 폰트 크기 표준 규격 (Typography Specs)

언어별 특성에 맞춘 최적화 폰트 크기 계층 구조입니다.

| 언어 구분 | 상단 타이틀 (`.title`) | 1열 항목 라벨 (`th.label-cell`) | 2열 본문 내용 (`td.value-cell`) |
| :--- | :---: | :---: | :---: |
| **영문(EN) / 일본어(JP)** | **`60~64px`** (Bold 700) | **`30~32px`** (Bold 700) | **`30~32px`** (Regular 400) |
| **중국어(CN / TW / HK)** | **`52px`** (Bold 700) | **`26px`** (Bold 700, 폭 300px) | **`26px`** (Regular 400, 폭 490px) |

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
