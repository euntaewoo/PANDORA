import os
import sys
from playwright.sync_api import sync_playwright

html_content = """
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>製品詳細情報案内</title>
    <style>
        body {
            font-family: 'Noto Sans JP', 'Meiryo', sans-serif;
            background-color: white;
            color: black;
            padding: 20px;
            margin: 0;
            line-height: 1.5;
        }
        .header-title {
            font-size: 48px;
            font-weight: bold;
            margin-bottom: 40px;
            margin-top: 10px;
            text-align: center;
            font-family: 'Noto Sans JP', sans-serif;
        }
        .product-info-table {
            width: 100%;
            border-collapse: collapse;
            border: 1px solid #cccccc;
            font-size: 24px;
            table-layout: fixed;
        }
        .product-info-table tr {
            border-bottom: 1px solid #cccccc;
        }
        .product-info-table thead tr {
            background-color: #f8f8f8;
        }
        .product-info-table td,
        .product-info-table th {
            padding: 15px;
            border: 1px solid #cccccc;
            text-align: left;
            vertical-align: top;
        }
        .product-info-table th {
            font-weight: bold;
            width: 190px;
            font-size: 24px;
            white-space: normal;
            word-break: break-all;
            padding-left: 10px;
            padding-right: 10px;
        }
        .product-info-table td {
            color: #333333;
            word-break: break-all;
        }
        .product-info-table td.label-column {
            font-weight: bold;
            width: 190px;
            font-size: 24px;
            background-color: #ffffff;
            white-space: normal;
            word-break: break-all;
            padding-left: 10px;
            padding-right: 10px;
        }
        .ingredients {
            white-space: normal;
            word-wrap: break-word;
            word-break: break-all;
            line-height: 1.5;
            font-size: 24px;
        }
    </style>
</head>
<body>
    <div id="capture-target" style="width: 820px; padding: 30px; background-color: #ffffff; display: block; box-sizing: border-box;">
        <div class="header-title">製品詳細情報案内</div>
        <table class="product-info-table">
            <colgroup>
                <col style="width: 190px;">
                <col style="width: 570px;">
            </colgroup>
            <thead>
                <tr>
                    <th>項目</th>
                    <th>内容</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td class="label-column">製品名</td>
                    <td>マルチ コレクティブ アイクリーム (Multi-Corrective Eye Cream)</td>
                </tr>
                <tr>
                    <td class="label-column">製造業者 /<br>製造販売業者</td>
                    <td>(株)ナウコス / Skin Revers Lab Co., Ltd</td>
                </tr>
                <tr>
                    <td class="label-column">原産国</td>
                    <td>韓国</td>
                </tr>
                <tr>
                    <td class="label-column">ご使用方法</td>
                    <td>適量をプッシュし、なじませます。</td>
                </tr>
                <tr>
                    <td class="label-column">内容量</td>
                    <td>25ml</td>
                </tr>
                <tr>
                    <td class="label-column">区分</td>
                    <td>化粧品</td>
                </tr>
                <tr>
                    <td class="label-column">ご使用上の注意</td>
                    <td>
                        1) 化粧品の使用中または使用後、直射日光により使用部位に赤み、腫れ、かゆみなどの異常症状や副作用がある場合は、専門医等に相談すること<br>
                        2) 傷がある部位等には使用を控えること<br>
                        3) 保管及び取り扱い上の注意事項<br>
                        &nbsp;（ア）乳幼児の手の届かない場所に保管すること<br>
                        &nbsp;（イ）直射日光を避けて保管すること
                    </td>
                </tr>
                <tr>
                    <td class="label-column">全成分</td>
                    <td class="ingredients">
                        水、グリセリン、ＤＰＧ、イソステアリン酸イソプロピル、ミツロウ、シア脂、ステアリルアルコール、水添ポリイソブテン、ジメチコン、ステアリン酸ソルビタン、ポリソルベート６０、パルミチン酸、エチルヘキサンジオール、ポリアクリレート－１３、1,2-ヘキサンジオール、（Ｃ１２－１６）アルコール、ポリイソブテン、（アクリロイルジメチルタウリンアンモニウム／ベヘネス－２５）クロスポリマー、水添レシチン、カプリル酸グリセリル、酢酸トコフェロール、オレンジ果皮油、ヒアルロン酸、アデノシン、ラベンダー油、ＥＤＴＡ－２Ｎａ、ポリソルベート２０、イソステアリン酸ソルビタン、ヘキサペプチド－２、アラントイン、ローマカミツレ花油、ビオチン、エチルヘキシルグリセリン、ハナスゲ根エキス、トコフェロール、リナロール、リモネン
                    </td>
                </tr>
            </tbody>
        </table>
    </div>
</body>
</html>
"""

target_dir = r"C:\Users\euntaewoo\Desktop\이미지번역워크스페이스\변역결과\5_(일본어)Multi Corrective Eye cream"
os.makedirs(target_dir, exist_ok=True)
out_path = os.path.join(target_dir, "08_상품정보고시_Multi-Corrective-Eye-Cream_JP_Surgical_v5.png")

with sync_playwright() as p:
    print("[INFO] Launching headless browser...")
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    # 세로 auto 지정을 위해 충분한 높이의 뷰포트 확보
    page.set_viewport_size({"width": 1400, "height": 4000}) 
    page.set_content(html_content)
    
    # 폰트 로드 등을 위해 약간 대기
    page.wait_for_timeout(1000)
    
    element_handle = page.locator("#capture-target")
    print(f"[INFO] Taking screenshot to {out_path}...")
    element_handle.screenshot(path=out_path)
    
    browser.close()
    print("[SUCCESS] HTML to PNG Rendering Complete!")
