import json
import logging
import base64
import os
import sys

try:
    import requests
    import numpy as np
    from PIL import Image, ImageDraw, ImageFont, ImageFilter
    from datetime import datetime
except ImportError as e:
    print(f"❌ Missing lib: {e}")
    sys.exit(1)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("V3")

class Engine:
    def __init__(self, key):
        self.key = key
        self.out = "./output_v3"
        if not os.path.exists(self.out): os.makedirs(self.out)

    def run(self, path):
        print(f"🚀 Processing: {os.path.basename(path)}")
        img = Image.open(path).convert('RGB')
        w, h = img.size
        
        # API Call
        with open(path, "rb") as f: b64 = base64.b64encode(f.read()).decode()
        resp = requests.post(f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-image:generateContent?key={self.key}", 
                             json={"contents": [{"parts": [{"text": "Return JSON [{'box_2d':[y1,x1,y2,x2],'translated':'JP'}] for Korean text."}, {"inline_data": {"mime_type": "image/png", "data": b64}}]}], "generationConfig": {"responseMimeType": "application/json"}})
        
        items = json.loads(resp.json()['candidates'][0]['content']['parts'][0]['text'])
        draw = ImageDraw.Draw(img)
        for it in items:
            box = it['box_2d']
            draw.rectangle([box[1]*w/1000, box[0]*h/1000, box[3]*w/1000, box[2]*h/1000], fill="white")
            draw.text(((box[1]+box[3])*w/2000, (box[0]+box[2])*h/2000), it['translated'], fill="black", anchor="mm")
        
        out_path = os.path.join(self.out, f"result_JP_v3.png")
        img.save(out_path)
        print(f"✅ SUCCESS: {w}x{h}")

if __name__ == "__main__":
    with open(r"C:\Users\euntaewoo\AppData\Roaming\Antigravity\config\api_keys.json", "r") as f:
        key = json.load(f)["GEMINI_API_KEY"]
    e = Engine(key)
    e.run(r"C:\Users\euntaewoo\Desktop\다국어번역_화장품상품페이지_와이즈엠엔\프롬더팩토리_20260407\상품상세설명페이지_프롬더팩토리\토너\한글_원본파일\보태닉-그린-토너-상세페이지-01_01.png")
