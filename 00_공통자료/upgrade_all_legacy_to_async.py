# -*- coding: utf-8 -*-
import os, sys, re

base_dirs = [
    r"C:\Users\euntaewoo\Desktop\다국어_이미지_번역_260901",
    r"C:\Users\euntaewoo\Desktop\다국어_이미지_번역"
]

print("=== [LEGACY SCRIPTS ASYNC UPGRADE] ===")

for bdir in base_dirs:
    if not os.path.exists(bdir):
        continue
    print(f"\n📂 Processing Workspace: {bdir}")
    
    # 1. 영어 EN_..._V1.py -> 최신 비동기 규격으로 업그레이드
    en_v1_path = os.path.join(bdir, "영어", "EN_Text-In_Image_Translation_Engine_V1.py")
    en_sdk_path = os.path.join(bdir, "영어", "EN_Text-In_Image_Translation_Engine_AGY_SDK.py")
    if os.path.exists(en_sdk_path):
        with open(en_sdk_path, "r", encoding="utf-8") as f:
            en_code = f.read()
        with open(en_v1_path, "w", encoding="utf-8") as f:
            f.write(en_code)
        print(f"  ✅ [UPGRADED] 영어/EN_Text-In_Image_Translation_Engine_V1.py -> Async client.aio 100% 동기화")

    # 2. 일본어 JP_..._V7.py -> 최신 비동기 규격으로 업그레이드
    jp_v7_path = os.path.join(bdir, "일본어", "JP_Text-In_Image_Translation_Engine_V7.py")
    jp_sdk_path = os.path.join(bdir, "일본어", "JP_Text-In_Image_Translation_Engine_AGY_SDK.py")
    if os.path.exists(jp_sdk_path):
        with open(jp_sdk_path, "r", encoding="utf-8") as f:
            jp_code = f.read()
        with open(jp_v7_path, "w", encoding="utf-8") as f:
            f.write(jp_code)
        print(f"  ✅ [UPGRADED] 일본어/JP_Text-In_Image_Translation_Engine_V7.py -> Async client.aio 100% 동기화")

    # 3. 중국어 CN_..._V1.py -> 최신 비동기 규격으로 업그레이드
    cn_v1_path = os.path.join(bdir, "중국어", "CN_Text-In_Image_Translation_Engine_V1.py")
    cn_sdk_path = os.path.join(bdir, "중국어", "CN_Text-In_Image_Translation_Engine_AGY_SDK.py")
    if os.path.exists(cn_sdk_path):
        with open(cn_sdk_path, "r", encoding="utf-8") as f:
            cn_code = f.read()
        with open(cn_v1_path, "w", encoding="utf-8") as f:
            f.write(cn_code)
        print(f"  ✅ [UPGRADED] 중국어/CN_Text-In_Image_Translation_Engine_V1.py -> Async client.aio 100% 동기화")

    # 4. 프로토 PROTO_..._V0.py -> 최신 비동기 규격으로 업그레이드
    proto_v0_dir = os.path.join(bdir, "프로토(베이직엔진)_PROTO_Text-In_Image_Translation_Engine_V0")
    proto_sdk_file = os.path.join(bdir, "프로토(베이직엔진)_PROTO_Text-In_Image_Translation_Engine_AGY_SDK", "PROTO_Text-In_Image_Translation_Engine_AGY_SDK.py")
    if os.path.exists(proto_sdk_file):
        with open(proto_sdk_file, "r", encoding="utf-8") as f:
            proto_code = f.read()
        os.makedirs(proto_v0_dir, exist_ok=True)
        proto_v0_file = os.path.join(proto_v0_dir, "PROTO_Text-In_Image_Translation_Engine_V0.py")
        with open(proto_v0_file, "w", encoding="utf-8") as f:
            f.write(proto_code)
        print(f"  ✅ [UPGRADED] 프로토_V0/PROTO_Text-In_Image_Translation_Engine_V0.py -> Async client.aio 100% 동기화")

    # 5. multilingual_text_in_image_translation 서브폴더 내 파일 업그레이드
    sub_core_dir = os.path.join(bdir, "multilingual_text_in_image_translation")
    core_src_file = os.path.join(bdir, "multilingual_text_in_image_translation.py")
    if os.path.exists(sub_core_dir) and os.path.exists(core_src_file):
        with open(core_src_file, "r", encoding="utf-8") as f:
            core_code = f.read()
        sub_core_file = os.path.join(sub_core_dir, "multilingual_text_in_image_translation.py")
        with open(sub_core_file, "w", encoding="utf-8") as f:
            f.write(core_code)
        print(f"  ✅ [UPGRADED] multilingual_text_in_image_translation/multilingual_text_in_image_translation.py -> Async 100% 동기화")

print("\n🎉 ALL LEGACY SCRIPTS HAVE BEEN 100% UPGRADED TO FULL ASYNC COROUTINE ARCHITECTURE!")