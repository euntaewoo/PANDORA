# -*- coding: utf-8 -*-
import os, sys

# 1. Update Global_Text-In_Image_Translation_rules.md
r1_path = r"C:\Users\euntaewoo\Desktop\multilingual_text_in_image_translatio_agy_sdk_uv-version\.agents\rules\Global_Text-In_Image_Translation_rules.md"
with open(r1_path, "r", encoding="utf-8") as f:
    r1 = f.read()

new_r1_section = """## 1. 아키텍처 원칙: 설정 주도형 플러그인 격리 (Configuration-Driven Pack)
- **하드코딩 금지**: 코어 엔진 스크립트(`multilingual_text_in_image_translatio_agy_sdk.py`) 내에 특정 언어의 폰트 명칭, 규제 금지어, 약기법 등을 `if/else`로 하드코딩하는 것을 절대 금지합니다.
- **표준 렉시콘 DB 연동**: 언어별 법률 규제 및 금지어/대체어는 반드시 `00_공통자료/compliance_lexicons/` 하위의 독립된 JSON 팩(예: `en_fda_mocra_lexicon.json`, `jp_pmda_pharm_lexicon.json`, `cn_nmpa_adlaw_lexicon.json`, `tw_tfda_lexicon.json`)에 분리 저장하고, 엔진 구동 시 `--lang` 파라미터에 따라 `load_dynamic_compliance_lexicon()`을 통해 런타임에 동적으로 주입(로드)해야 합니다.

## 2. 언어별 렌더링, 폰트 및 컴플라이언스 강제 원칙
- **영어(EN)**: 미국 FDA MoCRA 및 FTC 기준 의약품 오인(세포/생리기능 cellular vitality/resilience) 클레임 전면 차단, 노화는 반드시 `the signs of premature aging`으로 한정, K-뷰티 콩글리시(`Complex skin issues` -> `Multiple skin concerns`, `Troubled skin` -> `Blemish-prone skin`) 배제 및 럭셔리 초월번역 톤앤매너 강제. 렌더링 시 영미권 글로벌 프리미엄 지오메트릭 산세리프인 `Montserrat (몬세라트)` 폰트를 메인 서체로 100% 강제 적용합니다. (단, 고시정보 테이블 렌더링 시에만 `Pretendard` 적용).
- **일본어(JP)**: 후생노동성 기준 56종 약기법 포지티브 리스트(Positive List) 엄격 준수, 치료/재생 클레임 배제, 렌더링 시 반드시 `NotoSansJP` 폰트를 지정합니다.
- **중국어(CN/TW)**: 중국 신광고법 8대 절대화 금지어('最', '第一', '顶级' 등) 및 NMPA/TFDA 화장품 규정 필터링을 적용하며, 렌더링 시 `Noto Sans SC` (간체자) / `Noto Sans TC` (번체자) 폰트를 적용합니다.

## 2-1. [GLOBAL-COMPLIANCE] 전역 시스템 인스트럭션 & 원천 법리 (First Principles Heuristic)
- 모든 번역 엔진 호출 시 `GLOBAL_COMPLIANCE_SYSTEM_INSTRUCTION`을 최상위 시스템 지침으로 주입하여 '다국어 법무 감사관 + 럭셔리 카피라이터' 역할을 강제합니다.
- 사전에 등록되지 않은 신규 성분/어휘라도 인체 세포/생리기능에 직접 관여하는 뉘앙스가 있다면 무조건 '피부 표면의 미용적 외관 개선(-looking, appearance of, moisture barrier)'으로 안전하게 우회해야 합니다."""

r1 = r1.replace("""## 1. 아키텍처 원칙: 설정 주도형 플러그인 격리 (Configuration-Driven Pack)
- **하드코딩 금지**: 코어 엔진 스크립트(`multilingual_text_in_image_translatio_agy_sdk.py`) 내에 특정 언어의 폰트 명칭, 규제 금지어, 약기법 등을 `if/else`로 하드코딩하는 것을 절대 금지합니다.
- **플러그인 로드**: 언어별 규칙은 반드시 `config/` 디렉토리 하위의 독립된 JSON 팩(예: `EN_translation_rules.json`, `JP_translation_rules.json`)에 분리하여 저장하고, 엔진 구동 시 `--lang` 파라미터에 따라 런타임에 동적으로 주입(로드)해야 합니다.

## 2. 언어별 렌더링 및 폰트 강제 원칙
- **일본어(JP)**: 후생노동성 기준 56종 약기법 금지어 정규식(Regex) 락을 가동하고, 렌더링 시 반드시 `NotoSansJP` 폰트를 지정합니다.
- **영어(EN)**: 규제 단어 강제 필터링 락을 해제하고 초월번역 톤앤매너를 지향하며, 렌더링 시 영미권 글로벌 프리미엄 지오메트릭 산세리프인 `Montserrat (몬세라트)` 폰트를 메인 서체로 강제 적용합니다. (단, 상품상세정보 고시정보 테이블 렌더링 시에만 `Pretendard` 적용).
- **중국어(CN/TW)**: 중국 신광고법 및 NMPA 규정 필터링을 적용하며, 렌더링 시 `Noto Sans SC` (간체자) / `Noto Sans TC` (번체자) 폰트를 적용합니다.""", new_r1_section)

with open(r1_path, "w", encoding="utf-8") as f:
    f.write(r1)
print("SUCCESS: Updated Global_Text-In_Image_Translation_rules.md")

# 2. Update multilingual_text_in_image_translation_rules.md
r2_path = r"C:\Users\euntaewoo\Desktop\multilingual_text_in_image_translatio_agy_sdk_uv-version\.agents\rules\multilingual_text_in_image_translation_rules.md"
with open(r2_path, "r", encoding="utf-8") as f:
    r2 = f.read()

r2_add = """
## 9. [COMPLIANCE-FIRST] 글로벌 법무 & 럭셔리 마케팅 초월번역 표준 규격
1. **시스템 인스트럭션 전역 고정**: 모든 Pass 1 호출 시 `GLOBAL_COMPLIANCE_SYSTEM_INSTRUCTION` (다국어 법무팀 + 럭셔리 카피라이터) 주입 필수.
2. **동적 렉시콘 연동**: `00_공통자료/compliance_lexicons/*.json`에서 4개국 법령 DB를 실시간 동적 로드.
3. **5대 법적 리스크 & 콩글리시 100% 강제 치환**:
   - `Complex skin issues` ➔ `Multiple skin concerns`
   - `Troubled skin` ➔ `Blemish-prone skin`
   - `nutrients for cellular vitality` ➔ `hydration for a resilient-looking complexion`
   - `reinforces cellular resilience` ➔ `reinforces the skin's natural moisture barrier`
   - `combats premature aging` ➔ `combats the signs of premature aging`
4. **결정론적 후처리 게이트 (`apply_deterministic_qa_overrides`)**: Python 정규식 필터에서 금지어를 1ms 내에 전수 자동 교정.
"""

if "## 9. [COMPLIANCE-FIRST]" not in r2:
    r2 = r2 + "\n" + r2_add

with open(r2_path, "w", encoding="utf-8") as f:
    f.write(r2)
print("SUCCESS: Updated multilingual_text_in_image_translation_rules.md")

# 3. Update 초월번역_품질평가_4대루브릭_표준규격.md
r3_path = r"C:\Users\euntaewoo\Desktop\multilingual_text_in_image_translatio_agy_sdk_uv-version\00_공통자료\초월번역_품질평가_4대루브릭_표준규격.md"
with open(r3_path, "r", encoding="utf-8") as f:
    r3 = f.read()

r3_update = """| **② 국가별 광고법 무결성**<br>(Ad-Law Compliance) | **30점** | • **미국 MoCRA/FTC**: 세포/생리기능(cellular vitality/resilience) 직접 클레임 100% 배제, 노화는 반드시 `signs of aging`으로 한정, 콩글리시(`Complex issues` -> `Multiple concerns`, `Troubled` -> `Blemish-prone`) 교정 여부 검증.<br>• **일본 약기법**: 후생노동성 56종 허용 효능 준수 (치료, 재생, 소염 배제)<br>• **중국 신광고법/NMPA**: 8대 절대화 금지어(`最`, `第一` 등) 및 의약품 오인 표현 차단<br>• **고시정보표 4대 법적 표준**: 기능성화장품 한국 식약처(`MFDS, Republic of Korea`) 관할 명시, 3대 법정 주의사항, 공정위 소비자분쟁기준, +82 고객상담번호 자동 검증 |"""

r3 = r3.replace("""| **② 국가별 광고법 무결성**<br>(Ad-Law Compliance) | **30점** | • **미국 MoCRA**: 질병/치료 오인 표현(`Cure`, `Treatment` 등) 100% 배제<br>• **일본 약기법**: 후생노동성 56종 허용 효능 준수 (재생, 디톡스 배제)<br>• **중국 신광고법/NMPA**: 8대 절대화 금지어(`最`, `第一` 등) 및 '인증' 표현 차단<br>• **고시정보표 4대 법적 표준**: 기능성화장품 한국 식약처(`MFDS, Republic of Korea`) 관할 명시, 3대 법정 주의사항, 공정위 소비자분쟁기준, +82 고객상담번호 자동 검증 |""", r3_update)

with open(r3_path, "w", encoding="utf-8") as f:
    f.write(r3)
print("SUCCESS: Updated 초월번역_품질평가_4대루브릭_표준규격.md")

# 4. Update GenerationConfig 규격서 (2개 위치)
cfg_files = [
    r"C:\Users\euntaewoo\Desktop\multilingual_text_in_image_translatio_agy_sdk_uv-version\00_공통자료\제미나이_AI_번역_안전장치_안티그래비티2.0_Gemini_GenerationConfig_기술규격서.md",
    r"C:\Users\euntaewoo\Desktop\multilingual_text_in_image_translatio_agy_sdk_uv-version\제미나이_AI_번역_안전장치_안티그래비티2.0_Gemini_GenerationConfig_기술규격서.md"
]

for cfg_path in cfg_files:
    if os.path.exists(cfg_path):
        with open(cfg_path, "r", encoding="utf-8") as f:
            cfg = f.read()
        cfg_add = """
## 8. 글로벌 컴플라이언스(법무) 시스템 인스트럭션 (`GLOBAL_COMPLIANCE_SYSTEM_INSTRUCTION`) 규격
- **목적**: 단순 번역기를 넘어선 '글로벌 법무 감사관 + 럭셔리 카피라이터' 이중 페르소나 및 원천 법리 강제.
- **주입 위치**: `types.GenerateContentConfig(system_instruction=GLOBAL_COMPLIANCE_SYSTEM_INSTRUCTION, temperature=0.6, top_p=0.9, max_output_tokens=8192)`
- **연동 데이터**: `00_공통자료/compliance_lexicons/*.json` (4개국 법령 DB 실시간 동적 바인딩).
"""
        if "GLOBAL_COMPLIANCE_SYSTEM_INSTRUCTION" not in cfg:
            cfg = cfg + "\n" + cfg_add
            with open(cfg_path, "w", encoding="utf-8") as f:
                f.write(cfg)
            print(f"SUCCESS: Updated {os.path.basename(cfg_path)}")