import os
import tempfile
import re
import json
from google.cloud import vision
from google import genai
from playwright.sync_api import sync_playwright

MODEL_PRO = "gemini-3.1-pro-preview"

def load_credentials():
    """Vertex AI 서비스 계정 키 및 API 키를 탐색하여 genai.Client 및 vision.ImageAnnotatorClient를 초기화합니다."""
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    if not os.path.exists(os.path.join(project_root, "00_공통자료")):
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "multilingual_text_in_image_translatio_agy_sdk"))

    key_candidates = [
        os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"),
        r"C:\Users\euntaewoo\Desktop\multilingual_text_in_image_translatio_agy_sdk\00_공통자료\APIs_KEY\인증키_및_계정\김차장_vertex api_key\vertex_ai_auth_key.json",
        os.path.join(project_root, "00_공통자료", "APIs_KEY", "인증키_및_계정", "김차장_vertex api_key", "vertex_ai_auth_key.json"),
        os.path.join(project_root, "일본어", "vertex_service_account.json"),
    ]

    gemini_client = None
    vision_client = None

    for kpath in key_candidates:
        if kpath and os.path.exists(kpath) and kpath.endswith(".json"):
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = kpath
            try:
                with open(kpath, "r", encoding="utf-8") as f:
                    key_data = json.load(f)
                    project_id = key_data.get("project_id")
                gemini_client = genai.Client(vertexai=True, project=project_id, location="global")
                vision_client = vision.ImageAnnotatorClient()
                print(f"[AUTH SUCCESS] Vertex AI & Vision API Client 연결 완료 (Model: {MODEL_PRO}, Location: global, Project: {project_id})")
                return gemini_client, vision_client
            except Exception as e:
                print(f"[AUTH ERROR] Google Cloud API 연결 실패 ({kpath}): {e}")

    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key:
        try:
            if api_key.startswith("AQ."):
                gemini_client = genai.Client(vertexai=True, api_key=api_key)
            else:
                gemini_client = genai.Client(api_key=api_key)
            return gemini_client, None
        except Exception as e:
            print(f"[AUTH ERROR] Gemini API Key 연결 실패: {e}")

    print("[AUTH INFO] 외부 API 인증키 없음 -> 룰베이스 Fallback 모드로 동작합니다.")
    return None, None

def extract_notice_items_from_image(image_path: str, vision_client=None, gemini_client=None) -> list:
    """[이미지/패키지 사진 모드] Google Cloud Vision API로 깨알 텍스트(OCR) 추출 후 Gemini 3.1 Pro로 구조화"""
    if not os.path.exists(image_path):
        print(f"[ERROR] 이미지 파일이 존재하지 않습니다: {image_path}")
        return []

    print(f"  👁️ [GCP Vision API] 이미지 고정밀 문서 OCR(DOCUMENT_TEXT_DETECTION) 가동: {os.path.basename(image_path)}", flush=True)
    raw_ocr_text = ""
    if vision_client:
        try:
            with open(image_path, "rb") as f:
                content = f.read()
            v_img = vision.Image(content=content)
            resp = vision_client.document_text_detection(image=v_img)
            raw_ocr_text = resp.full_text_annotation.text if resp.full_text_annotation else ""
            print(f"  ✅ [GCP Vision OCR 완료] 총 {len(raw_ocr_text)} 글자 추출 성공", flush=True)
        except Exception as e:
            print(f"  ⚠️ [Vision OCR 오류] {e}")

    if not raw_ocr_text and not gemini_client:
        return []

    print(f"  🧠 [Gemini 3.1 Pro] OCR 스캔 텍스트 KCID/INCI 표준 교정 및 테이블 구조화 중...", flush=True)
    struct_prompt = f"""
당신은 대한민국 화장품 표시광고법, 대한화장품협회(KCID) 및 미국화장품협회(INCI) 표준을 완벽히 숙지한 화장품 고시정보(Notice Table) 데이터 구조화 전문가입니다.
아래의 OCR 스캔 텍스트를 분석하여, 상품정보제공고시 표준 테이블 구조의 JSON 데이터로 복원하십시오.

[정제 및 구조화 규칙]
1. 라벨(label)과 본문(value)을 정확히 분리하십시오.
2. 전성분 및 주의사항의 오타를 KCID 공인 표준 명칭에 맞춰 자동 교정하십시오. (특히 '메타크라일레이트' -> '메타크릴레이트', 중복 텍스트 제거)
3. 10자 이상의 긴 복합 전성분명에는 소프트 하이픈 `&shy;`을 결합 위치에 삽입하십시오. (예: `아이소프로필&shy;아이소스테아레이트`)
4. 주의사항의 문맥 어절은 `&nbsp;`로 결속하십시오. ('붉은&nbsp;반점', '이상&nbsp;증상이나', '부작용이&nbsp;있는&nbsp;경우', '전문의&nbsp;등과', '상담할&nbsp;것')
5. 법인 약칭 `(주)`가 분리되지 않도록 보존하십시오.
6. 1), 2), 3), (가), (나) 순번 앞에는 줄바꿈(`<br>`)을 삽입하십시오.

[OCR 원본 텍스트]
{raw_ocr_text}

[출력 형식]
반드시 순수 JSON 배열만 반환:
[
  {{"label": "내용물의 용량", "value": "25ml"}},
  ...
]
"""
    try:
        resp = gemini_client.models.generate_content(
            model=MODEL_PRO,
            contents=[struct_prompt]
        )
        resp_text = resp.text.strip()
        if resp_text.startswith("```json"): resp_text = resp_text[7:]
        if resp_text.startswith("```"): resp_text = resp_text[3:]
        if resp_text.endswith("```"): resp_text = resp_text[:-3]
        parsed_items = json.loads(resp_text.strip())
        print(f"  🎉 [복원 완료] 총 {len(parsed_items)}개 고시 항목 테이블 복원 성공")
        return parsed_items
    except Exception as e:
        print(f"  ❌ [Gemini 구조화 오류] {e}")
        return []

def enrich_notice_items_with_gemini(items: list, client: genai.Client = None) -> list:
    """Gemini 3.1 Pro를 호출하여 화장품 고시정보의 형태소 분석, 스마트 하이픈(&shy;), 의미단위 결속(&nbsp;)을 지능적으로 수행"""
    if not client:
        return items

    prompt = f"""
당신은 대한민국 화장품 표시광고법, 대한화장품협회(KCID) 성분사전 및 미국화장품협회(INCI) 표준을 완벽히 숙지한 화장품 고시정보(Notice Table) 타이포그래피 & 형태소 분석 전문가입니다.
전성분 분석 시 반드시 대한민국 식약처 및 대한화장품협회(KCID) 공인 표준 성분명을 100% 엄격히 준수하며, 오타(예: '메타크라일레이트' -> '메타크릴레이트') 및 중복 표기는 표준 정규명으로 교정하십시오.
아래의 한국어 화장품 고시정보 JSON 데이터를 분석하여 웹 렌더링에 최적화된 HTML 텍스트로 정제하십시오.

[정제 및 타이포그래피 필수 규칙]
1. [전성분 스마트 하이픈 (&shy;)]
   - 10자 이상의 긴 복합 화학성분명(예: '아이소프로필아이소스테아레이트', '하이드로제네이티드폴리아이소부텐', '암모늄아크릴로일다이메틸타우레이트/베헤네스-25메타크릴레이트크로스폴리머' 등)은 가로폭 초과 시 줄 끝에서 자연스럽게 하이픈(-)으로 분할될 수 있도록 유의미한 형태소 결합 지점에 소프트 하이픈 `&shy;`을 삽입하십시오. (예: `아이소프로필&shy;아이소스테아레이트`, `암모늄아크릴로일&shy;다이메틸타우레이트/&shy;베헤네스-25&shy;메타크릴레이트크로스폴리머`)
2. [의미단위 결속 (&nbsp;)]
   - '주의사항' 및 본문에서 문맥상 줄바꿈으로 끊어지면 안 되는 핵심 어절('붉은&nbsp;반점', '이상&nbsp;증상이나', '부작용이&nbsp;있는&nbsp;경우', '전문의&nbsp;등과', '상담할&nbsp;것', '피해서&nbsp;보관할&nbsp;것' 등) 사이에 `&nbsp;`를 삽입하십시오.
3. [라벨 2줄 균형 (<br>)]
   - '기능성 화장품 심사 필 유무' -> `기능성 화장품<br>심사 필 유무`
   - '화장품제조업자/책임판매업자' -> `화장품제조업자/<br>책임판매업자`
   - '사용기한 또는 개봉 후 사용기간' -> `사용기한 또는<br>개봉 후 사용기간`
4. [법인 약칭 (주) 보존]
   - 제조업자/책임판매업자의 `(주)` 법인명 약칭이 혼자 다음 줄로 떨어지지 않도록 앞 회사명과 밀착하십시오.
5. [목차 순번 개행]
   - 1), 2), 3), (가), (나) 등 순번 앞에는 줄바꿈(`<br>`)을 삽입하십시오.

[입력 데이터]
{json.dumps(items, ensure_ascii=False, indent=2)}

[출력 형식]
반드시 유효한 JSON 형식(리스트 형태: [{{"label": "...", "value": "..."}}])만 반환하십시오.
"""
    try:
        resp = client.models.generate_content(
            model=MODEL_PRO,
            contents=[prompt]
        )
        resp_text = resp.text.strip()
        if resp_text.startswith("```json"):
            resp_text = resp_text[7:]
        if resp_text.startswith("```"):
            resp_text = resp_text[3:]
        if resp_text.endswith("```"):
            resp_text = resp_text[:-3]
        enriched_items = json.loads(resp_text.strip())
        print(f"[GEMINI 3.1 PRO] 고시정보 지능형 타이포그래피 정제 완료 ({len(enriched_items)}개 항목)")
        return enriched_items
    except Exception as e:
        print(f"[GEMINI 3.1 PRO] AI 정제 중 예외 발생, 룰베이스 Fallback 진행: {e}")
        return items

def _smart_ingredient_hyphenator_fallback(text: str) -> str:
    """[룰베이스 Fallback] 주요 긴 복합 전성분명에 소프트 하이픈(&shy;) 주입 및 KCID 표준 교정"""
    morphemes = [
        ('아이소프로필아이소스테아레이트', '아이소프로필&shy;아이소스테아레이트'),
        ('하이드로제네이티드폴리아이소부텐', '하이드로제네이티드&shy;폴리아이소부텐'),
        ('암모늄아크릴로일다이메틸타우레이트/베헤네스-25메타크라일레이트크로스폴리머타크릴레이트크로스폴리머',
         '암모늄아크릴로일&shy;다이메틸타우레이트/&shy;베헤네스-25&shy;메타크릴레이트크로스폴리머'),
        ('암모늄아크릴로일다이메틸타우레이트/베헤네스-25메타크릴레이트크로스폴리머',
         '암모늄아크릴로일&shy;다이메틸타우레이트/&shy;베헤네스-25&shy;메타크릴레이트크로스폴리머'),
        ('하이드로제네이티드레시틴', '하이드로제네이티드&shy;레시틴'),
        ('글리세릴카프릴레이트', '글리세릴&shy;카프릴레이트'),
        ('토코페릴아세테이트', '토코페릴&shy;아세테이트'),
        ('하이알루로닉애씨드', '하이알루로닉&shy;애씨드'),
        ('다이소듐이디티에이', '다이소듐&shy;이디티에이'),
        ('솔비탄아이소스테아레이트', '솔비탄&shy;아이소스테아레이트'),
        ('에틸헥실글리세린', '에틸헥실&shy;글리세린'),
        ('지모뿌리추출물', '지모뿌리&shy;추출물')
    ]
    for orig, rep in morphemes:
        text = text.replace(orig, rep)
    return text

def _build_html(title: str, items: list, line_height: float = 1.45, cell_pad_v: int = 24) -> str:
    html_template = f"""
    <!DOCTYPE html>
    <html lang="ko">
    <head>
        <meta charset="UTF-8">
        <style>
            @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
            
            * {{ box-sizing: border-box; margin: 0; padding: 0; }}
            body {{
                margin: 0; padding: 0; background-color: white;
                font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, sans-serif;
                color: #222222; letter-spacing: -0.5px; line-height: {line_height}; width: 860px;
            }}
            #notice-container {{
                width: 860px;
                padding: 15px 20px 20px 20px;
                background-color: white;
            }}
            .title {{
                font-size: 60px; font-weight: bold; text-align: center; 
                color: #111111; margin-bottom: 30px; margin-top: 15px;
            }}
            table {{
                table-layout: fixed; width: 100%; border-collapse: collapse; 
                border-top: 3px solid #111111; border-bottom: 2px solid #333333;
            }}
            th, td {{ border-bottom: 1px solid #E0E0E0; }}
            th {{
                width: 295px; word-break: break-word; overflow-wrap: break-word; 
                font-size: 30px; font-weight: bold; background-color: #F8F9FA; 
                color: #333333; padding: {cell_pad_v}px 20px; border-right: 1px solid #EAEAEA; 
                text-align: left; vertical-align: middle;
            }}
            td {{
                font-size: 30px; font-weight: normal; background-color: #FFFFFF; 
                color: #222222; padding: {cell_pad_v}px 26px; vertical-align: middle; white-space: pre-line; 
                word-break: break-word; overflow-wrap: break-word;
            }}
            td.ingredients {{
                word-break: break-word;
                overflow-wrap: break-word;
                text-align: left;
                line-height: 1.55;
            }}
            tr:last-child th, tr:last-child td {{ border-bottom: none; }}
        </style>
    </head>
    <body>
        <div id="notice-container">
            <div class="title">{title}</div>
            <table>
                <tbody>
    """
    for item in items:
        lbl = item.get("label", "").replace(chr(92), "")
        val = item.get("value", "")
        val_str = str(val)
        
        # [KCID 공인 표준명 교정: 오타 및 중복 제거]
        val_str = re.sub(r'메타크라일레이트', '메타크릴레이트', val_str)
        val_str = re.sub(r'크로스폴리머(&shy;)?타크릴레이트크로스폴리머', '크로스폴리머', val_str)
        val_str = val_str.replace('암모늄아크릴로일다이메틸타우레이트/베헤네스-25메타크릴레이트크로스폴리머', '암모늄아크릴로일&shy;다이메틸타우레이트/&shy;베헤네스-25&shy;메타크릴레이트크로스폴리머')
        
        # 룰베이스 보정 결합
        if "성분" in lbl or "Ingredients" in lbl or "成分" in lbl:
            if "&shy;" not in val_str:
                val_str = _smart_ingredient_hyphenator_fallback(val_str)
                
        # 💡 기능성/특수용도 심사 항목의 괄호 효능 부가설명 앞 강제 줄바꿈 (KO/CN/TW/JP/EN 전 언어 공통)
        if any(k in lbl for k in ["기능성", "심사", "审查", "審查", "審査", "Functional", "Review", "含藥"]):
            val_str = re.sub(r'(?<!<br>)\s*([（(])', r'<br>\1', val_str)
        val_str = val_str.replace('식품의약품안전처 심사 필 완료 (', '식품의약품안전처 심사 필 완료<br>(')
        val_str = val_str.replace('식품의약품안전처 심사 필 무 (', '식품의약품안전처 심사 필 무<br>(')
        val_str = val_str.replace('붉은 반점', '붉은&nbsp;반점')
        val_str = val_str.replace('이상 증상', '이상&nbsp;증상')
        val_str = val_str.replace('부작용이 있는', '부작용이&nbsp;있는')
        val_str = val_str.replace('전문의 등과', '전문의&nbsp;등과')
        val_str = val_str.replace('상담할 것', '상담할&nbsp;것')
        val_str = val_str.replace('부위 등에는', '부위&nbsp;등에는')
        val_str = val_str.replace('자제할 것', '자제할&nbsp;것')
        val_str = val_str.replace('닿지 않는 곳에', '닿지&nbsp;않는&nbsp;곳에')
        val_str = val_str.replace('보관할 것', '보관할&nbsp;것')
        val_str = val_str.replace('피해서 보관', '피해서&nbsp;보관')
        val_str = val_str.replace('심사 필 완료', '심사&nbsp;필&nbsp;완료')
        val_str = val_str.replace('2중 기능성', '2중&nbsp;기능성')
        val_str = val_str.replace('분쟁해결 규정에', '분쟁해결&nbsp;규정에')
        val_str = val_str.replace('분쟁해결 기준에', '분쟁해결&nbsp;기준에')
        
        val = re.sub(r'(?<!^)(?<!<br>)(?<!\n)\s*(\d+\)|[①-⑳]|\([가나다라마바사아자차카타파하]\)|[㈎-㈛])', r'<br>\1', val_str)
        
        if "<br>" not in lbl:
            lbl = lbl.replace("개봉 후 사용기간", "개봉&nbsp;후&nbsp;사용기간")
            lbl = lbl.replace("기능성 화장품 심사 필 유무", "기능성 화장품<br>심사 필 유무")
            lbl = lbl.replace("소비자 상담 관련 전화번호", "소비자 상담 관련<br>전화번호")
            lbl = lbl.replace("소비자 상담 전화번호", "소비자 상담<br>전화번호")
            if "/" in lbl:
                lbl = lbl.replace(" / ", "/<br>").replace(" /", "/<br>").replace("/ ", "/<br>")
                if "/<br>" not in lbl:
                    lbl = lbl.replace("/", "/<br>")
            elif " 또는 " in lbl:
                lbl = lbl.replace(" 또는 ", " 또는<br>")
                
        if "성분" in lbl or "Ingredients" in lbl or "成分" in lbl:
            html_template += f'<tr><th>{lbl}</th><td class="ingredients">{val}</td></tr>'
        else:
            html_template += f'<tr><th>{lbl}</th><td>{val}</td></tr>'
        
    html_template += """
                </tbody>
            </table>
        </div>
    </body>
    </html>
    """
    return html_template

def _render_html_to_png(html_content: str, p, output_path: str) -> int:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".html", mode="w", encoding="utf-8") as f:
        f.write(html_content)
        temp_html = f.name
    
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 860, "height": 1000})
    page.goto(f"file:///{temp_html.replace(os.sep, '/')}")
    page.wait_for_load_state("networkidle")
    
    container = page.locator("#notice-container")
    container.screenshot(path=output_path)
    box = container.bounding_box()
    height = int(box["height"]) if box else 0
    
    browser.close()
    try:
        os.remove(temp_html)
    except:
        pass
    return height

def render_korean_notice_table(title: str, items_or_image_path, output_path: str, max_height: int = 2580, use_gemini: bool = True):
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    
    gemini_client, vision_client = (None, None)
    if use_gemini:
        gemini_client, vision_client = load_credentials()

    # 1. 입력이 이미지 파일 경로인 경우 (GCP Vision API OCR + Gemini 3.1 Pro 복원)
    if isinstance(items_or_image_path, str) and os.path.exists(items_or_image_path):
        print(f"[입력 감지: 이미지 파일] Vision OCR 및 Gemini 지능형 테이블 복원 모드 가동: {items_or_image_path}")
        items = extract_notice_items_from_image(items_or_image_path, vision_client, gemini_client)
        if not items:
            print("[ERROR] 이미지로부터 고시정보 복원에 실패하였습니다.")
            return
    else:
        items = items_or_image_path
        if use_gemini and gemini_client:
            items = enrich_notice_items_with_gemini(items, gemini_client)
        
    with sync_playwright() as p:
        # 1차 시도: 기본 행간(1.45, 패딩 24px)
        html_content = _build_html(title, items, line_height=1.45, cell_pad_v=24)
        height = _render_html_to_png(html_content, p, output_path)
        
        if height <= max_height:
            print(f"[✅ 성공] 고시표 1페이지 렌더링 완료: {output_path} (860 x {height}px)")
            return
            
        print(f"[⚠️ 알림] 기본 행간 세로 높이({height}px) 초과. 행간을 유동적으로 압축(Squeeze)하여 1페이지 내 수납을 재시도합니다.")
        
        # 2차 시도: 행간 압축(1.25, 패딩 22px)
        html_squeezed = _build_html(title, items, line_height=1.25, cell_pad_v=22)
        height_squeezed = _render_html_to_png(html_squeezed, p, output_path)
        
        if height_squeezed <= max_height:
            print(f"[✅ 성공] 행간 유동적 압축 렌더링 완료: {output_path} (860 x {height_squeezed}px)")
            return
            
        print(f"[⚠️ 알림] 행간 압축 후에도 세로 높이({height_squeezed}px)가 한도({max_height}px)를 초과하여 자동 2페이지 분할합니다.")
        
        # 3차 시도: 자동 2페이지 분할 (Part 1, Part 2)
        mid = len(items) // 2
        items_part1 = items[:mid]
        items_part2 = items[mid:]
        
        base_name, ext = os.path.splitext(output_path)
        out_part1 = f"{base_name}_Part1{ext}"
        out_part2 = f"{base_name}_Part2{ext}"
        
        html_p1 = _build_html(f"{title} (1/2)", items_part1, line_height=1.45, cell_pad_v=24)
        h1 = _render_html_to_png(html_p1, p, out_part1)
        
        html_p2 = _build_html(f"{title} (2/2)", items_part2, line_height=1.45, cell_pad_v=24)
        h2 = _render_html_to_png(html_p2, p, out_part2)
        
        print(f"[✅ 성공] 고시표 Part 1 저장 완료: {out_part1} (860 x {h1}px)")
        print(f"[✅ 성공] 고시표 Part 2 저장 완료: {out_part2} (860 x {h2}px)")
