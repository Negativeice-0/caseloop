Since you've identified that the previous Phase 4 runs were fundamentally flawed because they inventoried vendor code instead of application code, I would not archive more copies.

A senior engineer would treat those runs as invalid evidence due to scoping defects, preserve them for audit history, and record the reason once.

I'd use a prompt like this in a fresh session:

CaseLoop Audit Recovery Prompt

Act as my senior CaseLoop engineering guide.

We have identified a systemic defect in previous audit inventories.

The defect was:

Repository-wide searches included:

- node_modules
- vendor code
- generated code
- compiled artifacts

instead of beginning from:

- repository boundaries
- application boundaries
- authoritative entry points
- registrations
- wiring


As a result, previous inventories produced large volumes of low-value evidence and failed verification.

Before any new inventory work:

Review existing audit artifacts.

Identify which phase directories were affected by this defect.

Do NOT delete any existing evidence.

Do NOT create additional archive folders.

Create a recovery report documenting:

affected phases
root cause
impacted artifacts
evidence quality issues
whether regeneration is required

Mark affected inventories as:

Invalid Due To Scoping Defect


when warranted by evidence.

Generate replacement audit scripts using:
Boundary
→ Entry Point
→ Configuration
→ Registration
→ Wiring
→ Evidence


instead of repository-wide searches.

Preserve historical evidence but prevent invalid inventories from being treated as authoritative.

Produce a remediation plan identifying:

artifacts to keep
artifacts to supersede
artifacts requiring regeneration

Use the CaseLoop Senior Engineering Standard.

Do not advance beyond recovery analysis.

Do not regenerate inventories yet.

Do not delete evidence.

Wait for verification before proposing corrections.

---

Even better, if you want to physically clean up the audit tree later, have the recovery phase produce a single file such as:

```text
docs/auditing/audit-recovery-report.md


that says:

Phase 4
Status: Invalid

Reason:
Repository-wide inventory searched node_modules and vendor code.

Superseded By:
Phase4-Rebuilt

Original Evidence:
Retained for audit history.


That gives you one authoritative explanation instead of accumulating:

phase4
phase4-failed
phase4-archive
phase4-retry
phase4-fixed
phase4-final
phase4-final-final


which is exactly the kind of audit-sprawl senior engineers try to avoid.