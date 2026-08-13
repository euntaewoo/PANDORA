# -*- coding: utf-8 -*-
import os
import sys
import subprocess

def install_playwright():
    try:
        import playwright
    except ImportError:
        print("[INFO] Installing playwright...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "playwright"])
        subprocess.check_call([sys.executable, "-m", "playwright", "install", "chromium"])

install_playwright()

from playwright.sync_api import sync_playwright

font_path = r"C:/Users/euntaewoo/Desktop/이미지번역워크스페이스/JP_Ecom_Visual_Localizer_V5_이미지번역메인시스템엔진/NotoSansJP-VF.ttf"

# 기계번역 오염이 완벽히 정제된 순수 일본어 데이터 정의
title = "商品情報提供告示"
rows = [
    ("内容量", "200ml"),
    ("製品の主な仕様", "すべての肌タイプ用"),
    ("使用期限", "製品に別途表記"),
    ("ご使用方法", "適量を手に取り、十分に泡立ててから顔全体をマッサージするようにやさしく洗い、ぬるま湯で十分に洗い流します。"),
    ("化粧品製造業者および化粧品責任販売業者", "株式会社ナチュゼン / スキンリバースラボ株式会社"),
    ("製造国", "韓国"),
    ("機能性化粧品審査の有無", "該当なし"),
    ("全成分", "コメ発酵液、ココアンホジ酢酸2Na、グリセリン、1,2-ヘキサンジオール、ココイルアラニンNa、ココイルグルタミン酸TEA、クエン酸、アラントイン、ベルガモット果実油、グリセリルグルコシド、エチルヘキシルグリセリン、クエン酸Na、乳酸桿菌／ダイズ発酵エキス、酵母／ヤドリギ発酵エキス、酵母／チガヤ根発酵エキス、アナナス果実エキス、リナロール、リモネン")
]

caution_text = (
    "1) 化粧品の使用中、または使用後に直射日光により使用部位に赤み、腫れ、またはかゆみ等の異常症状や副作用がある場合は、専門医等に相談すること<br>"
    "2) 傷がある部位等には使用を控えること<br>"
    "3) 保管及び取り扱い時の注意事項<br>"
    "&nbsp;&nbsp;&nbsp;（ア）乳幼児の手の届かない場所に保管すること<br>"
    "&nbsp;&nbsp;&nbsp;（イ）直射日光を避けて保管すること<br>"
    "4) 目に入らないように注意すること<br>"
    "5) 3歳以下の乳幼児への使用は避けること<br>"
    "6) 広範囲に使用する場合、または局所的に使用する場合には、十分に注意して使用すること"
)

rows.append(("ご使用上の注意", caution_text))
rows.append(("品質保証基準", "関連法及び消費者紛争解決規定に従う"))
rows.append(("消費者相談窓口", "02-6743-3206"))

# HTML 동적 조립
tbody_html = ""
for label, val in rows:
    tbody_html += f"<tr><th>{label}</th><td>{val}</td></tr>"

html_content = f"""
<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="utf-8">
<style>
  @font-face {{
    font-family: 'Noto Sans JP';
    src: url('{font_path}') format('truetype');
  }}
  body {{ margin: 0; padding: 20px; background-color: #ffffff; display: flex; justify-content: center; }}
  .info-table {{
    width: 820px;
    height: auto;
    font-family: 'Noto Sans JP', sans-serif;
    font-size: 24px;
    border-collapse: collapse;
    line-height: 1.5;
    color: #333333;
    background-color: #ffffff;
  }}
  .info-table th, .info-table td {{
    border: 1px solid #cccccc;
    padding: 16px 20px;
    text-align: left;
    vertical-align: top;
  }}
  .info-table th {{
    background-color: #f9f9f9;
    font-weight: 700;
    width: 30%;
  }}
  .info-table td {{
    font-weight: 400;
    width: 70%;
    white-space: pre-wrap;
    word-break: break-all;
  }}
  .title-row {{
    background-color: #e9e9e9;
    text-align: center;
    font-weight: 700;
    padding: 20px;
  }}
</style>
</head>
<body>
  <table class="info-table">
    <thead>
      <tr>
        <th colspan="2" class="title-row">{title}</th>
      </tr>
    </thead>
    <tbody>
      {tbody_html}
    </tbody>
  </table>
</body>
</html>
"""

# 결과 폴더 정의
target_dir = r"C:\Users\euntaewoo\Desktop\이미지번역워크스페이스\변역결과\8_(일본어)_폼클렌져폼200ml"
os.makedirs(target_dir, exist_ok=True)

out_path = os.path.join(target_dir, "상품상세정보제공고시_JP_Surgical_v5.png")

with sync_playwright() as p:
    print("[INFO] Launching headless browser...")
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.set_viewport_size({"width": 950, "height": 1600}) 
    page.set_content(html_content)
    
    element_handle = page.locator(".info-table")
    print(f"[INFO] Taking screenshot to {out_path}...")
    element_handle.screenshot(path=out_path)
    
    browser.close()
    print("[SUCCESS] HTML to PNG Rendering Complete!")
