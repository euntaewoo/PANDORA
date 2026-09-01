# -*- coding: utf-8 -*-
import os, re

target_dir = r"C:\Users\euntaewoo\Desktop\multilingual_text_in_image_translatio_agy_sdk_uv-version\04_번역교정\LogicallySkin_MultiVitaminSerum_영어"
txt_file = os.path.join(target_dir, "LogicallySkin_MultiVitaminSerum_EN_SEO_GEO_AEO.txt")
html_file = os.path.join(target_dir, "LogicallySkin_MultiVitaminSerum_EN_SEO_GEO_AEO_VIEWER.html")

# 1. Update TXT
new_txt = """1. Official Product Title
Logically Skin Multi-Vitamin Serum: Ultimate Skin Vitality 30ml

2. Core Value & Active Ingredient Summary
Brand: Logically Skin
Core Ingredients: High-Potency Multi-Vitamin Complex, Centella Asiatica Extract
Key Benefits: Visibly revitalizes complexion, combats the signs of premature aging, and reinforces the skin's natural moisture barrier
Texture & Finish: Lightweight, fast-absorbing daily infusion with a refreshing, non-greasy finish
Target Skin Concerns: Multiple skin concerns, dullness, signs of premature aging, and blemish-prone or irritated skin

3. Product Usage Guide & Frequently Asked Questions (FAQ)
Q1: How should I incorporate this serum into my skincare routine?
A: Apply a few drops directly onto cleansed and toned skin twice a day as part of your high-potency vitamin ritual.

Q2: Is this serum safe for sensitive or blemish-prone skin?
A: Yes, it features Centella Asiatica Extract to visibly soothe irritation and clarify blemish-prone skin safely and gently.

Q3: What are the primary anti-aging benefits of this product?
A: It provides essential hydration for a resilient-looking complexion, visibly revitalizing the skin and combating the signs of premature aging.

Q4: Does this product help strengthen the skin barrier?
A: Absolutely, this targeted solution enhances natural skin vitality and reinforces the skin's natural moisture barrier for a healthier-looking complexion.

Q5: Will this serum leave a heavy or sticky residue?
A: No, it is designed as a daily infusion of vital nutrients that absorbs quickly, leaving your skin refreshed and perfectly prepped for moisturizer.
"""

with open(txt_file, "w", encoding="utf-8") as f:
    f.write(new_txt)

print("SUCCESS: Updated TXT file.")

# 2. Update HTML Viewer
with open(html_file, "r", encoding="utf-8") as f:
    html_content = f.read()

replacements = [
    ("Complex skin issues", "Multiple skin concerns"),
    ("troubled skin", "blemish-prone skin"),
    ("Troubled skin", "Blemish-prone skin"),
    ("nutrients for cellular vitality", "hydration for a resilient-looking complexion"),
    ("cellular vitality", "resilient-looking complexion"),
    ("reinforces cellular resilience", "reinforces the skin's natural moisture barrier"),
    ("cellular resilience", "skin's natural moisture barrier"),
    ("combats premature aging", "combats the signs of premature aging"),
    ("combats signs of premature aging", "combats the signs of premature aging"),
]

for orig, rep in replacements:
    html_content = html_content.replace(orig, rep)

with open(html_file, "w", encoding="utf-8") as f:
    f.write(html_content)

print("SUCCESS: Updated HTML Viewer file.")