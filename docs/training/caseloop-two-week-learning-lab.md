# CaseLoop Two-Week Learning Lab

This is a focused, learn-by-doing route through the existing CaseLoop app. The goal is not to add features for their own sake. The goal is to run the app, trace one workflow, test it, make one useful change yourself, and explain what happened.

Allow about 60-90 minutes per session. A day is a suggested session, not a deadline. Use synthetic data only. Do not practise destructive actions on a database you care about or experiment on a public production deployment.

## How we will work

- **You drive.** You type and run the commands, inspect the files, and write the test or code.
- **Tutor mode by default.** Ask for a hint first. I will not write the solution unless you explicitly ask.
- **Attempt before assistance.** Spend 15-20 minutes reading, predicting, and trying. Then consult project code, tests, official documentation, or Google. Use AI if it is useful, not because you must.
- **Keep evidence.** Save the command, result, a short explanation, and the next question. The [Student Attachment Guide](./Student%20Attachment%20Guide%20updated%20Jan2021.pdf) emphasizes recording work and learning in the logbook; record only what you actually did.
- **Protect the app.** Do not add practice-only features to the main product without a user need. A useful exercise can live on a private local branch and be deleted after you learn from it.

## Two confusing phrases, in plain language

### “Rotate the credential at its issuer”

It means **make the old password/key stop working where it was created**, then update the app to use a replacement:

- CaseLoop account password: reset it through CaseLoop.
- PostgreSQL password: change it in PostgreSQL, then update the API's connection settings.
- Meta verify token: replace it in both the Meta webhook configuration and the API settings.
- Meta app secret: regenerate it in Meta, then update the API settings.
- OCI SSH key: add a new public key, prove it works, then remove the old one.

Copying a password into `.env` does not revoke the old password. A comment is ignored by Compose and does not configure anything. Never write secrets into comments or a logbook.

Checkpoint 10 was previously identified as containing credentials. Before making a GitHub repository, redact those values in the local file or exclude that checkpoint from the initial repository, then rotate the credentials at their issuers. If a secret was ever pushed, rotate it even if the file is later edited.

### “Add Git's folder to your Windows user Path”

`Path` is a list of folders Windows searches when you type a command. Git is installed at `C:\Program Files\Git\cmd\git.exe`, but PowerShell did not know to search that folder.

For the current PowerShell window only:

```powershell
$env:Path = "C:\Program Files\Git\cmd;" + $env:Path
git --version
```

For future windows, open Start and search **Edit environment variables for your account**. Select the user `Path` entry, choose **Edit**, then **New**, enter the folder `C:\Program Files\Git\cmd` (the folder, not `git.exe`), save, and reopen PowerShell or VS Code. Alternatively, open Git Bash from the Start menu and use Git there. Do not mix Windows Git and WSL Git on the same working files while learning.

## Session 1 — Check the tools and run Docker

Before starting, close any old API or Vite terminal you may have left running. In PowerShell:

```powershell
Set-Location C:\Users\Admin\Documents\caseloop
docker version
docker compose version
Test-Path .env
```

Write down what each command tells you. `docker version` should show both a client and a server; the server means the Docker engine is running. If it cannot connect, start Docker Desktop and retry. The Desktop window is a way to manage/start the engine; once the engine is running, Compose commands can be run in the terminal.

If `.env` does not exist, copy `.env.example` to `.env`, edit the copy, and replace the placeholder password with a new **local-only** value. Never overwrite an existing `.env` blindly, and never paste its contents into chat.

```powershell
Copy-Item .env.example .env
docker compose up --build -d
docker compose ps
docker compose logs --tail=60 db api
Invoke-RestMethod http://localhost:8000/
```

The last command should report `database: postgresql`. If Docker says port 8000 is already in use, stop a separately running local API with Ctrl+C and retry. If the health response says `sqlite`, check which server is answering on port 8000.

Start the frontend in a second terminal:

```powershell
Set-Location C:\Users\Admin\Documents\caseloop\frontend
npm.cmd run dev -- --host 127.0.0.1
```

Open `http://127.0.0.1:5173`, sign in with a synthetic local account, and confirm the page loads. At the end, stop the frontend with Ctrl+C and stop Compose without deleting its data:

```powershell
Set-Location C:\Users\Admin\Documents\caseloop
docker compose down
```

Never use `docker compose down -v` on data you want to keep.

**Evidence:** Docker client/server result; API health response; what process runs the UI, API, and database.

## Session 2 — Trace the database connection

Read these files in order; do not edit them:

1. `backend/app/core/config.py`
2. `backend/app/core/database.py`
3. `backend/app/api/webhooks.py`
4. `backend/app/main.py`
5. `frontend/src/services/api.ts`
6. `frontend/src/features/workflow/WorkflowViews.tsx`

Draw this path in your own words:

```text
Compose environment -> backend settings -> SQLAlchemy engine
-> get_db session -> FastAPI route -> JSON response
-> frontend API client -> Intake Review screen
```

Check your explanation against these facts: Compose gives the API container a PostgreSQL URL using host `db`; local backend startup defaults to SQLite unless its environment overrides that; React chooses an API URL but never chooses the database.

**Evidence:** a small diagram and one sentence describing the purpose of each file.

## Session 3 — Learn what the existing tests actually prove

Read `backend/tests/conftest.py` and the webhook-related tests in `backend/tests/test_assignments.py`. Notice that the assignment tests override `get_db` with their own in-memory SQLite database. They do not use the running Compose PostgreSQL database.

Run the focused tests safely:

```powershell
Set-Location C:\Users\Admin\Documents\caseloop\backend
$env:DATABASE_URL = "sqlite://"
.\venv\Scripts\python.exe -m pytest tests\test_assignments.py -k "meta_webhook or whatsapp_intake" -q
```

For each selected test, write: input, expected status/result, actual status/result, and what database fixture it uses. Then run the full backend suite and frontend build:

```powershell
.\venv\Scripts\python.exe -m pytest -q
Set-Location C:\Users\Admin\Documents\caseloop\frontend
npm.cmd run build
```

**Evidence:** exact commands and pass/fail results. A failure is useful evidence; do not edit an assertion just to make it pass.

## Session 4 — Explain the webhook without memorizing it

In `backend/app/api/webhooks.py`, trace the POST handler in order. Describe what each stage protects:

1. configuration check;
2. maximum request size;
3. HMAC signature check over the original request bytes;
4. JSON parsing and supported text-message extraction;
5. duplicate message-ID check;
6. saving a pending intake draft.

Then trace where the draft appears: the intake API lists pending records; the Intake Review UI loads them; coordinator approval creates the response, optional assignment, and timeline events. A real webhook does not send anything directly to React; React fetches data from the API.

**Evidence:** a 6-8 step request-flow note and answers to “what happens to an invalid signature?” and “why is a valid message still pending?”

## Session 5 — Add a test before changing application code

Pick one uncovered boundary behavior from the webhook, such as a too-large request or a supported event containing no text messages. Before editing, state the expected response in a sentence. Add one focused test beside the existing webhook tests, using synthetic data and test-only secrets. Run just that test.

The current implementation already has request-size and supported-message handling, so a new test may pass immediately. That is still useful: it turns an assumption into executable evidence. If it fails, do not guess at a fix. Record the actual result, find the relevant branch, and ask for a hint only after you have a hypothesis.

**Evidence:** test name, expected/actual result, and the code path that caused it.

## Session 6 — Make one useful UI change yourself

A real webhook can arrive while the Intake Review page is already open. The current UI loads drafts on page open and after its own actions, but it does not push new webhook events to the screen. A small **Refresh drafts** control would be useful; it is not pointless decoration.

Before coding, write acceptance criteria:

- a coordinator can request a fresh list without reloading the whole app;
- the list shows a newly arrived pending draft;
- an API failure is visible to the user;
- the refresh control does not publish or approve anything.

Find the existing `refresh` function in `IntakeReview`, make the smallest change you can, and run `npm.cmd run build`. Manually verify it in the browser with synthetic records. Do not ask AI to write the component first. If you get stuck, ask for a hint about the next small step.

**Evidence:** acceptance criteria, changed behavior, build result, and a short explanation of how the button gets fresh data.

## Session 7 — Practise Git locally, not on GitHub yet

First address the Checkpoint 10 credential issue described above. Do not stage or publish it unsanitized. Once Git is available, check whether the workspace is already a repository:

```powershell
Set-Location C:\Users\Admin\Documents\caseloop
git status --short --branch
```

If Git says this is not a repository, do not rush to `git add .`. Sanitize/exclude credential-bearing documents and review `.gitignore` first. The root `.gitignore` excludes `.env`, local databases, `venv`, and `node_modules`; it does not automatically exclude every project document.

In a safe local repository, practise:

```text
git status
git diff
git add <one-reviewed-file>
git diff --cached
git commit -m "Describe one focused change"
git log --oneline
```

The learning goal is to see exactly what changed and be able to return to a known state—not to push quickly. Create a GitHub remote only after the secret review is complete.

**Evidence:** a reviewed diff, one focused local commit, and what the commit contains.

## Session 8 — Recheck Docker PostgreSQL and persistence

Start Docker Desktop if needed, run `docker compose up --build -d`, and confirm the API health response again. Create or edit only synthetic data. Stop with `docker compose down`, start again, and observe whether the named volume retained the data.

Explain the difference:

- the Compose file and `.env` configure services and connections;
- the named PostgreSQL volume stores database contents;
- neither the connection URL nor GitHub is a backup.

**Evidence:** health response before/after restart and a statement about what persists.

## Session 9 — Rehearse the full workflow locally

Run the existing signed-webhook test, then use the UI:

1. Confirm a valid synthetic webhook payload creates a pending intake.
2. Confirm a repeated message ID is counted as a duplicate, not a second draft.
3. Open or refresh Intake Review and inspect the source text.
4. Approve the draft as a coordinator; optionally assign a synthetic team.
5. Confirm the response appears in the read-only register and the assignment/timeline are linked.
6. Sign in as a responder in a separate browser and confirm the responder can view, but not approve, coordinator intake.

The existing tests exercise most of the backend path. Your browser exercise proves the separate frontend/API wiring.

**Evidence:** a hand-drawn data path, test output, and a short screen recording or screenshots using synthetic data only.

## Session 10 — Decide whether you are ready for Oracle and Meta

Do not treat deployment as a single button. Check the gates:

- Git and secret review complete; exposed credentials rotated and old values removed from the initial commit.
- Local Docker Compose API reports PostgreSQL; the UI works.
- Existing webhook tests pass; you can explain signature verification and deduplication.
- You accept that Oracle budget alerts are soft alerts, not a guaranteed cost cap.
- You have a domain/DNS plan for a valid HTTPS certificate; a domain may cost money.
- You understand current Compose lacks a production frontend and HTTPS proxy, so those must be built and tested before the Meta callback is public.
- PostgreSQL will stay private; only the HTTPS proxy will be publicly reachable.
- Meta developer app and approved test recipient are available; only synthetic messages will be sent.

If all gates are satisfied, follow the [Oracle and WhatsApp runbook](../deployment/oracle-whatsapp-learning-runbook.md) for the cloud rehearsal. The first live provider message should be a direct message to Meta's official test number, arrive as a pending draft, and require explicit coordinator approval. Do not scrape existing groups.

## A light LeetCode routine

LeetCode is useful for interview practice, but it is not a measure of whether you can be a full-stack developer. Add 15-20 minutes of original algorithm practice three times a week, after the app exercise:

1. Given a list of webhook IDs, determine which IDs repeat.
2. Count synthetic assignments by status using a dictionary/map.
3. Group synthetic reports by branch tag and count each branch.
4. Explain the time and space cost of your solution.

Try first without AI. Use language documentation and small examples. Ask for a hint before a solution, then reimplement it yourself. Keep the exercise separate from production code unless it solves a real product need.

## End-of-session learning record

Keep it factual and short:

```text
Goal:
What I read or changed:
Command/test and result:
What I can now explain:
What confused me:
Next experiment:
```

Do not claim hours of coding, a successful deployment, or a live webhook if you did not perform those things. One accurate observation and one unresolved question are enough for a useful learning record.
