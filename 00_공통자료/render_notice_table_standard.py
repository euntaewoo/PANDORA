import os
import sys
import html
import re
from html2image import Html2Image
from PIL import Image, ImageChops

sys.stdout.reconfigure(encoding='utf-8')

def build_notice_html(title, items, lang="EN"):
    """
    고시정보 표 표준 HTML 생성기
    - lang: "EN" (Pretendard), "JP" (Noto Sans JP), "CN" (Noto Sans SC), "KO" (Pretendard)
    - title: 상단 제목 (예: PRODUCT DETAILS, PRODUCT SPECIFICATIONS, 상품 상세 정보)
    - items: [{"label": "항목명", "value": "본문 내용"}, ...]
    """
    if lang.upper() == "JP":
        font_family = "'Noto Sans JP', 'NotoSansJP', 'Meiryo', sans-serif"
        title_size = "64px"
        cell_size = "32px"
        cell_padding = "24px 20px"
        val_padding = "24px 26px"
        line_height = "1.5"
        letter_spacing = "-0.2px"
        label_width = "280px"
    elif lang.upper() in ["CN", "ZH", "SC", "TC"]:
        font_family = "'Noto Sans SC', 'NotoSansSC', 'Source Han Sans SC', '思源黑体', 'PingFang SC', 'Microsoft YaHei', sans-serif"
        title_size = "52px"
        cell_size = "26px"
        cell_padding = "20px 18px"
        val_padding = "20px 22px"
        line_height = "1.65"
        letter_spacing = "0.6px"
        label_width = "275px"
    else:  # EN / KO (영문 및 한국어 고시표 표준: Pretendard 64px/32px)
        font_family = "'Pretendard', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif"
        title_size = "64px"
        cell_size = "32px"
        cell_padding = "24px 20px"
        val_padding = "24px 26px"
        line_height = "1.5"
        letter_spacing = "-0.5px"
        label_width = "295px"

    rows_html = ""
    for it in items:
        lbl = it.get("label", "")
        val = it.get("value", "")
        # 줄바꿈 및 리스트 서식 처리
        val_formatted = val.replace("\n", "<br>")
        rows_html += f"""
        <tr>
            <th class="label-cell">{lbl}</th>
            <td class="value-cell">{val_formatted}</td>
        </tr>
        """

    html_content = f"""<!DOCTYPE html>
<html lang="{lang.lower()}">
<head>
    <meta charset="UTF-8">
    <style>
        @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
        @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;700&family=Noto+Sans+SC:wght@400;700&display=swap');

        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}
        body {{
            background-color: #FFFFFF;
            font-family: {font_family};
            width: 860px;
            margin: 0;
            padding: 45px 25px;
            color: #111111;
            -webkit-font-smoothing: antialiased;
        }}

        .notice-container {{
            width: 810px;
            margin: 0 auto;
        }}
        .title {{
            font-size: {title_size};
            font-weight: 700;
            text-align: center;
            letter-spacing: {letter_spacing};
            margin-bottom: 40px;
            color: #111111;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            border-top: 3px solid #111111;
            border-bottom: 3px solid #111111;
        }}
        tr {{
            border-bottom: 1px solid #E0E0E0;
        }}
        tr:last-child {{
            border-bottom: none;
        }}
        th.label-cell {{
            width: {label_width};
            background-color: #F8F9FA;
            font-size: {cell_size};
            font-weight: 700;
            color: #333333;
            padding: {cell_padding};
            text-align: left;
            vertical-align: middle;
            line-height: {line_height};
            letter-spacing: {letter_spacing};
            word-break: keep-all;
            border-right: 1px solid #EAEAEA;
        }}
        td.value-cell {{
            font-size: {cell_size};
            font-weight: 400;
            color: #333333;
            padding: {val_padding};
            text-align: left;
            vertical-align: middle;
            line-height: {line_height};
            letter-spacing: {letter_spacing};
            word-break: keep-all;
            background-color: #FFFFFF;
        }}

    </style>
</head>

<body>
    <div class="notice-container">
        <div class="title">{title}</div>
        <table>
            <tbody>
                {rows_html}
            </tbody>
        </table>
    </div>
</body>
</html>
"""
    return html_content

def _render_single_html_to_image(html_content, output_path):
    output_dir = os.path.dirname(os.path.abspath(output_path))
    os.makedirs(output_dir, exist_ok=True)
    filename = os.path.basename(output_path)
    temp_html_path = os.path.join(output_dir, f"temp_{filename}.html")

    with open(temp_html_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    try:
        hti = Html2Image(size=(860, 4500))
        hti.output_path = output_dir
        hti.screenshot(html_file=temp_html_path, save_as=filename)

        if not os.path.exists(output_path):
            return 0

        img = Image.open(output_path)
        bg = Image.new(img.mode, img.size, (255, 255, 255))
        diff = ImageChops.difference(img, bg)
        bbox = diff.getbbox()

        if bbox:
            crop_bottom = min(img.size[1], bbox[3] + 45)
            cropped_img = img.crop((0, 0, 860, crop_bottom))
        else:
            cropped_img = img.crop((0, 0, 860, 1000))

        cropped_img.save(output_path, format="PNG")
        return cropped_img.size[1]
    finally:
        if os.path.exists(temp_html_path):
            os.remove(temp_html_path)

def render_notice_table_to_png(title, items, output_path, lang="EN", max_height=2580):
    """
    고시정보 표 렌더링 실행 함수 (Html2Image 기반 표준)
    - 가로 860px 고정, 세로 auto-fit (max 2,580px 이하 1장 수납 원칙)
    - [1열 너비 기준]: 언어별 최적화 폭 적용
    - [의미단위 줄바꿈]: 복합 항목은 의미 단위 <br> 개행
    - 2580px 초과 시 지능형 2페이지(Part 1, Part 2) 분할 렌더링
    """
    # 1. 단일 이미지로 렌더링 시도
    full_html = build_notice_html(title, items, lang=lang)
    cur_height = _render_single_html_to_image(full_html, output_path)

    if cur_height <= max_height and cur_height > 0:
        print(f"[SUCCESS] 고시정보 표 단일 이미지 저장 완료: {output_path} (860 x {cur_height} px)")
        return True

    # 2. 2,580px 초과 시 -> 지능형 2페이지 분할
    print(f"[INFO] 세로 높이({cur_height}px)가 허용 한도({max_height}px)를 초과하여 지능형 2페이지 분할을 수행합니다.")
    
    # 전성분(Ingredients) 위치 탐색
    split_idx = len(items) // 2
    for idx, it in enumerate(items):
        lbl_lower = it.get("label", "").lower()
        if "ingredient" in lbl_lower or "전성분" in lbl_lower or "全成分" in lbl_lower or "成分" in lbl_lower:
            # 전성분까지를 Part 1에 포함 (idx + 1)
            split_idx = idx + 1
            break

    items_p1 = items[:split_idx]
    items_p2 = items[split_idx:]

    base_name, ext = os.path.splitext(output_path)
    # 기존에 단일로 저장되었던 파일 삭제
    if os.path.exists(output_path):
        os.remove(output_path)

    out_p1 = f"{base_name}_Part1{ext}"
    out_p2 = f"{base_name}_Part2{ext}"

    # Part 1 렌더링
    html_p1 = build_notice_html(f"{title} (1/2)", items_p1, lang=lang)
    h1 = _render_single_html_to_image(html_p1, out_p1)
    print(f"[SUCCESS] 고시정보 표 Part 1 저장 완료: {out_p1} (860 x {h1} px)")

    # Part 2 렌더링
    html_p2 = build_notice_html(f"{title} (2/2)", items_p2, lang=lang)
    h2 = _render_single_html_to_image(html_p2, out_p2)
    print(f"[SUCCESS] 고시정보 표 Part 2 저장 완료: {out_p2} (860 x {h2} px)")

    return True

if __name__ == "__main__":
    print("[TEST] 표준 고시정보 렌더러 모듈 준비 완료.")
