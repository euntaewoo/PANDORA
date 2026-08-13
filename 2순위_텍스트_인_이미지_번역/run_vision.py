import os
from google.cloud import vision

# 1. 실제 존재 확인된 올바른 JSON 키 경로 적용
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\Users\euntaewoo\Desktop\다국어_이미지_번역\00_공통자료\인증키_및_계정\김차장_vertex api_key\vertex_ai_auth_key.json"

# 2. Vision API 클라이언트 생성
client = vision.ImageAnnotatorClient()

def analyze_text(image_path):
    """
    이미지 경로를 받아 이미지 속 텍스트(OCR)를 추출하는 함수
    """
    try:
        # 이미지 파일 읽기
        with open(image_path, "rb") as image_file:
            content = image_file.read()

        image = vision.Image(content=content)

        # Vision API 텍스트 감지 요청
        response = client.text_detection(image=image)
        texts = response.text_annotations

        if response.error.message:
            print(f"❌ API 오류 발생: {response.error.message}")
            return

        print("\n=================== [ 추출된 텍스트 ] ===================")
        if texts:
            # 첫 번째 요소(texts[0])에 전체 감지된 문장이 들어있습니다.
            print(texts[0].description)
        else:
            print("이미지에서 텍스트를 발견하지 못했습니다.")
        print("=========================================================\n")

    except Exception as e:
        print(f"❌ 파일 읽기 또는 실행 중 에러 발생: {e}")

if __name__ == "__main__":
    # 테스트할 이미지 파일 경로를 아래에 입력해 주세요.
    test_image_path = r"C:\Users\euntaewoo\Desktop\test.png"  
    
    analyze_text(test_image_path)