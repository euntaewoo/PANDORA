import os
from google.genai import Client
from google.genai.types import GenerateImagesConfig
from PIL import Image

def test_v5_image_to_image():
    print("Testing V5 Image-to-Image API...")
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "vertex_service_account.json"
    client = Client(vertexai=True, location='us-central1', project='light-depot-238403')

    # Read original image to use as reference
    img_path = r"D:\Users\euntaewoo\Desktop\이미지번역_KOR_To_JP_와이즈엠엔씨\이미지_한국어_일본어번역\07.Professional Sun Block SPF50+\07_sun_Block_SPF50++\국문\웹상세설명페이지\01_웹상세페이지_Professional Sun Block 70.png"
    original_img = Image.open(img_path)

    # Prompt: We need to translate text to Japanese, following PMDA rules, keeping layout.
    prompt = """
    Recreate this cosmetic promotional image exactly.
    Change the Korean text to Japanese with the following PMDA-compliant copywriting:
    - Main Title: プロフェッショナル
    - Subtitle: ロジカリ・スキンのディフェンスロジック
    - Features: コットンフィットテクスチャ, 多機能マルチスキンケア
    Keep the typography, font weights, and layout exactly as the original. Do not distort the product package.
    """

    # Using the google-genai SDK 2.8.0
    try:
        # In the newest SDKs, image-to-image is often done via 'generate_content' with multimodal input
        # or 'generate_images' with a reference image. Let's try generate_images with reference_image first.
        result = client.models.generate_images(
            model='gemini-2.5-flash-image',
            prompt=prompt,
            config=GenerateImagesConfig(
                number_of_images=1,
                aspect_ratio="1:1" # Just for sandbox test
            )
        )
        
        for generated_image in result.generated_images:
            image = Image.open(io.BytesIO(generated_image.image.image_bytes))
            image.save('v5_test_output.png')
            print("Successfully generated Image-to-Image output.")

    except Exception as e:
        print(f"API Error: {e}")
        # Inspect GenerateImagesConfig to see if there's a reference image parameter
        print("\nAvailable fields in GenerateImagesConfig:")
        print(GenerateImagesConfig.model_fields.keys())

if __name__ == "__main__":
    import io
    test_v5_image_to_image()
