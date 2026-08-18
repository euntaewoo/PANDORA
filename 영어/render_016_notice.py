import os
import sys

sys.path.append(r"C:\Users\euntaewoo\Desktop\다국어_이미지_번역\00_공통자료")
from render_notice_table_standard import render_notice_table_to_png

title = "PRODUCT DETAILS"
items = [
    {"label": "Volume / Weight", "value": "200g"},
    {"label": "Product Specifications", "value": "For all skin types"},
    {"label": "Expiration Date", "value": "Marked separately on product packaging"},
    {"label": "How to Use", "value": "Dispense an appropriate amount of foam onto wet hands, gently massage over face and desired areas, and rinse thoroughly with lukewarm water."},
    {"label": "Manufacturer /<br>Responsible Distributor", "value": "Natuzen Co., Ltd. / Skin Reverse Lab Co., Ltd."},
    {"label": "Country of Manufacture", "value": "Republic of Korea"},
    {"label": "Full Ingredients", "value": "Water, Glycerin, Myristic Acid, Lauric Acid, Lauramide DEA, Sodium Laureth Sulfate, Potassium Hydroxide, Butylene Glycol, Cocamidopropyl Betaine, PEG-120 Methyl Glucose Dioleate, Salicylic Acid, Sodium Chloride, Lavandula Angustifolia (Lavender) Oil, Decylene Glycol, Laurylpyridinium Chloride, Linalool, Tetrasodium EDTA, PCA Ethyl Cocoyl Arginate, Camellia Sinensis Leaf Extract, Aloe Barbadensis Leaf Extract, Tocopherol"},
    {"label": "Functional Cosmetics Review", "value": "MFDS Certified Functional Cosmetic for Acne-Prone Skin Relief"},
    {"label": "Precautions for Use", "value": "1) If you experience abnormal symptoms or side effects such as red spots, swelling, or itching due to direct sunlight during or after use, consult a specialist.<br>2) Refrain from using on wounded or damaged areas.<br>3) Precautions for storage and handling:<br>&nbsp;&nbsp;A. Keep out of reach of children.<br>&nbsp;&nbsp;B. Store away from direct sunlight."},
    {"label": "Quality Assurance Standards", "value": "In accordance with applicable consumer dispute resolution regulations."},
    {"label": "Customer Service", "value": "+82-2-6743-3206"}
]

output_dir = r"C:\Users\euntaewoo\Desktop\다국어_이미지_번역\영어\output"
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, "016_상품상세정보_RED BLEMISH RELIEF CLEANSER_200ml_수정번역.png")

success = render_notice_table_to_png(title, items, output_path, lang="EN")
if success:
    print(f"[COMPLETE] Notice table generated: {output_path}")
else:
    print("[FAIL] Failed to generate notice table")
