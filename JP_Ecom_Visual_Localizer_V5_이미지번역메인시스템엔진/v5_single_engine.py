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

# 원본 타겟 파일 및 결과물 저장 경로 명시
in_path = r"D:\Users\euntaewoo\Desktop\이미지번역_KOR_To_JP_와이즈엠엔씨\이미지_한국어_일본어번역\07.Professional Sun Block SPF50+\07_sun_Block_SPF50++\국문\웹상세설명페이지\05_웹상세페이지_Professional Sun Block 70g_상세정보안내.jfif"
out_path = r"D:\Users\euntaewoo\Desktop\이미지번역_KOR_To_JP_와이즈엠엔씨\이미지_한국어_일본어번역\07.Professional Sun Block SPF50+\07_sun_Block_SPF50++\일본어번역_웹상세페이지_Professional Sun Block 70g\05_웹상세페이지_Professional Sun Block 70g_상세정보안내_V5_FINAL.png"

# PMDA 약기법 강제 지침 프롬프트 (전성분 및 상세정보에서도 위반 방지)
prompt = """
첨부된 원본 이미지 속의 텍스트 위치와 배경 텍스처, 디자인 레이아웃을 1픽셀의 왜곡 없이 그대로 유지해라.
그리고 원본에 있는 **모든 한국어 텍스트를 단 한 문장도 빠짐없이 100% 일본어로 번역**하여 자연스럽게 교체한 완성된 단일 이미지를 생성해 줘.

[초강력 강제 지침 - 번역 누락 절대 금지]
1. 원본 이미지는 실제 소비자의 리뷰(Real Voice) 모음집이다. 텍스트가 빽빽하더라도 절대로 임의로 문장을 생략하거나 건너뛰지 마라.
2. 결과물 이미지 내에 **한국어(한글)가 단 한 글자라도 남아있으면 완벽한 실패**다. 모든 한국어 리뷰 문장(처음 들어보는 브랜드라... 등)을 샅샅이 찾아내어 100% 일본어로 교체할 것.

[일본 약기법 필수 준수 강제 지침]
1. '자극 없이(刺激なく)', '무자극'과 같은 단정적인 표현은 절대 금지. 반드시 '피부에 순하게(肌にやさしく)' 또는 '저자극 처방(低刺激処方)'으로 안전하게 의역할 것.
2. '진정(鎮静)'이라는 의학적 치료 효능 단어 사용 절대 금지. 반드시 '피부를 정돈하다(肌を整える)' 또는 '피부 거칠어짐을 방지하다(肌荒れを防ぐ)'로 대체할 것.
"""

print(f"[START] 05번 상세정보안내 단일 V5 렌더링 가동...")
try:
    original_image = Image.open(in_path)
    
    # jfif(jpeg) 포맷을 PIL이 잘 다룰 수 있도록 내부적으로 강제 로드
    original_image.load()
except Exception as e:
    print(f"[ERROR] 05번 이미지 로드 실패: {e}")
    exit()

try:
    response = client.models.generate_content(
        model=MODEL_ID,
        contents=[prompt, original_image]
    )
    
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
        print(f"[SUCCESS] 05번 렌더링 및 저장 완료!\n저장 경로: {out_path}")
    else:
        print("[FAILED] API 호출 성공이나 이미지 데이터 반환 안됨 (차단 가능성).")
        
except Exception as e:
    print(f"[ERROR] API 호출 실패: {e}")
