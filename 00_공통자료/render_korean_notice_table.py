import os
import sys
import docx
import html
import re
from html2image import Html2Image
from PIL import Image, ImageChops

sys.stdout.reconfigure(encoding='utf-8')

def apply_semantic_breaks(txt):
    replacements = {
        '사용기한 또는 개봉 후 사용기간': '사용기한 또는<br>개봉 후 사용기간',
        '사용기한 또는 \\n개봉 후 사용기간': '사용기한 또는<br>개봉 후 사용기간',
        '사용기한 또는 \\\n개봉 후 사용기간': '사용기한 또는<br>개봉 후 사용기간',
        '화장품제조업자 / 책임판매업자': '화장품제조업자 /<br>책임판매업자',
        '화장품제조업자 및 책임판매업자': '화장품제조업자 및<br>책임판매업자',
        '화장품제조업자 및 화장품책임판매업자': '화장품제조업자 및<br>화장품책임판매업자',
        '기능성 화장품 심사 필 유무': '기능성 화장품<br>심사 필 유무',
        '기능성화장품 심사 필 유무': '기능성 화장품<br>심사 필 유무',
        '사용할 때의 주의사항': '사용할 때의<br>주의사항',
        '소비자 상담 전화번호': '소비자 상담<br>전화번호',
        '소비자상담 관련 전화번호': '소비자상담 관련<br>전화번호'
    }
    for k, v in replacements.items():
        if k in txt:
            return v
    return txt

def render_korean_notice(doc_path, output_png_path):
    output_dir = os.path.dirname(os.path.abspath(output_png_path))
    os.makedirs(output_dir, exist_ok=True)
    temp_html = os.path.join(output_dir, "temp_korean_notice.html")
    filename = os.path.basename(output_png_path)

    doc = docx.Document(doc_path)
    table = doc.tables[0]

    rows_html = ""
    start_row = 1 if table.rows[0].cells[0].text.strip() in ['항목', '구분'] else 0
    for row in table.rows[start_row:]:
        cells = row.cells
        if len(cells) >= 2:
            k = cells[0].text.strip()
            v = cells[1].text.strip()

            k_formatted = apply_semantic_breaks(html.escape(k))
            v_escaped = html.escape(v)

            # 1) 2) 번호 및 가. 나. 서식 처리
            v_formatted = re.sub(r'([1-9]\))', r'<br>\1', v_escaped)
            v_formatted = re.sub(r'(㈎|㈏|㈐)', r'<br>&nbsp;&nbsp;\1', v_formatted)
            v_formatted = v_formatted.replace('\\n', '<br>').replace('\n', '<br>')
            v_formatted = re.sub(r'(<br>\s*)+', '<br>', v_formatted).strip('<br>')

            rows_html += f"""
            <tr>
                <th class="label-cell">{k_formatted}</th>
                <td class="value-cell">{v_formatted}</td>
            </tr>
            """

    full_html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <style>
        @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}
        body {{
            background-color: #FFFFFF;
            font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
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
            font-size: 64px;
            font-weight: 700;
            text-align: center;
            letter-spacing: -0.5px;
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
            width: 295px;
            background-color: #F8F9FA;
            font-size: 32px;
            font-weight: 700;
            color: #333333;
            padding: 24px 20px;
            text-align: left;
            vertical-align: middle;
            line-height: 1.5;
            letter-spacing: -0.3px;
            word-break: keep-all;
            border-right: 1px solid #EAEAEA;
        }}
        td.value-cell {{
            font-size: 32px;
            font-weight: 400;
            color: #333333;
            padding: 24px 26px;
            text-align: left;
            vertical-align: middle;
            line-height: 1.5;
            letter-spacing: -0.3px;
            word-break: keep-all;
            background-color: #FFFFFF;
        }}
    </style>
</head>
<body>
    <div class="notice-container">
        <div class="title">상품 상세 정보</div>
        <table>
            <tbody>
                {rows_html}
            </tbody>
        </table>
    </div>
</body>
</html>
"""

    with open(temp_html, 'w', encoding='utf-8') as f:
        f.write(full_html)

    try:
        hti = Html2Image(size=(860, 4500))
        hti.output_path = output_dir
        hti.screenshot(html_file=temp_html, save_as=filename)

        img = Image.open(output_png_path)
        bg = Image.new(img.mode, img.size, (255, 255, 255))
        diff = ImageChops.difference(img, bg)
        bbox = diff.getbbox()

        if bbox:
            crop_bottom = min(img.size[1], bbox[3] + 45)
            cropped_img = img.crop((0, 0, 860, crop_bottom))
        else:
            cropped_img = img.crop((0, 0, 860, 1000))

        cropped_img.save(output_png_path, format='PNG')
        print(f"[SUCCESS] 한국어 고시정보표 렌더링 완료: {output_png_path} (860 x {cropped_img.size[1]} px)")
        return cropped_img.size[1]
    finally:
        if os.path.exists(temp_html):
            os.remove(temp_html)

if __name__ == '__main__':
    doc_file = r'01_번역대상_원본\05_Multi Corrective Eye cream\05. 멀티코렉티브 아이크림 -Multi Corrective Eye cream\010_PDP_상품상세정보.docx'
    out_file = r'01_번역대상_원본\05_Multi Corrective Eye cream\05. 멀티코렉티브 아이크림 -Multi Corrective Eye cream\010_PDP_상품상세정보_테이블.png'
    render_korean_notice(doc_file, out_file)
