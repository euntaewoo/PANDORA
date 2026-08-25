# ✅ 코드 검증 규칙 (Lint Rules)

에이전트가 코드 작성 후 EVALUATOR에게 제출하기 전 반드시 통과해야 할 체크리스트.

## Python 코드 검증
```
□ python -m py_compile <파일명>.py  → 문법 오류 없음
□ API 키 하드코딩 여부 스캔
□ 모든 파일 경로 os.path.exists() 로 실제 존재 확인
□ try-except 예외 처리 존재 여부
□ 실행 결과 output/ 폴더에 저장 확인
```

## 공통 검증
```
□ 하드코딩된 경로 없음 (변수 사용)
□ 민감 정보 노출 없음
□ 주석 한국어 작성 여부
□ 파일 복제(중복) 없음
```

## PASS 기준
- 위 항목 100% 통과 시만 EVALUATOR가 PASS 판정
- 하나라도 실패 시 CREW에게 피드백 후 재작업
