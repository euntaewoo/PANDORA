# -*- coding: utf-8 -*-
import os, json

lex_dir = r"C:\Users\euntaewoo\Desktop\multilingual_text_in_image_translatio_agy_sdk_uv-version\00_공통자료\compliance_lexicons"
os.makedirs(lex_dir, exist_ok=True)

en_lex = {
  "jurisdiction": "US_FDA_MoCRA_FTC",
  "target_language": "EN",
  "version": "2026.1.0",
  "last_updated": "2026-09-01",
  "categories": {
    "1_medical_cellular_claims": {
      "description": "인체 구조/세포/생리기능 직접 관여 클레임 차단 (미승인 신약 Unapproved Drug 오인 방지)",
      "banned_terms": [
        {
          "banned": "nutrients for cellular vitality",
          "preferred": "hydration for a resilient-looking complexion",
          "reason": "FDA FD&C Act 201(g)(1) 세포 생리작용 클레임 차단 -> 피부 표면 외관 보습으로 순화"
        },
        {
          "banned": "cellular vitality",
          "preferred": "resilient-looking complexion",
          "reason": "세포 생리작용 오인 차단 -> 피부 표면 외관 표현으로 순화"
        },
        {
          "banned": "reinforces cellular resilience",
          "preferred": "reinforces the skin's natural moisture barrier",
          "reason": "세포 회복력 클레임 배제 -> 피부 천연 수분 장벽 강화로 규제 차단"
        },
        {
          "banned": "cellular resilience",
          "preferred": "skin's natural moisture barrier",
          "reason": "세포 회복력 클레임 배제 -> 피부 천연 수분 장벽으로 순화"
        },
        {
          "banned": "cellular metabolism",
          "preferred": "natural skin vitality",
          "reason": "세포 대사 작용 클레임 배제 -> 자연스러운 피부 생기 표현으로 전환"
        },
        {
          "banned": "stimulates collagen production",
          "preferred": "supports skin's visible firmness and elasticity",
          "reason": "콜라겐 생합성 의료 클레임 방어 -> 시각적 탄력 지지로 순화"
        },
        {
          "banned": "cures acne",
          "preferred": "clarifies blemish-prone skin",
          "reason": "여드름 치료제(OTC Drug) 오인 차단 -> 잡티성 피부 정화로 순화"
        },
        {
          "banned": "anti-inflammatory",
          "preferred": "visibly soothes and calms skin",
          "reason": "소염/항염 의약품 클레임 방어 -> 시각적 진정 완화로 순화"
        },
        {
          "banned": "dna repair",
          "preferred": "advanced revitalizing care",
          "reason": "DNA 복구 유전공학적 클레임 전면 배제"
        },
        {
          "banned": "cell regeneration",
          "preferred": "renews the look of skin surface",
          "reason": "세포 재생 의료 클레임 배제 -> 피부 표면 외관 갱신으로 순화"
        },
        {
          "banned": "hormone production",
          "preferred": "balanced skin nourishment",
          "reason": "호르몬 생성 관여 금지 클레임 배제"
        },
        {
          "banned": "Prescribe",
          "preferred": "Targeted Solution for",
          "reason": "의사 처방 단어 배제"
        },
        {
          "banned": "Bio-Immunity",
          "preferred": "Skin Defense",
          "reason": "생체 면역력 단어 배제"
        }
      ]
    },
    "2_absolute_and_exaggerated_claims": {
      "description": "입증 불가능한 절대적 효능 및 시술 연상 클레임 (FTC 진실광고법 위반 방어)",
      "banned_terms": [
        {
          "banned": "combats premature aging",
          "preferred": "combats the signs of premature aging",
          "reason": "노화 자체를 막는 구조적 변화가 아닌 노화 징후 완화로 한정"
        },
        {
          "banned": "combats aging",
          "preferred": "combats the signs of aging",
          "reason": "노화 징후 완화로 한정하여 과장 광고 규제 방어"
        },
        {
          "banned": "stops aging",
          "preferred": "delays the visible appearance of aging",
          "reason": "노화 정지 클레임 배제 -> 외관상 노화 지연으로 순화"
        },
        {
          "banned": "wrinkle-free",
          "preferred": "visibly smooths the appearance of fine lines",
          "reason": "주름 완전 박멸 과장 광고 방어"
        },
        {
          "banned": "botox-like effect",
          "preferred": "delivers a visibly firm and plump finish",
          "reason": "보톡스 시술 연상 표현 전면 배제"
        },
        {
          "banned": "filler-like effect",
          "preferred": "delivers a deeply hydrated, bouncy look",
          "reason": "필러 시술 연상 표현 전면 배제"
        },
        {
          "banned": "100% guaranteed results",
          "preferred": "clinically proven high-performance formula",
          "reason": "100% 절대적 보장 표현 배제"
        },
        {
          "banned": "permanent whitening",
          "preferred": "enhances radiant luminosity and clarity",
          "reason": "영구적 미백 과장 표현 순화"
        }
      ]
    },
    "3_k_beauty_translationese_to_luxury": {
      "description": "K-뷰티 특유의 어색한 직역 및 콩글리시 -> 글로벌 럭셔리 뷰티(Sephora/Ulta) 표준어 매핑",
      "banned_terms": [
        {
          "banned": "Complex skin issues",
          "preferred": "Multiple skin concerns",
          "reason": "복합적인 피부 고민의 단순 직역(콩글리시) 배제 -> 글로벌 표준 뷰티 용어로 대체"
        },
        {
          "banned": "Troubled skin",
          "preferred": "Blemish-prone skin",
          "reason": "북미 소비자에게 모호한 표현 -> 여드름성/잡티성 피부를 직관적으로 나타내는 어휘 적용"
        },
        {
          "banned": "skin trouble",
          "preferred": "skin breakouts and blemishes",
          "reason": "콩글리시 trouble 배제"
        },
        {
          "banned": "Tone up",
          "preferred": "Radiance-boosting",
          "reason": "톤업 콩글리시 배제 -> 광채 강화 표현 적용"
        },
        {
          "banned": "Water bomb",
          "preferred": "Intense hydration infusion",
          "reason": "직역 표현을 럭셔리 하이드레이션 어휘로 격상"
        },
        {
          "banned": "Skin barrier",
          "preferred": "Natural moisture barrier",
          "reason": "화장품 정규 명칭(천연 수분 장벽)으로 통일"
        },
        {
          "banned": "Kyel-Tan-Tone",
          "preferred": "Texture, Elasticity & Luminosity",
          "reason": "한국식 신조어 결탄톤을 3대 글로벌 효능으로 완벽 초월번역"
        },
        {
          "banned": "fed directly",
          "preferred": "infused daily",
          "reason": "피부에 먹인다는 직역투를 데일리 영양 주입(Infusion)으로 격상"
        }
      ]
    },
    "4_mandatory_qualifiers": {
      "description": "기능성 효능 서술 시 결합이 법적으로 강제되는 필수 안전 수식어",
      "rules": [
        {
          "trigger": "aging",
          "mandatory_prefix": "the signs of / the appearance of",
          "rule": "노화 언급 시 반드시 징후(signs) 또는 외관(appearance) 결합 강제"
        },
        {
          "trigger": "wrinkles",
          "mandatory_prefix": "the look of / the appearance of fine lines and",
          "rule": "주름 언급 시 잔주름 및 주름의 외관 강제"
        },
        {
          "trigger": "elasticity",
          "mandatory_prefix": "visibly improves / restores visible",
          "rule": "탄력 언급 시 시각적으로 개선 강제"
        }
      ]
    }
  }
}

jp_lex = {
  "jurisdiction": "JP_MHLW_PMDA",
  "target_language": "JP",
  "version": "2026.1.0",
  "last_updated": "2026-09-01",
  "categories": {
    "1_pharmaceutical_claims": {
      "description": "의약품/의약부외품 오인 표현 금지 및 화장품 영역 56종 순화",
      "banned_terms": [
        {"banned": "治療", "preferred": "肌を整えるケア", "reason": "치료 표현 금지"},
        {"banned": "再生", "preferred": "すこやかに保つ", "reason": "재생 표현 금지"},
        {"banned": "消炎", "preferred": "肌荒れを防ぐ", "reason": "소염 표현 금지"},
        {"banned": "無刺激", "preferred": "低刺激処方", "reason": "무자극 단정 표현 금지"},
        {"banned": "細胞活性化", "preferred": "肌にハリとうるおいを与える", "reason": "세포 활성화 표현 금지"},
        {"banned": "美白", "preferred": "うるおいによる透明感", "reason": "의약부외품 미백 효능 오인 방지"}
      ]
    },
    "2_absolute_claims": {
      "description": "절대적 과대표현 금지",
      "banned_terms": [
        {"banned": "世界初", "preferred": "先進テクノロジー", "reason": "세계 최초 표현 금지"},
        {"banned": "No.1", "preferred": "こだわり抜いた", "reason": "넘버원 표현 금지"},
        {"banned": "最高", "preferred": "上質な", "reason": "최고 표현 금지"},
        {"banned": "究極", "preferred": "高機能", "reason": "궁극 표현 금지"}
      ]
    }
  }
}

cn_lex = {
  "jurisdiction": "CN_NMPA_SAMR",
  "target_language": "CN",
  "version": "2026.1.0",
  "last_updated": "2026-09-01",
  "categories": {
    "1_ad_law_absolute_banned": {
      "description": "중국 신광고법 8대 절대화 금지어",
      "banned_terms": [
        {"banned": "最", "preferred": "优 / 臻", "reason": "신광고법 절대어 금지"},
        {"banned": "第一", "preferred": "前沿 / 首选", "reason": "제1 절대어 금지"},
        {"banned": "顶级", "preferred": "高端 / 臻选", "reason": "최상급 표현 금지"},
        {"banned": "极品", "preferred": "甄选", "reason": "극품 표현 금지"},
        {"banned": "永久", "preferred": "持久", "reason": "영구적 표현 금지"},
        {"banned": "万能", "preferred": "多效", "reason": "만능 표현 금지"},
        {"banned": "100%", "preferred": "显著", "reason": "100% 보장 표현 금지"},
        {"banned": "彻底", "preferred": "深入", "reason": "철저/완전 표현 금지"}
      ]
    },
    "2_medical_claims": {
      "description": "NMPA 의료 및 세포 치료 오인 표현 금지",
      "banned_terms": [
        {"banned": "细胞再生", "preferred": "修护肌肤屏障", "reason": "세포 재생 클레임 금지"},
        {"banned": "根除皱纹", "preferred": "淡化细纹", "reason": "주름 근절 클레임 금지"},
        {"banned": "消炎抗敏", "preferred": "舒缓修护", "reason": "소염 항민 클레임 금지"}
      ]
    }
  }
}

tw_lex = {
  "jurisdiction": "TW_MOHW_TFDA",
  "target_language": "TW",
  "version": "2026.1.0",
  "last_updated": "2026-09-01",
  "categories": {
    "1_tfda_cosmetics_regulations": {
      "description": "대만 TFDA 화장품 표기 기준",
      "banned_terms": [
        {"banned": "細胞再生", "preferred": "強化肌膚屏障", "reason": "세포 재생 표현 금지"},
        {"banned": "撫平所有皺紋", "preferred": "淡化細紋與乾紋", "reason": "절대적 주름 완화 금지"},
        {"banned": "消炎舒敏", "preferred": "安撫舒緩肌膚", "reason": "소염 표현 금지"},
        {"banned": "第一", "preferred": "經典熱銷", "reason": "최고/제1 표현 금지"}
      ]
    }
  }
}

with open(os.path.join(lex_dir, "en_fda_mocra_lexicon.json"), "w", encoding="utf-8") as f:
    json.dump(en_lex, f, ensure_ascii=False, indent=2)

with open(os.path.join(lex_dir, "jp_pmda_pharm_lexicon.json"), "w", encoding="utf-8") as f:
    json.dump(jp_lex, f, ensure_ascii=False, indent=2)

with open(os.path.join(lex_dir, "cn_nmpa_adlaw_lexicon.json"), "w", encoding="utf-8") as f:
    json.dump(cn_lex, f, ensure_ascii=False, indent=2)

with open(os.path.join(lex_dir, "tw_tfda_lexicon.json"), "w", encoding="utf-8") as f:
    json.dump(tw_lex, f, ensure_ascii=False, indent=2)

print("SUCCESS: 4 Compliance Lexicon JSON files written.")