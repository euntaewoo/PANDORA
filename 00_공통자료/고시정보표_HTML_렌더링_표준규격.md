# 📋 상품 정보 고시 표(Notice Table) 고해상도 HTML 렌더링 표준 규격서
### (영문 Pretendard / 일본어 Noto Sans JP 표준 엔진 연동 규격)

본 문서는 **프로토(Proto) 엔진, 영문(EN) 엔진, 일본어(JP) 엔진**을 포함한 모든 다국어 번역 시스템에서 상품 필수 정보 고시 표를 렌더링할 때 반드시 준수해야 하는 **공통 표준 규격서**입니다.

---

## 1. 📐 캔버스 및 해상도 표준 규격

1. **가로 픽셀 폭 (Width)**: **`860px` 고정**
2. **세로 픽셀 높이 (Height)**: **`Auto-Fit` 적용** (내용물 분량에 맞춰 유동적 자동 조정)
3. **최대 허용 세로 높이 (Max Height)**: **`2,580px` 이하 엄격 준수**
4. **🚨 2페이지 자동 분할 룰 (Two-Page Split Rule)**:
   - 전성분(Ingredients / 全成分), 주의사항, 법적 고시 내용이 방대하여 Auto-Fit 세로 높이가 **`2,580px`를 초과하는 경우**, 글자 크기를 강제로 줄여 찌그러뜨리지 말고 **무조건 2개 페이지(Part 1, Part 2)로 분할 작성**하여 개별 이미지 파일로 렌더링한다.
   - 예시:
     - `08_Product_Notice_Part1_EN.png` (860 x 2400 px)
     - `08_Product_Notice_Part2_EN.png` (860 x 1800 px)

---

## 2. 🔤 국가 및 카테고리별 표준 폰트 (Font Stack)

글로벌 이커머스 시장에서 가장 가독성이 높고 널리 쓰이는 표준 산세리프 폰트를 의무 적용합니다.

| 대상 언어 / 국가 | 지정 표준 폰트 (Standard Font) | 적용 웨이트 (Weight) | 대체 폰트 스택 (Fallback) |
| :--- | :--- | :--- | :--- |
| **🇺🇸 영문 (EN / Global)** | **`Pretendard`** | • 타이틀: **Bold (700)**<br>• 본문: **Regular (400) / Medium (500)** | `-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif` |
| **🇯🇵 일본어 (JP / Qoo10·Rakuten)** | **`Noto Sans JP`** | • 타이틀: **Bold (700)**<br>• 본문: **Regular (400) / Medium (500)** | `"Hiragino Sans", "Meiryo", sans-serif` |
| **🇨🇳 중국어 (CN / Shopee·Taobao)** | **`Alibaba PuHuiTi` (알리바바 푸후이체)** | • 타이틀: **Bold (700)**<br>• 본문: **Regular (400) / Medium (500)** | `"Noto Sans SC", "PingFang SC", "Microsoft YaHei", sans-serif` |


---

## 3. 📏 타이포그래피 및 폰트 크기 표준 규격 (Typography Specs)

모든 국가/언어 표에서 공통 적용되는 폰트 크기 계층 구조입니다.

```css
/* 상단 메인 타이틀 */
.notice-title {
    font-size: 64px;
    font-weight: 700;
    line-height: 1.2;
    text-align: center;
    color: #111111;
    margin-bottom: 40px;
}

/* 테이블 좌측 항목명 (라벨 열) */
.notice-table th, .notice-label {
    font-size: 32px;
    font-weight: 600;
    line-height: 1.4;
    color: #333333;
    background-color: #F8F9FA;
    padding: 24px 20px;
    width: 260px;
    vertical-align: middle;
}

/* 테이블 우측 본문 내용 (값 열) */
.notice-table td, .notice-value {
    font-size: 32px;
    font-weight: 400;
    line-height: 1.5;
    color: #222222;
    background-color: #FFFFFF;
    padding: 24px 28px;
    vertical-align: middle;
    word-break: keep-all;
}
```

---

## 4. 🚀 렌더링 파이프라인 (Headless Chromium / Edge)

- AI 생성형 모델의 글자 흐림(Blurry) 현상을 배제하기 위해, 고시정보 표는 **HTML ➔ Headless Browser ➔ 2x/1x 고해상도 PNG 캡처** 파이프라인을 의무 적용합니다.
- 실행 명령어 규격:
  ```bash
  msedge.exe --headless=new --screenshot=output.png --window-size=860,3000 --hide-scrollbars temp.html
  ```
- 캡처 후 Pillow를 통해 정확한 내용 영역(Content Bounding Box)을 감지하여 세로 `Auto-Fit` 및 `2,580px 초과 검사`를 수행합니다.
