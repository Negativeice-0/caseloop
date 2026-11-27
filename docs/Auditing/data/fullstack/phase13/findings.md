# Findings

- Files Parsed: 2
- Lines Parsed: 24
- Text mentions (not test outcomes): PASS 0; FAIL 0; WARNING 0; ERROR 0; TODO 0

## Responsibility Review

- `WorkflowViews.tsx` is 718 lines and contains the separate `IntakeReview`, `TimelineView`, and `ReportsView` components. This is the strongest candidate for a future feature-file split, with no behavior change intended.
- `AdminControl.tsx` is 384 lines and renders multiple administration sections. Consider extracting section views only if focused tests can preserve the current navigation and access behavior.
- `App.tsx` (166 lines) handles session state, role gates, backend health, and tab selection. It currently acts as the application orchestrator; no immediate refactor is recommended.
- `MainLayout.tsx` (274 lines) renders desktop and mobile navigation. Their role behavior passed Phase 10 checks; keep parity if this is later extracted.
- No refactor was performed. Evidence: `rawshell/phase13/component-metrics.txt` and `rawshell/phase13/component-boundaries.txt`.
