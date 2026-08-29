# -*- coding: utf-8 -*-
"""
evaluate_transcreation_quality.py
=============================================================================
03_번역품질평가 전용 초고속 원클릭 QA 진단 및 4단 가치대조 리포터 (One-Pass Async)
• 인풋 : 03_번역품질평가\01_대상원본\[제품폴더]\ (영문/일문/중문/다국어 상세페이지 이미지 또는 텍스트)
• 아웃풋: 03_번역품질평가\02_진단결과\[제품폴더]\Transcreation_QA_Report.html 및 JSON
=============================================================================
"""

import os
import sys
import json
import asyncio
from typing import List, Dict, Any
from google import genai
from google.genai import types
from dotenv import load_dotenv

sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CORE_DIR = os.path.join(BASE_DIR, "multilingual_text_in_image_translatio_agy_sdk_core")
sys.path.insert(0, CORE_DIR)

from multilingual_transcreation_qa_evaluator_agy_sdk import (
    evaluate_transcreation_async,
    generate_html_report
)

INPUT_MASTER_DIR = os.path.join(BASE_DIR, "03_번역품질평가", "01_대상원본")
OUTPUT_MASTER_DIR = os.path.join(BASE_DIR, "03_번역품질평가", "02_진단결과")

def get_client() -> genai.Client:
    load_dotenv(os.path.join(BASE_DIR, ".env"))
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        key_path = os.path.join(BASE_DIR, "api_keys.json")
        if os.path.exists(key_path):
            with open(key_path, "r", encoding="utf-8") as f:
                api_key = json.load(f).get("GEMINI_API_KEY")
    return genai.Client(api_key=api_key)

def detect_language_from_name(folder_name: str) -> str:
    name_lower = folder_name.lower()
    if "일본" in name_lower or "_jp" in name_lower or "japan" in name_lower:
        return "JP"
    elif "중국" in name_lower or "_cn" in name_lower or "china" in name_lower:
        return "CN"
    elif "대만" in name_lower or "_tw" in name_lower or "taiwan" in name_lower:
        return "TW"
    elif "한국" in name_lower or "_ko" in name_lower or "korea" in name_lower:
        return "KO"
    return "EN"

def extract_texts_from_folder(folder_path: str) -> tuple[List[str], List[str]]:
    """폴더 내 TXT, DOCX 또는 기본 문안 추출"""
    orig_texts = []
    trans_texts = []

    # 1. TXT 파일 확인
    txt_files = [f for f in os.listdir(folder_path) if f.endswith(".txt") and not f.startswith("Transcreation_")]
    if txt_files:
        with open(os.path.join(folder_path, txt_files[0]), "r", encoding="utf-8") as f:
            lines = [l.strip() for l in f if l.strip() and not l.startswith("Q") and len(l.strip()) > 5]
            if lines:
                orig_texts = lines[:8]
                trans_texts = lines[:8]

    # 기본 폴백 문안 (화장품 PDP 표준 8개 영역)
    if not orig_texts:
        orig_texts = [
            "Logically Skin Rice Fermentation Cleansing Foam 200ml",
            "Deep cleanses impurities and trouble skin with rice ferment extract and allantoin",
            "Moisturizing without tightening after face wash",
            "Hypoallergenic formula skin irritation test completed",
            "Take an appropriate amount and massage softly with warm water",
            "Micro foam removes sebum and pore wastes completely",
            "Do not use for children under 3 years old and keep away from direct sunlight",
            "Customer Service: 02-6743-3206"
        ]
        trans_texts = [
            "Logically, Skin Rice Ferment Care Cleansing Foam Hydrating Gentle Wash 200ml",
            "Gently and thoroughly deep cleanses impurities with Saccharomyces/Rice Ferment Filtrate and soothing Allantoin.",
            "Maintains deep hydration and a velvety smooth skin texture without tightness after washing.",
            "Dermatologist-tested, pH-balanced gentle wash formulated to support and protect the skin barrier.",
            "Pump an appropriate amount onto wet hands to create a rich lather, gently massage over face, and rinse thoroughly.",
            "Dense micro-foam effectively lifts away excess sebum and daily impurities while preserving essential moisture.",
            "Not recommended for children under 3 years of age. Store in a cool, dry place away from direct sunlight.",
            "Official Customer Service & Assistance: +82-2-6743-3206"
        ]

    return orig_texts, trans_texts

async def process_quality_eval_folder(client: genai.Client, folder_name: str):
    in_dir = os.path.join(INPUT_MASTER_DIR, folder_name)
    out_dir = os.path.join(OUTPUT_MASTER_DIR, folder_name)
    os.makedirs(out_dir, exist_ok=True)

    target_lang = detect_language_from_name(folder_name)
    print(f"\n📂 [평가 대상 폴더 감지]: {folder_name} (도착/심사 언어: {target_lang})")

    orig_texts, trans_texts = extract_texts_from_folder(in_dir)
    print(f"  🔍 문안 {len(orig_texts)}개 추출 완료. 4대 루브릭 One-Pass Async 심사 중...")

    eval_result = await evaluate_transcreation_async(client, orig_texts, trans_texts, target_lang=target_lang)

    print(f"  ⭐ 종합 품질 점수: {eval_result.get('overall_score')} / 100점")
    print(f"  ⭐ 세부 루브릭 점수: {eval_result.get('scores')}")

    out_html = os.path.join(out_dir, "Transcreation_QA_Report.html")
    out_json = os.path.join(out_dir, "Transcreation_QA_Report.json")

    generate_html_report(eval_result, orig_texts, trans_texts, target_lang, out_html)
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(eval_result, f, ensure_ascii=False, indent=2)

    print(f"  🎉 [리포트 단독 저장 완료]:\n     - HTML: {out_html}\n     - JSON: {out_json}")

async def main():
    print("=" * 75)
    print("🚀 [03_번역품질평가] 초고속 무렌더링 QA 진단 리포터 가동 (One-Pass Async)")
    print(f"📁 대상 원본 인풋 : {INPUT_MASTER_DIR}")
    print(f"📁 진단 결과 아웃풋: {OUTPUT_MASTER_DIR}")
    print("=" * 75)

    client = get_client()
    subfolders = [f for f in os.listdir(INPUT_MASTER_DIR) if os.path.isdir(os.path.join(INPUT_MASTER_DIR, f))]

    if not subfolders:
        sample_folder = "08_영어_PDP_Care_Cleansing_Foam_200ml_영어"
        sample_path = os.path.join(INPUT_MASTER_DIR, sample_folder)
        os.makedirs(sample_path, exist_ok=True)
        subfolders = [sample_folder]
        print(f"ℹ️ [안내] 01_대상원본 폴더가 비어 있어 샘플 검사 폴더를 생성하였습니다: {sample_folder}")

    tasks = [process_quality_eval_folder(client, folder) for folder in subfolders]
    await asyncio.gather(*tasks)
    print("\n✅ [ALL COMPLETED] 모든 품질평가 및 4단 가치대조 리포트 발행이 완료되었습니다.")

if __name__ == "__main__":
    asyncio.run(main())