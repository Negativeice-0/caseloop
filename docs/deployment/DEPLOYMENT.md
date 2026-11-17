# CaseLoop deployment and test guide

## Database architecture

SQLAlchemy remains the ORM and database access layer. SQLite is the local, offline, single-workstation option; PostgreSQL is the shared-database option. Docker Compose runs the API and PostgreSQL on this workstation and persists PostgreSQL data in the `postgres_data` named volume. Compose is not a cloud deployment.

The local SQLite database is not automatically copied to PostgreSQL. Do not point either mode at a live dataset as a migration test.

## Local development

From the project root, use two PowerShell terminals:

```powershell
# Terminal 1: API backed by SQLite
Set-Location backend
.\venv\Scripts\python.exe -m uvicorn app.main:app --reload --port 8000
```

```powershell
# Terminal 2: frontend
Set-Location frontend
npm.cmd run dev -- --host 127.0.0.1
```

Open `http://127.0.0.1:5173`; API health is `http://127.0.0.1:8000/`. The backend defaults to `sqlite:///./caseloop.db` relative to its working directory. To provision a local admin, run `.\venv\Scripts\python.exe -m app.create_admin` from `backend`.

## PostgreSQL using Docker Compose

Install Docker Desktop, start it, and from the project root:

```powershell
Copy-Item .env.example .env
# Replace the example local-only password in .env.
docker compose up --build -d
docker compose exec api python -m app.create_admin
```

The UI still runs through Vite on port 5173. The API is at `http://localhost:8000` and its OpenAPI docs at `http://localhost:8000/docs`. `docker compose down` stops containers but retains the database volume. `docker compose down -v` deletes it. PostgreSQL binds to localhost only; do not expose port 5432 publicly.

Fresh databases are created from the current SQLAlchemy models and stamped at the Alembic head by `app.db_bootstrap`. Databases already stamped at a prior revision are upgraded at startup. The historic Alembic chain began on an older SQLite schema; review and test every migration against both SQLite and PostgreSQL before relying on it operationally.

## Same-Wi-Fi phone preview (not public hosting)

For a private-device demo, use the PC's Wi-Fi IPv4 address, not a WSL or virtual-adapter address. In PowerShell, find it with:

```powershell
Get-NetIPAddress -AddressFamily IPv4 |
  Where-Object { $_.InterfaceAlias -match 'Wi-Fi' -and $_.IPAddress -notlike '169.254.*' } |
  Select-Object InterfaceAlias, IPAddress
```

Replace `<LAN_IP>` below with that address. From the project root, bind only the API port to the LAN interface and allow the exact frontend origin:

```powershell
$env:API_BIND_HOST = "0.0.0.0"
$env:CORS_ORIGINS = "http://<LAN_IP>:5174,http://localhost:5173,http://127.0.0.1:5173"
docker compose up -d
```

In another terminal:

```powershell
Set-Location frontend
$env:VITE_API_BASE_URL = "http://<LAN_IP>:8000/api"
npm.cmd run dev -- --host 0.0.0.0 --port 5174 --strictPort
```

Open `http://<LAN_IP>:5174` on the PC and a phone on the same trusted Wi-Fi. Keep port 5432 bound to localhost; do not configure router port forwarding. This is HTTP without secure cookies and is only for synthetic data on a trusted LAN—not cloud hosting or an internet-facing deployment. If Windows Firewall blocks access, allow the development ports only on a private network.

## Account and access setup

The landing page allows public responder registration; coordinator/admin accounts are provisioned by an administrator. Create the first admin via the CLI. Admins can add accounts with generated one-time temporary passwords, which must be changed on first login; they can also reset another user's password. Public registration has no email verification or signup abuse throttling yet. Existing legacy accounts with plaintext/placeholder passwords will not authenticate until a trusted admin resets/promotes them or the CLI is used.

This controlled-provisioning approach is typical: an authorized administrator or identity provider grants elevated roles instead of allowing public admin signup. CaseLoop currently has no SSO, MFA, or email invitation links; those are sensible additions before using it with an organization.

Choose a unique password in the private local prompt; never put credentials in source, checkpoints, or chat. If a password is exposed, rotate it immediately.

Authentication uses PBKDF2-HMAC-SHA256 password hashes, opaque revocable server-side sessions, HttpOnly cookies, CSRF checks on cookie-authenticated mutations, and backend role authorization. These controls are not a substitute for an independent security review or hosting safeguards.

Use `/` for the regular sign-in and `/admin` for the dedicated administrator sign-in. An admin account is still created through the CLI; public registration always creates a responder. If you are currently signed in as a responder, use the mobile **More → Sign out / switch account** menu before opening `/admin`.

## WhatsApp Cloud API test

The webhook endpoint is `/api/webhooks/whatsapp`. It handles Meta's verification GET request, validates signed POST requests using the configured app secret, deduplicates WhatsApp message IDs, and stores supported text messages as pending intake drafts only. It does not send outbound messages, fetch old messages, read arbitrary group history, approve reports, or assign responders.

To run a real provider test:

1. Create a Meta developer app with the WhatsApp use case and use its provided Cloud API test number.
2. Add/verify an allowed recipient in the Meta app dashboard and send a test message to the test number.
3. Make the local API temporarily reachable via a trusted HTTPS tunnel or deploy a test instance. The webhook callback must be publicly reachable over HTTPS at `https://<host>/api/webhooks/whatsapp`; Meta cannot call a localhost URL.
4. Set an unpredictable `WHATSAPP_VERIFY_TOKEN` in both the Meta webhook configuration and application environment. Set `WHATSAPP_APP_SECRET` to the Meta app secret in the application environment. Keep both out of source, screenshots, logs, and chat.
5. Subscribe the WhatsApp Business Account webhook to the `messages` field and complete Meta's endpoint verification.
6. Send a synthetic test message from the approved recipient. Confirm it appears only in coordinator intake review; review, correct, and explicitly approve it before it becomes a response.
7. Remove the tunnel or test deployment after the test. Do not send real beneficiary information without explicit organizational and privacy approval.

Follow Meta's [Cloud API getting-started guide](https://developers.facebook.com/documentation/business-messaging/whatsapp/get-started) and [webhook setup guide](https://developers.facebook.com/docs/graph-api/webhooks/getting-started). WhatsApp integration has not been live-tested in this workspace because Meta credentials and a public HTTPS callback are not configured.

This is an official webhook, not a crawler: Meta delivers supported inbound text sent to the configured Business/test number. It cannot retrieve personal WhatsApp history or arbitrary group messages. A real webhook message first appears in coordinator Intake Review; human review is required before it enters the read-only response board and can be assigned.

Meta also documents a separate [Groups API](https://developers.facebook.com/documentation/business-messaging/whatsapp/groups). As of this guide's review date, it requires an Official Business Account, creates invite-only groups, and limits them to 8 participants. It can deliver messages from those API-created groups, but it does not provide a way to scrape arbitrary existing chats. CaseLoop does not currently implement Groups API payloads; a group integration would need approved eligibility, participant notice/consent, and dedicated implementation/testing.

For an eligible, consent-based group, Meta's message webhook includes the group ID, message ID, participant's business-scoped user ID, message text, and provider timestamp. A future CaseLoop integration could preserve these as source evidence, map an explicit branch tag such as `KLB`, and extract a structured intake draft. The sender ID should be matched to an authorized person; text claiming who completed work is not proof by itself. A coordinator should confirm the extracted response and assignment before publication. This is feasible through Meta's official API, but not currently implemented and is not silent scraping of an existing WhatsApp group.

## Hosting guide: live demo with Render and Neon

### Recommended synthetic demo stack (checked November 13, 2026)

For the least complicated internet-accessible demo of this stack, use **Render Static Site + Render Python Web Service + Neon Free Postgres**. CaseLoop's Docker Compose PostgreSQL remains the easy local development setup; the hosted API connects to Neon instead. Render's Python runtime can install the existing requirements and use Python 3.11, so a Docker image is not required for the first deployment. Render does not deploy this local multi-container Compose stack as-is; self-hosting PostgreSQL in a Docker container on a small VPS adds Linux administration, TLS, backups, firewall, and update work. Keep the frontend and API on their Render `onrender.com` hostnames: they are different origins for CORS, but share a site for this app's `SameSite=Lax` session cookies. Avoid splitting the free demo across unrelated domains until cookie behavior is deliberately redesigned and tested.

This is not production hosting. Render's free web service spins down after 15 minutes idle and can take about a minute to wake; it has 750 free instance hours per workspace/month. Free web-service filesystems are ephemeral. Render's free PostgreSQL expires after 30 days, so use Neon rather than Render Postgres for a persistent demo database. Neon currently lists a permanent Free plan with 100 CU-hours and 1 GB storage per project; compute can suspend when monthly limits are exhausted. Recheck the providers' limits before deployment:

- [Render free services and limitations](https://render.com/docs/free)
- [Render Python version configuration](https://render.com/docs/python-version)
- [Neon current pricing and limits](https://neon.com/pricing)

### Deployment steps

1. Create a private GitHub repository and push the project only after checking for secrets and local data. This workspace has no configured Git remote or hosting account, so deployment cannot be completed from here without your provider sign-ins.
2. Create a Neon project. Copy its connection string from the dashboard; keep it private.
3. In Render, create a **Web Service** from that repository with root directory `backend`, Python runtime, build command `pip install -r requirements.txt`, and start command `uvicorn app.main:app --host 0.0.0.0 --port $PORT`. Add `backend\.python-version` with `3.11` to retain the project's Python baseline.
4. Configure the API service environment: `APP_ENV=production`, `COOKIE_SECURE=true`, `DATABASE_URL` set to the Neon PostgreSQL URL using the `postgresql+psycopg` driver and `sslmode=require`, and `CORS_ORIGINS` set to the exact Render static-site origin (no wildcard). Add `WHATSAPP_VERIFY_TOKEN` and `WHATSAPP_APP_SECRET` only when setting up the Meta test webhook.
5. In Render, create a **Static Site** from the same repo with root directory `frontend`, build command `npm ci && npm run build`, and publish directory `dist`. Set build-time `VITE_API_BASE_URL` to `https://<api-service>.onrender.com/api`. Add a rewrite `/*` → `/index.html` (status 200) so `/admin` opens the React app.
6. Create the first cloud administrator from a trusted local terminal. In PowerShell, set `DATABASE_URL` temporarily to the Neon URL, run `.\venv\Scripts\python.exe -m app.create_admin` from `backend`, then remove the environment variable. The interactive command creates or promotes the email you enter; it sets a new password if that email already exists.
7. Open the Render static-site URL on the PC and phone. Sign in at `/admin`, confirm the Admin dashboard/report, and test using synthetic records. Validate the first API call after idle wake, cookies, CORS, report download, and account sign-out.
8. For WhatsApp, use a Meta-provided test number and approved test recipient. Configure the Render API URL ending `/api/webhooks/whatsapp` as the callback, set the Meta secrets in Render, and verify a synthetic message moves only into Intake Review before coordinator approval.

Neon's database URL and all account credentials must be entered only in provider dashboards or local secret prompts, never committed to Git or pasted into chat. Do not use real beneficiary or operational data on this free demo.

Do not host operational or personal data until the organization has approved the deployment and data handling. Before public access:

- Complete an independent auth/authorization and privacy review; add login abuse protection and operational monitoring.
- Use HTTPS end-to-end, `COOKIE_SECURE=true`, exact frontend CORS origins, and secret-manager values. Cookie auth across frontend/API hosts requires compatible same-site domains.
- Use managed PostgreSQL with private networking, automated backups, and tested restore procedures.
- Test upgrades and rollback on a staging copy; define retention, deletion, user offboarding, audit access, and incident response.
- Configure budget alerts, an owner, and an availability expectation. Free-tier services are not a humanitarian service-level commitment.
- Use only synthetic records in preview deployments.

No Git remote, provider account, public host, public DNS name, or live WhatsApp connection is configured in this workspace. Docker Compose is local only.

## Learning plan for working independently

The highest-value skill is tracing one feature end to end and verifying it, not memorizing every framework. Practice in this order:

1. **Git and safe changes:** inspect status/diffs, make a small branch, commit a focused change, and recover from mistakes without deleting unknown work.
2. **Trace the app:** follow a response from React UI → `frontend/src/services/api.ts` → FastAPI route/schema/service → SQLAlchemy model/PostgreSQL → response back to the UI. Draw the path and name each file before asking Copilot to change it.
3. **Learn one language at a time:** TypeScript/React essentials (props, state, forms, async requests), then Python/FastAPI essentials (types, schemas, routes, dependencies, exceptions).
4. **Own the data:** read the SQLAlchemy models, understand foreign keys and migrations, and practice SELECT/INSERT/UPDATE against synthetic local data. Never experiment on operational records.
5. **Test and debug:** reproduce one bug, inspect the traceback/network response, add or run the smallest relevant test, then run `npm.cmd run build` or the focused backend test.
6. **Operate the stack:** understand `.env`, Docker Compose logs/health, PostgreSQL persistence, Render environment variables, and how to roll back a deployment.
7. **Add integrations last:** read webhook examples, verify signatures, deduplicate retries, preserve source/timestamps, and keep human approval for consequential records.

For each Copilot task, first write the expected behavior in your own words, ask for a small change, inspect every changed line, explain the data flow back to yourself, run the focused test, and only then accept it. A useful weekly exercise is to make one tiny UI change, one API/test change, and one database/query change on synthetic data. Keep a learning log of terms you had to look up.

For the complete 12-week schedule, safe offline setup, AI-last routine, and hands-on evidence checklist, see the [Independent, Offline-First Learning Program](../training/independent-learning-program.md).

For the detailed local PostgreSQL verification, credential rotation practices, secrets-safe Git preparation, Oracle HTTPS architecture, and live Meta test sequence, see the [Oracle and WhatsApp learning runbook](./oracle-whatsapp-learning-runbook.md).

## Verification commands

```powershell
Set-Location backend
.\venv\Scripts\python.exe -m pytest -q

Set-Location ..\frontend
npm.cmd run build
```
