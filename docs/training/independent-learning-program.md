# CaseLoop Independent, Offline-First Learning Program

## Purpose and finish line

This program is for learning to maintain CaseLoop yourself, not for memorizing frameworks. By the end, you should be able to:

- start the app and explain how a feature moves from React to FastAPI to the database;
- make a small change from a written requirement, test it, diagnose a failure, and explain the result;
- understand the data, authorization, privacy, and retry risks in an inbound WhatsApp webhook;
- rehearse a deployment and its recovery steps before putting anything on the public internet.

Plan for **12 weeks, four 60- to 90-minute sessions each week**. Take longer when needed. A week is complete when you can demonstrate its evidence without someone else driving your keyboard.

Senior engineers do use AI and other tools for more than boilerplate: they use them to explore options, draft tests, and speed up debugging. The professional difference is that they can evaluate the output, identify what is unsafe or wrong, and remain responsible for the system. The aim here is independent judgment, not refusing useful tools forever.

## Working rules

1. **Use synthetic data only.** Do not put beneficiary, personnel, or operational information into exercises, screenshots, logs, or AI prompts.
2. **Predict before running.** Write down what you expect a command, test, or code path to do; compare the result with your prediction.
3. **Make the smallest reversible change.** State the behavior first, change one thing, run the narrowest relevant check, then check for regressions.
4. **Read the failure before changing code.** Capture the exact error, identify the layer that produced it, and form a testable hypothesis.
5. **Do not run destructive database or Git commands by guesswork.** In particular, `docker compose down -v` removes the Compose database volume.
6. **Keep secrets local.** Never commit `.env`, API keys, passwords, database files, or provider credentials.
7. **Keep a daily logbook.** Record the task, what you learned, evidence, and the next question. Make a short weekly summary. This supports the [Student Attachment Guide](./Student%20Attachment%20Guide%20updated%20Jan2021.pdf)'s logbook and reporting expectations.

### The AI-last routine

For each exercise, work through this ladder in order:

1. Try it yourself for 20 minutes and write down what you know.
2. Search the local code, tests, error output, and installed documentation.
3. Reduce the problem to one reproducible example and ask a person for a **hint**, not a solution.
4. If still blocked, ask AI for one explanation or alternative, with no secrets or real data.
5. Verify every suggestion against the source, tests, and observed behavior. Rewrite the explanation in your own words.

During Weeks 1–2, do not ask AI to generate code. During Weeks 3–6, use it only after your own attempt, mainly for hints or test ideas. From Week 7 onward, use it as a reviewer or accelerator when useful, but never merge or deploy code you cannot explain.

## Prepare a safe local practice environment

The repo has Windows PowerShell instructions in the [project README](../../README.md). The local SQLite mode is the default practice path; it does not require Docker, a cloud account, or WhatsApp credentials. The existing virtual environment and frontend dependencies can be used without installing packages when they are present.

Open two PowerShell terminals:

```powershell
# Terminal 1: API with local SQLite
Set-Location C:\Users\Admin\Documents\caseloop\backend
.\venv\Scripts\python.exe -m uvicorn app.main:app --reload --port 8000
```

```powershell
# Terminal 2: React development server
Set-Location C:\Users\Admin\Documents\caseloop\frontend
npm.cmd run dev -- --host 127.0.0.1
```

Open `http://127.0.0.1:5173`. In another terminal, check the API and run the existing backend tests:

```powershell
Invoke-RestMethod http://127.0.0.1:8000/

Set-Location C:\Users\Admin\Documents\caseloop\backend
.\venv\Scripts\python.exe -m pytest -q
```

For frontend type-check/build verification:

```powershell
Set-Location C:\Users\Admin\Documents\caseloop\frontend
npm.cmd run build
```

These are local, repeatable checks. They do not prove that the app is production-ready.

### Protect the existing work before practicing

First run `git status --short --branch`. If Git reports that this workspace is not a repository, do not assume there is a usable commit history. Before initializing Git or changing project files, make a **separate, reviewed practice copy** and ensure local databases, `venv`, `node_modules`, `.env`, and secrets are excluded. Never use a broad cleanup command to make a copy or “reset” the workspace. Keep a list of the files you changed and check each diff before considering a change complete.

Use the existing test database fixtures and synthetic seed data where possible. Do not experiment on `backend/caseloop.db`, `backend/sql_app.db`, or a Docker volume you care about. The Compose database is separate from the local SQLite database.

## Twelve-week curriculum

Each week's suggested four sessions are: **learn and inspect**, **guided practice**, **independent change**, and **explain/review**. Adjust the pace to your schedule.

| Week | Focus and hands-on work | Evidence to keep |
| --- | --- | --- |
| 1 | PowerShell basics, paths, processes, ports, environment variables, and starting/stopping the local app. Follow the README's commands; distinguish the API terminal from the Vite terminal. | A one-page startup and shutdown checklist; explain what the API health response says about the database mode. |
| 2 | Read the architecture and trace one response through `frontend/src/App.tsx`, `frontend/src/services/api.ts`, a component, a FastAPI route, schema/model, and database. Draw arrows; do not edit yet. | A hand-drawn or Mermaid data-flow diagram and a plain-language explanation of each layer. |
| 3 | Python fundamentals through the API: functions, types, dictionaries, exceptions, imports, request validation, and response codes. Read one route in `backend/app/api/` and its related test. | A short route walkthrough, including valid input, invalid input, and expected status codes. |
| 4 | TypeScript and React: components, props, state, events, effects, async calls, and rendering. Trace one view from `frontend/src/App.tsx` into its feature component. | A small UI change in a practice copy, plus a clear before/after description and build result. |
| 5 | Relational data: tables, keys, constraints, transactions, SQLAlchemy models, and migrations. Compare SQLite's local role with PostgreSQL's shared-database role. | A diagram of one entity and its relationships; a safe, synthetic query and its expected result. |
| 6 | Testing: assertions, fixtures, isolated tests, API integration tests, and frontend build/type checks. Start with `backend/tests/`; improve a missing behavior test before changing implementation. | A focused test that fails for the intended reason before a fix and passes after it, with the full relevant command recorded. |
| 7 | Debugging: reproduce, observe, localize, hypothesize, test, fix, regress. Practice with a harmless UI/API mismatch in a separate branch or copy. Use browser console/network tools, API logs, and Python tracebacks. | A bug report with exact reproduction steps, evidence, root cause, fix, and regression test. |
| 8 | Authentication and authorization: sessions, roles, CSRF, password handling, read-only response access, and admin-only changes. Follow a request to the server-side permission check; hiding a button is not authorization. | An access matrix for responder, coordinator, and administrator, plus tests for allowed and denied actions. |
| 9 | WhatsApp webhook, **offline simulation only**: inspect `backend/app/api/webhooks.py`; understand verification challenge, HMAC signature, JSON parsing, payload limits, deduplication, and pending intake review. Use synthetic payloads and tests; do not scrape WhatsApp Web or existing groups. | A test matrix for valid, invalid-signature, malformed, repeated, unsupported, and oversized messages; show that accepted messages remain pending until human review. |
| 10 | Docker and database operations: images, containers, networks, volumes, health checks, environment configuration, logs, restart behavior, and backup/restore concepts. Practice only with disposable synthetic data. | A service diagram and a verified recovery rehearsal; explicitly identify which commands preserve and which can delete the database. |
| 11 | Hosting rehearsal: compare a simple hosted frontend/API plus managed database with self-hosted Docker Compose on a VM. Practice build settings, environment variables, HTTPS, CORS, cookies, database migrations, backups, logs, and rollback on paper or in a non-public test environment. | A deployment runbook and cost/security checklist. Identify which resources are billable and why budget alerts are not hard spending caps. |
| 12 | Capstone: make one small, user-requested change from requirement through test and documentation. Then demonstrate the flow, show a failure you diagnosed, and explain deployment and WhatsApp limitations. | A short demo, test output, reviewed change list, updated documentation, and a reflection on what you can now do without AI. |

### How to approach WhatsApp and hosting

The first WhatsApp milestone is **not** connecting a real group. Learn and test the signed webhook locally with fictional payloads first. A real provider test later needs a Meta developer setup, an approved test recipient, secrets stored outside source control, and a public HTTPS callback. Meta's official WhatsApp APIs do not grant arbitrary access to existing group history. Any permitted group-based design requires checking current Meta eligibility, participant notice/consent, and organizational approval. The [deployment guide](../deployment/DEPLOYMENT.md#whatsapp-cloud-api-test) describes the current test path and limitations.

For hosting, learn local Docker Compose first, then choose deliberately:

- **Simpler first internet demo:** separate frontend and API hosting plus managed PostgreSQL. Fewer server-administration tasks, but it does not preserve a Dockerized PostgreSQL server in the cloud. Free plans, sleep limits, storage, and retention can change.
- **Keep the full Docker stack:** a self-managed VM can run the app and PostgreSQL containers, but you own Linux updates, firewall, TLS, backups, restore drills, monitoring, and incident response. Oracle Always Free availability and price rules are not a guaranteed zero-cost cap.

The existing [hosting guide](../deployment/DEPLOYMENT.md#hosting-guide-live-demo-with-render-and-neon) documents the simpler demo route and its limitations. Do not deploy operational or personal data as a learning exercise. Use synthetic data, enable cost alerts, check provider billing settings, and do not assume a “free tier” prevents charges.

For a step-by-step local PostgreSQL, Oracle, credential-rotation, and Meta webhook rehearsal, use the [Oracle and WhatsApp learning runbook](../deployment/oracle-whatsapp-learning-runbook.md).

For a focused two-week sequence of hands-on sessions and evidence, use the [CaseLoop Two-Week Learning Lab](./caseloop-two-week-learning-lab.md).

## A repeatable 75-minute session

1. **5 min — goal:** write one observable result, e.g. “A repeated webhook message is not stored twice.”
2. **10 min — predict:** identify likely files and expected behavior before reading the implementation.
3. **20 min — inspect:** read the relevant code and tests; note unknown terms.
4. **20 min — do:** make one small change or add a test in a safe practice copy.
5. **15 min — verify:** run the narrow test, inspect the diff, then run the relevant broader check.
6. **5 min — teach back:** explain the change aloud without reading generated explanations.

If stuck, do not randomly edit. Record: **expected / actual / evidence / hypothesis / next experiment**. Change one variable at a time.

## Testing and debugging checklist

Before calling a change done, answer:

- Can I reproduce the original behavior or bug reliably?
- Did I add or update a test for the requirement or regression?
- Did I run the smallest relevant test and inspect its output?
- Did I inspect the final diff and check for unrelated edits or secrets?
- Did I consider invalid input, duplicate requests, permissions, and offline/service failure where relevant?
- Can I explain why the test would fail if the fix were removed?

When a test fails, preserve the first useful traceback/assertion. Check which process and database the test uses, whether the API/frontend are actually running, and whether an environment variable points somewhere unexpected. Do not “fix” a failing test by weakening or deleting its assertion without understanding the behavior.

## Progress scorecard

At the end of each week, rate each from 0 to 2:

- **0:** cannot do it yet;
- **1:** can do it with notes or a hint;
- **2:** can do and explain it independently.

Score: start/stop local app; trace UI-to-database flow; interpret an API error; write/run a focused test; inspect a change; explain role permissions; explain webhook signature and deduplication; explain database persistence and recovery; identify hosting costs and risks. Repeat a week when an essential safety or data-integrity item is below 2. Progress is demonstrated by evidence, not by finishing the calendar.

## Start now: first offline session

1. Open the two terminals and start the API and frontend using the commands above.
2. Call `http://127.0.0.1:8000/` and write down the app status, database mode, and what you think “offline-first” means here.
3. Open `http://127.0.0.1:8000/docs` and identify one read-only endpoint and one state-changing endpoint. Do not submit a real record.
4. In a separate note, trace the first page from `frontend/src/App.tsx` to `frontend/src/services/api.ts`; find the backend health route in `backend/app/main.py`.
5. Run `pytest` and the frontend build. Record the command, result, and any warnings exactly.
6. Finish by explaining in your own words which pieces work without internet and which later tasks (Meta webhooks, provider hosting) require it.

Do not add a dummy production endpoint merely to practice typing. Use tests and a separate practice copy for the first code change, so the exercise builds safe habits as well as muscle memory.
