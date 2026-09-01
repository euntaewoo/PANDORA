# -*- coding: utf-8 -*-
"""
sync_regulatory_lexicon.py
=============================================================================
글로벌 크로스보더 뷰티 규제(FDA MoCRA, 일본 약기법, 중국 NMPA, 대만 TFDA)
표준 렉시콘 데이터베이스 자동 초기화, 동적 로더 및 자율 규제 동기화 엔진
=============================================================================
"""

import os
import sys
import json
import re
from typing import Dict, Any, List, Optional, Tuple

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))
LEXICON_DIR = os.path.join(SCRIPT_DIR, "compliance_lexicons")
os.makedirs(LEXICON_DIR, exist_ok=True)

MAPPING = {
    "EN": "en_fda_mocra_lexicon.json",
    "JP": "jp_pmda_pharm_lexicon.json",
    "CN": "cn_nmpa_adlaw_lexicon.json",
    "TW": "tw_tfda_lexicon.json",
}

def load_compliance_lexicon(lang_code: str) -> Dict[str, Any]:
    """지정된 언어 코드(EN, JP, CN, TW)에 해당하는 컴플라이언스 렉시콘을 동적 로드합니다."""
    fname = MAPPING.get(lang_code.upper(), "en_fda_mocra_lexicon.json")
    fpath = os.path.join(LEXICON_DIR, fname)
    if os.path.exists(fpath):
        try:
            with open(fpath, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"[ERROR] Failed to load {fpath}: {e}")
    return {}

def extract_banned_and_replacement_map(lang_code: str) -> Tuple[Dict[str, str], List[Dict[str, str]]]:
    """
    렉시콘 JSON에서 (1) 정규식 치환용 맵 {banned: preferred}, (2) 프롬프트 주입용 목록을 추출합니다.
    """
    lexicon = load_compliance_lexicon(lang_code)
    replacements = {}
    prompt_rules = []
    
    categories = lexicon.get("categories", {})
    for cat_key, cat_data in categories.items():
        desc = cat_data.get("description", "")
        banned_terms = cat_data.get("banned_terms", [])
        for item in banned_terms:
            b = item.get("banned", "").strip()
            p = item.get("preferred", "").strip()
            r = item.get("reason", "").strip()
            if b and p:
                replacements[b] = p
                prompt_rules.append({
                    "banned": b,
                    "preferred": p,
                    "reason": r,
                    "category": desc
                })
    return replacements, prompt_rules

def append_banned_term(lang_code: str, category_key: str, banned: str, preferred: str, reason: str) -> bool:
    """신규 감지된 규제 금지어를 해당 언어 렉시콘 JSON에 동적으로 추가합니다."""
    fname = MAPPING.get(lang_code.upper(), "en_fda_mocra_lexicon.json")
    fpath = os.path.join(LEXICON_DIR, fname)
    lexicon = load_compliance_lexicon(lang_code)
    if not lexicon:
        return False
    
    cat = lexicon.get("categories", {}).get(category_key, {})
    if not cat:
        # 첫 번째 카테고리에 기본 추가
        first_key = list(lexicon.get("categories", {}).keys())[0]
        cat = lexicon["categories"][first_key]
        
    banned_list = cat.setdefault("banned_terms", [])
    
    for item in banned_list:
        if item.get("banned", "").lower() == banned.lower():
            print(f"[INFO] Term '{banned}' already exists in {fname}")
            return False
            
    banned_list.append({
        "banned": banned,
        "preferred": preferred,
        "reason": reason
    })
    
    with open(fpath, "w", encoding="utf-8") as f:
        json.dump(lexicon, f, ensure_ascii=False, indent=2)
    print(f"[SUCCESS] Added '{banned}' -> '{preferred}' to {fname}")
    return True

if __name__ == "__main__":
    for code in ["EN", "JP", "CN", "TW"]:
        reps, rules = extract_banned_and_replacement_map(code)
        print(f"[VERIFY] {code} Lexicon: {len(reps)} active replacement rules loaded.")
    print("\n[COMPLIANCE LEXICON SYSTEM INITIALIZED SUCCESSFULLY]")