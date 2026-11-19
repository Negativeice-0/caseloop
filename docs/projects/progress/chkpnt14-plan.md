# Baby steps

Don't rush, today it took you few hours to figure all this out, tomorrow it might take seconds. Plus later you can upload checkpoints for final readme darft. 

FYI: ensure docker engine is up first -> docker compose up -d db ->
backend server launch -> start frontend

## The complete one-step-at-a-time mega prompt
Text

Copy

---

Act as my senior CaseLoop engineering guide.

I will work in separate sessions. In each session, guide me through exactly ONE checklist step, from preparation through completion. Do not give me the next step until I provide a result and explicitly say the current step is complete.

For every step:
1. State the objective.
2. Explain why it matters.
3. State what must not be changed.
4. Give exact PowerShell 5.1 commands or exact file edits.
5. Tell me the expected output.
6. Tell me how to interpret success, failure, or ambiguity.
7. Ask me to paste the result.
8. Help me verify the result.
9. Give me a concise completion summary.
10. Stop and wait.

Maintain this order:
1. Confirm backend and frontend health.
2. Capture Git status and create a safety branch.
3. Record baseline backend tests and frontend build.
4. Inventory all frontend routes and navigation entries.
5. Inventory backend routes and authorization dependencies.
6. Build the role-permission matrix.
7. Build the frontend-to-backend-to-database connection map.
8. Audit README and every linked documentation file.
9. Remove redundant navigation entries only.
10. Test desktop, mobile, direct URLs, and role visibility.
11. Decide whether old routes should remain, redirect, or be deleted.
12. Remove unused imports and dead route wiring.
13. Refactor components only where responsibility is clearly mixed.
14. Audit Python, Docker, frontend, and configuration file references.
15. Produce deletion candidates; never delete automatically.
16. Add or improve backend authorization tests.
17. Add or improve frontend navigation and role tests.
18. Run final tests, build, and manual smoke checks.
19. Update README with verified current behavior.
20. Create the final session summary and logbook entry.

Rules:
- Never invent filenames or routes; search first.
- Never treat hidden UI as security.
- Backend authorization is authoritative.
- Never delete code without evidence, a reversible Git commit, and passing tests.
- Use synthetic data only.
- Keep each session focused and non-overwhelming.
- Begin with Step 1 only.

---

That checklist is not an everyday task list or just for interns. It is a structured process for auditing, securing, refactoring, and preparing a full-stack application for release.

Use the full checklist when:

- Taking over an unfamiliar codebase

- Preparing a major refactor or release

- Reviewing authentication, permissions, or routes

- Cleaning up a risky or poorly documented project

For normal daily work, use only the relevant parts: check Git status, run tests, make a focused change, review the diff, and verify the result.

Main message: the checklist is useful, but it should be applied proportionally—not followed mechanically for every small change.

## What “check Git, test, change, review, verify” means
For a developer, the normal loop is:

- Check Git status — know which branch you are on and whether existing changes might be affected.

- Understand the task — identify the user problem and the expected result.

- Make a focused change — avoid mixing unrelated cleanup with the requested work.

- Run relevant tests — use fast targeted tests first, then broader tests when the change is risky.

- Review the diff — look for accidental edits, missing tests, security problems, and unclear code.

- Verify the result — test the actual user path, including error cases and permissions where relevant.

Record the outcome — explain what changed, what was tested, and any remaining risk.

---

GitHub pull requests are appropriate for preserving discussion, checks, diffs, and review history; small changes are easier to review and reverse. 
GitHub Docs
GitHub Docs
+1
---

## Final session summary
A user comment usually moves through a filtered, collaborative process:

Text

Copy
User comment
   ↓
Support team / feedback system
   ↓
Product team groups similar comments
   ↓
Product manager identifies the underlying problem
   ↓
User researchers + data scientists investigate
   ↓
Data engineers prepare reliable data and measurement tools
   ↓
Designers create possible solutions
   ↓
Security, legal, accessibility, and infrastructure teams review risks
   ↓
Developers build the feature or fix
   ↓
Testers, engineers, and automated systems test it
   ↓
Small release or experiment with selected users
   ↓
Data team measures results
   ↓
Product leaders decide: improve, expand, pause, or remove
   ↓
Support and users provide new feedback
   ↺
The cycle continues
How one large building stays busy
A large company does not have every employee working on the same user comment. Different teams work on different products, problems, and company responsibilities:

---

Copy
Many user comments
   ├── Search problems → Search teams
   ├── Video problems → YouTube teams
   ├── Cloud requests → Cloud teams
   ├── Security reports → Security teams
   ├── App issues → Android or application teams
   ├── Data questions → Analysts and data scientists
   ├── Infrastructure needs → Reliability and platform teams
   ├── Business needs → Sales, finance, legal, and operations
   └── Employee needs → Recruiting, facilities, and internal IT
The data team does not simply read comments and hand finished data to developers. It may analyze comments, user behavior, experiments, surveys, and system performance. Developers, product managers, designers, researchers, and data specialists usually work together from the beginning.

Main idea: users provide feedback, product teams prioritize it, research and data teams investigate it, designers plan solutions, engineers build them, testing teams verify them, and the company measures whether the result actually helps. Not every request becomes a feature, and not every employee is involved in every request.
---