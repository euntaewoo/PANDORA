import os
import io
import sys
import time
from google import genai
from PIL import Image

sys.stdout.reconfigure(encoding='utf-8')

# 로컬 상대경로의 .env 파일 탐색 및 키 추출
script_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(script_dir, ".env")
api_key = None
if os.path.exists(env_path):
    with open(env_path, "r", encoding="utf-8") as f:
        for line in f:
            if line.startswith("GEMINI_API_KEY="):
                api_key = line.split("=")[1].strip()
                break

if not api_key:
    api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    print("[ERROR] GEMINI_API_KEY가 설정되지 않았습니다. .env 파일 또는 환경변수를 확인하세요.")
    sys.exit(1)

client = genai.Client(api_key=api_key)

# [V5 규칙 강제]: 2026년 6월 1일부로 서비스 종료(Shut down)된 구형 모델(1.5, 2.0, 2.5 등)의 선언 및 호출을 차단하는 가드
DEPRECATED_MODELS = ["gemini-3.1-pro-preview", "gemini-3.1-flash-image", "gemini-2.0-flash", "gemini-2.5-pro"]
MODEL_ID = "gemini-3.1-flash-image"

if MODEL_ID in DEPRECATED_MODELS:
    print(f"[FATAL ERROR] {MODEL_ID} 모델은 2026년 6월 1일부로 서비스가 완전히 종료되어 사용이 불가합니다. 최신 규격 모델을 사용하십시오.")
    sys.exit(1)

# 커맨드라인 파라미터 파싱
if len(sys.argv) > 1:
    source_dir = sys.argv[1]
    if len(sys.argv) > 2:
        base_target_dir = sys.argv[2]
    else:
        base_target_dir = os.path.join(os.path.dirname(source_dir), os.path.normpath(source_dir).split(os.sep)[-1] + "_JP_Translated")
else:
    source_dir = r"C:\Users\euntaewoo\Desktop\이미지번역워크스페이스\변역대상\05. 멀티코렉티브 아이크림 -Multi Corrective Eye cream-20260225T123156Z-1-001\05. 멀티코렉티브 아이크림 -Multi Corrective Eye cream"
    base_target_dir = r"C:\Users\euntaewoo\Desktop\이미지번역워크스페이스\변역결과\5_(일본어)Multi Corrective Eye cream"

# 사용자가 명령 파라미터로 명시적인 번역결과 폴더를 지정한 경우 서브폴더를 중복 생성하지 않고 그대로 타겟 폴더로 사용
if len(sys.argv) > 2:
    target_dir = base_target_dir
else:
    if len(sys.argv) == 1:
        target_dir = base_target_dir
    else:
        folder_name = os.path.normpath(source_dir).split(os.sep)[-1]
        target_dir = os.path.join(base_target_dir, folder_name)
os.makedirs(target_dir, exist_ok=True)

# [번역 엔진 주입 핵심 규칙 - 재번역 규정]
# 1. 1차 번역작업 완료 후 검수 시점에 이미지 번역 오류가 발견되어 수정작업을 진행할 경우,
#    절대로 이미 번역 가공 처리된 이미지 위에 추가 덮어씌우기 수정(2차 터치업)을 진행하지 않는다.
# 2. 반드시 오류가 존재하지 않는 순수한 '한국어 원본 번역대상물 이미지(KOR)'를 처음부터 새로 로드하여,
#    백지 상태에서 완전히 새롭게 이미지 번역 연산을 수행해 결과 이미지를 창조하여 저장해야 한다.

# 6월 12일 원본 번역 통제 지침 프롬프트 (제품 포장 텍스트 원문 보존 규칙 초강력 반영)
prompt = """
첨부된 원본 이미지 속의 한국어 텍스트 위치와 배경 텍스처, 디자인 레이아웃을 1픽셀의 왜곡 없이 그대로 유지해라.
그리고 모든 한국어 텍스트만 일본어(Qoo10 Japan PMDA 규정 완벽 준수)로 자연스럽게 교체한 완성된 단일 이미지를 생성해 줘.

[CRITICAL RULE - KOREAN TEXT ERASING & OVERWRITING]
1. 상세페이지 배경의 모든 한국어 텍스트(예: "얼루어 평가단" 같은 작은 평가단 텍스트 등 포함)는 원래 자리에 남겨두지 말고 반드시 깨끗하게(배경색으로 덮어써서) 완전히 지워라. 누락 없이 모든 한국어는 일본어로 번역되어야 한다.
2. 지워진 그 자리에 일본어 번역본만 단독으로 렌더링해야 하며, 한국어 원문과 일본어 번역문이 동시에 기재되는 병기 현상은 절대 허용되지 않는다. 반드시 한글 원문은 100% 삭제되고 일본어만 보여야 한다.
3. 이미지 내에 번역과 무관한 AI 모델의 자체 주석, 영어 설명 문장, 괄호 안의 메타 설명(예: "Allergy-tested/Stinging tested...", "This is for natural text...", "PMDA compliance avoids...") 등을 절대로 텍스트로 그려 넣거나 노출시키지 마라. 오직 최종 일본어 번역본 본문 내용만 이미지 상에 렌더링해야 한다.
4. 이미지 하단의 세로로 나열된 3개의 소비자 리뷰 단락(첫 번째, 두 번째, 세 번째 세로 열 전체)을 100% 빠짐없이 일본어로 번역해야 한다. 한글 원문은 배경색으로 완전히 지우고 오직 번역된 일본어만 인페인팅해라. 한글 텍스트가 번역되지 않고 방치되는 일이 절대로 없어야 한다.

[CRITICAL RULE - PRODUCT PACKAGING TEXT PRESERVATION]
1. 이미지 내에 배치된 실제 제품 본품(용기, 튜브, 세럼 병) 및 제품 박스(단상자 패키지) 표면에 인쇄된 모든 텍스트(브랜드명, 한글 문구, 영어 문장, 용량 등)는 한글이건 영어이건 절대 일본어로 번역하거나 지우지 말고, 원본 픽셀 그대로 100% 보존해라.
   * 특히 패키지 표면에 인쇄되어 있는 영어 브랜드명 'Logically, Skin' 및 영문 제품명 'Multi-lifting Cream' (또는 'Aquatide Resurface Serum'), 그리고 단상자/용기/튜브 표면의 모든 영문 성분표 및 설명글은 절대 번역하지 말고 원본 이미지 픽셀 그대로 보존할 것.
2. 실물 제품 패키지 표면이 아닌, 상세페이지 배경의 설명 타이틀, 세부 설명 텍스트, 바디 텍스트만 일본어로 정밀 번역 및 교체해라.
3. 원본 이미지 상에 존재하지 않는 화장품 실물 용기나 종이 상자 패키지 디자인을 임의로 창조하여 이미지의 빈 공간(예: "Real Voice" 헤드 타이틀 우측 등)에 그려 넣지 마라. 원래 없는 요소는 절대 추가하지 말고 원본 배경과 동일하게 여백으로 깨끗이 유지해라.

[일본 약기법 필수 준수 강제 지침]
1. '자극 없이(刺激なく)', '무자극'과 같은 단정적인 표현은 절대 금지. 반드시 '피부에 순하게(肌にやさしく)' 또는 '저자극 처방(低刺激処方)'으로 안전하게 의역할 것. 리뷰 내 '주의 성분 전혀 없음' 표현 또한 '마일드한 처방(マイルドな処方)' 또는 '피부를 배려한 마일드한 사용감(肌에 부드러운 사용감)'으로 순화하여 의역할 것.
2. '진정(鎮静)'이라는 의학적 치료 효능 단어 사용 절대 금지. 반드시 화장품 공식 허용 문구인 '피부를 정돈하다(肌を整える)' 또는 '피부 거칠어짐을 방지하다(肌荒れを防ぐ)'로 대체할 것.
3. '흡수' 또는 '침투' 단어는 반드시 '浸透'로 번역하고, 이 단어가 번역 이미지 내에 사용되었을 경우, 이미지 최하단 영역에 아주 작게(원래 텍스트 대비 약 1.2% 크기) 법적 필수 면책 문구인 `*浸透は角質層まで` (침투는 각질층까지)를 일본어 자모의 깨짐이나 한글의 뒤섞임 현상 없이 선명하고 명확하게 렌더링해 넣어라.
4. '적당량'은 화장품 제형(고농축 세럼 및 크림)의 특성에 맞게 일본어 '適量' (적당량)으로 번역해라. 절대 '500円玉大'로 번역하지 마라.
5. '컨디션 유지'는 'コンディション維持'로 번역해라.
6. '치료'는 'ケア'로, '개선'은 '整える'로, '재생'은 'いきいき'로 순화하여 번역해라.
7. '리프팅' 또는 '리프트업' 효능을 주장하는 한국어 설명글은 일본 약기법 준수를 위해 반드시 'ハリ' (탄력) 또는 'ハリ感' (탄력감)으로 의역하여 번역해라.
8. '세포 활성화(細胞活性化)', '세포 분해 및 교체', '세포 재생' 등 세포 단위의 대사/활성화를 표방하는 표현은 화장품 법규상 금지되므로 절대 기재하지 마라. 이는 '피부에 생기를 부여하다(肌にいきいきとしたハリを与える)', '피부를 매끄럽고 건강하게 정돈하다(肌を健やかに整える)' 등으로 전면 완화하여 번역할 것.
9. '노벨 생리학·의학상 수상 원료', '노벨상 수상 원리' 등 노벨상을 화장품의 실제 효능과 결합해 부당한 우수성을 강조하는 표현은 금지한다. 노벨상 단어 노출 없이 단순히 '오토파지 기술(オートファジー技術)' 등으로 사실에 기반한 명칭으로 완화하여 번역해라.
10. 일반 화장품 상세페이지이므로 허가받지 않은 직접적인 '안티에이징(アンチエイジング)' 단어는 '에이징 케어(エイジングケア)'로 번역하며, 이 단어가 사용될 시 주변이나 최하단에 주석으로 `*エイジングケアとは、年齢に応じたお手入れのこと` (에이징 케어는 연령에 따른 관리를 의미함) 면책 문구를 1.2% 크기로 렌더링해라.
11. '강력한', '강한' 등 효능을 부풀리는 최상급/배타적 표현은 약기법 위반이므로 절대 금지한다. 반드시 '高い保湿感' (높은 보습감), '優れた保湿力' (뛰어난 보습력), 'しっかりとした' (탄탄한) 등의 완화된 표현으로 대체하여 번역해라.

[SPECIAL RULE - PRODUCT INFO NOTICE (TABLE)]
이미지 파일명에 '상품정보고시' 또는 '04' 또는 '07'이 포함된 상품 정보 고시 표 이미지의 경우 아래의 지침을 100% 준수해라:
1. 표 속의 모든 항목명(제품명, 기능성, 제조국, 전성분 등)과 그 결과값들은 단 한 글자의 한글도 남겨두지 말고 100% 일본어로 완전하게 번역해라. (예: '대한민국' ➔ '大韓民国', '(주)코스나인' ➔ '(株)コスナイン', '정제수' ➔ '水' 또는 '精製水' 등 전성분 전체를 일본어로 완벽히 번역할 것)
2. 표의 첫 번째 열 항목(헤더 칸) 중 '기능성화장품 심사필유무' 혹은 '기능성화장품의 심사 필 유무'는 한글을 완전히 지우고, 일본 고시 표준인 '区分' (구분)으로 완전히 교체하여 번역해라. 절대 한글 '심사 필 유무'를 남겨두지 마라.
3. 위 '区分' (구분) 항목의 결과값(오른쪽 칸)은 한국 승인 사실을 포함한 일체의 부연설명 없이, 반드시 일본 고시 표준인 '化粧品' 단독으로만 번역하여 표기해라. 단독으로 '美白'이나 'しわ改善' 또는 '2重機能性'을 적지 마라. (일본 화장품법상 외국 정부의 승인/추천을 광고하는 표현은 전면 금지된다)
4. '주요특장(主要特長)' 혹은 '주요특징(主な特徴)' 항목의 번역 결과값은 주름(しわ) 개선이나 '스킨벌크업', '빌드업', 'DEJ' 같은 단어를 직접 사용하는 대신, 안전하게 'オートファジー技術を活用し、肌にハリとツヤを与え、健やかに整えます。' (오토파지 기술을 활용하여 피부에 탄력과 윤기를 부여하고 건강하게 정돈합니다)로 번역해라.
5. '사용방법(使用方法)' 항목의 '흡수시켜 줍니다'는 약기법상 침투 한계를 명시하기 위해 'なじませます' (밀착시킵니다) 또는 '角質層まで浸透させます' (각질층까지 침투시킵니다)로 번역해라. 절대 단독으로 '吸収させます' (흡수시킵니다)로 번역하지 마라.
6. 표의 왼쪽 헤더 칸에 있는 한글 '제조국'은 100% '製造国'으로 번역하고, '소비자상담실'은 100% '消費者相談室'로 번역해라. 절대 표 내에 한글 '제조국', '상담실' 등이 섞이거나 잔류해서는 안 된다.
"""

print("[START] JP_Ecom_Visual_Localizer_V5 일괄 렌더링 배치 엔진 가동...")
print(f"[INFO] 타겟 스캔 폴더: {source_dir}")
print(f"[INFO] 결과 저장 폴더: {target_dir}")

# 번역 대상 이미지 스캔 (GIF 포맷 포함)
targets = [f for f in os.listdir(source_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.jfif', '.gif'))]

if not targets:
    print(f"[WARNING] '{source_dir}' 폴더에 처리할 이미지가 없습니다.")
    sys.exit(0)

for filename in targets:
    if 'JP' in filename:
        print(f"  -> [SKIP] 이미 일본어화된 파일(JP 태그): {filename}")
        continue
        
    # [V5 규칙 강제]: 상세정보 고시 파일 및 표 결과물은 이미지 번역기 루프에서 전격 제외
    if '상세정보안내' in filename or '상품정보제공고시' in filename or '상품상세정보' in filename or filename.endswith('.txt'):
        print(f"  -> [SKIP] 고시정보 텍스트 및 관련 표 파일은 번역기 제외: {filename}")
        continue
        
    in_path = os.path.join(source_dir, filename)
    # 원본이 GIF 등 타 확장자이더라도 결과물은 반드시 .png 파일명으로 통일
    out_name = f"{os.path.splitext(filename)[0]}_JP_Surgical_v5.png"
    out_path = os.path.join(target_dir, out_name)
    
    # if os.path.exists(out_path):
    #     print(f"  -> [SKIP] 렌더링 완료본이 타겟 폴더에 이미 존재함: {filename}")
    #     continue
        
    print(f"\n[RENDER] 변환 시작: {filename}")
    
    try:
        original_image = Image.open(in_path)
        original_image.load()
    except Exception as e:
        print(f"  -> [ERROR] 이미지 로드 실패: {e}")
        continue

    try:
        response = client.models.generate_content(
            model=MODEL_ID,
            contents=[prompt, original_image]
        )
        
        img_saved = False
        if hasattr(response, 'candidates'):
            for cand in response.candidates:
                if hasattr(cand, 'content') and hasattr(cand.content, 'parts'):
                    for part in cand.content.parts:
                        if hasattr(part, 'inline_data') and part.inline_data:
                            img = Image.open(io.BytesIO(part.inline_data.data))
                            # [V5 정밀 리사이징 보완]: AI 모델에 의한 픽셀 크기 변형을 원천 차단하고 원본 가로세로 픽셀을 100% 보존
                            img = img.resize(original_image.size, Image.Resampling.LANCZOS)
                            img.save(out_path, format="PNG")
                            img_saved = True
                            break
                        elif hasattr(part, 'image') and part.image:
                            img = Image.open(io.BytesIO(part.image.image_bytes))
                            # [V5 정밀 리사이징 보완]: AI 모델에 의한 픽셀 크기 변형을 원천 차단하고 원본 가로세로 픽셀을 100% 보존
                            img = img.resize(original_image.size, Image.Resampling.LANCZOS)
                            img.save(out_path, format="PNG")
                            img_saved = True
                            break
                            
        if img_saved:
            print(f"  -> [SUCCESS] {out_name} 저장 완료!")
        else:
            print("  -> [FAILED] API 호출 성공이나 이미지 데이터 반환 안됨.")
            if response.text:
                print(f"텍스트 반환값: {response.text[:200]}")
            
    except Exception as e:
        print(f"  -> [ERROR] API 호출 실패: {e}")
    
    time.sleep(6)

print("\n[FINISH] JP_Ecom_Visual_Localizer_V5 이미지 번역 완료!")
