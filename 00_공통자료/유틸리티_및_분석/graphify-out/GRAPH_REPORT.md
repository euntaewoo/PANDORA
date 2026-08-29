# Graph Report - 이미지번역워크스페이스  (2026-06-14)

## Corpus Check
- 42 files · ~9,857,070 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 131 nodes · 107 edges · 42 communities (34 shown, 8 thin omitted)
- Extraction: 100% EXTRACTED · 0% INFERRED · 0% AMBIGUOUS
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Community 0|Community 0]]
- [[_COMMUNITY_Community 1|Community 1]]
- [[_COMMUNITY_Community 2|Community 2]]
- [[_COMMUNITY_Community 3|Community 3]]
- [[_COMMUNITY_Community 4|Community 4]]
- [[_COMMUNITY_Community 5|Community 5]]
- [[_COMMUNITY_Community 6|Community 6]]
- [[_COMMUNITY_Community 7|Community 7]]
- [[_COMMUNITY_Community 8|Community 8]]
- [[_COMMUNITY_Community 30|Community 30]]
- [[_COMMUNITY_Community 31|Community 31]]
- [[_COMMUNITY_Community 32|Community 32]]
- [[_COMMUNITY_Community 33|Community 33]]
- [[_COMMUNITY_Community 34|Community 34]]

## God Nodes (most connected - your core abstractions)
1. `NanoBananaV3MasterEngine` - 7 edges
2. `NanoBananaV3MasterEngine` - 7 edges
3. `process_single_image()` - 7 edges
4. `6단계 파이프라인 (Workflow)` - 7 edges
5. `🚀 Antigravity 2.0 이미지 번역 자동화 파이프라인 완벽 가이드` - 6 edges
6. `🚀 JP_Ecom_Visual_Localizer_V3 (Master Surgical Edition)` - 5 edges
7. `JP_Ecom_Visual_Localizer_V3 작업 지침 (V3 Ultimate)` - 5 edges
8. `find_price()` - 4 edges
9. `Engine` - 3 edges
10. `main()` - 3 edges

## Surprising Connections (you probably didn't know these)
- None detected - all connections are within the same source files.

## Communities (42 total, 8 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.14
Nodes (13): 1. 이미지 전처리 (Pre-processing), 1. 통합 Vision 분석 및 배경 복원 (Unified Pipeline), 2. 정밀 배경 복원 및 디자인 보존, 2. 레이아웃 분석 (Vision Analysis), 3. 고수준 번역 및 현지화 (Localization), 4. 배경 복원 (Surgical Inpainting), 5. 프리미엄 렌더링 (Rendering), 6. 자동 QA (Verification) (+5 more)

### Community 1 - "Community 1"
Cohesion: 0.27
Nodes (10): analyze_and_translate_image(), calculate_luminance(), get_font_by_role(), get_smart_bg_color(), main(), process_single_image(), Gemini API를 사용하여 이미지 속 한글 텍스트를 검출 및 번역.     무료 API 503(Spikes/Unavailable) 오류 발생, 비율 고정 기반의 배경 소거 및 텍스트 렌더링, 엑셀 누적 보고 (+2 more)

### Community 4 - "Community 4"
Cohesion: 0.36
Nodes (7): char_similarity(), find_price(), normalize(), 상품명 비교용: 괄호·불용어·숫자·단위·스펙 모두 제거, 공백 제거, 두 문자열의 글자 수준 유사도 (0~1) - 공통 글자 비율, bigram 비교 전단계: 숫자, 단위, 기술스펙 제거, strip_specs()

### Community 5 - "Community 5"
Cohesion: 0.25
Nodes (7): 🎯 요약, 🚀 Antigravity 2.0 이미지 번역 자동화 파이프라인 완벽 가이드, code:text (안티그래비티! 오늘 작업할 폴더 경로는 여기야: "D:\Qoo10_Translation_Factory\01_), 📂 STEP 1: 전용 워크스페이스(본부) 창설하기, 🗂️ STEP 2: Input / Output 폴더 분리하기 (섞임 방지), 🔢 STEP 3: 칼같은 파일 넘버링 (가장 중요!), 🗣️ STEP 4: Antigravity에게 명령 내리기 (마법의 프롬프트)

### Community 6 - "Community 6"
Cohesion: 0.33
Nodes (5): 📂 구조, 🛠 핵심 사양, 📝 관리 이력, 🚀 JP_Ecom_Visual_Localizer_V3 (Master Surgical Edition), 🌟 핵심 원칙 (Zero-Distortion)

### Community 8 - "Community 8"
Cohesion: 0.5
Nodes (3): Sheet: 전체 상품 리스트, Sheet: 주요제품판매업체, Sheet: 자동화시장조사

## Knowledge Gaps
- **34 isolated node(s):** `역할별(title, body, legal 등)로 적합한 폰트 종류를 선택하여 반환`, `텍스트 박스 좌표 주변을 샘플링하여 NumPy Median(중앙값)으로 원래 배경색을 정밀 복원`, `Gemini API를 사용하여 이미지 속 한글 텍스트를 검출 및 번역.     무료 API 503(Spikes/Unavailable) 오류 발생`, `비율 고정 기반의 배경 소거 및 텍스트 렌더링, 엑셀 누적 보고`, `상품명 비교용: 괄호·불용어·숫자·단위·스펙 모두 제거, 공백 제거` (+29 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **8 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **What connects `역할별(title, body, legal 등)로 적합한 폰트 종류를 선택하여 반환`, `텍스트 박스 좌표 주변을 샘플링하여 NumPy Median(중앙값)으로 원래 배경색을 정밀 복원`, `Gemini API를 사용하여 이미지 속 한글 텍스트를 검출 및 번역.     무료 API 503(Spikes/Unavailable) 오류 발생` to the rest of the system?**
  _34 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Community 0` be split into smaller, more focused modules?**
  _Cohesion score 0.14 - nodes in this community are weakly interconnected._