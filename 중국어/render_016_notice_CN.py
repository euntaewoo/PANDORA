import os
import sys

sys.path.append(r"C:\Users\euntaewoo\Desktop\다국어_이미지_번역\00_공통자료")
from render_notice_table_standard import render_notice_table_to_png

title = "商品詳細資訊"
items = [
    {"label": "容量 / 重量", "value": "200g"},
    {"label": "產品主要規格", "value": "適用於所有膚質"},
    {"label": "使用期限或開封後使用期間", "value": "標示於產品包裝上"},
    {"label": "使用方法", "value": "取適量泡沫於濕潤的手中，輕柔按摩於臉部及需要清潔的部位後，用溫水洗淨。"},
    {"label": "化妝品製造商 /<br>責任銷售商", "value": "(株)Natuzen / Skin Reverse Lab (株)"},
    {"label": "製造國", "value": "韓國"},
    {"label": "全成分", "value": "水, 甘油, 肉豆蔻酸, 月桂酸, 月桂醯胺 DEA, 月桂醇聚醚硫酸酯鈉, 氫氧化鉀, 丁二醇, 椰油醯胺丙基甜菜鹼, PEG-120 甲基葡糖二油酸酯, 水楊酸, 氯化鈉, 薰衣草油, 癸二醇, 氯化月桂基吡啶, 芳樟醇, 乙二胺四乙酸四鈉, PCA 乙基椰油醯精氨酸鹽, 綠茶萃取物, 蘆薈葉萃取物, 生育酚"},
    {"label": "機能性化妝品審查與否", "value": "食品藥物安全處認證，緩解痘痘肌機能性化妝品"},
    {"label": "使用時的注意事項", "value": "1) 使用化妝品時或使用後，若因陽光直射導致使用部位出現紅斑、腫脹或發癢等異常症狀或副作用，請諮詢專業醫師。<br>2) 請避免使用於有傷口等部位。<br>3) 保管及處理注意事項:<br>&nbsp;&nbsp;A. 請放置於兒童無法觸及之處。<br>&nbsp;&nbsp;B. 請避開陽光直射保管。"},
    {"label": "品質保證基準", "value": "遵循相關法律及消費者糾紛解決規定。"},
    {"label": "消費者諮詢電話", "value": "+82-2-6743-3206"}
]

output_dir = r"C:\Users\euntaewoo\Desktop\다국어_이미지_번역\중국어\output"
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, "016_상품상세정보_RED BLEMISH RELIEF CLEANSER_200ml_CN_TW.png")

success = render_notice_table_to_png(title, items, output_path, lang="CN")
if success:
    print(f"[COMPLETE] Notice table generated: {output_path}")
else:
    print("[FAIL] Failed to generate notice table")
