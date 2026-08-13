import os
import io
from google.genai import Client
from google.genai.types import Part
from PIL import Image

def run_v5_sandbox():
    print("V5 Sandbox Initialization - AI Studio Fallback Mode")
    
    # Load API Key from .env
    env_path = r"D:\Users\euntaewoo\Desktop\JP_Ecom_Visual_Localizer_V3\.env"
    with open(env_path, "r") as f:
        for line in f:
            if line.startswith("GEMINI_API_KEY="):
                os.environ["GEMINI_API_KEY"] = line.split("=")[1].strip()
                break
                
    # Initialize Client without vertexai parameters to route to AI Studio
    client = Client()
    
    img_path = r"D:\Users\euntaewoo\Desktop\이미지번역_KOR_To_JP_와이즈엠엔씨\이미지_한국어_일본어번역\07.Professional Sun Block SPF50+\07_sun_Block_SPF50++\국문\웹상세설명페이지\04_웹상세페이지_Professional Sun Block 70g.png"
    out_path = r"D:\Users\euntaewoo\Desktop\JP_Ecom_Visual_Localizer_V3\v5_sandbox_output_04.png"

    prompt = """
    Recreate this cosmetic product image completely from scratch using Image-to-Image generation. 
    Maintain the exact same white cream texture background and the product layout.
    Translate the Korean text into Japanese copywriting adhering to PMDA regulations.
    - Title (Huge Bold Typography): アウトドアに最適なテクスチャ
    - Subtitle (Medium Typography): 肌にやさしく、すっと馴染むテクスチャ
    - Body (Light Typography): 汗をかいても崩れにくく、サラサラ感をキープ
    
    You must output a generated visual image (pixels), not just text description.
    """
    
    with open(img_path, "rb") as f:
        image_bytes = f.read()

    try:
        print("\n[TEST] Attempting Gemini 3.1 Pro Preview via AI Studio API...")
        response = client.models.generate_content(
            model='gemini-3.1-pro-preview',
            contents=[Part.from_bytes(data=image_bytes, mime_type='image/png'), prompt]
        )
        
        print("\n[SUCCESS] Response Received (200 OK) from AI Studio!")
        if response.text:
            print(f"Text Output: {response.text[:200]}...")
            
    except Exception as e:
        print(f"\n[ERROR] AI Studio Fallback failed: {e}")

if __name__ == "__main__":
    run_v5_sandbox()
