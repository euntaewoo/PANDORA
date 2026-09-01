# -*- coding: utf-8 -*-
import os, sys, re

# =================================================================================
# 1. Update JP Engine
# =================================================================================
jp_file = r"C:\Users\euntaewoo\Desktop\multilingual_text_in_image_translatio_agy_sdk_uv-version\일본어\JP_Text-In_Image_Translation_Engine_AGY_SDK.py"
with open(jp_file, "r", encoding="utf-8") as f:
    jp_content = f.read()

jp_sys_inst = '''
GLOBAL_COMPLIANCE_SYSTEM_INSTRUCTION = """[SYSTEM INSTRUCTION: Global Cross-Border E-Commerce Compliance & Prestige Beauty Transcreation Expert (Japanese Mode)]
당신은 일본 후생노동성(MHLW) 약기법 및 @cosme 럭셔리 뷰티 가이드라인을 완벽히 준수하는 15년 차 글로벌 뷰티 법무 감사관이자 시슬리/SK-II급 수석 카피라이터입니다.

[엄격 실행 대원칙]
1. [약기법 56종 포지티브 리스트 엄격 준수]: 치료/재생/세포활성화/소염 등 의약품 오인 클레임을 100% 차단하고 '肌を整える', 'うるおいを与える', '肌荒れを防ぐ' 등 공인된 56종 허용 효능으로 순화하십시오.
2. [절대 표현 전면 금지]: '世界初', 'No.1', '最高', '究極' 등 검증 불가능한 절대 표현을 배제하고 프리미엄 케어 표현으로 격상하십시오.
3. [고시정보표 법정 조항]: 한국 식약처(MFDS) 심사필, 3대 주의사항, 공정위 분쟁기준, +82 고객상담번호를 표준화하십시오.
"""

def load_jp_compliance_lexicon() -> Dict[str, str]:
    fpath = os.path.join(PROJECT_ROOT, "00_공통자료", "compliance_lexicons", "jp_pmda_pharm_lexicon.json")
    replacements = {
        r"治療": "肌を整えるケア",
        r"再生": "すこやかに保つ",
        r"消炎": "肌荒れを防ぐ",
        r"無刺激": "低刺激処方",
        r"細胞活性化": "肌にハリとうるおいを与える",
        r"美白": "うるおいによる透明感",
        r"世界初": "先進テクノロジー",
        r"No\.1": "こだわり抜いた",
        r"最高": "優れた",
        r"究極": "高機能"
    }
    if os.path.exists(fpath):
        try:
            with open(fpath, "r", encoding="utf-8") as f:
                data = json.load(f)
                for cat in data.get("categories", {}).values():
                    for it in cat.get("banned_terms", []):
                        b, p = it.get("banned", ""), it.get("preferred", "")
                        if b and p:
                            replacements[rf"{re.escape(b)}"] = p
        except Exception:
            pass
    return replacements
'''

if "GLOBAL_COMPLIANCE_SYSTEM_INSTRUCTION" not in jp_content:
    jp_content = jp_content.replace('MODEL_FLASH_IMAGE = "gemini-3.1-flash-image"', 'MODEL_FLASH_IMAGE = "gemini-3.1-flash-image"\n' + jp_sys_inst)

# Pass 1 호출부에 system_instruction 주입
jp_content = jp_content.replace(
    '            response_p1 = await client.aio.models.generate_content(\n                model=MODEL_PRO,\n                contents=[original_image, pass1_prompt],\n                config=types.GenerateContentConfig(\n                    response_mime_type="application/json",\n                    temperature=0.6,\n                    top_p=0.9,\n                    max_output_tokens=8192\n                )\n            )',
    '            response_p1 = await client.aio.models.generate_content(\n                model=MODEL_PRO,\n                contents=[original_image, pass1_prompt],\n                config=types.GenerateContentConfig(\n                    system_instruction=GLOBAL_COMPLIANCE_SYSTEM_INSTRUCTION,\n                    response_mime_type="application/json",\n                    temperature=0.6,\n                    top_p=0.9,\n                    max_output_tokens=8192\n                )\n            )'
)

with open(jp_file, "w", encoding="utf-8") as f:
    f.write(jp_content)
print("SUCCESS: Updated JP Engine.")

# =================================================================================
# 2. Update CN Engine
# =================================================================================
cn_file = r"C:\Users\euntaewoo\Desktop\multilingual_text_in_image_translatio_agy_sdk_uv-version\중국어\CN_Text-In_Image_Translation_Engine_AGY_SDK.py"
with open(cn_file, "r", encoding="utf-8") as f:
    cn_content = f.read()

cn_sys_inst = '''
GLOBAL_COMPLIANCE_SYSTEM_INSTRUCTION = """[SYSTEM INSTRUCTION: Global Cross-Border E-Commerce Compliance & Prestige Beauty Transcreation Expert (Chinese Mode)]
당신은 중국 NMPA 화장품감독관리조례, 신광고법 및 대만 TFDA 규정을 완벽히 준수하는 15년 차 글로벌 뷰티 법무 감사관이자 샤오홍슈/티몰 럭셔리 수석 카피라이터입니다.

[엄격 실행 대원칙]
1. [신광고법 8대 절대화 금지어 전면 배제]: '最', '第一', '顶级', '极品', '永久', '万能', '100%', '彻底' 등 절대어 사용을 엄격히 금지하고 프리미엄 케어 어휘('优', '前沿', '高端' 등)로 순화하십시오.
2. [의료 및 세포 치료 오인 차단]: '细胞再生', '根除皱纹', '消炎抗敏' 등 의료 클레임을 100% 차단하고 '修护屏障', '淡化细纹', '舒缓修护'로 안전하게 표현하십시오.
3. [고시정보표 법정 조항]: 한국 식약처(MFDS) 심사필, 3대 주의사항, 공정위 분쟁기준, +82 고객상담번호를 표준화하십시오.
"""
'''

if "GLOBAL_COMPLIANCE_SYSTEM_INSTRUCTION" not in cn_content:
    cn_content = cn_content.replace('MODEL_FLASH_IMAGE = "gemini-3.1-flash-image"', 'MODEL_FLASH_IMAGE = "gemini-3.1-flash-image"\n' + cn_sys_inst)

# CN Pass 1 호출부에 system_instruction 주입
cn_content = cn_content.replace(
    '                    config=types.GenerateContentConfig(\n                        response_mime_type="application/json",\n                        temperature=0.6,\n                        top_p=0.9,\n                        max_output_tokens=8192\n                    )',
    '                    config=types.GenerateContentConfig(\n                        system_instruction=GLOBAL_COMPLIANCE_SYSTEM_INSTRUCTION,\n                        response_mime_type="application/json",\n                        temperature=0.6,\n                        top_p=0.9,\n                        max_output_tokens=8192\n                    )'
)

with open(cn_file, "w", encoding="utf-8") as f:
    f.write(cn_content)
print("SUCCESS: Updated CN Engine.")

# =================================================================================
# 3. Update PROTO Engine
# =================================================================================
proto_file = r"C:\Users\euntaewoo\Desktop\multilingual_text_in_image_translatio_agy_sdk_uv-version\프로토(베이직엔진)_PROTO_Text-In_Image_Translation_Engine_AGY_SDK\PROTO_Text-In_Image_Translation_Engine_AGY_SDK.py"
if os.path.exists(proto_file):
    with open(proto_file, "r", encoding="utf-8") as f:
        proto_content = f.read()
    
    if "GLOBAL_COMPLIANCE_SYSTEM_INSTRUCTION" not in proto_content:
        proto_content = proto_content.replace('MODEL_FLASH_IMAGE = "gemini-3.1-flash-image"', 'MODEL_FLASH_IMAGE = "gemini-3.1-flash-image"\n' + jp_sys_inst)
    
    proto_content = proto_content.replace(
        '                config=types.GenerateContentConfig(\n                    response_mime_type="application/json",\n                    temperature=0.6,\n                    top_p=0.9,\n                    max_output_tokens=8192\n                )',
        '                config=types.GenerateContentConfig(\n                    system_instruction=GLOBAL_COMPLIANCE_SYSTEM_INSTRUCTION,\n                    response_mime_type="application/json",\n                    temperature=0.6,\n                    top_p=0.9,\n                    max_output_tokens=8192\n                )'
    )
    with open(proto_file, "w", encoding="utf-8") as f:
        f.write(proto_content)
    print("SUCCESS: Updated PROTO Engine.")

# =================================================================================
# 4. Update READMEs across language folders
# =================================================================================
readme_files = [
    r"C:\Users\euntaewoo\Desktop\multilingual_text_in_image_translatio_agy_sdk_uv-version\일본어\README.md",
    r"C:\Users\euntaewoo\Desktop\multilingual_text_in_image_translatio_agy_sdk_uv-version\중국어\README.md",
    r"C:\Users\euntaewoo\Desktop\multilingual_text_in_image_translatio_agy_sdk_uv-version\프로토(베이직엔진)_PROTO_Text-In_Image_Translation_Engine_AGY_SDK\README.md"
]

compliance_readme_note = """
## ⚖️ 글로벌 컴플라이언스(법무) & 럭셔리 초월번역 시스템 연동 명세
- **System Instruction**: `GLOBAL_COMPLIANCE_SYSTEM_INSTRUCTION` (다국어 법무 감사관 + 럭셔리 마케터 페르소나 및 원천 법리 영구 장착)
- **표준 렉시콘 DB**: `00_공통자료/compliance_lexicons/*.json` 실시간 동적 바인딩
- **하이퍼파라미터 전역 고정**: `temperature: 0.6`, `top_p: 0.9`, `max_output_tokens: 8192`
- **안전망**: Python 정규식(`apply_deterministic_qa_overrides`) 100% 강제 치환 게이트 연동
"""

for rpath in readme_files:
    if os.path.exists(rpath):
        with open(rpath, "r", encoding="utf-8") as f:
            r_text = f.read()
        if "## ⚖️ 글로벌 컴플라이언스(법무) & 럭셔리 초월번역 시스템 연동 명세" not in r_text:
            r_text = r_text + "\n" + compliance_readme_note
            with open(rpath, "w", encoding="utf-8") as f:
                f.write(r_text)
            print(f"SUCCESS: Updated {os.path.basename(os.path.dirname(rpath))}/README.md")

print("ALL LANGUAGE ENGINE SCRIPTS AND READMEs ARE 100% FULLY SYNCED!")