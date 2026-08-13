import os
import sys
import json
import base64
import shutil
from pathlib import Path
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from google import genai

# 상위 백엔드 모듈 경로 추가
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from vision_ocr import detect_text_bounding_boxes
from imagen_erase import erase_text_for_clean_plate
from style_analyzer import analyze_font_styles

app = FastAPI(title="2순위 텍스트 인 이미지 번역 에디터 API")

BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"
UPLOAD_DIR = BASE_DIR / "uploads"
OUTPUT_DIR = BASE_DIR / "outputs"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 프론트엔드 정적 파일 마운트
app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR)), name="static")

def get_genai_client():
    auth_key_path = Path("C:/Users/euntaewoo/Desktop/다국어_이미지_번역/00_공통자료/인증키_및_계정/김차장_vertex api_key/vertex_ai_auth_key.json")
    if auth_key_path.exists():
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = str(auth_key_path)
        with open(auth_key_path, 'r', encoding='utf-8') as f:
            key_data = json.load(f)
            project_id = key_data.get('project_id')
        return genai.Client(vertexai=True, project=project_id, location="us-central1")
    
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key:
        if api_key.startswith("AQ."):
            return genai.Client(vertexai=True, api_key=api_key)
        else:
            return genai.Client(api_key=api_key)
            
    raise HTTPException(status_code=500, detail="Google Cloud Vertex AI 인증키를 찾을 수 없습니다.")

@app.get("/", response_class=HTMLResponse)
async def read_index():
    index_path = FRONTEND_DIR / "index.html"
    if index_path.exists():
        return HTMLResponse(content=index_path.read_text(encoding="utf-8"))
    return HTMLResponse(content="<h1>Index.html 파일을 찾을 수 없습니다.</h1>", status_code=404)

@app.post("/api/process-image")
async def process_image(file: UploadFile = File(...), target_lang: str = Form("JP")):
    try:
        # 1. 파일 저장
        upload_path = UPLOAD_DIR / file.filename
        with open(upload_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        client = get_genai_client()

        # 2. Vision OCR 탐지
        ocr_result = detect_text_bounding_boxes(str(upload_path), client)
        if isinstance(ocr_result, list):
            detected_blocks = ocr_result
        elif isinstance(ocr_result, dict):
            detected_blocks = ocr_result.get("detected_text_blocks", [])
        else:
            detected_blocks = []

        # 3. Clean Plate 배경 생성
        clean_plate_filename = f"clean_{file.filename}"
        clean_plate_path = OUTPUT_DIR / clean_plate_filename
        erase_text_for_clean_plate(str(upload_path), detected_blocks, client, str(clean_plate_path))

        # 4. 폰트 스타일 및 번역 분석
        style_result = analyze_font_styles(str(upload_path), detected_blocks, client, target_lang=target_lang)
        if isinstance(style_result, list):
            styled_blocks = style_result
        elif isinstance(style_result, dict):
            styled_blocks = style_result.get("styled_text_blocks", style_result.get("text_blocks", []))
        else:
            styled_blocks = []

        # 백엔드 데이터 안전 포맷팅
        formatted_blocks = []
        for item in styled_blocks:
            if isinstance(item, dict):
                formatted_blocks.append(item)
            elif isinstance(item, list) and len(item) > 0:
                if isinstance(item[0], dict):
                    formatted_blocks.append(item[0])

        # 5. Clean Plate 이미지 base64 인코딩
        with open(clean_plate_path, "rb") as img_file:
            clean_plate_b64 = base64.b64encode(img_file.read()).decode('utf-8')

        return JSONResponse(content={
            "status": "success",
            "clean_plate_b64": f"data:image/png;base64,{clean_plate_b64}",
            "styled_blocks": formatted_blocks
        })

    except Exception as e:
        print(f"[ERROR] API 처리 중 오류 발생: {e}")
        return JSONResponse({"status": "error", "detail": str(e)}, status_code=500)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
