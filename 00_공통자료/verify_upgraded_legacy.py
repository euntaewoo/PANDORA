# -*- coding: utf-8 -*-
import os

files = [
    r"C:\Users\euntaewoo\Desktop\다국어_이미지_번역_260901\영어\EN_Text-In_Image_Translation_Engine_V1.py",
    r"C:\Users\euntaewoo\Desktop\다국어_이미지_번역_260901\일본어\JP_Text-In_Image_Translation_Engine_V7.py",
    r"C:\Users\euntaewoo\Desktop\다국어_이미지_번역_260901\중국어\CN_Text-In_Image_Translation_Engine_V1.py",
    r"C:\Users\euntaewoo\Desktop\다국어_이미지_번역_260901\프로토(베이직엔진)_PROTO_Text-In_Image_Translation_Engine_V0\PROTO_Text-In_Image_Translation_Engine_V0.py"
]

for fp in files:
    if os.path.exists(fp):
        with open(fp, "r", encoding="utf-8") as f:
            code = f.read()
        has_async_call = "await client.aio.models.generate_content" in code
        has_sys = "GLOBAL_COMPLIANCE_SYSTEM_INSTRUCTION" in code
        async_tag = "✅ 통과" if has_async_call else "❌ 실패"
        sys_tag = "✅ 통과" if has_sys else "❌ 실패"
        print(f"📄 {os.path.basename(fp)} -> Async Call: {async_tag} | System Instruction: {sys_tag}")
    else:
        print(f"❌ 파일 없음: {fp}")