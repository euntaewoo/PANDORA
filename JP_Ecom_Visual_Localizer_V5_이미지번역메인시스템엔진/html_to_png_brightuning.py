import os
import sys
from playwright.sync_api import sync_playwright

html_content = """
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>商品情報公示案内</title>
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
            font-family: 'Noto Sans JP', sans-serif;
        }
        .product-info-table {
            width: 100%;
            border-collapse: collapse;
            font-size: 24px;
            border-top: 3px solid #555;
            border-bottom: 3px solid #555;
        }
        .product-info-table tr {
            border-bottom: 1px solid #e0e0e0;
        }
        .product-info-table tr:first-child {
            border-bottom: 2px solid #555;
        }
        .product-info-table td,
        .product-info-table th {
            padding: 15px 20px;
            text-align: left;
            vertical-align: top;
        }
        .product-info-table th {
            font-weight: bold;
            width: 180px;
            color: #333;
            background-color: #f7f7f7; /* Very light gray */
            white-space: nowrap;
        }
        .product-info-table td {
            color: #555;
            background-color: white;
            word-break: break-all;
        }
        .cautions-list {
            margin: 0;
            padding: 0;
            list-style-type: none;
        }
        .cautions-list li {
            margin-bottom: 8px;
        }
        .cautions-list li:last-child {
            margin-bottom: 0;
        }
        .nested-cautions-list {
            margin-top: 8px;
            margin-left: 25px;
            list-style-type: none;
        }
        .ingredients {
            white-space: normal;
            word-wrap: break-word;
            word-break: break-all;
            line-height: 1.5;
            font-size: 24px; /* Set to 24px to match user requirement */
        }
        #capture-target {
            width: 820px;
            box-sizing: border-box;
            background-color: #ffffff;
            padding: 30px;
            display: block;
        }
    </style>
</head>
<body>
    <div id="capture-target">
        <div class="header-title">商品情報公示案内</div>
        <table class="product-info-table">
            <tr>
                <th>製品名</th>
                <td><strong>ブライトニング ペプチド アンプル / Brightuning Peptide Ampoule</strong></td>
            </tr>
            <tr>
                <th>製造販売業者</th>
                <td>Skin Revers Lab Co., Ltd</td>
            </tr>
            <tr>
                <th>製造国</th>
                <td>韓国</td>
            </tr>
            <tr>
                <th>ご使用方法</th>
                <td>スポイトで適量を手に取り、軽くたたいてなじませます。</td>
            </tr>
            <tr>
                <th>内容量</th>
                <td>30ml</td>
            </tr>
            <tr>
                <th>区分</th>
                <td>化粧品</td>
            </tr>
            <tr>
                <th>ご使用上の注意</th>
                <td>
                    <ul class="cautions-list">
                        <li>1) 化粧品の使用中または使用後、直射日光により使用部位に赤み、腫れ、かゆみなどの異常症状や副作用がある場合は、専門医等に相談すること</li>
                        <li>2) 傷がある部位等には使用を控えること</li>
                        <li>3) 保管及び取り扱い上の注意事項
                            <ul class="nested-cautions-list">
                                <li>（ア）乳幼児の手の届かない場所に保管すること</li>
                                <li>（イ）直射日光を避けて保管すること</li>
                            </ul>
                        </li>
                    </ul>
                </td>
            </tr>
            <tr>
                <th>全成分</th>
                <td class="ingredients">
                    サッカロミセス／コメ発酵液、水、グリセリン、メチルプロパンジオール、グリセリルグルコシド、ナイアシンアミド、ベタイン、1,2-ヘキサンジオール、ＢＧ、トリ（カプリル酸／カプリン酸）グリセリル、パルミチン酸エチルヘキシル、ジステアリン酸ポリグリセリル-3、（アクリロイルジメチルタウリンアンモニウム／ＶＰ）コポリマー、ステアリン酸ポリグリセリル-6、エチルヘキシルグリセリン、ステアリン酸グリセリル、（アクリロイルジメチルタウリンアンモニウム／メタクリル酸ベヘネス－２５）クロスポリマー、カプリリルグリコール、クエン酸ステアリン酸グリセリル、ベヘン酸ポリグリセリル-6、キサンタンガム、アケビエキス、ヘプタナトリウムヘキサカルボキシメチルジペプチド-12 (250ppm)、ＥＤＴＡ－２Ｎａ、タカサブロウエキス、カミメボウキ葉エキス、ペンタナトリウムテトラカルボキシメチルジペプチド-51 (62.5ppm)、メリアアザジラクタ葉エキス、マデカッソシド、ジペプチド-1 (50ppm)、ウコン根エキス、サンゴモエキス、パイナップル果実エキス
                </td>
            </tr>
            <tr>
                <th>使用期限</th>
                <td>製品内に別途表記</td>
            </tr>
        </table>
    </div>
</body>
</html>
"""

target_dir = r"C:\Users\euntaewoo\Desktop\이미지번역워크스페이스\변역결과\4_(일본어)Brightuning Peptide Ampoule"
os.makedirs(target_dir, exist_ok=True)
out_path = os.path.join(target_dir, "03_상품정보고시_Brightuning-Peptide-Ampoule_JP_Surgical_v5.png")

with sync_playwright() as p:
    print("[INFO] Launching headless browser...")
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.set_viewport_size({"width": 1400, "height": 3000}) 
    page.set_content(html_content)
    
    # 폰트 로드 등을 위해 약간 대기
    page.wait_for_timeout(1000)
    
    element_handle = page.locator("#capture-target")
    print(f"[INFO] Taking screenshot to {out_path}...")
    element_handle.screenshot(path=out_path)
    
    browser.close()
    print("[SUCCESS] HTML to PNG Rendering Complete!")
