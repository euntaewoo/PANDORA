# -*- coding: utf-8 -*-
import os
import sys
import json
import html

sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(BASE_DIR, "03_번역품질평가", "02_진단결과", "Aquatide-Resurface_Serum_EN")
os.makedirs(OUT_DIR, exist_ok=True)

data = {
    "product_name": "Logically, Skin Aquatide Resurface Serum 50ml",
    "target_lang": "EN",
    "overall_score": 50,
    "passed": False,
    "scores": {
        "domain_relevance": 14,
        "ad_law_compliance": 12,
        "luxury_transcreation_tone": 15,
        "visual_layout_conciseness": 9
    },
    "executive_summary": "심각한 브랜드명 오타(Logcally Skin), 핵심 영문 스펠링 오타(dysfuntional, ight, Inaredients), 한국어 미번역 방치(서울어워드 본문 및 금상 스탬프), 그로테스크한 직역(Autophagy 'self-eating'), 미국 MoCRA/FDA 의약품 오인 금지 표현(whitening, skin regeneration, small acnes disappeared, repair damaged skin)이 다수 발견되어 품질 심사 결과 불합격(FAILED - 50점) 판정되었습니다. 전면적인 초월번역(Transcreation) 교정 및 재렌더링(Track 3)이 필수적입니다.",
    "transcreation_comparisons": [
        {
            "index": 1,
            "original": "브랜드 앰블럼 및 공식 어워드 (Logcally Skin SEOUL AWARDS 2023 EXCLUSIVE PARTNER)",
            "literal_translation": "Logcally Skin / SEOUL AWARDS 2023 EXCLUSIVE PARTNER",
            "transcreation": "Logically, Skin / SEOUL AWARDS 2023 OFFICIAL EXCELLENCE AWARD",
            "value_analysis": "브랜드명 철자 오류(Logcally -> Logically, Skin)를 바로잡고 프레스티지 뷰티 브랜드의 공식 수상 앰블럼 규격 확립"
        },
        {
            "index": 2,
            "original": "[서울 어워드 우수상품 선정] 아쿠아타이드 리서페이스 세럼 / 로지컬리스킨의 핵심 로직인 Cell Alarming Logic이 적용된 아쿠아타이드 리서페이스 세럼의 제품 우수성을 인정받았습니다",
            "literal_translation": "(한국어 전면 미번역 방치)",
            "transcreation": "[Seoul Awards Selection of Excellence] Aquatide Resurface Serum: Celebrated for its groundbreaking derma-science innovation powered by Logically, Skin’s proprietary Cell-Targeted Mechanism.",
            "value_analysis": "영문 PDP 내 방치된 한국어 원문을 전면 해소하고, 글로벌 바이어 및 소비자 신뢰도를 극대화하는 어워드 스토리텔링으로 승격"
        },
        {
            "index": 3,
            "original": "인코스메틱스 아시아 2016 금상 수상 및 오토파지(자가포식) 노벨상 원리 (Autophagy (self-eating) principle / In-Cosmetics Asia 2016 금상)",
            "literal_translation": "Autophagy (self-eating) principle / In-Cosmetics Asia 2016 금상 금상",
            "transcreation": "Harnessing the Nobel Prize–Winning Principle of Autophagy: Skin's Natural Cellular Recycling & Renewal Mechanism | In-Cosmetics Asia 2016 Gold Prize Winner",
            "value_analysis": "소비자에게 혐오감을 줄 수 있는 'self-eating' 직역을 배제하고 'Cellular Recycling & Renewal'로 품격화하며 하단 미번역 한글 '금상' 완전 제거"
        },
        {
            "index": 4,
            "original": "미세먼지, 자외선 등으로 지친 피부를 위해 단계를 줄이고 간결하게 시작하는 세럼",
            "literal_translation": "Makeup, UVA, UVB, sweat, dusts- / Too many things are already put on the skin. / So curtail skincare products. / Start skin care simply with Aquatide Resurface Serum.",
            "transcreation": "Shielded from Environmental Stressors: Daily pollution, UV exposure, and heavy makeup fatigue your skin. Simplify and elevate your daily ritual with Aquatide Resurface Serum.",
            "value_analysis": "투박한 단어(dusts-, curtail)를 세포라급 스킨케어 내러티브(Environmental Stressors, Simplify and elevate your daily ritual)로 전환"
        },
        {
            "index": 5,
            "original": "가볍고 산뜻한 흡수감 및 피부 진정/결 개선 실사용자 리뷰",
            "literal_translation": "its texture is ight and good / this serum really makes me feel 'skin regeneration' / helps skin cell activation / Small acnes disappeared",
            "transcreation": "Delivers an ultra-lightweight, fast-absorbing texture / Visibly revitalizes skin renewal / Supports natural skin vitality / Visibly clarifies blemish-prone areas",
            "value_analysis": "[스펠링 오타 및 MoCRA 준수] 'ight' -> 'lightweight' 수정 및 의약품 오인 소지(세포 재생, 여드름 완치)를 미용적 외관 개선 표현으로 안전하게 교정"
        },
        {
            "index": 6,
            "original": "아쿠아타이드 5000 4% 함유 안티에이징 로직 및 손상 피부 리서페이스",
            "literal_translation": "sp ecial mechanism for anti-a ging, which activates the skin to replace aging fa ctors with nutrients. Helps regenerating damaged skin while reducing wrinkles.",
            "transcreation": "Formulated with 4% High-Potency Aquatide 5000 to visibly recharge fatigued skin, smooth surface texture, and diminish the appearance of fine lines and wrinkles.",
            "value_analysis": "[레이아웃 및 FDA 준수] 단어 강제 개행 깨짐(sp ecial, anti-a ging, fa ctors) 정상화 및 의약품성 손상 재생 클레임(regenerating damaged skin)을 화장품 안전선으로 전환"
        },
        {
            "index": 7,
            "original": "3대 핵심 효능 (에너지 강화, 미백/주름 이중 시너지, 피부 활성화)",
            "literal_translation": "1. A Logic That Enhances Natural Energy / 2. works well as whitening and wrinkle treatment with Niacinamide / 3. Logically Wakes the Skin Asleep",
            "transcreation": "1. Fortifying Skin Resilience: 4% Aquatide deeply revitalizes skin barriers / 2. Dual-Action Radiance & Firming: Synergized with Niacinamide / 3. Awakens Dormant Radiance: Empowers skin's natural vitality",
            "value_analysis": "[MoCRA/광고법 준수] 미 FDA 금기어 'whitening' 및 의약품성 'treatment'를 'Radiance & Firming', 'Awakens Dormant Radiance'로 전면 격상"
        },
        {
            "index": 8,
            "original": "오토파지 수상 내역 및 손상 세포 정화 원리 (The principle that recycles dysfuntional cells)",
            "literal_translation": "The principle that recycles dysfuntional cells as nutrient for other healthy cells and human body",
            "transcreation": "The Nobel Prize-inspired mechanism that purifies cellular waste and revitalizes skin's natural moisture barrier.",
            "value_analysis": "[스펠링 오타 수정] 'dysfuntional' -> 'dysfunctional' 오타 수정 및 인체 직접 관여 표현을 바이오-더마 뷰티 표준어로 교정"
        },
        {
            "index": 9,
            "original": "피부 고민 자가 진단 체크리스트 (건조, 칙칙한 피부톤, 요철, 탄력 저하)",
            "literal_translation": "I'm worried about dryness or moisturizing / I want to keep my bumpy skin smooth / The elasticity has been decreased / So-called efficacious cosmetics don't work well",
            "transcreation": "Persistent dehydration and loss of radiance / Uneven, bumpy skin texture needing smooth refinement / Visible loss of skin firmness and elasticity / Looking for genuinely effective skincare backed by proven science",
            "value_analysis": "투박한 콩글리시 직역투를 글로벌 럭셔리 더마 브랜드의 프리미엄 피부 진단 카피로 전환"
        },
        {
            "index": 10,
            "original": "부위별 집중 케어, 슬리핑 팩, 메이크업 부스터 활용 팁",
            "literal_translation": "Fine Part Care / Apply around troubles for intensive treatment / Solve flakey, cakey skin problem",
            "transcreation": "Targeted Contour Care: Smooth gently around delicate eye contours and smile lines / Flawless Makeup Booster: Blend a drop with foundation for a dewy, cake-free luminous finish",
            "value_analysis": "어색한 어휘(Fine Part Care, troubles, flakey cakey problem)를 세포라 뷰티 팁 표준 용어로 정제"
        },
        {
            "index": 11,
            "original": "상품 정보 고시표 (이중기능성, 주요성분, 전성분 표기)",
            "literal_translation": "Functional Cosmetics Examination: Dual-functional cosmetics for whitening and wrinkle improvement / Inaredients (오타 및 하단 전성분 잘림)",
            "transcreation": "Key Cosmetic Benefits: Dual-Action Brightening & Anti-Wrinkle Care / Full Ingredients List: Complete 100% INCI standard vector table",
            "value_analysis": "[헤더 오타 및 규정] 'Inaredients' -> 'Ingredients' 오타 수정, 'whitening' -> 'Brightening' 치환, 잘린 전성분 860px 표준 고시정보표로 100% 완전 렌더링 규격화"
        }
    ],
    "violations": [
        "FDA MoCRA Cosmetic Claim Violation: 'whitening' (의약적 피부 표백 오인 단어)",
        "FDA MoCRA Drug Claim Violation: 'skin regeneration' (피부 재생 클레임)",
        "FDA MoCRA Drug Claim Violation: 'Small acnes disappeared' (여드름 질환 치료 클레임)",
        "FDA MoCRA Drug Claim Violation: 'Helps regenerating damaged skin' (손상 피부 치료 클레임)",
        "FDA MoCRA Physiological Claim Violation: 'helps skin cell activation' / 'recycles dysfunctional cells for human body'"
    ],
    "correction_feedbacks": [
        {
            "original": "Logcally Skin (Image 1_02)",
            "current_translation": "Logcally Skin",
            "recommended_correction": "Logically, Skin",
            "reason": "최우선 브랜드명 철자 오류 ('i' 누락)"
        },
        {
            "original": "서울어워드 선정확인서 본문 (Image 01_01)",
            "current_translation": "[서울 어워드 우수상품 선정] ... 우수성을 인정받았습니다",
            "recommended_correction": "[Seoul Awards Selection of Excellence] Aquatide Resurface Serum: Celebrated for its groundbreaking derma-science innovation",
            "reason": "영문 상세페이지 내 한국어 원문 전면 미번역 방치"
        },
        {
            "original": "In-Cosmetics Asia 금상 도장 (Image 02-01 & 02-01_860)",
            "current_translation": "In-Cosmetics Asia 2016 금상 / 금상",
            "recommended_correction": "In-Cosmetics Asia 2016 Gold Prize / Gold Award",
            "reason": "상세페이지 이미지 내 한국어 미번역 방치"
        },
        {
            "original": "Autophagy principle (Image 02-01 & 07)",
            "current_translation": "Autophagy (self-eating) principle",
            "recommended_correction": "Autophagy: Skin's Natural Cellular Recycling & Renewal Mechanism",
            "reason": "화장품 구매욕구를 저해하는 기괴한 직역 단어 ('self-eating')"
        },
        {
            "original": "Review texture (Image 04)",
            "current_translation": "its texture is ight and good",
            "recommended_correction": "delivers an ultra-lightweight, fast-absorbing texture",
            "reason": "영문 스펠링 오타 ('ight' -> 'light')"
        },
        {
            "original": "Review acne claim (Image 04)",
            "current_translation": "Small acnes disappeared",
            "recommended_correction": "Visibly clarifies blemish-prone areas",
            "reason": "미국 FDA MoCRA 여드름 치료제(OTC Drug) 오인 클레임 위반"
        },
        {
            "original": "Anti-aging box (Image 05)",
            "current_translation": "sp ecial ... anti-a ging ... fa ctors",
            "recommended_correction": "Special mechanism for age-defying care",
            "reason": "텍스트 박스 폭 미조정으로 인한 비정상 단어 쪼개짐/분절 레이아웃 결함"
        },
        {
            "original": "Autophagy spelling (Image 07)",
            "current_translation": "recycles dysfuntional cells",
            "recommended_correction": "purifies dysfunctional elements (또는 cellular waste)",
            "reason": "영문 스펠링 오타 ('dysfuntional' -> 'dysfunctional') 및 세포 클레임"
        },
        {
            "original": "Checklist wording (Image 08)",
            "current_translation": "I'm worried about dryness or moisturizing",
            "recommended_correction": "Persistent dehydration and loss of radiance",
            "reason": "부자연스러운 콩글리시 직역투"
        },
        {
            "original": "Notice Table Header (Image 11)",
            "current_translation": "Inaredients",
            "recommended_correction": "Full Ingredients List",
            "reason": "핵심 표 헤더 스펠링 오타 ('Inaredients' -> 'Ingredients') 및 하단 전성분 텍스트 잘림"
        }
    ]
}

# 1. JSON 저장
json_path = os.path.join(OUT_DIR, "Transcreation_QA_Report.json")
with open(json_path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

# 2. HTML 생성
score = data["overall_score"]
passed = data["passed"]
scores = data["scores"]
summary = data["executive_summary"]
comparisons = data["transcreation_comparisons"]
feedbacks = data["correction_feedbacks"]
violations = data["violations"]

badge_color = "#2e7d32" if passed else "#c62828"
badge_text = "PASSED (초월번역 승인)" if passed else "FAILED (보완 및 교정 필수)"

comp_rows_html = ""
for item in comparisons:
    comp_rows_html += f"""
    <tr>
        <td style="padding:14px; border-bottom:1px solid #e2e8f0; font-size:13px; color:#1e293b; font-weight:600; line-height:1.5;">{html.escape(item.get('original', ''))}</td>
        <td style="padding:14px; border-bottom:1px solid #e2e8f0; font-size:12.5px; color:#dc2626; line-height:1.5; background:#fef2f2;">{html.escape(item.get('literal_translation', ''))}</td>
        <td style="padding:14px; border-bottom:1px solid #e2e8f0; font-size:13px; color:#0f766e; font-weight:600; line-height:1.5; background:#f0fdf4;">{html.escape(item.get('transcreation', ''))}</td>
        <td style="padding:14px; border-bottom:1px solid #e2e8f0; font-size:12.5px; color:#334155; line-height:1.5;">{html.escape(item.get('value_analysis', ''))}</td>
    </tr>
    """

feed_rows_html = ""
for fb in feedbacks:
    feed_rows_html += f"""
    <tr>
        <td style="padding:13px; border-bottom:1px solid #eee; font-weight:700; color:#1e293b; font-size:13px;">{html.escape(fb.get('original', ''))}</td>
        <td style="padding:13px; border-bottom:1px solid #eee; color:#dc2626; text-decoration:line-through; font-size:12.5px; background:#fef2f2;">{html.escape(fb.get('current_translation', ''))}</td>
        <td style="padding:13px; border-bottom:1px solid #eee; color:#0f766e; font-weight:700; font-size:13px; background:#f0fdf4;">{html.escape(fb.get('recommended_correction', ''))}</td>
        <td style="padding:13px; border-bottom:1px solid #eee; font-size:12.5px; color:#475569;">{html.escape(fb.get('reason', ''))}</td>
    </tr>
    """

viol_html = ""
if violations:
    for v in violations:
        viol_html += f"""<li style="margin-bottom:6px; color:#b91c1c; font-size:13.5px; font-weight:600;">⚠️ {html.escape(v)}</li>"""
else:
    viol_html = "<li style='color:#2e7d32;'>위반 사항 없음</li>"

html_content = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>다국어 이커머스 초월번역(Transcreation) 품질 진단 리포트 (Aquatide Resurface Serum EN)</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", sans-serif; background: #f1f5f9; color: #0f172a; padding: 40px 20px; margin: 0; }}
        .container {{ max-width: 1240px; margin: 0 auto; background: #ffffff; border-radius: 14px; box-shadow: 0 10px 30px rgba(0,0,0,0.06); overflow: hidden; border: 1px solid #e2e8f0; }}
        .header {{ background: #0f172a; color: #ffffff; padding: 32px 36px; display: flex; justify-content: space-between; align-items: center; border-bottom: 3px solid #3b82f6; }}
        .header h1 {{ margin: 0; font-size: 23px; font-weight: 700; letter-spacing: -0.5px; }}
        .badge {{ background: {badge_color}; color: #ffffff; padding: 8px 18px; border-radius: 20px; font-weight: 700; font-size: 14px; box-shadow: 0 2px 6px rgba(0,0,0,0.15); }}
        .score-card {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; padding: 24px 36px; background: #f8fafc; border-bottom: 1px solid #e2e8f0; }}
        .score-box {{ background: #ffffff; padding: 16px; border-radius: 10px; text-align: center; border: 1px solid #cbd5e1; }}
        .score-box .label {{ font-size: 12.5px; color: #475569; font-weight: 600; margin-bottom: 4px; }}
        .score-box .num {{ font-size: 22px; font-weight: 800; color: {'#1e40af' if passed else '#b91c1c'}; }}
        .summary-box {{ padding: 24px 36px; border-bottom: 1px solid #e2e8f0; background: #ffffff; }}
        .summary-box h3 {{ margin: 0 0 8px 0; color: #1e293b; font-size: 16px; display: flex; align-items: center; gap: 8px; }}
        .section-box {{ padding: 32px 36px; border-bottom: 1px solid #e2e8f0; }}
        .section-box:last-child {{ border-bottom: none; }}
        .section-title {{ margin: 0 0 16px 0; color: #0f172a; font-size: 17px; font-weight: 700; display: flex; align-items: center; gap: 8px; }}
        table {{ width: 100%; border-collapse: collapse; text-align: left; background: #ffffff; border-radius: 8px; overflow: hidden; border: 1px solid #e2e8f0; }}
        th {{ background: #f1f5f9; padding: 14px; font-size: 13.5px; color: #334155; border-bottom: 2px solid #cbd5e1; font-weight: 700; }}
        .viol-card {{ background: #fff1f2; border: 1px solid #fecdd3; border-radius: 8px; padding: 16px 20px; margin-bottom: 20px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div>
                <h1>📊 다국어 이커머스 초월번역(Transcreation) 품질 진단 리포트 (Track 2 사전감사)</h1>
                <div style="font-size: 14px; opacity: 0.85; margin-top: 6px;">도착 언어: <strong>EN (영어 / 미국 MoCRA & 세포라 표준)</strong> | 대상: <strong>Logically, Skin Aquatide Resurface Serum 50ml</strong> | 종합 점수: <strong>{score} / 100점</strong></div>
            </div>
            <div class="badge">{badge_text}</div>
        </div>

        <div class="score-card">
            <div class="score-box">
                <div class="label">① 전문 어휘 적합성</div>
                <div class="num">{scores.get('domain_relevance')}/30</div>
            </div>
            <div class="score-box">
                <div class="label">② 국가별 광고법 무결성</div>
                <div class="num">{scores.get('ad_law_compliance')}/30</div>
            </div>
            <div class="score-box">
                <div class="label">③ 럭셔리 초월번역 톤</div>
                <div class="num">{scores.get('luxury_transcreation_tone')}/25</div>
            </div>
            <div class="score-box">
                <div class="label">④ 시각 레이아웃 가독성</div>
                <div class="num">{scores.get('visual_layout_conciseness')}/15</div>
            </div>
        </div>

        <div class="summary-box">
            <h3>📝 심사관 종합 진단 총평</h3>
            <p style="margin: 0; line-height: 1.65; color: #334155; font-size: 14px;">{html.escape(summary)}</p>
        </div>

        <!-- ⚖️ 광고 규정 및 MoCRA 위반 사항 -->
        <div class="section-box" style="background:#fffafb;">
            <div class="section-title">🚨 1. 미국 FDA MoCRA 및 해외 광고법 위반 검출 내역</div>
            <div class="viol-card">
                <ul style="margin: 0; padding-left: 20px;">
                    {viol_html}
                </ul>
            </div>
        </div>

        <!-- ⚖️ 결함 전수 상세 내역 (QA Feedbacks) -->
        <div class="section-box">
            <div class="section-title">🔍 2. 결함 전수 상세 내역 (Defect Catalog & QA Feedbacks)</div>
            <table>
                <thead>
                    <tr>
                        <th style="width: 22%;">검출 위치 및 원문 맥락</th>
                        <th style="width: 24%;">수정 전 오류 문안 (Before)</th>
                        <th style="width: 26%;">권고 교정 문안 (Target Transcreation)</th>
                        <th style="width: 28%;">결함 사유 및 개선 지침</th>
                    </tr>
                </thead>
                <tbody>
                    {feed_rows_html}
                </tbody>
            </table>
        </div>

        <!-- 💎 4단 품질 진단 대조표 -->
        <div class="section-box">
            <div class="section-title">💎 3. 4단 품질 진단 정밀 대조표 (Literal vs Luxury Transcreation Matrix)</div>
            <table>
                <thead>
                    <tr>
                        <th style="width: 22%;">① 한국어 원문 맥락</th>
                        <th style="width: 24%;">② 기존 직역/오류본 (Literal)</th>
                        <th style="width: 27%;">③ 💎 세포라급 초월번역안 (Transcreation)</th>
                        <th style="width: 27%;">④ 초월번역 가치 및 법률 개선점</th>
                    </tr>
                </thead>
                <tbody>
                    {comp_rows_html}
                </tbody>
            </table>
        </div>
    </div>
</body>
</html>
"""

html_path = os.path.join(OUT_DIR, "Transcreation_QA_Report.html")
with open(html_path, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"SUCCESS: {json_path}")
print(f"SUCCESS: {html_path}")
