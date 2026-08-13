import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import json
import os

def run_hybrid_renderer():
    print("V5 Hybrid Rendering Engine - Initializing...")
    
    img_path = r"D:\Users\euntaewoo\Desktop\이미지번역_KOR_To_JP_와이즈엠엔씨\이미지_한국어_일본어번역\07.Professional Sun Block SPF50+\07_sun_Block_SPF50++\국문\웹상세설명페이지\04_웹상세페이지_Professional Sun Block 70g.png"
    out_path = r"D:\Users\euntaewoo\Desktop\JP_Ecom_Visual_Localizer_V3\v5_hybrid_renderer_output_qa.png"
    font_path = r"D:\Users\euntaewoo\Desktop\JP_Ecom_Visual_Localizer_V3\NotoSansJP-VF.ttf"

    img_array = np.fromfile(img_path, np.uint8)
    img_cv = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

    # 교정된 실제 텍스트 좌표 및 배경 커버 박스 (QA 1차 루프 적용)
    gemini_data = [
        # Point 3 박스 영역 덮기 (x:350~550, y:70~150) -> 검은 배경 + 흰 글씨
        {"point": [380, 95], "text": "3つのポイント", "size": 35, "color": (255, 255, 255), "bg_box": (350, 70, 550, 150), "bg_color": (0, 0, 0)},
        
        # 메인 헤딩 (야외활동에...) (x:150~850, y:170~250) -> 크림 배경 + 검은 글씨
        {"point": [180, 185], "text": "アウトドアに最適なテクスチャ", "size": 50, "color": (0, 0, 0), "bg_box": (150, 160, 850, 250), "bg_color": (245, 241, 244)},
        
        # 서브 텍스트 1 (피부에 자극없이...)
        {"point": [280, 280], "text": "肌にやさしく、すっと馴染むテクスチャ", "size": 30, "color": (50, 50, 50), "bg_box": (250, 260, 850, 320), "bg_color": (242, 237, 240)},
        
        # 서브 텍스트 2 (땀에도 무너짐없이...)
        {"point": [280, 345], "text": "汗をかいても崩れにくく、サラサラ感をキープ", "size": 30, "color": (50, 50, 50), "bg_box": (250, 325, 850, 390), "bg_color": (240, 234, 238)}
    ]

    # 개별 BBox 클리닝 (원본 텍스트 지우기)
    for item in gemini_data:
        x1, y1, x2, y2 = item["bg_box"]
        cv2.rectangle(img_cv, (x1, y1), (x2, y2), item["bg_color"], -1)

    # PIL 텍스트 렌더링
    img_cv_rgb = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)
    pil_img = Image.fromarray(img_cv_rgb)
    draw = ImageDraw.Draw(pil_img)

    for item in gemini_data:
        x, y = item["point"]
        text = item["text"]
        font_size = item["size"]
        color = item["color"]
        
        try:
            font = ImageFont.truetype(font_path, font_size)
        except Exception:
            font = ImageFont.load_default()

        draw.text((x, y), text, font=font, fill=color)

    pil_img.save(out_path, format="PNG")
    print(f"\n[SUCCESS] QA Pass 1: Rendered image to {out_path}")

if __name__ == "__main__":
    run_hybrid_renderer()
