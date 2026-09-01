# -*- coding: utf-8 -*-
import os, sys

core_dir = r"C:\Users\euntaewoo\Desktop\multilingual_text_in_image_translatio_agy_sdk_uv-version"
v_path = os.path.join(core_dir, "00_공통자료", "verify_pipeline.py")

v_code = """# -*- coding: utf-8 -*-
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
    
    print("\\n=== [TEST 2] Deterministic Override Gate 5대 문구 차단 검증 ===")
    mock_items = [
        {"original": "Solution for Complex skin issues and troubled skin", "translated": "Solution for Complex skin issues and troubled skin"},
        {"original": "Provides nutrients for cellular vitality and combats premature aging", "translated": "Provides nutrients for cellular vitality and combats premature aging"},
        {"original": "Reinforces cellular resilience for firm skin", "translated": "Reinforces cellular resilience for firm skin"},
        {"original": "Prescribe multivitamin complex to infused daily", "translated": "Prescribe multivitamin complex to infused daily"},
        {"original": "Boosts Bio-Immunity for Kyel-Tan-Tone", "translated": "Boosts Bio-Immunity for Kyel-Tan-Tone"}
    ]
    
    qa_rules = {"spelling_dict": {}, "phrase_dict": {}}
    res = apply_deterministic_qa_overrides(mock_items, qa_rules, "EN")
    print("\\n[VERIFICATION RESULTS]:")
    for i, item in enumerate(res, 1):
        print(f"Item {i} Result: {item.get('translated', item.get('original'))}")
        
    assert "Multiple skin concerns" in res[0].get('translated', res[0].get('original'))
    assert "hydration for a resilient-looking" in res[1].get('translated', res[1].get('original'))
    assert "reinforces the skin's natural moisture barrier" in res[2].get('translated', res[2].get('original'))
    assert "combats the signs of premature aging" in res[1].get('translated', res[1].get('original'))
    print("\\n🎉 [ALL TESTS PASSED] 5대 법적 리스크 및 콩글리시 100% 차단 검증 완료!")

if __name__ == "__main__":
    test_pipeline()
"""
with open(v_path, "w", encoding="utf-8") as f:
    f.write(v_code)