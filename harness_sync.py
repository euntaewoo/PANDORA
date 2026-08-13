# ============================================================
# harness_sync.py - Antigravity 하네스 자동 동기화 스크립트
# GitHub PANDORA 리포지토리 → 로컬 C드라이브 자동 업데이트
# 실행: python harness_sync.py
# 자동화: Windows 작업 스케줄러에 등록하여 주기적 실행
# ============================================================

import os
import sys
import json
import shutil
import urllib.request
import urllib.error
from datetime import datetime

# ── 설정 ────────────────────────────────────────────────────
GITHUB_OWNER = "euntaewoo"
GITHUB_REPO  = "PANDORA"
GITHUB_BRANCH = "main"
LOCAL_AGENT_ROOT = r"C:\Users\euntaewoo\.agent"
LOG_FILE = r"C:\Users\euntaewoo\.agent\harness\sync_log.txt"

# 동기화할 파일 목록 (GitHub 경로 → 로컬 경로)
SYNC_FILES = {
    ".agent/harness/HARNESS.md":                    r"harness\HARNESS.md",
    ".agent/harness/verification/lint_rules.md":     r"harness\verification\lint_rules.md",
    ".agent/harness/verification/test_checklist.md": r"harness\verification\test_checklist.md",
    ".agent/rules/global_rules.md":                  r"rules\global_rules.md",
}

RAW_BASE = f"https://raw.githubusercontent.com/{GITHUB_OWNER}/{GITHUB_REPO}/{GITHUB_BRANCH}"
# ────────────────────────────────────────────────────────────

def log(msg):
    """동기화 로그 기록"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] {msg}"
    print(line)
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line + "\n")

def fetch_file(github_path):
    """GitHub에서 파일 내용 가져오기"""
    url = f"{RAW_BASE}/{github_path}"
    try:
        with urllib.request.urlopen(url, timeout=10) as resp:
            return resp.read().decode("utf-8")
    except urllib.error.HTTPError as e:
        log(f"  ❌ HTTP 오류 {e.code}: {github_path}")
        return None
    except Exception as e:
        log(f"  ❌ 연결 오류: {e}")
        return None

def sync():
    """메인 동기화 실행"""
    log("====== 하네스 동기화 시작 ======")
    updated = 0
    skipped = 0
    failed  = 0

    for github_path, local_rel in SYNC_FILES.items():
        local_path = os.path.join(LOCAL_AGENT_ROOT, local_rel)
        log(f"→ 확인 중: {github_path}")

        # GitHub에서 최신 내용 가져오기
        new_content = fetch_file(github_path)
        if new_content is None:
            failed += 1
            continue

        # 로컬 파일과 비교
        if os.path.exists(local_path):
            with open(local_path, "r", encoding="utf-8") as f:
                old_content = f.read()
            if old_content == new_content:
                log(f"  ✅ 최신 상태 (변경 없음)")
                skipped += 1
                continue

        # 업데이트 적용
        os.makedirs(os.path.dirname(local_path), exist_ok=True)
        with open(local_path, "w", encoding="utf-8") as f:
            f.write(new_content)
        log(f"  🔄 업데이트 완료: {local_path}")
        updated += 1

    log(f"====== 동기화 완료: 업데이트 {updated}개 / 최신 {skipped}개 / 실패 {failed}개 ======")
    return updated, skipped, failed

if __name__ == "__main__":
    updated, skipped, failed = sync()
    if failed > 0:
        sys.exit(1)  # 작업 스케줄러에서 실패 감지용
