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

def _format_label_semantic_break(lbl: str, lang: str) -> str:
    lbl_str = str(lbl).strip()
    if "<br>" in lbl_str:
        return lbl_str
    
    lang_upper = str(lang).upper()

    # ==========================================
    # [SANDBOX 1] 중국어 간체 (CN / ZH / SC) 전용 샌드박스 (10자 이상 긴 라벨만 개행)
    # ==========================================
    if lang_upper in ["CN", "ZH", "SC"]:
        if len(lbl_str) >= 10:
            if any(k in lbl_str for k in ["特殊用途", "含药", "审查", "特证"]):
                lbl_str = re.sub(r'(特殊用途化妆品|特殊用途|含药化妆品)\s*(审查状态|审查|备案状态)', r'\1<br>\2', lbl_str)
            if any(k in lbl_str for k in ["生产企业", "责任销售商", "生产者"]):
                lbl_str = re.sub(r'(化妆品生产企业|生产企业|生产商)\s*([/＆& 및\s]+)\s*(责任销售商|境内责任人|销售商)', r'\1 \2<br>\3', lbl_str)
            if any(k in lbl_str for k in ["使用期限", "保质期", "有效期"]):
                lbl_str = re.sub(r'(使用期限|保质期|有效期)\s*(或|及|或开封后)\s*(开封后|开盖后)?', r'\1 \2<br>\3', lbl_str)
        return lbl_str

    # ==========================================
    # [SANDBOX 2] 중국어 번체 (TW / HK / TC) 전용 샌드박스 (10자 이상 긴 라벨만 개행)
    # ==========================================
    elif lang_upper in ["TW", "HK", "TC"]:
        if len(lbl_str) >= 10:
            if any(k in lbl_str for k in ["特殊用途", "含藥", "審查", "許可證"]):
                lbl_str = re.sub(r'(特殊用途化妝品|特殊用途|含藥化粧品|特定用途化粧品)\s*(審查狀態|審查|許可字號)', r'\1<br>\2', lbl_str)
            if any(k in lbl_str for k in ["生產企業", "責任銷售商", "製造廠", "進口商"]):
                lbl_str = re.sub(r'(化妝品生產企業|製造廠|生產商)\s*([/＆& 及\s]+)\s*(責任銷售商|進口商|總代理)', r'\1 \2<br>\3', lbl_str)
            if any(k in lbl_str for k in ["保存期限", "有效期間", "使用期限"]):
                lbl_str = re.sub(r'(保存期限|有效期間|使用期限)\s*(或|及)\s*(開封後|開蓋後)?', r'\1 \2<br>\3', lbl_str)
        return lbl_str

    # ==========================================
    # [SANDBOX 3] 일본어 (JP) 전용 샌드박스
    # ==========================================
    elif lang_upper == "JP":
        if any(k in lbl_str for k in ["製造販売業者", "製造業者", "発売元", "製造元"]):
            lbl_str = re.sub(r'(製造販売業者|発売元)\s*(及び|／|/|&)\s*(製造業者|製造元)', r'\1<br>\2 \3', lbl_str)
        if any(k in lbl_str for k in ["使用期限", "使用期間"]):
            lbl_str = re.sub(r'(使用期限)\s*(又は|または|及び)\s*(開封後の使用期間|開封後)', r'\1<br>\2 \3', lbl_str)
        if any(k in lbl_str for k in ["医薬部外品", "審査", "承認"]):
            lbl_str = re.sub(r'(医薬部外品|機能性化粧品)\s*(審査区分|承認有無|審査)', r'\1<br>\2', lbl_str)
        if any(k in lbl_str for k in ["使用上の注意"]):
            lbl_str = lbl_str.replace("ご使用上の注意", "ご使用上の<br>注意").replace("使用上の注意", "使用上の<br>注意")
        if any(k in lbl_str for k in ["お客様相談室", "問い合わせ", "電話番号"]):
            lbl_str = re.sub(r'(お客様|消費者)\s*(相談室|窓口|お問い合わせ)', r'\1<br>\2', lbl_str)
        return lbl_str

    # ==========================================
    # [SANDBOX 4] 영어 (EN) 전용 샌드박스 (단어 중간 분절 결함 원천 차단)
    # ==========================================
    elif lang_upper == "EN":
        clean_lbl = re.sub(r'\s+', ' ', lbl_str).strip()
        # 1) 원산지 / 제조국: 'Country of Origin' 1줄 완벽 유지
        if re.search(r'Country\s+of\s+Origin', clean_lbl, re.I) or clean_lbl.lower() in ["country of origin", "origin"]:
            return "Country of Origin"
        # 2) 고객상담: 'Customer Service' 1줄 완벽 유지
        elif "customer" in clean_lbl.lower() and "service" in clean_lbl.lower():
            return "Customer Service"
        # 3) 단문 라벨 1줄 유지
        elif clean_lbl.lower() in ["skin type", "skintype", "directions", "direction", "ingredients", "ingredient"]:
            return clean_lbl
        # 4) 용량/중량: 'Size / Net Wt.' 2줄 대칭 개행
        elif any(k in clean_lbl.lower() for k in ["size", "net wt", "volume", "weight"]):
            return "Size /<br>Net Wt."
        # 5) 품질보증기준: 'Quality Assurance' / 'Standard' 완벽 2줄 안착
        elif re.search(r'Quality\s+Assurance\s+Standard', clean_lbl, re.I) or "quality assurance" in clean_lbl.lower():
            return "Quality Assurance<br>Standard"
        # 6) 사용할 때의 주의사항: 'Precautions for Use' 1줄 완벽 유지 (자간 -0.8px 최적화)
        elif re.search(r'Precautions\s+(for|in)\s+Use', clean_lbl, re.I) or "precautions" in clean_lbl.lower():
            return "Precautions for Use"
        # 7) 제조업자 및 책임판매업자: 'Manufacturer /' / 'Distributed by' 2줄 안착
        elif any(k in clean_lbl.lower() for k in ["manufacturer", "distributed by", "distributor"]):
            return "Manufacturer /<br>Distributed by"
        # 8) 기능성 화장품 심사: 'Functional Cosmetics' / 'Review Status' 2줄 안착
        elif any(k in clean_lbl.lower() for k in ["functional cosmetics", "review status"]):
            return "Functional Cosmetics<br>Review Status"
        # 9) 사용기한 / 개봉 후 사용기간: 'Shelf Life /' / 'Period After Opening' 2줄 안착
        elif any(k in clean_lbl.lower() for k in ["shelf life", "expiration", "period after opening", "pao"]):
            return "Shelf Life /<br>Period After Opening"
        return lbl_str

    # ==========================================
    # [SANDBOX 5] 한국어 (KO) 전용 샌드박스
    # ==========================================
    else:
        lbl_str = lbl_str.replace("기능성 화장품 심사 필 유무", "기능성 화장품<br>심사 필 유무")
        lbl_str = lbl_str.replace("기능성 화장품의 경우", "기능성 화장품의<br>경우")
        lbl_str = lbl_str.replace("화장품제조업자 및 책임판매업자", "화장품제조업자 및<br>책임판매업자")
        lbl_str = lbl_str.replace("화장품제조업자/책임판매업자", "화장품제조업자/<br>책임판매업자")
        lbl_str = lbl_str.replace("사용기한 또는 개봉 후 사용기간", "사용기한 또는<br>개봉 후 사용기간")
        lbl_str = lbl_str.replace("사용할 때의 주의사항", "사용할 때의<br>주의사항")
        lbl_str = lbl_str.replace("소비자 상담 전화번호", "소비자 상담<br>전화번호")
        lbl_str = lbl_str.replace("소비자상담관련 전화번호", "소비자상담관련<br>전화번호")

    # ==========================================
    # [공통 2차 Fallback] 기호 및 단어 단위 경계(\b) 접속사 기준 자동 개행
    # ==========================================
    if "<br>" not in lbl_str and len(lbl_str) >= 10:
        if re.search(r'[/／&＆+＋]', lbl_str):
            lbl_str = re.sub(r'\s*([/／&＆+＋])\s*', r' \1<br>', lbl_str, count=1)
        elif re.search(r'(\s*(?:및|또는|혹은|或|及|以及|又は|または|\band\b|\bor\b)\s*)', lbl_str, flags=re.IGNORECASE):
            lbl_str = re.sub(r'(\s*(?:및|또는|혹은|或|及|以及|又は|または|\band\b|\bor\b)\s*)', r' \1<br>', lbl_str, count=1, flags=re.IGNORECASE)

    return lbl_str

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
        val_padding = "20px 15px"
        line_height = "1.65"
        letter_spacing = "0px"
        label_width = "270px"
    elif lang.upper() in ["CN", "ZH", "SC"]:
        font_family = "'Noto Sans SC', 'NotoSansSC', 'Source Han Sans SC', '思源黑体', 'PingFang SC', 'Microsoft YaHei', sans-serif"
        title_size = "52px"
        cell_size = "26px"
        cell_padding = "20px 15px"
        val_padding = "20px 15px"
        line_height = "1.65"
        letter_spacing = "0px"
        label_width = "250px"
    elif lang.upper() == "EN":  # 영문 고시표 전용: compact padding & line-height (2570px 이내 단일 통합 수납)
        font_family = "'Pretendard', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif"
        title_size = "52px"
        cell_size = "28px"
        cell_padding = "10px 12px"
        val_padding = "10px 14px"
        line_height = "1.36"
        letter_spacing = "-0.8px"
        label_width = "295px"
    else:  # KO 한국어 고시표 표준: Pretendard 60px/30px
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
        lbl_formatted = _format_label_semantic_break(lbl, lang)
        # 💡 업데이트: 2열 의미단위 보호 및 순번 강제 줄바꿈
        val_str = str(val)
        
        # 💡 [제품명/상품명 중·영문 병기 가로폭 초과 시 의미단위 괄호 앞 스마트 줄바꿈]
        if any(k in lbl for k in ["제품명", "상품명", "产品名称", "產品名稱", "Product Name", "商品名"]):
            if "<br>" not in val_str and ("(" in val_str or "（" in val_str):
                m_paren = re.search(r'\s*([（(])', val_str)
                if m_paren:
                    # CJK 문자(26px)와 영문/숫자/공백(14px) 기준 예상 가로폭 산정
                    cjk_count = len(re.findall(r'[\u4e00-\u9fff\uac00-\ud7af\u3040-\u30ff]', val_str))
                    latin_count = len(val_str) - cjk_count
                    est_width = (cjk_count * 26) + (latin_count * 14)
                    # 2열 본문 안전 너비(520px)를 초과하여 자동 개행 시 단어 분절 결함이 생기는 경우에만 의미단위 개행
                    if est_width > 520:
                        val_str = val_str[:m_paren.start()] + "<br>" + val_str[m_paren.start():].lstrip()

        # 💡 [회사 단위 분리]: 제조업자/책임판매업자/생산기업/판매상 각 회사명 단위로 <br> 분리 및 Co., Ltd. 결속
        if any(k in lbl for k in ["제조업자", "책임판매업자", "생산기업", "판매상", "生产企业", "责任销售商", "Manufacturer", "Distributor", "製造販売元", "発売元"]):
            val_str = re.sub(r'(Co\.,?\s*Ltd\.?|Inc\.?|Corp\.?|\(주\)|주식회사|회사)\s*[,，/]\s*', r'\1<br>', val_str, flags=re.IGNORECASE)
            val_str = val_str.replace("Co., Ltd.", "Co.,\u00A0Ltd.").replace("Co.,Ltd.", "Co.,\u00A0Ltd.")

        # 💡 [전성분 표준 텍스트 플로우 및 가독성 최적화]
        if "성분" in lbl or "Ingredients" in lbl or "成分" in lbl:
            val_str = _smart_ingredient_hyphenator(val_str)
            # 중국/대만은 표준 모점(、)으로 정규화하여 글자 간격 벌어짐 방지 및 자연스러운 플로우 유지
            if lang in ["CN", "TW"]:
                val_str = re.sub(r'[,，、]\s*', '、', val_str)
                val_str = re.sub(r'、+', '、', val_str).strip()
                if val_str.endswith('、'):
                    val_str = val_str[:-1]
            else:
                val_str = re.sub(r'[,，、]\s*', ', ', val_str)
                val_str = re.sub(r'(,\s*)+', ', ', val_str).strip()
                if val_str.endswith(','):
                    val_str = val_str[:-1]

        # 💡 기능성/특수용도 심사 항목의 괄호 효능 부가설명 앞 강제 줄바꿈 (KO/CN/TW/JP/EN 전 언어 공통)
        if any(k in lbl for k in ["기능성", "심사", "审查", "審查", "審査", "Functional", "Review", "含藥"]):
            # （或报告） 또는 (또는 보고) 등의 불필요한 행정 문구는 제거하여 1줄 단일행 유지
            val_str = re.sub(r'[\(（]\s*(?:또는\s*보고|或报告)\s*[\)）]', '', val_str)
            # 효능 부가설명 괄호 앞 개행 처리 (이미 개행된 경우는 보존)
            if "<br>" not in val_str:
                val_str = re.sub(r'\s*([（(])', r'<br>\1', val_str, count=1)
        val_str = val_str.replace('식품의약품안전처 심사 필 완료 (', '식품의약품안전처 심사 필 완료<br>(')
        val_str = val_str.replace('식품의약품안전처 심사 필 무 (', '식품의약품안전처 심사 필 무<br>(')
        val_str = val_str.replace('붉은 반점', '붉은\u00A0반점')
        val_str = val_str.replace('이상 증상', '이상\u00A0증상')
        val_str = val_str.replace('부작용이 있는', '부작용이\u00A0있는')
        val_str = val_str.replace('전문의 등과', '전문의\u00A0등과')
        val_str = val_str.replace('상담할 것', '상담할\u00A0것')
        val_str = val_str.replace('부위 등에는', '부위\u00A0등에는')
        val_str = val_str.replace('자제할 것', '자제할\u00A0것')
        val_str = val_str.replace('닿지 않는 곳에', '닿지\u00A0않는\u00A0곳에')
        val_str = val_str.replace('보관할 것', '보관할\u00A0것')
        val_str = val_str.replace('피해서 보관', '피해서\u00A0보관')
        val_str = val_str.replace('심사 필 완료', '심사\u00A0필\u00A0완료')
        val_str = val_str.replace('2중 기능성', '2중\u00A0기능성')
        val_str = val_str.replace('분쟁해결 규정에', '분쟁해결\u00A0규정에')
        val_str = val_str.replace('분쟁해결 기준에', '분쟁해결\u00A0기준에')

        # 💡 [중국어 간체/번체 2열 전문의 상담 단어 결속 (외톨이 글자 방지)]
        val_str = val_str.replace('专业医生', '<span style="white-space: nowrap">专业医生</span>')
        val_str = val_str.replace('专业医师', '<span style="white-space: nowrap">专业医师</span>')
        val_str = val_str.replace('專業醫師', '<span style="white-space: nowrap">專業醫師</span>')
        val_str = val_str.replace('專業醫生', '<span style="white-space: nowrap">專業醫生</span>')

        val = re.sub(r'(?<!^)(?<!<br>)(?<!\n)\s*(\(\d+\)|\d+\)|[①-⑳]|\([가나다라마바사아자차카타파하甲乙丙丁a-zA-Z]\)|[㈎-㈛])', r'<br>\1', val_str)
        # 줄바꿈 및 리스트 서식 처리
        val_formatted = val.replace("\n", "<br>")
        # <br><br> 중복 정리
        val_formatted = re.sub(r'(<br>\s*)+', '<br>', val_formatted).strip()
        if val_formatted.startswith("<br>"):
            val_formatted = val_formatted[4:]
        
        is_ingredient = any(k in lbl for k in ["성분", "Ingredients", "成分"])
        cell_class = "value-cell ingredients" if is_ingredient else "value-cell"
        rows_html += f"""
        <tr>
            <th class="label-cell">{lbl_formatted}</th>
            <td class="{cell_class}">{val_formatted}</td>
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
            word-break: keep-all;
            overflow-wrap: break-word;
            border-right: 1px solid #EAEAEA;
        }}
        td.value-cell.ingredients {{
            font-size: 24px;
            font-weight: 400;
            color: #333333;
            padding: {val_padding};
            text-align: left;
            word-break: normal;
            overflow-wrap: break-word;
            line-height: 1.65;
            letter-spacing: 0px;
            background-color: #FFFFFF;
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

        with Image.open(output_path) as img:
            img.load()
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
