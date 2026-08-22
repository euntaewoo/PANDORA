import os
import sys

sys.path.append(r"C:\Users\euntaewoo\Desktop\다국어_이미지_번역\00_공통자료")
from render_notice_table_standard import render_notice_table_to_png

title = "商品详细信息"
items = [
    {"label": "容量 / 重量", "value": "200g"},
    {"label": "产品主要规格", "value": "适用于所有肤质"},
    {"label": "使用期限或开封后使用期间", "value": "产品内另行标示 (若标注开封后使用期间，则并列标示制造年月)"},
    {"label": "使用方法", "value": "取适量泡沫于手中，用于脸部及其他部位后，用清水洗净。"},
    {"label": "化妆品制造商 /<br>化妆品责任销售商及<br>定制型化妆品销售商", "value": "(株)Natuzen / Skin Reverse Lab (株)"},
    {"label": "制造国", "value": "韩国"},
    {"label": "全成分", "value": "纯净水, 甘油, 肉豆蔻酸, 月桂酸, 月桂酰胺 DEA, 月桂醇聚醚硫酸酯钠, 氢氧化钾, 丁二醇, 椰油酰胺丙基甜菜碱, PEG-120 甲基葡糖二油酸酯, 水杨酸, 氯化钠, 薰衣草油, 癸二醇, 氯化月桂基吡啶, 芳樟醇, 乙二胺四乙酸四钠, PCA 乙基椰油酰精氨酸盐, 绿茶提取物, 芦荟叶提取物, 生育酚"},
    {"label": "机能性化妆品有无", "value": "机能性认证：韩国食品药物安全处认证，缓解痘痘肌机能性化妆品"},
    {"label": "使用时的注意事项", "value": "1) 使用化妆品时或使用后，若因阳光直射导致使用部位出现红斑、肿胀或发痒等异常症状或副作用，请咨询专业医师。<br>2) 请避免使用于有伤口等部位。<br>3) 保管及处理注意事项<br>&nbsp;&nbsp;A. 请放置于儿童无法触及之处<br>&nbsp;&nbsp;B. 请避开阳光直射保管"},
    {"label": "品质保证基准", "value": "遵循相关法律及消费者纠纷解决规定"},
    {"label": "消费者咨询电话", "value": "02-6743-3206"}
]

output_dir = r"C:\Users\euntaewoo\Desktop\다국어_이미지_번역\중국어\output\중국어(간체)"
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, "016_상품상세정보_RED BLEMISH RELIEF CLEANSER_200ml_CN_CN.png")

success = render_notice_table_to_png(title, items, output_path, lang="CN")
if success:
    print(f"[COMPLETE] Notice table generated: {output_path}")
else:
    print("[FAIL] Failed to generate notice table")
