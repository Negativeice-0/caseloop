# CaseLoop Control Center

## Principles

Evidence > Assumptions

Artifacts > Script Output

Verified Facts > Search Hits

Authoritative Sources > Repository Scans

Discover Once → Consume Many Times

Normalize Before Analysis

Verification Before Conclusions

Small Safe Changes > Large Risky Changes

---

## Daily Startup

Read:

1. fullstack\session-summary.md
2. snrld\verification-audit.md

Do NOT:

- reread rawshell output
- reread old audit phases
- restart discovery
- trust PASS without evidence

---

## Source Hierarchy

1. Verified artifacts
2. Session summary
3. Authoritative source files
4. Generated evidence
5. Documentation

Documentation never overrides code.

---

## Recovery If Lost

Open:

- backend-route-inventory.json
- authorization-normalized.json
- latest matrix summary

Reconstruct from artifacts.

Never reconstruct from memory.

---

## Learning Workflow

Major milestone completed
→ Run Learn Prompt
→ Update knowledge base
→ Update portfolio/brag sheet if relevant

Do NOT run Learn Prompt every session.

Only after significant discoveries or completed checkpoints.

---

## Long-Term Goal

Understand systems well enough to:

- safely modify them
- verify them
- explain them
- hand them over
- rebuild understanding from artifacts

NB: chkpnt14-plan.md was the first master prompt.

Ask ai how do the scripts work, which lines do i need to change such that
I expect master to generate rawshell --excluding other docs (like readme or projects) or packages (like venv, node, etc). I then expect SessionSummary to have fixed variables that when chnaged apply to the current phase -- for example i am now in phase 7 after running below -- fullstack should be generated with summary and snr lead with verification <C:\Users\Admin\Documents\caseloop\backend\app\api\__init__.py>, when ready learn prompt should also have variables so i can switch learning tragtes or deposit target for example when done with checklist i will want to go through all my chkpnts.