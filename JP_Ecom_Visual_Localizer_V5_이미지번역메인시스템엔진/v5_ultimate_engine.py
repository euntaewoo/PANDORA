import os
import io
from google.genai import Client
from google.genai.types import Part
from PIL import Image

def run_ultimate_engine():
    print("V5 Ultimate Engine (Cloud Image Generation) Initialization...")
    # Use the original Vertex AI service account based on user requirement
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "vertex_service_account.json"
    
    # Initialize Vertex AI Client
    client = Client(vertexai=True, location='us-central1', project='light-depot-238403')
    
    img_path = r"D:\Users\euntaewoo\Desktop\이미지번역_KOR_To_JP_와이즈엠엔씨\이미지_한국어_일본어번역\07.Professional Sun Block SPF50+\07_sun_Block_SPF50++\국문\웹상세설명페이지\04_웹상세페이지_Professional Sun Block 70g.png"
    out_path = r"D:\Users\euntaewoo\Desktop\JP_Ecom_Visual_Localizer_V3\v5_ultimate_result_04.png"

    prompt = """
    Please perform an Image-to-Image translation.
    Maintain the exact background (white cream texture) and product arrangement.
    Erase the original Korean text and replace it with this Japanese translation in elegant typography:
    - Title: アウトドアに最適なテクスチャ
    - Subtitle 1: 肌にやさしく、すっと馴染むテクスチャ
    - Subtitle 2: 汗をかいても崩れにくく、サラサラ感をキープ
    Output ONLY the generated image. Do NOT output text.
    """

    with open(img_path, "rb") as f:
        image_bytes = f.read()

    # Models officially instructed by the user
    models_to_test = ["gemini-3-pro-image", "gemini-3.1-flash-image"]
    success = False

    for model_name in models_to_test:
        try:
            print(f"\n[TEST] Attempting {model_name} via Vertex AI...")
            response = client.models.generate_content(
                model=model_name,
                contents=[Part.from_bytes(data=image_bytes, mime_type='image/png'), prompt]
            )
            
            print(f"[SUCCESS] 200 OK from {model_name}!")
            
            image_found = False
            if hasattr(response, 'candidates'):
                for cand in response.candidates:
                    if hasattr(cand, 'content') and hasattr(cand.content, 'parts'):
                        for part in cand.content.parts:
                            # Try to extract pixel data from part
                            if hasattr(part, 'inline_data') and part.inline_data:
                                img = Image.open(io.BytesIO(part.inline_data.data))
                                img.save(out_path)
                                image_found = True
                                break
                            elif hasattr(part, 'image') and part.image:
                                img = Image.open(io.BytesIO(part.image.image_bytes))
                                img.save(out_path)
                                image_found = True
                                break
                    if image_found:
                        break
            
            if image_found:
                print(f"[SUCCESS] Final Image successfully rendered and saved to {out_path}")
                success = True
                break
            else:
                print(f"[WARNING] Model {model_name} returned 200 OK but NO image pixel data found.")
                if response.text:
                    print(f"Returned Text: {response.text[:200]}")
        except Exception as e:
            print(f"  -> [FAILED] Exception occurred: {e}")

    if not success:
        print("\n[ERROR] All Ultimate models failed to generate an image via Vertex AI generate_content().")

if __name__ == "__main__":
    run_ultimate_engine()
