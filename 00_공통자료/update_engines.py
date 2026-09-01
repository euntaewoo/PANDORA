# -*- coding: utf-8 -*-
import os, sys, re

core_file = r"C:\Users\euntaewoo\Desktop\multilingual_text_in_image_translatio_agy_sdk_uv-version\multilingual_text_in_image_translatio_agy_sdk_core\multilingual_text_in_image_translation.py"
root_file = r"C:\Users\euntaewoo\Desktop\multilingual_text_in_image_translatio_agy_sdk_uv-version\multilingual_text_in_image_translatio_agy_sdk.py"

with open(core_file, "r", encoding="utf-8") as f:
    content = f.read()

# 1. GLOBAL_COMPLIANCE_SYSTEM_INSTRUCTION 주입
sys_instruction_block = '''
# =================================================================================
# 0. 전역 글로벌 컴플라이언스(법무) & 럭셔리 초월번역 시스템 인스트럭션
# =================================================================================
GLOBAL_COMPLIANCE_SYSTEM_INSTRUCTION = """[SYSTEM INSTRUCTION: Global Cross-Border E-Commerce Compliance & Prestige Beauty Transcreation Expert]
당신은 미국 FDA(MoCRA), 일본 후생노동성(약기법), 중국 NMPA/신광고법, 대만 TFDA 규정을 완벽히 준수하는 15년 차 글로벌 뷰티 법무 감사관이자, 세포라(Sephora)·백화점 럭셔리 브랜드의 수석 카피라이터입니다.

[엄격 실행 4대 대원칙 (STRICT EXECUTION RULES)]
1. [컴플라이언스 & 의약품 오인 원천 차단 (First Principles Heuristic)]:
   - 인체 구조, 생리적 기능, 세포(Cell/Cellular) 단위의 생화학적 변화나 치료·재생을 암시하는 클레임(예: cellular vitality, cellular resilience, cell metabolism, collagen synthesis)을 100% 원천 차단하십시오.
   - 사전에 등록되지 않은 신규 성분/어휘라도 세포/생리기능 직접 관여 뉘앙스가 있다면 무조건 '피부 표면의 미용적 외관 개선(-looking, appearance of, natural moisture barrier)'으로 안전하게 우회하십시오.
2. [타겟 권역별 문화적 어댑테이션 및 콩글리시 배제]:
   - 영미권(EN): 콩글리시('Complex skin issues' -> 'Multiple skin concerns', 'Troubled skin' -> 'Blemish-prone skin') 전면 배제 및 직관적 뷰티 표준어 적용. 노화 서술 시 'combats the signs of premature aging'으로 징후(signs) 한정.
   - 일본(JP): 후생노동성 56종 허용 효능(Positive List) 엄격 준수 ('肌を整える', 'うるおいを与える' 등).
   - 중화권(CN/TW): 신광고법 8대 절대화 금지어('最', '第一', '顶级' 등) 배제 및 NMPA/TFDA 화장품 규정 준수.
3. [디자인 & 레이아웃 최적화]:
   - 이미지 레이아웃에 텍스트가 위화감 없이 안착하도록 글자 수 길이를 최적화하고, 백화점 럭셔리 브랜드 수준의 세련된 어휘로 초월번역을 수행하십시오.
4. [고시정보 및 법정 필수 조항]:
   - 고객센터 전화번호(+82 국제번호 통일), 기능성화장품 심사 상태, 주의사항 3대 조항을 정확히 표준화하십시오.
"""
'''

if "GLOBAL_COMPLIANCE_SYSTEM_INSTRUCTION" not in content:
    content = content.replace('MODEL_FLASH_IMAGE = "gemini-3.1-flash-image"', 'MODEL_FLASH_IMAGE = "gemini-3.1-flash-image"\n' + sys_instruction_block)

# 2. compliance_lexicons 동적 로더 함수 주입
loader_block = '''
# =================================================================================
# 2-0. [DYNAMIC-COMPLIANCE-LEXICON-LOADER] 국가별 표준 렉시콘 JSON 동적 로더
# =================================================================================
def load_dynamic_compliance_lexicon(lang_code: str) -> Tuple[Dict[str, str], str]:
    """
    00_공통자료/compliance_lexicons 디렉터리에서 해당 국가 표준 렉시콘 JSON을 실시간 로드하여
    (1) Python 정규식 강제 치환 딕셔너리, (2) Pass 1 프롬프트 주입문으로 변환합니다.
    """
    lex_dir_candidates = [
        os.path.join(PROJECT_ROOT, "00_공통자료", "compliance_lexicons"),
        os.path.join(SCRIPT_DIR, "..", "00_공통자료", "compliance_lexicons"),
        os.path.join(SCRIPT_DIR, "compliance_lexicons")
    ]
    lex_dir = None
    for cand in lex_dir_candidates:
        if os.path.exists(cand):
            lex_dir = cand
            break
            
    mapping = {
        "EN": "en_fda_mocra_lexicon.json",
        "JP": "jp_pmda_pharm_lexicon.json",
        "CN": "cn_nmpa_adlaw_lexicon.json",
        "TW": "tw_tfda_lexicon.json",
    }
    fname = mapping.get(lang_code.upper(), "en_fda_mocra_lexicon.json")
    fpath = os.path.join(lex_dir, fname) if lex_dir else None
    
    replacements = {}
    prompt_lines = []
    
    if fpath and os.path.exists(fpath):
        try:
            with open(fpath, "r", encoding="utf-8") as f:
                lex_data = json.load(f)
                cats = lex_data.get("categories", {})
                for c_key, c_val in cats.items():
                    desc = c_val.get("description", "")
                    banned_list = c_val.get("banned_terms", [])
                    if banned_list:
                        prompt_lines.append(f"### [COMPLIANCE LEXICON: {desc}]")
                        for item in banned_list:
                            b = item.get("banned", "").strip()
                            p = item.get("preferred", "").strip()
                            r = item.get("reason", "").strip()
                            if b and p:
                                replacements[b] = p
                                prompt_lines.append(f"- BANNED: `{b}` -> MUST USE: `{p}` ({r})")
        except Exception as e:
            print(f"  ⚠️ [WARN] 렉시콘 로드 실패 ({fpath}): {e}")
            
    prompt_str = "\\n".join(prompt_lines)
    return replacements, prompt_str
'''

if "def load_dynamic_compliance_lexicon" not in content:
    content = content.replace('def load_jp_efficacy_list() -> str:', loader_block + '\ndef load_jp_efficacy_list() -> str:')

# 3. apply_deterministic_qa_overrides 보강
old_mocra = '''    mocra_banned_replacements = {
        r"\\bPrescribe\\b": "Targeted Solution for",
        r"\\bprescribe\\b": "targeted solution for",
        r"\\bBio-Immunity\\b": "Skin Defense",
        r"\\bbio-immunity\\b": "skin defense",
        r"\\bfed directly\\b": "infused daily",
        r"\\bKyel-Tan-Tone\\b": "Texture, Elasticity & Luminosity",
        r"\\bkyel-tan-tone\\b": "texture, elasticity & luminosity",
    }'''

new_mocra = '''    # 동적 렉시콘 JSON에서 실시간 치환 규칙 병합
    dynamic_replacements, _ = load_dynamic_compliance_lexicon(lang_code)
    
    mocra_banned_replacements = {
        r"\\bPrescribe\\b": "Targeted Solution for",
        r"\\bprescribe\\b": "targeted solution for",
        r"\\bBio-Immunity\\b": "Skin Defense",
        r"\\bbio-immunity\\b": "skin defense",
        r"\\bfed directly\\b": "infused daily",
        r"\\bKyel-Tan-Tone\\b": "Texture, Elasticity & Luminosity",
        r"\\bkyel-tan-tone\\b": "texture, elasticity & luminosity",
        # 5대 법적 리스크 및 콩글리시 완벽 강제 치환
        r"\\bComplex skin issues\\b": "Multiple skin concerns",
        r"\\bcomplex skin issues\\b": "multiple skin concerns",
        r"\\bTroubled skin\\b": "Blemish-prone skin",
        r"\\btroubled skin\\b": "blemish-prone skin",
        r"\\bnutrients for cellular vitality\\b": "hydration for a resilient-looking complexion",
        r"\\bcellular vitality\\b": "resilient-looking complexion",
        r"\\breinforces cellular resilience\\b": "reinforces the skin's natural moisture barrier",
        r"\\bcellular resilience\\b": "skin's natural moisture barrier",
        r"\\bcombats premature aging\\b": "combats the signs of premature aging",
        r"\\bcombats aging\\b": "combats the signs of aging",
        r"\\bcellular metabolism\\b": "natural skin vitality",
    }
    for dyn_b, dyn_p in dynamic_replacements.items():
        dyn_pat = rf"\\b{re.escape(dyn_b)}\\b"
        if dyn_pat not in mocra_banned_replacements:
            mocra_banned_replacements[dyn_pat] = dyn_p'''

content = content.replace(old_mocra, new_mocra)

# 4. GenerateContentConfig 호출부에 system_instruction 주입
content = content.replace(
    '            config=types.GenerateContentConfig(\n                response_mime_type="application/json",\n                temperature=0.6,\n                top_p=0.9,\n                max_output_tokens=8192\n            )',
    '            config=types.GenerateContentConfig(\n                system_instruction=GLOBAL_COMPLIANCE_SYSTEM_INSTRUCTION,\n                response_mime_type="application/json",\n                temperature=0.6,\n                top_p=0.9,\n                max_output_tokens=8192\n            )'
)

with open(core_file, "w", encoding="utf-8") as f:
    f.write(content)

with open(root_file, "w", encoding="utf-8") as f:
    f.write(content)

print("SUCCESS: Updated core and root multilingual translation engines.")