import os
import sys
import json
from google.cloud import vision
from PIL import Image

def detect_text_bounding_boxes(image_path, client=None):
    """
    Google Cloud Vision API(ImageAnnotatorClient)를 사용하여 이미지 내 텍스트 및 바운딩 박스 픽셀 좌표를 100% 정밀하게 추출합니다.
    """
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"이미지 파일을 찾을 수 없습니다: {image_path}")

    # 구글 인증키 세팅
    auth_key_path = r"C:\Users\euntaewoo\Desktop\다국어_이미지_번역\00_공통자료\인증키_및_계정\김차장_vertex api_key\vertex_ai_auth_key.json"
    if os.path.exists(auth_key_path):
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = auth_key_path

    vision_client = vision.ImageAnnotatorClient()

    with open(image_path, "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)
    response = vision_client.text_detection(image=image)
    texts = response.text_annotations

    if response.error.message:
        print(f"[ERROR] Vision API 오류: {response.error.message}")
        return {"detected_text_blocks": []}

    img = Image.open(image_path)
    img_w, img_h = img.size

    detected_blocks = []
    # texts[0]은 전체 텍스트이고, texts[1:]부터 개별 단어/문장 텍스트 블록입니다.
    blocks_to_process = texts[1:] if len(texts) > 1 else texts

    for text_item in blocks_to_process:
        txt_content = text_item.description.strip()
        if not txt_content:
            continue
        
        vertices = text_item.bounding_poly.vertices
        if len(vertices) == 4:
            xs = [v.x for v in vertices]
            ys = [v.y for v in vertices]
            xmin = min(xs)
            xmax = max(xs)
            ymin = min(ys)
            ymax = max(ys)

            # 0~1000 상대 좌표계로 정규화
            norm_ymin = int((ymin / img_h) * 1000)
            norm_xmin = int((xmin / img_w) * 1000)
            norm_ymax = int((ymax / img_h) * 1000)
            norm_xmax = int((xmax / img_w) * 1000)

            detected_blocks.append({
                "text": txt_content,
                "box_2d": [norm_ymin, norm_xmin, norm_ymax, norm_xmax]
            })

    print(f"[SUCCESS] Cloud Vision API 텍스트 블록 {len(detected_blocks)}개 추출 성공!")
    return {"detected_text_blocks": detected_blocks}

if __name__ == "__main__":
    print("[INFO] vision_ocr.py 모듈 단체 테스트용 스크립트입니다.")
