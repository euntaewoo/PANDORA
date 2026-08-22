import os
import sys

sys.path.append(r"C:\Users\euntaewoo\Desktop\다국어_이미지_번역\00_공통자료")
from render_notice_table_standard import render_notice_table_to_png

title = "商品详细信息"
items = [
    {"label": "容量 / 重量", "value": "70g (2.47 oz.)"},
    {"label": "产品主要规格", "value": "适用于所有肤质"},
    {"label": "使用期限", "value": "另行标示于产品上"},
    {"label": "使用方法", "value": "在基础护肤最后阶段，取适量均匀涂抹于易受紫外线照射的部位。"},
    {"label": "化妆品制造商 /<br>化妆品责任销售商", "value": "Nowcos Co., Ltd. / Skin Reverse Lab Co., Ltd."},
    {"label": "制造国", "value": "韩国"},
    {"label": "特殊化妆品审核", "value": "焕亮、紧致淡纹、防晒多重功效 (韩国食品医药品安全处审核/报告完成)"},
    {"label": "全成分", "value": "水, 水杨酸丁辛酯, 氧化锌, 环五聚二甲基硅氧烷, 环己硅氧烷, 鲸蜡醇乙基己酸酯, 丁二醇, 聚二甲基硅氧烷, 二氧化硅, 烟酰胺, PEG-10 聚二甲基硅氧烷, 炉甘石, PEG-9 聚二甲基硅氧乙基聚二甲基硅氧烷, 聚二甲基硅氧烷/PEG-10/15 交联聚合物, 二硬脂二甲铵锂蒙脱石, 硫酸镁, 地蜡, 脱水山梨糖醇倍半油酸酯, 二氧化钛, 聚二甲基硅氧烷交联聚合物, 乙基己二醇, 三乙氧基辛基硅烷, 二甲基甲硅烷基化硅石, 硬脂酸, 辛酸甘油酯, 月桂酰赖氨酸, 1,2-己二醇, 乙二胺四乙酸二钠, 腺苷, 戊酸四羧甲基乙酰基羟丙基二肽-12, 戊酸四羧甲基二肽-51, 四羧甲基己酰基二肽-12"},
    {"label": "使用注意事项", "value": "1. 使用化妆品时或使用后，因阳光直射导致使用部位出现红斑、浮肿或瘙痒等异常症状或副作用时，请咨询专业医师。<br>2. 请勿在有伤口的部位使用。<br>3. 保管及使用注意事项<br>&nbsp;&nbsp;A. 请放置于儿童无法触及的地方。<br>&nbsp;&nbsp;B. 请避开阳光直射保存。"},
    {"label": "质量保证标准", "value": "本产品如有异常，依据相关法规及消费者争议解决标准进行赔偿。"},
    {"label": "消费者咨询电话", "value": "+82-2-6743-3206"}
]

output_dir = r"C:\Users\euntaewoo\Desktop\다국어_이미지_번역\중국어\output\07_(중국어_간체번역)Professional Sun Block SPF50+PA"
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, "8_웹상세페이지_Professional-Sun-Block-70_CN_CN_v1.png")

success = render_notice_table_to_png(title, items, output_path, lang="CN")
if success:
    print(f"[COMPLETE] Notice table generated: {output_path}")
else:
    print("[FAIL] Failed to generate notice table")
