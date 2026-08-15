import os
import sys
import subprocess
import shutil
from PIL import Image

sys.stdout.reconfigure(encoding='utf-8')

# Edge / Chrome 헤드리스 브라우저 실행 파일 경로 탐색
EDGE_PATHS = [
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Google\Chrome\Application\chrome.exe"
]

def get_browser_path():
    for p in EDGE_PATHS:
        if os.path.exists(p):
            return p
    return None

def build_notice_html(title, items, lang="EN"):
    """
    고시정보 표 표준 HTML 생성기
    - lang: "EN" (Pretendard), "JP" (Noto Sans JP), "CN" (Noto Sans SC)
    - title: 상단 제목 (예: PRODUCT DETAILS, 商品基本情報)
    - items: [{"label": "항목명", "value": "본문 내용"}, ...]
    """
    if lang.upper() == "JP":
        font_family = "'Noto Sans JP', 'NotoSansJP', 'Meiryo', sans-serif"
        title_size = "64px"
        cell_size = "32px"
        cell_padding = "24px 20px"
        val_padding = "24px 26px"
        line_height = "1.45"
        letter_spacing = "-0.2px"
    elif lang.upper() in ["CN", "ZH", "SC", "TC"]:
        font_family = "'Noto Sans SC', 'NotoSansSC', 'Source Han Sans SC', '思源黑体', 'PingFang SC', 'Microsoft YaHei', sans-serif"
        title_size = "52px"
        cell_size = "26px"
        cell_padding = "18px 16px"
        val_padding = "18px 20px"
        line_height = "1.65"
        letter_spacing = "0.6px"
    else:
        font_family = "'Pretendard', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif"
        title_size = "64px"
        cell_size = "32px"
        cell_padding = "24px 20px"
        val_padding = "24px 26px"
        line_height = "1.45"
        letter_spacing = "-0.5px"

    rows_html = ""
    for it in items:
        lbl = it.get("label", "")
        val = it.get("value", "")
        # 줄바꿈 처리
        val_formatted = val.replace("\n", "<br>")
        rows_html += f"""
        <tr>
            <th class="label-cell">{lbl}</th>
            <td class="value-cell">{val_formatted}</td>
        </tr>
        """

    html = f"""<!DOCTYPE html>
<html lang="{lang.lower()}">
<head>
    <meta charset="UTF-8">
    <style>
        @font-face {{
            font-family: 'Pretendard';
            src: local('Pretendard-Bold'), local('Pretendard Bold');
            font-weight: 700;
        }}
        @font-face {{
            font-family: 'Pretendard';
            src: local('Pretendard-Regular'), local('Pretendard Regular');
            font-weight: 400;
        }}
        @font-face {{
            font-family: 'Noto Sans JP';
            src: local('Noto Sans JP Bold'), local('NotoSansJP-Bold');
            font-weight: 700;
        }}
        @font-face {{
            font-family: 'Noto Sans JP';
            src: local('Noto Sans JP Regular'), local('NotoSansJP-Regular');
            font-weight: 400;
        }}
        @font-face {{
            font-family: 'Noto Sans SC';
            src: local('Noto Sans SC Bold'), local('NotoSansSC-Bold'), local('Source Han Sans SC Bold'), local('思源黑体 Bold');
            font-weight: 700;
        }}
        @font-face {{
            font-family: 'Noto Sans SC';
            src: local('Noto Sans SC Regular'), local('NotoSansSC-Regular'), local('Source Han Sans SC Regular'), local('思源黑体 Regular');
            font-weight: 400;
        }}

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
            padding: 45px 20px;
            color: #111111;
            -webkit-font-smoothing: antialiased;
        }}

        .notice-container {{
            width: 820px;
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
            border-bottom: 2px solid #333333;
        }}
        tr {{
            border-bottom: 1px solid #E0E0E0;
        }}
        th.label-cell {{
            width: 290px;
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
            color: #222222;
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
    return html

def render_notice_table_to_png(title, items, output_path, lang="EN", max_height=2580):
    """
    고시정보 표 렌더링 실행 함수
    - 가로 860px 고정, 세로 auto-fit
    - 2580px 초과 시 자동으로 2페이지(Part 1, Part 2) 분할 렌더링
    """
    browser_bin = get_browser_path()
    if not browser_bin:
        print("[ERROR] Headless Edge 또는 Chrome을 찾을 수 없습니다.")
        return False

    temp_html_path = output_path.replace(".png", "_temp.html")
    temp_raw_png = output_path.replace(".png", "_raw.png")

    # 1. 단일 페이지 HTML 생성 및 캡처
    full_html = build_notice_html(title, items, lang=lang)
    with open(temp_html_path, "w", encoding="utf-8") as f:
        f.write(full_html)

    # 860x4000 윈도우로 넉넉하게 캡처
    cmd = [
        browser_bin,
        "--headless=new",
        f"--screenshot={temp_raw_png}",
        "--window-size=860,4500",
        "--hide-scrollbars",
        f"file:///{os.path.abspath(temp_html_path).replace(os.sep, '/')}"
    ]
    subprocess.run(cmd, check=True)

    if not os.path.exists(temp_raw_png):
        print("[ERROR] 브라우저 스크린샷 생성 실패")
        return False

    # 2. 내용 높이(Bounding Box) 정밀 크롭
    raw_img = Image.open(temp_raw_png)
    bg = Image.new(raw_img.mode, raw_img.size, (255, 255, 255))
    from PIL import ImageChops
    diff = ImageChops.difference(raw_img, bg)
    bbox = diff.getbbox()

    if bbox:
        # 하단 여백 50px 추가
        crop_bottom = min(raw_img.size[1], bbox[3] + 50)
        cropped_img = raw_img.crop((0, 0, 860, crop_bottom))
    else:
        cropped_img = raw_img.crop((0, 0, 860, 1000))

    cur_height = cropped_img.size[1]
    print(f"[INFO] 렌더링된 고시정보 표 크기: 860 x {cur_height} px")

    # 3. 세로 2,580px 이하인 경우 -> 단일 파일 저장
    if cur_height <= max_height:
        cropped_img.save(output_path, format="PNG")
        print(f"[SUCCESS] 고시정보 표 단일 이미지 저장 완료: {output_path} (860 x {cur_height} px)")
        
        # 임시파일 정리
        if os.path.exists(temp_html_path): os.remove(temp_html_path)
        if os.path.exists(temp_raw_png): os.remove(temp_raw_png)
        return True

    # 4. 세로 2,580px 초과 시 -> [2페이지 분할 룰 적용]
    print(f"[WARNING] 세로 높이({cur_height}px)가 허용 한도({max_height}px)를 초과했습니다. 2페이지 분할 생성을 시작합니다.")
    half_idx = len(items) // 2
    items_p1 = items[:half_idx]
    items_p2 = items[half_idx:]

    base_name, ext = os.path.splitext(output_path)
    out_p1 = f"{base_name}_Part1{ext}"
    out_p2 = f"{base_name}_Part2{ext}"

    # Part 1 렌더링
    html_p1 = build_notice_html(f"{title} (1/2)", items_p1, lang=lang)
    with open(temp_html_path, "w", encoding="utf-8") as f: f.write(html_p1)
    subprocess.run(cmd, check=True)
    img_p1 = Image.open(temp_raw_png)
    bbox1 = ImageChops.difference(img_p1, bg).getbbox()
    crop_b1 = min(img_p1.size[1], bbox1[3] + 50) if bbox1 else 1000
    img_p1.crop((0, 0, 860, crop_b1)).save(out_p1, format="PNG")
    print(f"[SUCCESS] 고시정보 표 Part 1 저장 완료: {out_p1}")

    # Part 2 렌더링
    html_p2 = build_notice_html(f"{title} (2/2)", items_p2, lang=lang)
    with open(temp_html_path, "w", encoding="utf-8") as f: f.write(html_p2)
    subprocess.run(cmd, check=True)
    img_p2 = Image.open(temp_raw_png)
    bbox2 = ImageChops.difference(img_p2, bg).getbbox()
    crop_b2 = min(img_p2.size[1], bbox2[3] + 50) if bbox2 else 1000
    img_p2.crop((0, 0, 860, crop_b2)).save(out_p2, format="PNG")
    print(f"[SUCCESS] 고시정보 표 Part 2 저장 완료: {out_p2}")

    # 임시파일 정리
    if os.path.exists(temp_html_path): os.remove(temp_html_path)
    if os.path.exists(temp_raw_png): os.remove(temp_raw_png)
    return True

if __name__ == "__main__":
    print("[TEST] 표준 고시정보 렌더러 모듈 로드 완료.")
