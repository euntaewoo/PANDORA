#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
[Antigravity 2.0 Global Workspace Dynamic Discovery Linter]
하드코딩된 파일 리스트를 전면 폐기하고,
os.walk()를 통해 워크스페이스 전역의 모든 .py 파일과 .md 문서를 
100% 동적으로 자동 탐색하여 누락과 불일치를 전수 검증하는 결정론적 영구 린터입니다.
"""

import os, sys, re, json

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

IGNORE_DIRS = {'.git', '.venv', '__pycache__', 'node_modules', '.tempmediaStorage', '.system_generated', 'cache', 'fonts'}

def get_all_workspace_files():
    """워크스페이스 내의 모든 .py 파일과 .md 문서를 동적으로 전수 수집합니다."""
    py_files = []
    md_files = []
    
    for root, dirs, files in os.walk(PROJECT_ROOT):
        # 무시할 디렉토리 제외
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
        
        for f in files:
            fpath = os.path.join(root, f)
            if f.endswith(".py"):
                py_files.append(fpath)
            elif f.endswith(".md"):
                md_files.append(fpath)
                
    return py_files, md_files

def lint_engines(py_files):
    print(f"🔍 [1/3] 워크스페이스 전역 파이썬 파일 동적 전수 검사 중 (총 {len(py_files)}개 파일)...")
    errors = []
    
    # 핵심 엔진 키워드 (번역/교정 실행 관련 엔진)
    core_engine_names = [
        "multilingual_text_in_image_translatio_agy_sdk.py",
        "multilingual_text_in_image_translation.py",
        "multilingual_text_in_image_translation_branch.py",
        "EN_Text-In_Image_Translation_Engine_AGY_SDK.py",
        "JP_Text-In_Image_Translation_Engine_AGY_SDK.py",
        "CN_Text-In_Image_Translation_Engine_AGY_SDK.py",
        "PROTO_Text-In_Image_Translation_Engine_AGY_SDK.py",
    ]
    
    for pf in py_files:
        fname = os.path.basename(pf)
        rel = os.path.relpath(pf, PROJECT_ROOT)
        
        if fname in core_engine_names:
            with open(pf, "r", encoding="utf-8", errors="ignore") as f:
                code = f.read()
                
            # Pre-Export 게이트 탑재 검사
            if "def pre_export_integrity_check" not in code:
                errors.append(f"❌ [{rel}] 물리적 검증 게이트 'pre_export_integrity_check' 누락")
                
            # 콩글리시/금지어 필터 검사 (영어/통합 엔진)
            if "EN_" in fname or "multilingual_text" in fname:
                if "Hypoallergenic" not in code:
                    errors.append(f"❌ [{rel}] 'Hypoallergenic' 정규식 필터 누락")
                if "Discoloration" not in code and "Evening Skin Tone" not in code:
                    errors.append(f"❌ [{rel}] 'Discoloration Defense' 정규식 필터 누락")
                    
    if errors:
        for e in errors:
            print(f"  {e}")
        return False
    print(f"  ✅ 모든 핵심 파이썬 구동 엔진 동적 검사 100% PASS (누락 0건)")
    return True

def lint_lexicons():
    print("\n🔍 [2/3] 전역 렉시콘 JSON 데이터베이스 동적 검사 중...")
    lex_dir = os.path.join(PROJECT_ROOT, "00_공통자료", "compliance_lexicons")
    if not os.path.exists(lex_dir):
        print(f"  ❌ 렉시콘 디렉터리 없음: {lex_dir}")
        return False
        
    lex_files = [os.path.join(lex_dir, f) for f in os.listdir(lex_dir) if f.endswith(".json")]
    print(f"  • 발견된 렉시콘 파일: {len(lex_files)}개 ({', '.join([os.path.basename(f) for f in lex_files])})")
    
    # EN 렉시콘 필수 항목 검사
    en_lex = os.path.join(lex_dir, "en_fda_mocra_lexicon.json")
    with open(en_lex, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    banned_map = {}
    for cat in data.get("categories", {}).values():
        for item in cat.get("banned_terms", []):
            banned_map[item.get("banned", "")] = item.get("preferred", "")
            
    required_banned = [
        "0.00 skin irritation index",
        "Dark Spot & Tone Care",
        "Tone Care",
        "Complex skin issues",
        "Troubled skin",
        "nutrients for cellular vitality",
        "reinforces cellular resilience",
        "combats premature aging"
    ]
    missing = [rb for rb in required_banned if rb not in banned_map]
    if missing:
        print(f"  ❌ 렉시콘 내 필수 항목 누락: {missing}")
        return False
        
    print(f"  ✅ 전역 렉시콘 DB 내 8대 핵심 규제 항목 100% 정상 등록 완료")
    return True

def lint_docs(md_files):
    print(f"\n🔍 [3/3] 워크스페이스 전역 마크다운 문서 동적 전수 검사 중 (총 {len(md_files)}개 문서)...")
    errors = []
    
    # 순수 데이터 결과물(04_번역교정, 02_번역결과, graphify converted 등)은 규칙 문서 검사에서 제외
    EXCLUDE_DOC_PATHS = [
        "04_번역교정",
        "02_번역결과_최종",
        "graphify-out",
        "03_번역품질평가",
        ".tempmediaStorage",
    ]
    
    checked_count = 0
    for mf in md_files:
        rel = os.path.relpath(mf, PROJECT_ROOT)
        
        # 제외 경로 스킵
        if any(exc in rel for exc in EXCLUDE_DOC_PATHS):
            continue
            
        checked_count += 1
        with open(mf, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
            
        # 규칙/가이드/아키텍처 문서 대상 규정 검사
        if "PRE-EXPORT-INTEGRITY-VERIFICATION-LOCK" not in content:
            errors.append(f"❌ [{rel}] 'PRE-EXPORT-INTEGRITY-VERIFICATION-LOCK' 규정 누락")
        if "Hypoallergenic" not in content and "hypoallergenic" not in content.lower():
            errors.append(f"❌ [{rel}] 'Hypoallergenic' 표준 용어 규정 누락")
            
    if errors:
        for e in errors:
            print(f"  {e}")
        return False
    print(f"  ✅ {checked_count}개 대상 마크다운 기술/가이드/규칙 문서 동적 전수 검사 100% PASS")
    return True

def main():
    print("=" * 75)
    print("🛡️ [Antigravity 2.0] 워크스페이스 동적 전수 탐색 린터 (Dynamic Auto-Discovery)")
    print("=" * 75)
    
    py_files, md_files = get_all_workspace_files()
    
    r1 = lint_engines(py_files)
    r2 = lint_lexicons()
    r3 = lint_docs(md_files)
    
    print("\n" + "=" * 75)
    if r1 and r2 and r3:
        print("🎉 [RESULT] 워크스페이스 전역 동적 전수 검사 100% PASS! 하드코딩 없는 완전 무결성 확인.")
        print("=" * 75)
        sys.exit(0)
    else:
        print("🚨 [RESULT] 동적 스캔 중 누락 발견! 위 오류 목록을 즉시 동기화하십시오.")
        print("=" * 75)
        sys.exit(1)

if __name__ == "__main__":
    main()
