import os
import io
import sys
import time
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

source_dir = r"D:\Users\euntaewoo\Desktop\이미지번역_KOR_To_JP_와이즈엠엔씨\이미지_한국어_일본어번역\07.Professional Sun Block SPF50+\07_sun_Block_SPF50++\국문\웹상세설명페이지"
target_dir = r"D:\Users\euntaewoo\Desktop\이미지번역_KOR_To_JP_와이즈엠엔씨\이미지_한국어_일본어번역\07.Professional Sun Block SPF50+\07_sun_Block_SPF50++\국문\웹상세설명페이지_JP_Translated"
os.makedirs(target_dir, exist_ok=True)

prompt = """
첨부된 원본 이미지 속의 한국어 텍스트 위치와 배경 텍스처, 디자인 레이아웃을 1픽셀의 왜곡 없이 그대로 유지해라.
그리고 모든 한국어 텍스트만 일본어(Qoo10 Japan PMDA 규정 완벽 준수)로 자연스럽게 교체한 완성된 단일 이미지를 생성해 줘.

[일본 약기법 필수 준수 강제 지침]
1. '자극 없이(刺激なく)', '무자극'과 같은 단정적인 표현은 절대 금지. 반드시 '피부에 순하게(肌にやさしく)' 또는 '저자극 처방(低刺激処方)'으로 안전하게 의역할 것.
2. '진정(鎮静)'이라는 의학적 치료 효능 단어 사용 절대 금지. 반드시 화장품 공식 허용 문구인 '피부를 정돈하다(肌を整える)' 또는 '피부 거칠어짐을 방지하다(肌荒れを防ぐ)'로 대체할 것.
"""

print("[START] V5 일괄 렌더링 배치 엔진 가동...")
print(f"[INFO] 타겟 스캔 폴더: {source_dir}")

for filename in os.listdir(source_dir):
    if not filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        continue
    if 'JP' in filename:
        print(f"  -> [SKIP] 이미 일본어화된 파일(JP 태그): {filename}")
        continue
        
    in_path = os.path.join(source_dir, filename)
    out_path = os.path.join(target_dir, filename)
    
    if os.path.exists(out_path):
        print(f"  -> [SKIP] 렌더링 완료본이 타겟 폴더에 이미 존재함: {filename}")
        continue
        
    print(f"\n[RENDER] 변환 시작: {filename}")
    
    try:
        original_image = Image.open(in_path)
    except Exception as e:
        print(f"  -> [ERROR] 이미지 로드 실패: {e}")
        continue

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
            print(f"  -> [SUCCESS] 렌더링 및 저장 완료!")
        else:
            print("  -> [FAILED] API 호출 성공이나 이미지 데이터 반환 안됨.")
            
    except Exception as e:
        print(f"  -> [ERROR] API 호출 실패: {e}")
    
    time.sleep(3)

print("\n[FINISH] V5 웹상세설명페이지 배치 렌더링 완료!")
