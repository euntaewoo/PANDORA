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

in_path = r"D:\Users\euntaewoo\Desktop\이미지번역_KOR_To_JP_와이즈엠엔씨\이미지_한국어_일본어번역\07.Professional Sun Block SPF50+\07_sun_Block_SPF50++\국문\웹상세설명페이지\03_웹상세페이지_Professional Sun Block 70g.png"
# 아티팩트 디렉토리에 바로 최종 이미지 저장
out_path = r"C:\Users\euntaewoo\.gemini\antigravity\brain\d1efce9b-baf0-48ea-8e83-e981fb03c659\03_Translated.png"

# 1. 03번 원본 이미지 로드 및 크롭 (하단 임상데이터 폭탄 제거)
print("[INFO] 03번 이미지 로드 및 상단 크롭 진행 중...")
try:
    original_image = Image.open(in_path)
    width, height = original_image.size
    
    # 상단에서 약 40% 지점까지만 크롭 (노란색 원형 그래픽이 끝나는 여백)
    crop_height = int(height * 0.40)
    cropped_image = original_image.crop((0, 0, width, crop_height))
    print(f"[SUCCESS] 크롭 완료 (원본 높이: {height} -> 크롭 높이: {crop_height})")
    
except Exception as e:
    print(f"[ERROR] 이미지 로드 또는 크롭 실패: {e}")
    exit()

# 2. 사용자 강제 지시 약기법 대체 번역 프롬프트
prompt = """
첨부된 크롭된 원본 이미지 속의 텍스트 위치와 배경 텍스처(노란색 원 등), 디자인 레이아웃을 1픽셀의 왜곡 없이 그대로 유지해라.
그리고 한국어 텍스트만 일본어(Qoo10 Japan PMDA 규정 완벽 준수)로 자연스럽게 교체한 완성된 단일 이미지를 생성해 줘.

[상단 영역 필수 대체 번역 지침]
1. "회복 및 개선효과" -> 절대 직역 금지. "肌を健やかに保つ"로 완벽히 대체.
2. "#미백" -> 기능성 오해 소지가 있으므로 "#透明感ケア"로 우회.
3. "#주름개선" -> "#エイジングケア"로 우회.
4. "#광노화케어" -> "#紫外線ダメージケア"로 대체.
5. "#진정" -> "#肌荒れ防止"로 대체.
"""

print(f"[START] 03번 특수 대안 엔진 (크롭 + 텍스트 세탁) 렌더링 시작...")
try:
    response = client.models.generate_content(
        model=MODEL_ID,
        contents=[prompt, cropped_image]
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
        print(f"[SUCCESS] 03번 특수 렌더링 완료! 저장 경로: {out_path}")
    else:
        print("[FAILED] API 호출 성공이나 이미지 데이터 반환 안됨 (차단됨).")
        if response.text:
            print(f"텍스트 반환값: {response.text}")
            
except Exception as e:
    print(f"[ERROR] API 호출 실패: {e}")
