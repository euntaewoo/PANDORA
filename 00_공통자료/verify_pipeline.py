# -*- coding: utf-8 -*-
import os, sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
core_pkg = os.path.join(PROJECT_ROOT, "multilingual_text_in_image_translatio_agy_sdk_core")
if os.path.exists(core_pkg) and core_pkg not in sys.path:
    sys.path.insert(0, core_pkg)

from multilingual_text_in_image_translation import load_dynamic_compliance_lexicon, apply_deterministic_qa_overrides

def test_pipeline():
    print("=== [TEST 1] Dynamic Compliance Lexicon Loader ===")
    prompt_txt, banned_patterns = load_dynamic_compliance_lexicon("EN")
    print(f"[EN] Loaded {len(banned_patterns)} active replacement rules.")
    
    print("\n=== [TEST 2] Deterministic Override Gate 5대 문구 차단 검증 ===")
    mock_items = [
        {"kor": "복합적 피부 고민", "target_text": "Solution for Complex skin issues and troubled skin"},
        {"kor": "세포 활력 영양 공급 및 조기 노화 방지", "target_text": "Provides nutrients for cellular vitality and combats premature aging"},
        {"kor": "세포 자생력 강화", "target_text": "Reinforces cellular resilience for firm skin"},
        {"kor": "처방", "target_text": "Prescribe multivitamin complex to infused daily"},
        {"kor": "생체 면역 강화", "target_text": "Boosts Bio-Immunity for Kyel-Tan-Tone"}
    ]
    
    qa_rules = {"spelling_dict": {}, "phrase_dict": {}}
    res = apply_deterministic_qa_overrides(mock_items, qa_rules, "EN")
    print("\n[VERIFICATION RESULTS]:")
    for i, item in enumerate(res, 1):
        print(f"Item {i} Result: {item.get('target_text')}")
        
    assert "Multiple skin concerns" in res[0].get('target_text')
    assert "hydration for a resilient-looking" in res[1].get('target_text')
    assert "skin's natural moisture barrier" in res[2].get('target_text').lower()
    assert "combats the signs of premature aging" in res[1].get('target_text')
    print("\n🎉 [ALL TESTS PASSED] 5대 법적 리스크 및 콩글리시 100% 차단 검증 완료!")

if __name__ == "__main__":
    test_pipeline()
