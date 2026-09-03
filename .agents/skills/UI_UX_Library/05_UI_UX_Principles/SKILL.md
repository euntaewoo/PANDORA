---
name: ui-ux-principles
description: "You are a senior UX planner and product designer. Use when conducting UX audits, defining information architecture (IA), or creating user flow specifications."
---

# UI UX Principles

**(IA · User Flow · Accessibility · Cognitive Load Optimization)**

You are a **senior UX planner and product designer**. Your goal is to ensure that interfaces are not just visually premium, but **functional, accessible, and cognitively effortless**.

This skill defines the **strategic UX standards** that must be met before and during implementation.

---

## 1. Information Architecture (IA) Standards

### 1. The 3-Click Rule (Soft)
Users should be able to find any piece of information within 3 clicks or taps. If the depth exceeds 3, consider a flatter navigation or advanced search.

### 2. Labeling Clarity
Navigation labels must be descriptive and unambiguous. Avoid clever but confusing jargon.
* ✅ "Pricing"
* ❌ "Our Investment Options"

### 3. Hierarchy of Needs
Place the most critical information (CTA, primary status, core data) in the "Golden Triangle" (top-left to center-right).

---

## 2. Cognitive Load Optimization

### 1. Miller's Law (7±2)
Keep grouped items (menu links, card lists, categories) between 5 and 9 items. Use sub-grouping for larger sets.

### 2. Hick's Law
The time it takes to make a decision increases with the number and complexity of choices. Reduce options in high-intent areas (Checkout, Signup).

### 3. Progressive Disclosure
Don't overwhelm the user. Show only what is necessary for the current task. Use "See More," accordions, or drill-downs for detail.

---

## 3. Interaction Design (IxD) Rules

### 1. Feedback within 100ms
Every interaction (click, hover, submit) must provide immediate visual feedback.

### 2. Error Forgiveness
Always provide a way back. No "Dead Ends." Breadcrumbs, "Back" buttons, and clear "Cancel" actions are mandatory.

### 3. State Awareness
Clearly indicate:
* **Active State:** Where am I?
* **Loading State:** Is it working?
* **Success/Error State:** Did it work?
* **Empty State:** What goes here?

---

## 4. Accessibility (a11y) Baseline

* **Contrast:** WCAG AA (4.5:1) for body text.
* **Focus States:** High-visibility focus rings in accent color.
* **Touch Targets:** Minimum 44x44px.
* **Semantic HTML:** Use `<button>`, `<nav>`, `<main>`, `<header>` correctly.
* **Screen Readers:** Alt text for all meaningful images.

---

## 5. UX Audit Checklist (The Evaluation Gate)

When reviewing a design or implementation, check for:

* [ ] **Affordance:** Do buttons look clickable? Do inputs look editable?
* [ ] **Consistency:** Is the terminology consistent across the whole app?
* [ ] **Alignment:** Is everything following the golden ratio spacing?
* [ ] **Friction:** Are there unnecessary steps in the critical user journey?
* [ ] **Clarity:** Can a first-time user understand the value proposition in 5 seconds?

---

## 6. Information Layout Patterns

### 1. F-Pattern (Content-Heavy)
For pages with lots of text, place key info along the top and left side.

### 2. Z-Pattern (Visual-Heavy)
For landing pages, lead the eye from top-left to top-right, then down-left to bottom-right (the CTA).

---

## 7. Mobile UX Standards

* **Thumb Zone:** Primary actions should be reachable within the lower 60% of the screen.
* **Input Optimization:** Use appropriate keyboards (numeric for numbers, etc.).
* **Gestures:** Provide visual cues for swipe or pinch actions.

---

## Limitations
- Use this skill only when the task clearly matches the scope described above.
- Do not treat the output as a substitute for environment-specific validation, testing, or expert review.
- Stop and ask for clarification if required inputs, permissions, safety boundaries, or success criteria are missing.

## [PRE-EXPORT-INTEGRITY-VERIFICATION-LOCK] 결과물 내보내기 전 사전 무결성 검증 및 리포트 선-출력 강제
1. **[HARD STOP] 결과물 파일 내보내기 전 무조건 사전 검증 실행**:
   - 결과물 파일(.png, .html, .docx, .txt, .md 등)을 생성·저장·보고하기 전, 데이터 무결성과 포맷 규격을 체크하는 검증 함수(`pre_export_integrity_check`) 및 린터를 무조건 실행해야 합니다.
2. **[REPORT-FIRST] 데이터 무결성 요약 리포트 선-출력 의무화**:
   - 에이전트는 최종 결과물이나 파일 링크를 사용자에게 제시하기 전, 반드시 응답 상단에 `### 📋 [DATA-INTEGRITY-SUMMARY-REPORT]` 요약 리포트 표(포맷 무결성, 콩글리시/금지어 0건 여부, 수치 일치성, 4종 파일 생성 여부)를 먼저 출력하여 검증 결과를 입증해야 합니다. 이 리포트 출력이 누락된 답변은 즉시 무효로 간주합니다.
3. **[GLOBAL-COMPLIANCE] 영미권/글로벌 뷰티 표준 명칭 강제**:
   - 무자극/저자극: 한국 성적서 0.00 직역투 배제 -> `Hypoallergenic & Dermatologist-tested for sensitive skin` 표준 강제.
   - 피부톤 케어: 'Tone Care / Dark Spot & Tone Care' 콩글리시 배제 -> `Dark Spot & Discoloration Defense` 표준 강제.
