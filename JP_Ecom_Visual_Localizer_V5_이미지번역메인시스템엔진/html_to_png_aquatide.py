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
        <th>製品名</th>
        <td>アクアタイド マルチパーパス トナーミスト (Aquatide Multipurpose Toner Mist)</td>
      </tr>
      <tr>
        <th>機能性化粧品の審査有無</th>
        <td>美白・しわ改善 2重機能性</td>
      </tr>
      <tr>
        <th>主要成分</th>
        <td>アクアタイド 3%高配合</td>
      </tr>
      <tr>
        <th>主な特徴</th>
        <td>オートファジー技術を活用し、肌の美白、しわ改善をサポートします。</td>
      </tr>
      <tr>
        <th>使用方法</th>
        <td>洗顔後、手またはコットンに浸して使用するか、付属のアプリケーターに移し替えて2～3回プッシュし、微細なミストを肌に吹き付け、軽くたたいて浸透させます。</td>
      </tr>
      <tr>
        <th>容量</th>
        <td>200ml</td>
      </tr>
      <tr>
        <th>製造国</th>
        <td>大韓民国</td>
      </tr>
      <tr>
        <th>製造業者および責任販売業者</th>
        <td>Pabion / (株)スキンリバースラボ</td>
      </tr>
      <tr>
        <th>消費者相談室</th>
        <td>02-6743-3206</td>
      </tr>
      <tr>
        <th>全成分</th>
        <td style="word-break: keep-all;">精製水、プロパンジオール、メチルプロパンジオール、1,2-ヘキサンジオール、グリセ린、ナイアシンアミド、PPG-13デシルテトラデセス-24、カルボマー、トロメタミン、アデノシン、ラベンダー油、EDTA-2Na、ヘプタソジウムヘキサカルボキシメチルジペプチド-12、ベタイン、アラントイン、BG、ハッカ油、ツバキ花エキス、マグワ根皮エキス、トコフェロール、リナロール</td>
      </tr>
    </tbody>
  </table>
  <div class="footnote">*浸透は角質層まで</div>
</div>
</body>
</html>
"""

# 원본 폴더명을 동적으로 추출하여 결과 폴더 하위에 새 디렉토리 생성
source_dir = r"C:\\Users\\euntaewoo\\Desktop\\이미지번역워크스페이스\\변역대상\\02_아쿠아타이드 멀티퍼포스 토너 미스트\\한국어_로지컬리스킨_아쿠아멀티퍼포즈_토너"
base_target_dir = r"C:\\Users\\euntaewoo\\Desktop\\이미지번역워크스페이스\\변역결과"
folder_name = os.path.normpath(source_dir).split(os.sep)[-1]
target_dir = os.path.join(base_target_dir, folder_name)
os.makedirs(target_dir, exist_ok=True)

out_path = os.path.join(target_dir, "010_웹상세_아쿠아타이드_멀티퍼포스토너미스트_상품정보제공고시_JP_Surgical_v5.png")

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
