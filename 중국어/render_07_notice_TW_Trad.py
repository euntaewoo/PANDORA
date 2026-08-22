import os
import sys

sys.path.append(r"C:\Users\euntaewoo\Desktop\다국어_이미지_번역\00_공통자료")
from render_notice_table_standard import render_notice_table_to_png

title = "商品詳細資訊"
items = [
    {"label": "容量 / 重量", "value": "70g (2.47 oz.)"},
    {"label": "產品主要規格", "value": "適用於所有膚質"},
    {"label": "使用期限", "value": "另行標示於產品上"},
    {"label": "使用方法", "value": "在基礎保養最後階段，取適量均勻塗抹於易受紫外線照射的部位。"},
    {"label": "化妝品製造商 /<br>化妝品責任販售商", "value": "Nowcos Co., Ltd. / Skin Reverse Lab Co., Ltd."},
    {"label": "製造國", "value": "韓國"},
    {"label": "功能性化妝品審查", "value": "具備亮白、緊緻撫紋、防曬多重功效 (韓國食品醫藥品安全處審查/申報完成)"},
    {"label": "全成分", "value": "水, 水楊酸丁辛酯, 氧化鋅, 環五聚二甲基矽氧烷, 環己矽氧烷, 鯨蠟醇乙基己酸酯, 丁二醇, 聚二甲基矽氧烷, 二氧化矽, 菸鹼醯胺, PEG-10 聚二甲基矽氧烷, 爐甘石, PEG-9 聚二甲基矽氧乙基聚二甲基矽氧烷, 聚二甲基矽氧烷/PEG-10/15 交聯聚合物, 二硬脂二甲銨鋰蒙脫石, 硫酸鎂, 地蠟, 脫水山梨糖醇倍半油酸酯, 二氧化鈦, 聚二甲基矽氧烷交聯聚合物, 乙基己二醇, 三乙氧基辛基矽烷, 二甲基甲矽烷基化矽石, 硬脂酸, 辛酸甘油酯, 月桂醯賴胺酸, 1,2-己二醇, 乙二胺四乙酸二鈉, 腺苷, 戊酸四羧甲基乙醯基羥丙基二肽-12, 戊酸四羧甲基二肽-51, 四羧甲基己醯基二肽-12"},
    {"label": "使用注意事項", "value": "1. 使用化妝品時或使用後，因陽光直射導致使用部位出現紅斑、浮腫或搔癢等異常症狀或副作用時，請諮詢專業醫師。<br>2. 請勿在有傷口的部位使用。<br>3. 保管及使用注意事項<br>&nbsp;&nbsp;A. 請放置於兒童無法觸及之處。<br>&nbsp;&nbsp;B. 請避開陽光直射保存。"},
    {"label": "品質保證基準", "value": "本產品如有異常，依據相關法規及消費者爭議解決基準進行賠償。"},
    {"label": "消費者諮詢專線", "value": "+82-2-6743-3206"}
]

output_dir = r"C:\Users\euntaewoo\Desktop\다국어_이미지_번역\중국어\output\07_(중국어_번체번역)Professional Sun Block SPF50+PA"
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, "8_웹상세페이지_Professional-Sun-Block-70_CN_TW_v1.png")

success = render_notice_table_to_png(title, items, output_path, lang="TC")
if success:
    print(f"[COMPLETE] Notice table generated: {output_path}")
else:
    print("[FAIL] Failed to generate notice table")
