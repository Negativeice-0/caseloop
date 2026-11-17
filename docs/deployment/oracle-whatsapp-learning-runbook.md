# CaseLoop: Local PostgreSQL to Oracle and WhatsApp Test Runbook

This is a hands-on learning guide for running CaseLoop with Docker PostgreSQL, preparing a secrets-safe private GitHub repository, rehearsing an Oracle Cloud deployment, and testing Meta's official WhatsApp webhook with synthetic data.

Work in order and keep notes of commands, observations, and errors. Do not use real beneficiary, personnel, or operational information. This guide is not approval to deploy CaseLoop for operational use.

## What the end-to-end path should do

```text
Approved WhatsApp test sender
  -> Meta Cloud API
  -> public HTTPS callback on the CaseLoop API
  -> signature verification and duplicate check
  -> PostgreSQL IntakeSubmission with status=pending
  -> coordinator reviews it in Intake Review
  -> explicit approval creates a Response Register record
  -> optional team assignment and timeline events
```

The app must not publish or assign a message automatically. It does not scrape personal WhatsApp history or arbitrary existing group chats. Start with Meta's provided test number and an approved test recipient.

## 1. Credential handling: when, how, and what to record

### Credential rules

- Never put actual passwords, tokens, private keys, or app secrets in source code, comments, checkpoints, screenshots, chat, or Git history.
- `.env` is a local configuration file, not a vault. Keep it untracked and restrict access to the machine. On a Linux VM, use restrictive file permissions such as `chmod 600 .env`.
- `.env.example` is safe to commit only when it contains placeholders, not usable credentials. Comments in `.env` are ignored; secrets must be active assignments for configuration to use them.
- Rotate a secret immediately if it was exposed in a tracked file, pasted into a public location, shared with the wrong person, or may otherwise have been copied. Removing it from the visible file is not enough: revoke or replace it at the system that issued it.
- Also rotate when an owner leaves or changes roles, a device is lost, a credential is suspected to be misused, or policy requires rotation. Prefer short-lived or scoped credentials and automated rotation where available. Do not rotate on an arbitrary schedule without a reason if it creates avoidable outages; follow provider and organizational policy.
- Never rely on a private GitHub repository as a place to store secrets. Private repositories can be shared, copied, or made public later.

### Rotate an exposed credential

1. **Identify its type and issuer without copying its value.** CaseLoop account password, PostgreSQL password, Meta verify token, Meta app secret, OCI SSH key, and OCI API key each have different replacement procedures.
2. **Prepare the replacement safely.** Generate a new unique secret locally or in the issuing provider. Do not send it to an assistant or put it in a command-line argument that will be saved in shell history.
3. **Update the issuing system and the consuming app in a coordinated order.** For database passwords, plan a short maintenance window: stop the API, change the PostgreSQL role password interactively, update the local `.env` or cloud secret setting, then restart and verify the API connection. Changing `POSTGRES_PASSWORD` in `.env` alone does not change a password in an already-initialized database.
4. **Verify the replacement works** with a health check and a harmless synthetic operation.
5. **Revoke the old credential** at its issuer. Confirm it no longer works. Do not leave both credentials active indefinitely.
6. **Remove the exposed value from files and backups where practical.** If it entered Git history, treat it as compromised even if the latest file no longer contains it. Rotate first. History rewriting is a separate, coordinated cleanup; it does not replace rotation.
7. **Record the event without recording the secret.** Keep the credential type/owner, system, date, reason, rotation completion, old-key revocation, verification result, and responsible person. Do not record the credential value.

Use a private password manager or access-controlled operations log for the record. A safe entry looks like:

| Credential identifier (not value) | System/owner | Reason/date | Replacement verified | Old credential revoked | Follow-up |
| --- | --- | --- | --- | --- | --- |
| PostgreSQL app-role password | CaseLoop learning VM | Planned rotation / YYYY-MM-DD | Yes/No | Yes/No | Next review / owner |

### CaseLoop credential notes

- **CaseLoop administrator account:** use the admin password reset/change workflow and set a new unique password. Any temporary password should be delivered through an approved private channel and changed at first sign-in.
- **Local PostgreSQL:** the database role password and API connection URL must be updated together. With local synthetic data, stop the API and open an interactive PostgreSQL prompt:

  ```powershell
  docker compose stop api
  docker compose exec db sh -lc 'psql -U "$POSTGRES_USER" -d "$POSTGRES_DB"'
  ```

  At the `psql` prompt, run `\password` and follow its hidden prompts; then run `\q`. Edit the ignored `.env` so `POSTGRES_PASSWORD` has the same new value, then recreate the API container with `docker compose up -d --force-recreate api`. Check `docker compose ps` and `Invoke-RestMethod http://localhost:8000/`. If the connection fails, stop and diagnose the mismatch; do not keep changing passwords randomly. The database image's `POSTGRES_PASSWORD` variable initializes a new data directory; it does not change an existing database role by itself.
- **Meta webhook verify token:** choose a new random value and update both the Meta webhook configuration and `WHATSAPP_VERIFY_TOKEN` in the API environment.
- **Meta app secret:** rotate/regenerate it in Meta if exposed, then update `WHATSAPP_APP_SECRET` in the API environment. CaseLoop needs this secret to validate signed webhook POSTs. A receive-only webhook does not need a WhatsApp send access token.
- **OCI SSH key:** add a replacement public key, prove a new SSH login works, then remove the old public key. Keep the private key off GitHub and out of the VM.

**Known repository preparation issue:** Checkpoint 10 was previously identified as containing credentials. Do not copy its values into `.env`, comments, another document, or this guide. Before the first Git commit, replace the exposed values with a redaction and rotate the credentials. If you cannot safely sanitize that checkpoint yet, exclude it from the initial repository. Never paste the values into a secret scanner report or chat.

## 2. Verify local Docker PostgreSQL

Use PowerShell from the project root. Docker Desktop's engine must be running; the window does not need to be used to manage each service.

```powershell
Set-Location C:\Users\Admin\Documents\caseloop
docker version
docker compose version
```

`docker version` should show both a client and a server. If it only shows the client or reports that it cannot connect, start Docker Desktop and retry. A Docker Hub sign-in is separate from starting the engine; the public PostgreSQL image normally does not require a personal login.

Check whether `.env` already exists before copying anything. Do not overwrite an existing file:

```powershell
Test-Path .env
```

If it returns `False`, create a local file from the example and edit it before starting the stack:

```powershell
Copy-Item .env.example .env
```

Replace the example-only local password with a new local development password. Never use an exposed or production password for this exercise. Do not paste `.env` contents into chat.

Start the services:

```powershell
docker compose up --build -d
docker compose ps
docker compose logs --tail=80 db api
```

Look for the database health check to pass and the API to start. Then query the API's health route:

```powershell
Invoke-RestMethod http://localhost:8000/
```

Expected: `app` is `CaseLoop`, `status` is `online`, and `database` is `postgresql`. If it says `sqlite`, check whether you are querying the Compose API or a separately running local Uvicorn process. If startup reports a port conflict, stop the other local API with Ctrl+C and retry.

Start the React development server separately:

```powershell
Set-Location C:\Users\Admin\Documents\caseloop\frontend
npm.cmd run dev -- --host 127.0.0.1
```

Open `http://127.0.0.1:5173`. The development frontend calls the API at `http://127.0.0.1:8000/api`; the API connects to PostgreSQL inside Compose. Sign in with a local synthetic account and verify one harmless UI read/write flow.

Stop the containers without deleting the database volume:

```powershell
Set-Location C:\Users\Admin\Documents\caseloop
docker compose down
```

**Do not use `docker compose down -v`** unless you deliberately want to delete the database volume and all data in it.

### Which database do the tests use?

The current backend tests are deliberately isolated from the Compose database:

- `conftest.py` defaults `DATABASE_URL` to SQLite only if it was not already set.
- The assignment/webhook tests override `get_db` with their own in-memory SQLite engine.
- Do not point the current test suite at a database containing data you care about. Run it explicitly against in-memory SQLite:

```powershell
Set-Location C:\Users\Admin\Documents\caseloop\backend
$env:DATABASE_URL = "sqlite://"
.\venv\Scripts\python.exe -m pytest -q
```

The setting applies to this PowerShell process and its child processes. To verify the Compose PostgreSQL connection, use the running API health route and the synthetic UI flow above; do not change the test fixture to point at your working database.

## 3. Learn the app's database and UI wiring

Trace these links in the code and write one sentence for each:

1. `backend/app/core/config.py` reads `DATABASE_URL` (or uses SQLite's local default).
2. `backend/app/core/database.py` creates the SQLAlchemy engine, creates `SessionLocal`, and exposes `get_db()`.
3. API routes inject `get_db()` with FastAPI `Depends`, then query or update models.
4. `backend/app/main.py` includes the API routers and initializes the app.
5. `frontend/src/services/api.ts` sends HTTP requests to the configured API address. It does not select the database.
6. `frontend/src/features/workflow/WorkflowViews.tsx` loads pending drafts and calls the approval endpoint.
7. `backend/app/api/webhooks.py` verifies Meta's webhook request and stores supported text as a pending `IntakeSubmission`.
8. `backend/app/api/intakes.py` lists drafts for authorized coordinators/admins and handles approval/rejection. Approval creates the response, optional assignment, and timeline events.

Useful files:

- [Database settings](../../backend/app/core/config.py)
- [Database engine and session dependency](../../backend/app/core/database.py)
- [Compose services](../../docker-compose.yml)
- [WhatsApp webhook](../../backend/app/api/webhooks.py)
- [Intake API](../../backend/app/api/intakes.py)
- [Intake review UI](../../frontend/src/features/workflow/WorkflowViews.tsx)
- [API client](../../frontend/src/services/api.ts)

The current Compose file has `db` and `api`. The frontend runs separately through Vite in development. It is not yet a production frontend service.

## 4. Prepare a secrets-safe private GitHub repository

Git is local until you configure a remote and push. First make sure the Git executable is available in your chosen shell. In PowerShell, if Git is installed in its standard location but not on `PATH`, you can test it in the current terminal:

```powershell
$env:Path = "C:\Program Files\Git\cmd;" + $env:Path
git --version
```

Before `git init` or `git add`, do a local-only review:

1. Replace exposed values in Checkpoint 10 with redactions and rotate those credentials, or exclude that checkpoint from the initial repository.
2. Confirm `.env` is not present in the staged files and is ignored by `.gitignore`.
3. Review the project for local database files, temporary files, screenshots containing secrets, private keys, provider credentials, and real personal/operational data.
4. Confirm `.env.example` contains placeholders only.
5. Do not include passwords in comments. Do not treat GitHub's private setting as a secret store.

Only after that review, initialize and inspect the local repository:

```powershell
Set-Location C:\Users\Admin\Documents\caseloop
git init -b main
git status --short
git status --ignored --short
```

Stage only reviewed paths (do not stage `docs/projects/progress` until the checkpoint is sanitized), then inspect the staged names and diff before committing:

```powershell
git add README.md .gitignore .env.example docker-compose.yml backend frontend docs/design docs/training docs/deployment
git diff --cached --name-only
git diff --cached --check
git diff --cached
```

Do not continue if a secret, local database, or unintended file appears. The `.gitignore` file helps with untracked files; it cannot remove an already-staged or committed secret. Review the staged diff locally and do not paste it into chat.

Create a **private** GitHub repository only after sanitizing the local content. After reviewing the staged diff and making the initial commit, connect and push:

```powershell
git remote add origin https://github.com/<your-account>/<your-private-repository>.git
git remote -v
git push -u origin main
```

Authenticate with GitHub's browser or SSH flow; do not put a personal access token in a command, source file, or `.env.example`. Consider enabling secret scanning/push protection if available on the account.

## 5. Prepare the Oracle deployment safely

The current project cannot be deployed as a full production stack using the existing Compose file alone. A full single-VM setup needs:

- the FastAPI API service;
- PostgreSQL on a private Compose network with **no public port mapping**;
- a production `frontend/Dockerfile` that builds React and serves the static output;
- an HTTPS reverse proxy such as Caddy that routes the frontend and API;
- a domain and DNS records for public HTTPS;
- environment secrets stored on the VM or in a secret manager, not in Git.

For cookie authentication and the API's health check, use two HTTPS hostnames under the same registered domain, for example `app.example.org` and `api.example.org`. Set the frontend's build-time `VITE_API_BASE_URL` to `https://api.example.org/api`, and set backend `CORS_ORIGINS` to the exact frontend origin, `https://app.example.org`. The API helper derives its health-check origin from the API URL, so keep the API on its own hostname. Use `APP_ENV=production` and `COOKIE_SECURE=true`.

### What the production frontend Dockerfile does

The backend already has `backend/Dockerfile`; the frontend currently does not. A production frontend Dockerfile is a **multi-stage build**:

1. A Node build stage copies the frontend package files and source, receives the public `VITE_API_BASE_URL` at build time, and runs the existing production build (`npm ci` followed by `npm run build`).
2. The build output in `dist` is copied into a small static-server image.
3. That final image serves the React files. It does not contain Python, PostgreSQL, or database credentials.

The browser downloads those static files and calls the API using the compiled API URL. React never connects to PostgreSQL. Do not put secrets in `VITE_` variables: Vite embeds them into browser-visible JavaScript.

One simple full-stack design uses Caddy as the final frontend image and HTTPS proxy. Its configuration serves the single-page app on the app hostname and proxies the API hostname to the Compose `api` service:

```caddyfile
{$APP_DOMAIN} {
    root * /srv
    try_files {path} /index.html
    file_server
}

{$API_DOMAIN} {
    reverse_proxy api:8000
}
```

In this design the frontend Dockerfile has a Node build stage and a Caddy runtime stage; the `edge` Compose service publishes ports 80 and 443 and persists Caddy's certificate data. API and database communicate only over Compose's private network. Keep the project's development Vite workflow unchanged; introduce the production image as a separate, testable Docker/Compose change.

The intended traffic layout is:

```text
Internet :80/:443 -> HTTPS proxy
  app.example.org -> frontend container
  api.example.org -> API container on the private Compose network
API container -> db:5432 on the private Compose network
```

Only the proxy should publish ports 80 and 443. Do not publish PostgreSQL port 5432 to the internet. Restrict SSH (port 22) to your own current IP where possible. Configure both the OCI VCN/network rules and the Linux host firewall; an open host firewall alone does not make OCI ingress open, and an open OCI rule alone does not configure the host firewall.

### Oracle Cloud Console sequence

1. Review the current Oracle Free Tier terms and confirm whether you are willing to proceed with a payment method and possible charges. Oracle budgets are **soft alerts**, evaluated periodically; they are not hard spending caps. Do not create resources unless the console identifies their cost/tier clearly. Capacity and free-resource availability are not guaranteed.
2. Create a compartment or use a clearly named learning compartment. Create a small budget and email alert before launching resources; remember the alert is not a spending lock.
3. Create a VCN with internet connectivity and a Linux compute instance in the chosen region. Check the exact price/tier of every selected shape, boot volume, public IP, and add-on before confirming. Save the SSH private key locally with restricted access; never upload it to GitHub.
4. Add only the required ingress rules: SSH limited to your IP, and TCP 80/443 for HTTPS setup. Do not add a public rule for 5432. Confirm both network rules and the instance firewall.
5. Point DNS for the app and API hostnames at the VM's public IP. A registered domain may cost money; verify before purchasing.
6. SSH into the VM and install Docker Engine and the Compose plugin using the official instructions for the chosen Linux distribution. Check `docker version` (client and server) and `docker compose version`.
7. Clone the sanitized private repository onto the VM. Create `frontend/Dockerfile` with the Node build and Caddy runtime stages as a learning change; do not copy local `.env` files to Git or bake secrets into an image.
8. Add an `edge` Compose service with app/API hostname routing, Caddy certificate-data volumes, and only the required public ports. Create the VM's `.env` from placeholders, enter new secrets locally, restrict its permissions, and configure production values. Build the production images on the VM or build explicitly for its CPU architecture; verify that Python and Node dependencies support the selected Oracle VM architecture.
9. Keep the `db` service without a public `ports` mapping. Keep API and frontend reachable only from the proxy on the Compose network. Start the services and inspect `docker compose ps` and logs without sharing secret-bearing output.
10. Configure the reverse proxy for both hostnames and valid TLS. Meta requires a publicly reachable HTTPS callback with a valid certificate; self-signed TLS is not sufficient.
11. Verify `https://api.example.org/` reports PostgreSQL, sign in at `https://app.example.org`, and test the app with synthetic data from the PC and phone.
12. Rehearse a database backup and restore before relying on the host. A connection URL and Compose configuration do not back up database contents.

Oracle's official documentation:

- [Create a Compute instance](https://docs.oracle.com/en-us/iaas/Content/Compute/Tasks/launchinginstance.htm)
- [Oracle budgets and alerts](https://docs.oracle.com/en-us/iaas/Content/Billing/Concepts/budgetsoverview.htm)
- [Docker Engine installation](https://docs.docker.com/engine/install/)

Do not put real operational information on this learning deployment. Before any organizational use, complete privacy, access-control, backup/recovery, monitoring, incident-response, and organizational approval reviews.

## 6. Configure Meta's official test webhook

Do this only after the API is reachable at its final public HTTPS URL and the backend secrets have been set on the host.

1. Register for Meta developer access and create a Meta app with the WhatsApp use case.
2. Use the test phone number and test recipient provided by Meta. Add/verify your own test recipient in the dashboard.
3. Set the webhook callback URL to `https://api.example.org/api/webhooks/whatsapp`.
4. Choose a new unpredictable verify token. Put the same value in the dashboard and the API's `WHATSAPP_VERIFY_TOKEN` environment variable.
5. Set `WHATSAPP_APP_SECRET` from the Meta app settings in the API's secret environment. Do not include it in Git, a screenshot, or chat. Restart/redeploy the API after changing the environment.
6. Subscribe the WhatsApp Business Account webhook to the `messages` field and complete callback verification.
7. Confirm Meta verifies the GET challenge. The app's endpoint checks the verify token and returns the challenge.
8. Send a synthetic text message from the approved test recipient to Meta's provided test number.
9. Check the API response/logs without logging secrets, then sign in as coordinator/admin and open **Intake Review**. The message should be pending, not on the Response Register yet.
10. Review and structure the synthetic text. Approve it, optionally choose a team, and verify the response, assignment, and timeline appear. Check the read-only register in a second browser or signed-in responder account.
11. Revoke temporary tunnels, unused credentials, or test resources after the exercise. Check OCI spend and shut down resources you do not need.

Meta references:

- [WhatsApp Cloud API Get Started](https://developers.facebook.com/documentation/business-messaging/whatsapp/get-started)
- [Webhooks: verification and event notifications](https://developers.facebook.com/docs/graph-api/webhooks/getting-started)

This first test is a direct message to the official test number, not a crawler. Arbitrary existing WhatsApp group history is not available through this webhook. Any later group workflow requires checking Meta's current product eligibility, participant consent, and organizational approval.

## 7. Practice testing and debugging the workflow

There are already focused webhook and intake tests in `backend/tests/test_assignments.py`. They cover verification challenge handling, a valid signed payload, pending-only intake, duplicate delivery, coordinator approval/assignment, invalid signatures, and malformed JSON.

Run them without using a live database:

```powershell
Set-Location C:\Users\Admin\Documents\caseloop\backend
$env:DATABASE_URL = "sqlite://"
.\venv\Scripts\python.exe -m pytest tests\test_assignments.py -k "meta_webhook or whatsapp_intake" -q
```

Then run the full backend suite and frontend build:

```powershell
.\venv\Scripts\python.exe -m pytest -q

Set-Location C:\Users\Admin\Documents\caseloop\frontend
npm.cmd run build
```

For each test, write down: **expected result, observed result, evidence, hypothesis, next experiment**. Useful additional cases to implement yourself, one at a time:

- wrong verify token and missing webhook configuration;
- same message ID delivered twice;
- two different message IDs with the same text;
- unsupported message type, empty text, and text over the configured limit;
- invalid HMAC signature and malformed JSON;
- API unreachable, database unavailable, or stale browser session;
- responder attempting to approve an intake (must be denied);
- coordinator approval with and without a team assignment;
- verify that a pending intake is absent from the Response Register until approval.

First write a test and observe it fail for the intended reason; then implement the smallest fix and rerun it. Test intentional failures locally or on disposable staging with synthetic data. Do not try to break a live public instance, send real messages, or test destructive actions against a database you care about.

## 8. What not to forget

Before sharing the live demo, check:

- [ ] exposed credentials rotated; values removed from checkpoint and Git history plan reviewed;
- [ ] private repo contains no `.env`, secrets, database files, private keys, or real data;
- [ ] Docker API reports `postgresql`; database port is not public;
- [ ] production frontend and HTTPS proxy are included (not present in current Compose);
- [ ] app/API origins, CORS, secure cookies, DNS, and TLS are tested from phone and PC;
- [ ] Meta test recipient is approved; only synthetic messages are used;
- [ ] pending intake requires coordinator review before publication;
- [ ] backup/restore and spend review are rehearsed;
- [ ] organization has not been led to believe this demo is approved for operational use.

## Current starting point

The local API, database, and UI wiring exists. The official webhook receiver and the UI review/approval workflow exist, and webhook tests are already present. The production frontend container, HTTPS reverse-proxy deployment, Oracle VM, DNS/TLS configuration, and live Meta test are not yet established. Build and verify each missing piece rather than assuming a successful local test proves a live deployment.
