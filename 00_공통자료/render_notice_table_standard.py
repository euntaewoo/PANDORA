def _smart_ingredient_hyphenator(text: str) -> str:
    """긴 복합 전성분명에 소프트 하이픈(&shy;)을 주입하여 가로폭 초과 시 의미단위 하이픈(-) 줄바꿈 유도"""
    morphemes = [
        ('아이소프로필아이소스테아레이트', '아이소프로필&shy;아이소스테아레이트'),
        ('하이드로제네이티드폴리아이소부텐', '하이드로제네이티드&shy;폴리아이소부텐'),
        ('암모늄아크릴로일다이메틸타우레이트/베헤네스-25메타크라일레이트크로스폴리머타크릴레이트크로스폴리머',
         '암모늄아크릴로일다이메틸타우레이트/&shy;베헤네스-25메타크라일레이트크로스폴리머&shy;타크릴레이트크로스폴리머'),
        ('하이드로제네이티드레시틴', '하이드로제네이티드&shy;레시틴'),
        ('글리세릴카프릴레이트', '글리세릴&shy;카프릴레이트'),
        ('토코페릴아세테이트', '토코페릴&shy;아세테이트'),
        ('하이알루로닉애씨드', '하이알루로닉&shy;애씨드'),
        ('다이소듐이디티에이', '다이소듐&shy;이디티에이'),
        ('솔비탄아이소스테아레이트', '솔비탄&shy;아이소스테아레이트'),
        ('에틸헥실글리세린', '에틸헥실&shy;글리세린'),
        ('지모뿌리추출물', '지모뿌리&shy;추출물')
    ]
    for orig, rep in morphemes:
        text = text.replace(orig, rep)
    return text

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
    elif lang.upper() in ["TW", "HK", "TC"]:
        font_family = "'Noto Sans TC', 'NotoSansTC', 'Source Han Sans TC', '思源黑體', 'PingFang TC', 'Microsoft JhengHei', sans-serif"
        title_size = "52px"
        cell_size = "26px"
        cell_padding = "20px 15px"
        val_padding = "20px 22px"
        line_height = "1.65"
        letter_spacing = "0.6px"
        label_width = "300px"
    elif lang.upper() in ["CN", "ZH", "SC"]:
        font_family = "'Noto Sans SC', 'NotoSansSC', 'Source Han Sans SC', '思源黑体', 'PingFang SC', 'Microsoft YaHei', sans-serif"
        title_size = "52px"
        cell_size = "26px"
        cell_padding = "20px 15px"
        val_padding = "20px 22px"
        line_height = "1.65"
        letter_spacing = "0.6px"
        label_width = "300px"
    else:  # EN / KO (영문 및 한국어 고시표 표준: Pretendard 64px/32px)
        font_family = "'Pretendard', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif"
        title_size = "60px"
        cell_size = "30px"
        cell_padding = "24px 20px"
        val_padding = "24px 26px"
        line_height = "1.5"
        letter_spacing = "-0.5px"
        label_width = "295px"

    rows_html = ""
    for it in items:
        lbl = it.get("label", "")
        val = it.get("value", "")
        # 💡 업데이트: 2열 의미단위 보호 및 순번 강제 줄바꿈
        val_str = str(val)
        if "성분" in lbl or "Ingredients" in lbl or "成分" in lbl:
            val_str = _smart_ingredient_hyphenator(val_str)
        # 💡 기능성/특수용도 심사 항목의 괄호 효능 부가설명 앞 강제 줄바꿈 (KO/CN/TW/JP/EN 전 언어 공통)
        if any(k in lbl for k in ["기능성", "심사", "审查", "審查", "審査", "Functional", "Review", "含藥"]):
            val_str = re.sub(r'(?<!<br>)\s*([（(])', r'<br>\1', val_str)
        val_str = val_str.replace('식품의약품안전처 심사 필 완료 (', '식품의약품안전처 심사 필 완료<br>(')
        val_str = val_str.replace('식품의약품안전처 심사 필 무 (', '식품의약품안전처 심사 필 무<br>(')
        val_str = val_str.replace('붉은 반점', '붉은&nbsp;반점')
        val_str = val_str.replace('이상 증상', '이상&nbsp;증상')
        val_str = val_str.replace('부작용이 있는', '부작용이&nbsp;있는')
        val_str = val_str.replace('전문의 등과', '전문의&nbsp;등과')
        val_str = val_str.replace('상담할 것', '상담할&nbsp;것')
        val_str = val_str.replace('부위 등에는', '부위&nbsp;등에는')
        val_str = val_str.replace('자제할 것', '자제할&nbsp;것')
        val_str = val_str.replace('닿지 않는 곳에', '닿지&nbsp;않는&nbsp;곳에')
        val_str = val_str.replace('보관할 것', '보관할&nbsp;것')
        val_str = val_str.replace('피해서 보관', '피해서&nbsp;보관')
        val_str = val_str.replace('심사 필 완료', '심사&nbsp;필&nbsp;완료')
        val_str = val_str.replace('2중 기능성', '2중&nbsp;기능성')
        val_str = val_str.replace('분쟁해결 규정에', '분쟁해결&nbsp;규정에')
        val_str = val_str.replace('분쟁해결 기준에', '분쟁해결&nbsp;기준에')
        val = re.sub(r'(?<!^)(?<!<br>)(?<!\n)\s*(\(\d+\)|\d+\)|[①-⑳]|\([가나다라마바사아자차카타파하甲乙丙丁a-zA-Z]\)|[㈎-㈛])', r'<br>\1', val_str)
        # 줄바꿈 및 리스트 서식 처리
        val_formatted = val.replace("\n", "<br>")
        # <br><br> 중복 정리
        val_formatted = re.sub(r'(<br>\s*)+', '<br>', val_formatted).strip()
        if val_formatted.startswith("<br>"):
            val_formatted = val_formatted[4:]
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
        @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;700&family=Noto+Sans+SC:wght@400;700&family=Noto+Sans+TC:wght@400;700&display=swap');

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
            padding: 0;
            color: #111111;
            -webkit-font-smoothing: antialiased;
        }}

        .notice-container {{
            width: 860px;
            padding: 15px 20px 20px 20px;
            box-sizing: border-box;
            background-color: #FFFFFF;
        }}
        .title {{
            font-size: {title_size};
            font-weight: 700;
            text-align: center;
            letter-spacing: {letter_spacing};
            margin-bottom: 30px;
            margin-top: 15px;
            color: #111111;
        }}
        table {{
            table-layout: fixed;
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
            word-break: break-word;
            overflow-wrap: break-word;
            border-right: 1px solid #EAEAEA;
        }}
        td.value-cell.ingredients {{
            word-break: break-word;
            overflow-wrap: break-word;
            text-align: left;
            line-height: 1.55;
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
            word-break: break-word;
            overflow-wrap: break-word;
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
    고시정보 표 렌더링 실행 함수 (Html2Image / Playwright 기반 표준)
    - 가로 860px 고정, 세로 auto-fit (max 2,580px 이하 1장 수납 원칙)
    - [1열 너비 기준]: 언어별 최적화 폭 적용 (KO/EN: 295px)
    - [의미단위 줄바꿈]: 복합 항목은 의미 단위 <br> 개행 및 전성분 스마트 하이픈(-) 적용
    - 2580px 초과 시 지능형 행간 압축 및 2페이지(Part 1, Part 2) 분할 렌더링
    """
    if lang.upper() in ["KO", "KR"]:
        try:
            import render_notice_table_korean as rntk
            rntk.render_korean_notice_table(title, items, output_path, max_height=max_height, use_gemini=True)
            return True
        except Exception as e:
            print(f"[WARN] 한국어 전용 렌더러 호출 실패, 표준 렌더러로 계속: {e}")

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
