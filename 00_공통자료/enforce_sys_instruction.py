# -*- coding: utf-8 -*-
import os, sys

core_file = r"C:\Users\euntaewoo\Desktop\multilingual_text_in_image_translatio_agy_sdk_uv-version\multilingual_text_in_image_translatio_agy_sdk_core\multilingual_text_in_image_translation.py"
root_file = r"C:\Users\euntaewoo\Desktop\multilingual_text_in_image_translatio_agy_sdk_uv-version\multilingual_text_in_image_translatio_agy_sdk.py"

for target_file in [core_file, root_file]:
    with open(target_file, "r", encoding="utf-8") as f:
        text = f.read()

    # Pass 1 이미지 텍스트 추출 호출부에 system_instruction 강제 주입
    old_p1_call = """            response_p1 = await client.aio.models.generate_content(
                model=MODEL_PRO,
                contents=[original_image, pass1_prompt],
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    temperature=0.6,
                    top_p=0.9,
                    max_output_tokens=8192
                )
            )"""

    new_p1_call = """            response_p1 = await client.aio.models.generate_content(
                model=MODEL_PRO,
                contents=[original_image, pass1_prompt],
                config=types.GenerateContentConfig(
                    system_instruction=GLOBAL_COMPLIANCE_SYSTEM_INSTRUCTION,
                    response_mime_type="application/json",
                    temperature=0.6,
                    top_p=0.9,
                    max_output_tokens=8192
                )
            )"""

    text = text.replace(old_p1_call, new_p1_call)

    # DOCX 번역 호출부에도 주입
    old_docx_call = """        resp = await client.aio.models.generate_content(
            model=MODEL_PRO,
            contents=[full_prompt],
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                temperature=0.6,
                top_p=0.9,
                max_output_tokens=8192
            )
        )"""

    new_docx_call = """        resp = await client.aio.models.generate_content(
            model=MODEL_PRO,
            contents=[full_prompt],
            config=types.GenerateContentConfig(
                system_instruction=GLOBAL_COMPLIANCE_SYSTEM_INSTRUCTION,
                response_mime_type="application/json",
                temperature=0.6,
                top_p=0.9,
                max_output_tokens=8192
            )
        )"""

    text = text.replace(old_docx_call, new_docx_call)

    with open(target_file, "w", encoding="utf-8") as f:
        f.write(text)

print("SUCCESS: Enforced system_instruction across all Pass 1 calls.")