import os
import io
from google.genai import Client
from google.genai.types import GenerateImagesConfig
from PIL import Image

def run_image_gen_test():
    print("Testing gemini-3.1-flash-image in AI Studio mode with Billing Enabled...")
    
    # Load API Key from .env
    env_path = r"D:\Users\euntaewoo\Desktop\JP_Ecom_Visual_Localizer_V3\.env"
    with open(env_path, "r") as f:
        for line in f:
            if line.startswith("GEMINI_API_KEY="):
                os.environ["GEMINI_API_KEY"] = line.split("=")[1].strip()
                break
                
    # Initialize Client for AI Studio
    client = Client()
    out_path = r"D:\Users\euntaewoo\Desktop\JP_Ecom_Visual_Localizer_V3\v5_sandbox_output_flash_image.png"

    prompt = """
    A high-quality cosmetic product layout, white cream texture background.
    Include Japanese text: アウトドアに最適なテクスチャ
    """
    
    try:
        print("\n[TEST] Attempting Gemini 3.1 Flash Image Generation via AI Studio API...")
        # Since the user specifically mentioned gemini-3.1-flash-image for Image Generation (Nano Banana 2)
        result = client.models.generate_images(
            model='gemini-3.1-flash-image',
            prompt=prompt,
            config=GenerateImagesConfig(
                number_of_images=1,
                aspect_ratio="1:1"
            )
        )
        
        for generated_image in result.generated_images:
            image = Image.open(io.BytesIO(generated_image.image.image_bytes))
            image.save(out_path)
            print(f"\n[SUCCESS] Saved generated Image result to {out_path}")
            
    except Exception as e:
        print(f"\n[ERROR] AI Studio Image Generation failed: {e}")

if __name__ == "__main__":
    run_image_gen_test()
