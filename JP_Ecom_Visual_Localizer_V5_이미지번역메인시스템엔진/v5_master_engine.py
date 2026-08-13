import os
import io
import sys
from google import genai
from PIL import Image

sys.stdout.reconfigure(encoding='utf-8')

env_path = r"D:\Users\euntaewoo\Desktop\JP_Ecom_Visual_Localizer_V5\.env"
with open(env_path, "r") as f:
    for line in f:
        if line.startswith("GEMINI_API_KEY="):
            os.environ["GEMINI_API_KEY"] = line.split("=")[1].strip()
            break

api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)
MODEL_ID = "gemini-3.1-flash-image"

img_path = r"D:\Users\euntaewoo\Desktop\이미지번역_KOR_To_JP_와이즈엠엔씨\이미지_한국어_일본어번역\07.Professional Sun Block SPF50+\07_sun_Block_SPF50++\국문\웹상세설명페이지\04_웹상세페이지_Professional Sun Block 70g.png"
try:
    original_image = Image.open(img_path)
except FileNotFoundError:
    print("[ERROR] 원본 이미지를 찾을 수 없습니다. 경로를 확인하세요.")
    exit()

# [안티그래비티 수정]: 약기법 준수 강제 지침 적용 프롬프트
prompt = """
첨부된 원본 이미지 속의 한국어 텍스트 위치와 배경 텍스처, 디자인 레이아웃을 1픽셀의 왜곡 없이 그대로 유지해라.
그리고 모든 한국어 텍스트만 일본어(Qoo10 Japan PMDA 규정 완벽 준수)로 자연스럽게 교체한 완성된 단일 이미지를 생성해 줘.

[일본 약기법 필수 준수 강제 지침]
1. '자극 없이(刺激なく)', '무자극'과 같은 단정적인 표현은 절대 금지. 반드시 '피부에 순하게(肌にやさしく)' 또는 '저자극 처방(低刺激処方)'으로 안전하게 의역할 것.
2. '진정(鎮静)'이라는 의학적 치료 효능 단어 사용 절대 금지. 반드시 화장품 공식 허용 문구인 '피부를 정돈하다(肌を整える)' 또는 '피부 거칠어짐을 방지하다(肌荒れを防ぐ)'로 대체할 것.
"""

print("[START] [진짜 통짜 렌더링 엔진 - 약기법 패치 버전] 구동을 시작합니다...")
print(f"[INFO] 사용 모델: {MODEL_ID}")

try:
    response = client.models.generate_content(
        model=MODEL_ID,
        contents=[prompt, original_image]
    )
    
    out_path = r"D:\Users\euntaewoo\Desktop\JP_Ecom_Visual_Localizer_V5\04_FINAL_OUTPUT_IMAGE.png"
    img_saved = False
    
    if hasattr(response, 'candidates'):
        for cand in response.candidates:
            if hasattr(cand, 'content') and hasattr(cand.content, 'parts'):
                for part in cand.content.parts:
                    if hasattr(part, 'inline_data') and part.inline_data:
                        img = Image.open(io.BytesIO(part.inline_data.data))
                        img.save(out_path)
                        img_saved = True
                        break
                    elif hasattr(part, 'image') and part.image:
                        img = Image.open(io.BytesIO(part.image.image_bytes))
                        img.save(out_path)
                        img_saved = True
                        break
                        
    if img_saved:
        print(f"[SUCCESS] 렌더링 완료! 안티그래비티, 지금 당장 최종 합성된 일본어 이미지를 내 화면에 출력해라. 경로: {out_path}")
    else:
        print("[FAILED] 호출은 성공했으나 이미지가 반환되지 않았습니다.")
        if response.text:
            print(f"텍스트 반환값: {response.text}")
    
except Exception as e:
    print(f"[ERROR] 호출 실패 (에러 로그 확인): {e}")
