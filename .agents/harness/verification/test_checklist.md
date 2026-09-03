# 📋 결과물 최종 체크리스트 (Output Verification Checklist)

## 이미지 번역/로컬라이징 작업
```
□ output/ 폴더에 결과 이미지 파일 존재
□ 원본(input/) 파일 손상 없음
□ 이미지 가로세로 비율 원본과 동일
□ 일본어 금지 의학 용어 미포함 (治療, 改善, 再生)
□ 법적 면책 문구 자동 삽입 확인
□ 파일명 형식: 원본명_JP_Surgical_v3.png
```

## 코드/스크립트 작업
```
□ 실제 실행 테스트 완료 (에러 없음)
□ API 호출 성공 여부 확인
□ 결과 파일 정상 생성 여부
□ 로그에 오류 메시지 없음
```

## 최종 보고 형식
```
✅ 완료: [작업명]
📁 결과물: [경로]
⚠️ 특이사항: [있을 경우만]
```

## [PRE-EXPORT-INTEGRITY-VERIFICATION-LOCK] 결과물 내보내기 전 사전 무결성 검증 및 리포트 선-출력 강제
1. **[HARD STOP] 결과물 파일 내보내기 전 무조건 사전 검증 실행**:
   - 결과물 파일(.png, .html, .docx, .txt, .md 등)을 생성·저장·보고하기 전, 데이터 무결성과 포맷 규격을 체크하는 검증 함수(`pre_export_integrity_check`) 및 린터를 무조건 실행해야 합니다.
2. **[REPORT-FIRST] 데이터 무결성 요약 리포트 선-출력 의무화**:
   - 에이전트는 최종 결과물이나 파일 링크를 사용자에게 제시하기 전, 반드시 응답 상단에 `### 📋 [DATA-INTEGRITY-SUMMARY-REPORT]` 요약 리포트 표(포맷 무결성, 콩글리시/금지어 0건 여부, 수치 일치성, 4종 파일 생성 여부)를 먼저 출력하여 검증 결과를 입증해야 합니다. 이 리포트 출력이 누락된 답변은 즉시 무효로 간주합니다.
3. **[GLOBAL-COMPLIANCE] 영미권/글로벌 뷰티 표준 명칭 강제**:
   - 무자극/저자극: 한국 성적서 0.00 직역투 배제 -> `Hypoallergenic & Dermatologist-tested for sensitive skin` 표준 강제.
   - 피부톤 케어: 'Tone Care / Dark Spot & Tone Care' 콩글리시 배제 -> `Dark Spot & Discoloration Defense` 표준 강제.
