# 🇨🇳 중국어 이미지 번역 엔진 CLI 명령어 가이드 (CLI Usage Guide)

> **엔진 파일**: `CN_Text-In_Image_Translation_Engine_V1.py`  
> **엔진 위치**: `C:\Users\euntaewoo\Desktop\다국어_이미지_번역\중국어\`  
> **기반 코어**: Two-Pass Multimodal Neural Inpainting Architecture (Gemini 3.1 Pro + Flash-Image)  
> **표준 폰트**: Noto Sans SC (스위안헤이티 / 思源黑体 / Source Han Sans SC)

---


## 📌 1. 기본 명령어 문법 (Syntax)

```bash
python C:\Users\euntaewoo\Desktop\다국어_이미지_번역\중국어\CN_Text-In_Image_Translation_Engine_V1.py [원본_이미지_폴더] [출력_폴더_옵션] --target={CN|TW|HK}
```

---

## 🎯 2. 타겟 권역별 실행 명령어

### 1) 🇨🇳 중국 본토 시장 (간체자, zh-CN) — 기본값
- **적용 규격**: 간체자 강제, 중국 신(新) 광고법 8대 절대화 표현(`最`, `第一`, `顶级` 등) 자동 순화, 타오바오/티몰/샤오홍슈 톤앤매너
```bash
python C:\Users\euntaewoo\Desktop\다국어_이미지_번역\중국어\CN_Text-In_Image_Translation_Engine_V1.py "C:\Users\euntaewoo\Desktop\다국어_이미지_번역\01_번역대상_원본" --target=CN
```

### 2) 🇹🇼 대만 시장 (번체자, zh-TW)
- **적용 규격**: 대만 정체자(번체), 대만 TFDA 화장품법 준수, 대만 이커머스 어휘(`化妝水`, `鎖水`, `精華液`, `水光肌` 등)
```bash
python C:\Users\euntaewoo\Desktop\다국어_이미지_번역\중국어\CN_Text-In_Image_Translation_Engine_V1.py "C:\Users\euntaewoo\Desktop\다국어_이미지_번역\01_번역대상_원본" --target=TW
```

### 3) 🇭🇰 홍콩 시장 (번체자, zh-HK)
- **적용 규격**: 홍콩 정체자(번체), 홍콩 이커머스 어휘(`爽膚水`, `補濕`, `精華素`, `HK$` 등), HKTVmall 톤앤매너
```bash
python C:\Users\euntaewoo\Desktop\다국어_이미지_번역\중국어\CN_Text-In_Image_Translation_Engine_V1.py "C:\Users\euntaewoo\Desktop\다국어_이미지_번역\01_번역대상_원본" --target=HK
```

---

## 📂 3. 출력 폴더 직접 지정 시 명령어

출력 폴더 경로를 두 번째 인자로 전달하면 원하는 위치에 결과물이 저장됩니다:

```bash
python C:\Users\euntaewoo\Desktop\다국어_이미지_번역\중국어\CN_Text-In_Image_Translation_Engine_V1.py "C:\Users\euntaewoo\Desktop\다국어_이미지_번역\01_번역대상_원본" "C:\Users\euntaewoo\Desktop\다국어_이미지_번역\02_번역결과_최종\중국어_출력결과" --target=CN
```

---

## 📋 4. 상품 고시정보 표 렌더러 단독 실행 가이드

고시정보 표(Notice Table)를 가로 `860px`, 세로 `Auto-Fit`(타이틀 52px, 본문 26px, 자간+행간 최적화, 최대 2,580px 이하 1장 단일 통합 페이지) 표준 규격으로 단독 렌더링할 때:

```bash
python C:\Users\euntaewoo\Desktop\다국어_이미지_번역\00_공통자료\render_notice_table_standard.py
```



---

## ⚙️ 5. 주요 옵션 설명 (Options)

| 옵션 플래그 | 필수 여부 | 기본값 | 설명 |
| :--- | :---: | :---: | :--- |
| `source_dir` | 선택 | `..\01_번역대상_원본` | 번역할 한국어 원본 이미지가 위치한 디렉터리 경로 |
| `target_dir` | 선택 | `..\02_번역결과_최종\...` | 번역된 이미지를 저장할 디렉터리 경로 (미지정 시 자동 생성) |
| `--target` | 선택 | `CN` | 타겟 시장 권역 지정 (`CN`: 중국본토 간체, `TW`: 대만 번체, `HK`: 홍콩 번체) |
| `-h, --help` | 선택 | - | 도움말 및 사용법 출력 |

---

## 🛡️ 6. 작업 전 필수 체크리스트 (`[RULE 8]`)

> ⚠️ **주의**: 사용자가 중국어 번역을 요청할 때 타겟 권역을 지정하지 않은 경우, 에이전트는 절대 임의로 추측하지 않고 반드시 아래 표준 질문을 먼저 제시해야 합니다:
> 
> **"중국 본토(간체자)와 대만/홍콩(번체자) 중 어느 시장을 타겟으로 제작할까요?"**
