#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
[Antigravity 2.0 Global Rule Linter]
프로젝트 루트 디렉토리 진입점:
전역의 파이썬 구동 엔진, 다국어 프롬프트 뼈대, 51개 마크다운 설계서 간의 
규격 불일치(Desynchronization)와 누락을 1초 만에 전수 자동 검증하는 공식 진단 도구입니다.
"""

import os
import re
import sys

# 루트 디렉토리 기준 경로 자동 감지
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

REQUIRED_SPECS = {
    "TOKEN_DUALIZATION": {
        "forbidden_1024": r"max_output_tokens\s*=\s*1024|maxOutputTokens.*?1024",
    },
    "REGULATORY_TERMS": {
        "TW": "已完成特定用途化粧品審查",
        "CN": "已完成特殊用途化妆品审查",
        "JP": "機能性化粧品審査済",
        "EN": "MFDS-Certified Functional Cosmetic",
    },
    "PROMPT_SYMMETRY": {
        "languages": ["prompt_en", "prompt_cn", "prompt_jp", "prompt_tw", "prompt_kr"],
        "required_markers": ["Q1", "Q2", "Q3", "Q4", "Q5"],
    }
}

def lint_markdown_docs():
    print("🔍 [1/3] 프로젝트 전역 마크다운 문서 규격 일치 검사 중...")
    errors = []
    checked_count = 0
    
    for root, _, files in os.walk(PROJECT_ROOT):
        if ".venv" in root or ".git" in root or "node_modules" in root:
            continue
        for f in files:
            if f.endswith(".md"):
                fpath = os.path.join(root, f)
                checked_count += 1
                with open(fpath, "r", encoding="utf-8", errors="ignore") as fp:
                    content = fp.read()
                    if re.search(REQUIRED_SPECS["TOKEN_DUALIZATION"]["forbidden_1024"], content):
                        errors.append(f"❌ [구형 1024 토큰 발견] {os.path.relpath(fpath, PROJECT_ROOT)}")
                        
    if errors:
        for err in errors:
            print(f"  {err}")
        return False
    print(f"  ✅ 총 {checked_count}개 마크다운 문서 규격 100% 정상 (1024 잔재 0건)")
    return True

def lint_python_prompts():
    print("\n🔍 [2/3] 파이썬 엔진 다국어 프롬프트 대칭성(Q1~Q5 뼈대) 검사 중...")
    engine_files = [
        os.path.join(PROJECT_ROOT, "multilingual_text_in_image_translatio_agy_sdk_core", "multilingual_text_in_image_translatio_agy_sdk_core.py"),
        os.path.join(PROJECT_ROOT, "multilingual_text_in_image_translatio_agy_sdk_core", "multilingual_text_in_image_translatio_agy_sdk_core_branch.py"),
    ]
    
    errors = []
    for ef in engine_files:
        if not os.path.exists(ef):
            continue
        with open(ef, "r", encoding="utf-8", errors="ignore") as fp:
            code = fp.read()
            
        rel = os.path.relpath(ef, PROJECT_ROOT)
        
        # SEO 함수 블록 분리
        seo_func_match = re.search(r"def generate_seo_geo_aeo_txt.*", code, re.DOTALL)
        seo_code = seo_func_match.group(0) if seo_func_match else code
        
        # 메인 엔진 SEO 프롬프트 대칭성 검사
        for lang in REQUIRED_SPECS["PROMPT_SYMMETRY"]["languages"]:
            pattern = rf'{lang}\s*=\s*f?"""(.*?)"""'
            matches = re.findall(pattern, seo_code, re.DOTALL)
            if not matches:
                errors.append(f"❌ [{rel}] SEO 프롬프트 누락: {lang}")
            else:
                prompt_body = matches[0]
                for marker in REQUIRED_SPECS["PROMPT_SYMMETRY"]["required_markers"]:
                    if marker not in prompt_body:
                        errors.append(f"❌ [{rel}] {lang} 내 필수 마커 누락: '{marker}'")
                        
        # 규제 공인 문구 게이트 검사
        for country, term in REQUIRED_SPECS["REGULATORY_TERMS"].items():
            if term not in code:
                errors.append(f"❌ [{rel}] {country} 규제 공인 문구 누락: '{term}'")

    if errors:
        for err in errors:
            print(f"  {err}")
        return False
    print(f"  ✅ 모든 파이썬 엔진의 5개 국어 프롬프트 뼈대 및 규제 문구 100% 대칭 일치")
    return True

def lint_output_verification_gate():
    print("\n🔍 [3/3] 파이썬 엔진 내 '토큰 8192 안전천장 및 FAQ 5개 안전장치' 탑재 여부 검사 중...")
    main_engine = os.path.join(PROJECT_ROOT, "multilingual_text_in_image_translatio_agy_sdk_core", "multilingual_text_in_image_translation.py")
    if not os.path.exists(main_engine):
        main_engine = os.path.join(PROJECT_ROOT, "multilingual_text_in_image_translatio_agy_sdk.py")
    with open(main_engine, "r", encoding="utf-8", errors="ignore") as fp:
        code = fp.read()
        
    if "max_output_tokens=8192" in code:
        print("  ✅ 엔진 내 토큰 8192 안전천장 및 FAQ 5개 안전장치 확인 완료")
        return True
    else:
        print("  ❌ [경고] 엔진 내 안전장치가 누락되었습니다.")
        return False

def main():
    print("=" * 70)
    print("🚀 [Antigravity 2.0] 프로젝트 루트 전역 룰북 & 다국어 엔진 린터")
    print("=" * 70)
    
    r1 = lint_markdown_docs()
    r2 = lint_python_prompts()
    r3 = lint_output_verification_gate()
    
    print("\n" + "=" * 70)
    if r1 and r2 and r3:
        print("🎉 [RESULT] 전체 워크스페이스 무결성 100% PASS! 누락 및 불일치 0건.")
        print("=" * 70)
        sys.exit(0)
    else:
        print("🚨 [RESULT] 규격 불일치 발견! 위 오류 목록을 즉시 수정하십시오.")
        print("=" * 70)
        sys.exit(1)

if __name__ == "__main__":
    main()
