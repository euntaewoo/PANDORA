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
  table { width: 820px; border-collapse: collapse; font-family: 'Noto Sans JP', 'Meiryo', sans-serif; font-size: 13px; line-height: 1.6; color: #333333; border-top: 2px solid #111111; border-bottom: 1px solid #cccccc; margin: 0 auto; }
  th { width: 220px; padding: 12px 15px; border-bottom: 1px solid #eeeeee; border-right: 1px solid #eeeeee; text-align: left; font-weight: bold; background-color: #f9f9f9; }
  td { padding: 12px 15px; border-bottom: 1px solid #eeeeee; text-align: left; font-weight: normal; }
  .footnote { font-family: 'Noto Sans JP', 'Meiryo', sans-serif; font-size: 11px; color: #787878; text-align: center; margin-top: 15px; }
</style>
</head>
<body>
<div class="container">
  <table>
    <tbody>
      <tr>
        <th>内容物の容量または重量</th>
        <td>25g x 3ea</td>
      </tr>
      <tr>
        <th>製品の主な仕様</th>
        <td>すべての肌タイプ用</td>
      </tr>
      <tr>
        <th>使用期限または開封後の使用期間</th>
        <td>製品内に別途表記</td>
      </tr>
      <tr>
        <th>ご使用方法</th>
        <td>
          1. 洗顔後、化粧水で肌のキメを整えます。<br>
          2. マスクを取り出し、前後の保護シートを除去した後、目と口の周りを除いた顔全体に均一に密着させます。<br>
          3. 約10〜20分間休息を取った後、マスクを除去します。<br>
          4. 肌に残った内容物を軽くたたいて浸透させます。
        </td>
      </tr>
      <tr>
        <th>化粧品製造業者、化粧品責任販売業者及びオーダーメイド型化粧品販売業者</th>
        <td>(株)ISISCOSMETIC、スキンリバースラボ(株)</td>
      </tr>
      <tr>
        <th>製造国</th>
        <td>韓国</td>
      </tr>
      <tr>
        <th>全成分</th>
        <td style="word-break: keep-all;">精製水、ブチレングリコール、グリセリン、ナイアシンアミド、1,2-ヘキサンジオール、カルボマー、アルギニン、キシリトール、アラントイン、トレハロース、パンテノール、ベタイン、ポリグリセリル-10ラウレート、ポリグリセリル-4ラウレート、ジプロピレングリコール、ゼオライト、アデノシン、グルコノラクトン、シロヤナギ樹皮エキス、加水分解ヒアルロン酸Na、アロエベラ葉エキス、リナロール、酢酸リナリル、ラベンダー油、酢酸トコフェロール、マルトデキストリン、クエン酸Na、バージニアマンサクエキス、ウメ花エキス、バンブサウルガリス水、バンブサウルガリスエキス、バンブサウルガリス葉エキス、シトロネロール</td>
      </tr>
      <tr>
        <th>機能性化粧品審査の有無</th>
        <td>化粧品法による機能性化粧品審査（または報告）を完了／美白、しわ改善の二重機能性化粧品</td>
      </tr>
      <tr>
        <th>ご使用上の注意</th>
        <td>
          1) 化粧品の使用中、または使用後に直射日光により使用部位が赤い斑点、腫れ、またはかゆみ等の異常症状や副作用がある場合は、専門医等に相談すること<br>
          2) 傷がある部位等には使用を控えること<br>
          3) 保管及び取り扱い時の注意事項<br>
          &nbsp;&nbsp;&nbsp;（ア）乳幼児の手の届かない場所に保管すること<br>
          &nbsp;&nbsp;&nbsp;（イ）直射日光を避けて保管すること
        </td>
      </tr>
      <tr>
        <th>品質保証基準</th>
        <td>関連法及び消費者紛争解決規定に従う</td>
      </tr>
      <tr>
        <th>消費者相談関連電話番号</th>
        <td>02-6743-3206</td>
      </tr>
    </tbody>
  </table>
</div>
</body>
</html>
"""

# 원본 폴더명을 동적으로 추출하여 결과 폴더 하위에 새 디렉토리 생성
source_dir = r"C:\Users\euntaewoo\Desktop\이미지번역워크스페이스\변역대상\11. 바이오핏 글로우 PHA 컴플렉스 마스크 -BioFit Glow PHA Complex Mask-20260225T124720Z-1-001\(한국어)_웹설명페이지-BioFit Glow PHA Complex Mask"
base_target_dir = r"C:\Users\euntaewoo\Desktop\이미지번역워크스페이스\변역결과"
folder_name = os.path.normpath(source_dir).split(os.sep)[-1]
target_dir = os.path.join(base_target_dir, folder_name)
os.makedirs(target_dir, exist_ok=True)

out_path = os.path.join(target_dir, "10_BioFit Glow PHA_complex_Mask_상세정보안내_JP_Surgical_v5.png")

with sync_playwright() as p:
    print("[INFO] Launching headless browser...")
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.set_viewport_size({"width": 950, "height": 1600}) 
    page.set_content(html_content)
    
    element_handle = page.locator(".container")
    print(f"[INFO] Taking screenshot to {out_path}...")
    element_handle.screenshot(path=out_path)
    
    browser.close()
    print("[SUCCESS] HTML to PNG Rendering Complete!")
