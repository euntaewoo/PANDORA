# -*- coding: utf-8 -*-
import os, sys

g1_path = r"C:\Users\euntaewoo\Desktop\multilingual_text_in_image_translatio_agy_sdk_uv-version\global_rules.md"
g2_path = r"C:\Users\euntaewoo\Desktop\multilingual_text_in_image_translatio_agy_sdk_uv-version\.agents\rules\global_rules.md"

new_compliance_section = """
### 2.7 글로벌 컴플라이언스(법무) & 럭셔리 마케팅 초월번역 전역 표준 규격 (GLOBAL-COMPLIANCE-LEXICON-LOCK)
- **[GLOBAL-COMPLIANCE-SYSTEM-INSTRUCTION]**: 모든 다국어 번역 엔진 Pass 1 호출 시 `GLOBAL_COMPLIANCE_SYSTEM_INSTRUCTION`을 시스템 인스트럭션(`types.GenerateContentConfig(system_instruction=...)`)으로 전역 강제하여 **'15년 차 글로벌 뷰티 법무 감사관이자 세포라/백화점 수석 카피라이터'** 역할을 수행한다.
- **[FIRST-PRINCIPLES-HEURISTIC] (세포/생리기능 금지 원천 법리)**:
  - 인체 구조, 생리적 기능, 세포(Cell/Cellular) 단위의 생화학적 변화나 치료·재생을 암시하는 클레임(예: `cellular vitality`, `cellular resilience`, `cell metabolism`, `collagen synthesis`, `anti-inflammatory`)을 100% 원천 차단한다.
  - 사전에 등록되지 않은 신규 성분/어휘라도 세포/생리기능 직접 관여 뉘앙스가 있다면 무조건 **'피부 표면의 미용적 외관 개선(`-looking`, `appearance of`, `natural moisture barrier`)'**으로 안전하게 우회한다.
- **[4개국 표준 컴플라이언스 렉시콘 DB 연동 (Data-Driven Architecture)]**:
  - `00_공통자료/compliance_lexicons/` 하위의 4개국 JSON DB(`en_fda_mocra_lexicon.json`, `jp_pmda_pharm_lexicon.json`, `cn_nmpa_adlaw_lexicon.json`, `tw_tfda_lexicon.json`)를 `load_dynamic_compliance_lexicon()`으로 실시간 동적 바인딩한다.
  - **5대 법적 리스크 & 콩글리시 100% 강제 치환**:
    1. `Complex skin issues` ➔ **`Multiple skin concerns`**
    2. `Troubled skin` ➔ **`Blemish-prone skin`**
    3. `nutrients for cellular vitality` ➔ **`hydration for a resilient-looking complexion`**
    4. `reinforces cellular resilience` ➔ **`reinforces the skin's natural moisture barrier`**
    5. `combats premature aging` ➔ **`combats the signs of premature aging`**
- **[DETERMINISTIC-OVERRIDE-GATE] (Python 정규식 100% 안전망)**:
  - LLM 응답 텍스트에 대해 Python 코드 레벨(`apply_deterministic_qa_overrides`)에서 렉시콘 등록 금지어를 정규식(`re.sub`)으로 전수 검사하여 1ms 내에 럭셔리 표준어로 100% 강제 치환한다.
- **[AUTONOMOUS-REGULATORY-SENTINEL] (자율 규제 동기화 크론)**:
  - `00_공통자료/sync_regulatory_lexicon.py` 모듈을 통해 각국 정부(FDA Warning Letters, 후생성, NMPA) 웹 피드를 주기적으로 탐색하여 신규 단속 성분을 JSON DB에 스스로 추가(Append)한다.
"""

for target_file in [g1_path, g2_path]:
    if os.path.exists(target_file):
        with open(target_file, "r", encoding="utf-8") as f:
            content = f.read()
        if "### 2.7 글로벌 컴플라이언스(법무) & 럭셔리 마케팅" not in content:
            # 2.6 섹션 뒤에 추가
            content = content.replace("### 2.6 4대 마스터 폴더 체계", new_compliance_section + "\n### 2.6 4대 마스터 폴더 체계")
            with open(target_file, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"SUCCESS: Updated {os.path.basename(target_file)}")

print("COMPLETED: Synced global_rules.md and .agents/rules/global_rules.md")