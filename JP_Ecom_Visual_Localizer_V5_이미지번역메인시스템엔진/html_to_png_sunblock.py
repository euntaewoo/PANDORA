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

html_content = """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  body { margin: 0; padding: 20px; background-color: #ffffff; display: flex; flex-direction: column; justify-content: center; align-items: center; }
  .container { width: 850px; padding: 10px; border: 1px solid #ffffff; }
  h2 { font-family: 'Noto Sans JP', 'Meiryo', sans-serif; text-align: center; margin-bottom: 20px; color: #111; }
  table { width: 820px; border-collapse: collapse; font-family: 'Noto Sans JP', 'Meiryo', sans-serif; font-size: 13px; line-height: 1.6; color: #333333; border-top: 2px solid #111111; border-bottom: 1px solid #cccccc; margin: 0 auto; }
  th { width: 220px; padding: 12px 15px; border-bottom: 1px solid #eeeeee; border-right: 1px solid #eeeeee; text-align: center; font-weight: bold; background-color: #f9f9f9; }
  td { padding: 12px 15px; border-bottom: 1px solid #eeeeee; text-align: left; font-weight: normal; }
  .footnote { font-family: 'Noto Sans JP', 'Meiryo', sans-serif; font-size: 11px; color: #787878; text-align: center; margin-top: 15px; }
</style>
</head>
<body>
<div class="container">
  <h2>商品情報告示案内</h2>
  <table>
    <tbody>
      <tr>
        <th>製品名</th>
        <td>プロフェッショナル サンブロック / Professional Sun Block</td>
      </tr>
      <tr>
        <th>製造業者 /<br>製造販売業者</th>
        <td>NOWCOS Co., Ltd. / Skin Reverse Lab Co., Ltd.</td>
      </tr>
      <tr>
        <th>製造国</th>
        <td>大韓民国</td>
      </tr>
      <tr>
        <th>使用方法</th>
        <td>スキンケアの最後に、紫外線に露出する部分に適量をムラなく伸ばして塗ります。</td>
      </tr>
      <tr>
        <th>内容量</th>
        <td>70g</td>
      </tr>
      <tr>
        <th>効能・効果</th>
        <td>
          メラニンの生成を抑え、シミ・そばかすを防ぎます。<br>
          乾燥による小じわを目立たなくします。<br>
          紫外線から肌を保護します。(SPF50+ PA++++)
        </td>
      </tr>
      <tr>
        <th>使用上の注意</th>
        <td>
          1) 化粧品の使用中、または使用後、直射日光によって使用部位に赤い斑点、腫れ、またはかゆみなどの異常症状や副作用がある場合は、専門医などに相談すること<br><br>
          2) 傷がある部位などには使用を控えること<br><br>
          3) 保管及び取り扱い時の注意事項:<br>
          &nbsp;&nbsp;&nbsp;(ア) 子供の手の届かないところに保管すること<br>
          &nbsp;&nbsp;&nbsp;(イ) 直射日光を避けて保管すること
        </td>
      </tr>
      <tr>
        <th>全成分</th>
        <td style="word-break: keep-all;">精製水、サリチル酸ブチルオクチル、酸化亜鉛、シクロペンタシロキサン、シクロヘキサシロキサン、エチルヘキサン酸セチル、ＢＧ、ジメチコン、シリカ、ナイアシンアミド、ＰＥＧ－１０ジメチコン、カラミン、ＰＥＧ－９ポリジメチルシロキシエチルジメチコン、（ジメチコン／（ＰＥＧ－１０／１５））クロスポリマー、ジステアルジモニウムヘクトライト、硫酸Ｍｇ、セレシン、セスキオレイン酸ソルビタン、酸化チタン、ジメチコンクロスポリマー、エチルヘキサンジオール、トリエトキシカプリリルシラン、ジメチルシリル化シリカ、ステアリン酸、カプリル酸グリセリル、ラウロイルリシン、１，２－ヘキサンジオール、ＥＤＴＡ－２Ｎａ、アデノシン、ペンタナトリウムテトラカルボキシメチルアセチルヒドロキシプロリルジペプチド－１２、ペンタナトリウムテトラカルボキシメチルジペプチド－５１、テトラカルボキシメチルヘキサノイルジペプチド－１２</td>
      </tr>
      <tr>
        <th>使用期限</th>
        <td>製品内に別途表記</td>
      </tr>
    </tbody>
  </table>
</div>
</body>
</html>
"""

# 저장할 파일 경로 두 곳 (원본 폴더와 결과 폴더 모두 덮어쓰기)
source_out_path = r"C:\Users\euntaewoo\Desktop\이미지번역워크스페이스\변역대상\07_Professional Sun Block SPF50+PA\07. 프로페셔널 썬 블록 SPF50+ - Professional Sun Block SPF50+\국문\05_JP_product_info_announcement.png"
target_out_path = r"C:\Users\euntaewoo\Desktop\이미지번역워크스페이스\변역결과\7_(일본어)_웹상세페이지_Professional Sun Block 70g\05_JP_product_info_announcement.png"

html_file = "temp_sunblock.html"
with open(html_file, "w", encoding="utf-8") as f:
    f.write(html_content)

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(device_scale_factor=2)
    page.goto(f"file://{os.path.abspath(html_file)}")
    
    # 컨테이너 크기에 맞춰 캡처
    element = page.locator(".container")
    
    print(f"Generating image to: {source_out_path}")
    element.screenshot(path=source_out_path)
    print(f"Generating image to: {target_out_path}")
    element.screenshot(path=target_out_path)
    
    browser.close()

os.remove(html_file)
print("완료되었습니다.")
