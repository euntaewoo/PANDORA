# 🚀 JP_Ecom_Visual_Localizer_V3 (Master Surgical Edition)

본 프로젝트는 일본 이커머스 상세페이지 로컬라이징의 **'완전 자동화 및 초정밀 품질'**을 목표로 합니다.

## 🌟 핵심 원칙 (Zero-Distortion)

- **비율 유지**: 원본 이미지의 가로세로 비율을 1픽셀의 오차도 없이 100% 유지합니다. (1:1 강제 변환 금지)
- **서지컬 소거**: 디자인과 텍스처를 훼손하지 않는 0px 패딩 소거 방식을 사용합니다.

## 📂 구조

- `src/`: 엔진 코어 (Nano Banana V3 Master)
- `workflows/`: 에이전트 및 시스템 지침서
- `input/`: 원본 이미지 (KR)
- `output_v3/`: 결과물 (JP)

## 🛠 핵심 사양

- **모델**: gemini-3.1-flash-image-preview (Unified Engine)
- **폰트**: Noto Sans JP (Regular/Bold)
- **현지화**: 일본 약기법(薬機法) 자동 검수 및 관용구 치환

## 📝 관리 이력

- 2026-04-28: V3 Master Surgical 엔진 배포 및 비율 검증 로직 추가
