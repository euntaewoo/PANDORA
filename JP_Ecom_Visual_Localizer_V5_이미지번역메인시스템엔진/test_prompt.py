import os
import json
from google.genai import Client
from google.genai import types

def test_prompt():
    sa_path = os.path.join(os.path.dirname(__file__), "vertex_service_account.json")
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = sa_path
    
    client = Client(vertexai=True, location='us-central1', project='light-depot-238403')
    
    prompt = """
    [GOAL] Identify ALL Korean text blocks in the image and translate them into Japanese.
    Return a JSON list: [{"box_2d": [ymin, xmin, ymax, xmax], "translated": "Japanese Translation"}]
    
    CRITICAL RULES:
    1. Identify EVERY SINGLE block of Korean text in the image. Do not miss any labels, paragraphs, headers, or body text.
    2. Bounding boxes [ymin, xmin, ymax, xmax] must be normalized to 1000 (0 to 1000 scale relative to image height and width).
    3. Make sure the bounding box tightly encompasses the entire Korean text block to be replaced.
    4. Translate accurately to Japanese for E-commerce:
       - '흡수' -> '浸透'
       - '적당량' -> '500円玉大'
       - '컨디션 유지' -> 'コンディション維持'
    5. Safety: Do NOT use prohibited medical words like '治療', '改善', '再生'. Use milder words like 'ケア', '整える', 'いきいき'.
    """
    
    image_path = r"D:\Users\euntaewoo\Desktop\이미지번역_KOR_To_JP_와이즈엠엔씨\이미지_한국어_일본어번역\07.Professional Sun Block SPF50+\07_sun_Block_SPF50++\국문\웹상세설명페이지\01_웹상세페이지_Professional Sun Block 70.png"
    from PIL import Image
    img = Image.open(image_path)
    
    try:
        response = client.models.generate_content(
            model="gemini-2.5-pro",
            contents=[img, prompt],
            config=types.GenerateContentConfig(response_mime_type="application/json")
        )
        print("SUCCESS!")
        with open("test_response.json", "w", encoding="utf-8") as f:
            f.write(response.text)
        print("Wrote to test_response.json")
    except Exception as e:
        print("FAILED:", str(e))

if __name__ == '__main__':
    test_prompt()
