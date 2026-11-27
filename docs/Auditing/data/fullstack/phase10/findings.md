# Findings

- Files Parsed: 4
- Lines Parsed: 80
- PASS Indicators: 0
- FAIL Indicators: 0
- WARNING Indicators: 0
- ERROR Indicators: 0

## Runtime Visibility Results

- Responder desktop and mobile views expose only Register, Assignments, Timeline, and Profile; Intake, Reports, and Admin are absent.
- Coordinator desktop and mobile views expose Intake and Reports but not Admin.
- Administrator desktop and mobile views expose all seven navigation tabs.
- Direct `/admin` access is rejected for both responder and coordinator accounts and renders the administrator workspace for an administrator.
- Evidence: `rawshell/phase10/ui-role-test-results.txt`; source cross-checks: `rawshell/phase10/visibility-source-evidence.txt` and `rawshell/phase10/entry-point-evidence.txt`.
- No frontend test script or component test files were present; these are manual browser checks against an isolated SQLite database.
