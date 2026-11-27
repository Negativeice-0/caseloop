# Verification

Status: COMPLETE - FOLLOW-UP REQUIRED
Evidence Files: 1
Evidence Lines: 47
This generator reports evidence-derived facts; manual review is still required.

- Evidence files discovered: 1
- Evidence successfully parsed
- Keyword extraction completed
- Pytest pass summary present: True (evidence: backend-authorization-pytest.txt)
- Focused authorization test process exited successfully: False (evidence: backend-authorization-pytest.txt)
- Manifest detected

## Manual Review

- Review status: COMPLETE — FOLLOW-UP REQUIRED.
- 8 of 9 selected tests passed. `test_demo_seed_requires_an_existing_coordinator_or_admin` failed because the expected guard exception was not raised.
- Captured email addresses are redacted in the saved test output.
- No application code was changed. Reconcile the test expectation with the seed behavior before considering demo-seed authorization verified.
