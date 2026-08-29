import os
import sys
import io
import base64
from google import genai
from google.genai import types
from PIL import Image

def erase_text_for_clean_plate(image_path, detected_blocks, client, output_path):
    """
    Imagen 3 Erase / Image Editing 기능을 호출하여 텍스트 영역을 Clean Plate(깨끗한 배경)로 메웁니다.
    """
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"이미지 파일을 찾을 수 없습니다: {image_path}")

    original_image = Image.open(image_path)
    
    # 텍스트 영역만 배경으로 메우는 지시 프롬프트
    prompt = """
    Please erase all text from this image and restore the background seamlessly (Clean Plate generation). 
    Do not add any new elements or alter any non-text objects. Keep the original aspect ratio and background texture 100% untouched.
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[prompt, original_image]
    )

    img_saved = False
    if hasattr(response, 'candidates'):
        for cand in response.candidates:
            if hasattr(cand, 'content') and hasattr(cand.content, 'parts'):
                for part in cand.content.parts:
                    if hasattr(part, 'inline_data') and part.inline_data:
                        img = Image.open(io.BytesIO(part.inline_data.data))
                        img = img.resize(original_image.size, Image.Resampling.LANCZOS)
                        img.save(output_path, format="PNG")
                        img_saved = True
                        break

    # Gemini 텍스트 응답만 들어왔을 때 Pillow Bounding Box 기반 인페인팅 Fallback
    if not img_saved:
        print("[INFO] AI 이미지 직접 생성 미반환 감지 -> Bounding Box 픽셀 인페인팅 렌더링 시작...")
        from PIL import ImageDraw
        clean_img = original_image.copy().convert("RGB")
        draw = ImageDraw.Draw(clean_img)
        w, h = clean_img.size

        for block in detected_blocks:
            box = block.get("box_2d")
            if box and len(box) == 4:
                ymin, xmin, ymax, xmax = box
                # 상대 픽셀 좌표 전환
                left = int(xmin * w / 1000)
                top = int(ymin * h / 1000)
                right = int(xmax * w / 1000)
                bottom = int(ymax * h / 1000)

                # 주변 배경색 샘플링 및 마스킹
                sample_x = max(0, left - 5)
                sample_y = max(0, top - 5)
                bg_color = clean_img.getpixel((sample_x, sample_y))
                draw.rectangle([left, top, right, bottom], fill=bg_color)

        clean_img.save(output_path, format="PNG")
        img_saved = True

    if img_saved:
        print(f"[SUCCESS] Clean Plate 배경 생성 완료: {output_path}")
        return output_path
    else:
        raise RuntimeError("Clean Plate 이미지 생성을 완료하지 못했습니다.")

if __name__ == "__main__":
    print("[INFO] imagen_erase.py 모듈 단체 테스트용 스크립트입니다.")
