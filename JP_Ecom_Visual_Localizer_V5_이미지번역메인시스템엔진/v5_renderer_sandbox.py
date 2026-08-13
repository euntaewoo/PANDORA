import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import json
import os

def run_hybrid_renderer():
    print("V5 Hybrid Rendering Engine - Initializing...")
    
    # 1. 경로 설정
    img_path = r"D:\Users\euntaewoo\Desktop\이미지번역_KOR_To_JP_와이즈엠엔씨\이미지_한국어_일본어번역\07.Professional Sun Block SPF50+\07_sun_Block_SPF50++\국문\웹상세설명페이지\04_웹상세페이지_Professional Sun Block 70g.png"
    out_path = r"D:\Users\euntaewoo\Desktop\JP_Ecom_Visual_Localizer_V3\v5_hybrid_renderer_output.png"
    font_path = r"D:\Users\euntaewoo\Desktop\JP_Ecom_Visual_Localizer_V3\NotoSansJP-VF.ttf"

    if not os.path.exists(font_path):
        print(f"[ERROR] Font not found at {font_path}")
        return

    # 2. 이미지 로드 (OpenCV -> PIL 변환)
    # 한글/특수문자 경로 문제 방지를 위해 numpy로 읽기
    img_array = np.fromfile(img_path, np.uint8)
    img_cv = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    
    if img_cv is None:
        print("[ERROR] Failed to load image.")
        return

    # 3. 제미나이 3.1 Pro가 추출한 Mock JSON 좌표 데이터 (테스트용)
    # y축이 502, 513, 521, 520 이었던 아까 로그 기반
    # x축은 적당한 오프셋 적용
    gemini_data = [
        {"point": [50, 500], "text": "3つのポイント", "size": 40, "color": (80, 80, 80)},
        {"point": [50, 560], "text": "アウトドアに最適なテクスチャ", "size": 60, "color": (30, 30, 30)},
        {"point": [50, 650], "text": "肌にやさしく、すっと馴染むテクスチャ", "size": 35, "color": (100, 100, 100)},
        {"point": [50, 700], "text": "汗をかいても崩れにくく、サラサラ感をキープ", "size": 35, "color": (100, 100, 100)}
    ]

    # 4. 배경 클리닝 (Inpainting / 텍스처 덮어쓰기)
    # 테스트 목적상, 텍스트가 그려질 하단부(y:480~750)를 크림색(원본 배경과 유사한 색상)으로 덮어서 깨끗하게 만듦
    # 실제 프로덕션에서는 cv2.inpaint나 마스크를 사용
    bg_color = (250, 248, 245) # 연한 크림색 (BGR)
    cv2.rectangle(img_cv, (0, 480), (img_cv.shape[1], 750), bg_color, -1)

    # 5. PIL 변환 및 텍스트 렌더링
    img_cv_rgb = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)
    pil_img = Image.fromarray(img_cv_rgb)
    draw = ImageDraw.Draw(pil_img)

    print("Rendering Japanese text with NotoSansJP...")
    for item in gemini_data:
        x, y = item["point"]
        text = item["text"]
        font_size = item["size"]
        color = item["color"]
        
        # 폰트 로드
        try:
            font = ImageFont.truetype(font_path, font_size)
        except Exception as e:
            print(f"[ERROR] Font load failed: {e}")
            font = ImageFont.load_default()

        # 텍스트 합성
        draw.text((x, y), text, font=font, fill=color)

    # 6. 최종 이미지 저장
    pil_img.save(out_path, format="PNG")
    print(f"\n[SUCCESS] V5 Hybrid Render Complete. Saved to {out_path}")

if __name__ == "__main__":
    run_hybrid_renderer()
