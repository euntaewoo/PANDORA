import os
import sys
import json
from google import genai
from google.genai import types
from PIL import Image

def analyze_font_styles(image_path, detected_blocks, client, target_lang="JP"):
    """
    Gemini 3.1 Pro 멀티모달 프롬프팅으로 원본 글자의 색상 Hex Code, 굵기, 정렬 및 약기법/초월번역을 분석하여 JSON 출력.
    """
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"이미지 파일을 찾을 수 없습니다: {image_path}")

    image = Image.open(image_path)

    prompt = f"""
    첨부된 이미지의 한국어 텍스트 감지 데이터({json.dumps(detected_blocks, ensure_ascii=False)})를 기반으로, 
    각 텍스트 블록의 시각적 스타일(font_color_hex, font_weight, alignment)을 역추출하고, 
    타깃 언어({target_lang})에 맞추어 전문 번역문(translated_text)을 포함하는 JSON 배열을 생성하세요.

    출력 스키마:
    {{
      "styled_text_blocks": [
        {{
          "original_text": "한국어 원문",
          "translated_text": "타깃 언어 번역문",
          "font_color_hex": "#FFFFFF",
          "font_weight": "bold 또는 normal",
          "alignment": "center, left, right 중 하나",
          "box_2d": [ymin, xmin, ymax, xmax]
        }}
      ]
    }}
    """

    response = client.models.generate_content(
        model="gemini-2.5-pro",
        contents=[image, prompt],
        config=types.GenerateContentConfig(
            response_mime_type="application/json"
        )
    )

    try:
        result_json = json.loads(response.text)
        return result_json
    except Exception as e:
        print(f"[ERROR] Style Analyzer JSON 파싱 실패: {e}")
        return {"styled_text_blocks": [], "raw_response": response.text}

if __name__ == "__main__":
    print("[INFO] style_analyzer.py 모듈 단체 테스트용 스크립트입니다.")
