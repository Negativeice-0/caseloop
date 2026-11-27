# Findings

- Files Parsed: 1
- Lines Parsed: 47
- Text mentions (not test outcomes): PASS 0; FAIL 0; WARNING 0; ERROR 0; TODO 0

## Manual Review Outcome

Status: COMPLETE — FOLLOW-UP REQUIRED

- The focused authorization selection ran 9 tests: 8 passed and 1 failed.
- Session/CSRF enforcement, admin sign-in and password lifecycle, responder assignment restrictions, logout, and public-registration role constraints passed.
- `test_demo_seed_requires_an_existing_coordinator_or_admin` failed because `seed_database()` returned without the expected `RuntimeError`; its captured output shows the seed operation created default accounts. This is a mismatch between the test's expected guard and the current seeding behavior.
- Follow up by reconciling the seed guard and test expectations before treating demo seeding as protected. No application code was changed in this audit phase.
- Evidence: `rawshell/phase16/backend-authorization-pytest.txt` (email addresses redacted).
