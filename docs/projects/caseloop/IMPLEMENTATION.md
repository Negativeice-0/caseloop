# CaseLoop implementation notes

## Runtime baseline

- Python 3.11 in `backend\venv`; backend dependencies are pinned in `backend\requirements.txt`.
- React 18, TypeScript, and Vite in `frontend`; use `frontend\package-lock.json` with `npm ci` when installing dependencies.
- SQLAlchemy is the ORM for both SQLite and PostgreSQL. SQLite remains the local/offline option; PostgreSQL is the shared-database option.

## Start locally on Windows

Run the API from the backend folder:

```powershell
Set-Location C:\Users\Admin\Documents\caseloop\backend
.\venv\Scripts\python.exe -m uvicorn app.main:app --reload --port 8000
```

In another terminal:

```powershell
Set-Location C:\Users\Admin\Documents\caseloop\frontend
npm.cmd run dev -- --host 127.0.0.1
```

Open `http://127.0.0.1:5173`. API health is `http://127.0.0.1:8000/`; interactive API docs are at `http://127.0.0.1:8000/docs`.

The backend defaults to SQLite at `backend\caseloop.db` when launched from the backend folder. To use the Docker PostgreSQL database instead, start Compose from the project root and use its `api` service. Local SQLite records are not automatically copied to PostgreSQL.

## First administrator

The first administrator is provisioned by CLI; there is no default shared credential. From a backend terminal:

```powershell
.\venv\Scripts\python.exe -m app.create_admin
```

For the Docker database, run from the project root:

```powershell
docker compose exec api python -m app.create_admin
```

The command prompts for email, name, and a password of at least 12 characters. It may also promote/reset an existing account. Admin-created accounts receive a generated one-time temporary password and must change it after signing in.

The public **Launch Dispatch Portal** registration creates an active responder account and signs the user in. Registration accepts only name, email, and a password of at least 12 characters; clients cannot choose a role. Coordinator and admin accounts remain admin-provisioned. Public registration has no email verification or automated abuse throttling yet, so add the organization's required verification/invite policy and abuse protection before public production deployment.

The standard sign-in is at `/`; the dedicated administrator entry is `/admin`. Both use the same email/password session system, and the admin entry rejects non-admin roles server-side. On mobile, use **More** for Intake, Reports, Profile, Admin (when authorized), and Sign out. If signed in as a responder, sign out and use an administrator account to see management/report tools. Run the first-admin CLI command above; it can also promote/reset an existing account when you enter its email.

The normal profile shows password change as a linked expandable security card; accounts with a required temporary-password change still have to complete it before entering the workspace.

## Operational reports

Reports & Analysis is available from the main navigation to coordinators and admins, with an additional shortcut inside Admin. Date and team filters apply consistently to the summary, preview, and Word download. Select one of three formats: Operational (full breakdowns and records), Situation (priority and location coverage with open assignments), or Field Action Brief (active responses by location and open assignments). The preview and DOCX export use the same selected format and filters.

Analysis includes priority, category, source-channel, and recorded-location breakdowns, missing-location counts, active responses that have no assignment, and weekly response/assignment creation counts. The preview opens by default so the trend and coverage are visible without an extra click. With no date filter, the weekly trend contains the latest eight calendar weeks; an explicit long date range is capped to 26 calendar-week buckets for the trend only. Summary counts still use the full selected date range. The response exposes the trend window so the UI and DOCX identify its actual dates. Location coverage groups the submitted location text; it is not a map or geocoded measurement.

The report endpoints accept optional `from_date`, `to_date`, and `team_id` query parameters; `/api/reports/preview` and `/api/reports/word` also accept `template=operational`, `template=situation`, or `template=field`. For example, `/api/reports/preview?from_date=2026-11-01&to_date=2026-11-30&team_id=2&template=situation`. Directly created response records are labeled `coordinator`; approved intake records retain their `manual` or `whatsapp` source. Unreviewed intake drafts are excluded. Counts and breakdowns are deterministic; they are not AI-generated assessments.

To add bundled synthetic response examples, run `.\venv\Scripts\python.exe -m app.seed` only after an active admin or coordinator exists. It does not create placeholder users or login credentials. In Docker use `docker compose exec api python -m app.seed`.

## Docker PostgreSQL

Docker Desktop must be running. From the project root:

```powershell
Copy-Item .env.example .env
# Replace the example local-only database password.
docker compose up --build -d
docker compose exec api python -m app.create_admin
```

Compose starts PostgreSQL and the API; run Vite separately to see the UI. Database files persist in the `postgres_data` named volume. `docker compose down` preserves data; `docker compose down -v` deletes it. PostgreSQL binds to localhost only.

Fresh databases are initialized from the current SQLAlchemy models and stamped at Alembic head. Existing databases with migration history are upgraded at startup. The early migration chain originated from an older SQLite schema; review and test every revision against both database engines before production use.

## Tests and build

```powershell
Set-Location C:\Users\Admin\Documents\caseloop\backend
.\venv\Scripts\python.exe -m pytest -q

Set-Location C:\Users\Admin\Documents\caseloop\frontend
npm.cmd run build
```

## WhatsApp

`POST /api/webhooks/whatsapp` verifies `X-Hub-Signature-256`, deduplicates messages, and saves supported inbound text as pending drafts. `GET /api/webhooks/whatsapp` implements Meta's verification challenge. Configure `WHATSAPP_VERIFY_TOKEN` and `WHATSAPP_APP_SECRET` as environment secrets and provide a publicly reachable HTTPS callback before testing with Meta's test number. Never use real beneficiary information for setup.

See the [deployment guide](../../deployment/DEPLOYMENT.md) for step-by-step provider setup and remaining hosting gates.

After review, a coordinator can publish a response and optionally select a team to create its assignment in the same transaction. The response and assignment then appear in the Response Register, Teams & Assignments, and global operational timeline. Unreviewed messages never appear as published responses.

## Security and deployment caveats

Passwords are PBKDF2-HMAC-SHA256 hashed; session tokens are opaque, stored hashed server-side, expiring, and revocable. Mutating cookie-authenticated requests require a CSRF header. Backend routes enforce role permissions. The app still needs independent security/privacy review, login abuse protection, monitored operations, tested backups/restores, and organizational authorization before public or real-data deployment.

There is no configured Git remote, hosting account, public deployment, or live WhatsApp connection. Local Docker is not cloud hosting.
