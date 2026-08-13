import os
import sys

# 강제로 sys.argv 조작하여 인코딩 문제 회피
target_dir = r"D:\Users\euntaewoo\Desktop\다국어번역_화장품상품페이지_와이즈엠엔\로지컬리스킨_한국어(국문)_일본어번역\07. 프로페셔널 썬 블록 SPF50+ - Professional Sun Block SPF50+-20260225T123806Z-1-001\07. 프로페셔널 썬 블록 SPF50+ - Professional Sun Block SPF50+\국문\웹상세설명페이지"
sys.argv = ['perfect_image_engine_V3_0.py', target_dir]

import perfect_image_engine_V3_0
perfect_image_engine_V3_0.main()
