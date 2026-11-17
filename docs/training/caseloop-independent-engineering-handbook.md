# CaseLoop Independent Engineering Handbook

## What this handbook is—and is not

This is a working reference for learning to understand, test, change, and operate CaseLoop without needing an assistant to drive the work. It explains the current repository as it exists, gives repeatable investigation methods, and points to the more focused guides.

It is not proof that the app is production-ready, an organizational approval, or a substitute for the Student Attachment Guide or your university's report template. It uses synthetic data only. Do not copy real beneficiary, personnel, incident, or provider-secret data into exercises, screenshots, reports, or chat.

The repository already has focused guides for the two-week lab, the 12-week curriculum, the deployment runbook, and the completion roadmap. This handbook maps those materials and adds a practical debugging and file-connection reference. It is an editable Markdown draft, not a typeset or page-count-verified 60-page submission.

## 1. The professional learning loop

Use the same loop for a bug, feature, or unfamiliar tool:

1. **State the behavior.** Describe one observable result without prescribing an implementation.
2. **Predict.** Say what should happen, which layer probably owns it, and how you will observe it.
3. **Reproduce.** Use synthetic input and the smallest repeatable steps.
4. **Inspect evidence.** Read the test, request, response, log, traceback, browser network panel, or database state that proves what happened.
5. **Localize.** Decide whether the mismatch is in the browser, API, authorization, schema, database, container, or external provider.
6. **Hypothesize.** Write one possible cause that could be disproved.
7. **Change one thing.** Prefer a focused test first, then the smallest code or configuration change.
8. **Verify.** Run the narrowest relevant check, then appropriate regression checks.
9. **Review.** Inspect the diff, errors, side effects, and secret exposure.
10. **Explain.** Teach back the reason for the change without reading an AI-generated answer.

Keep a small notebook entry with `Expected / Actual / Evidence / Hypothesis / Next experiment`. A failure is useful when it narrows the cause. Random edits, multiple simultaneous changes, and deleting an assertion make the cause harder to find.

## 2. CaseLoop in one picture

```text
Person using a browser
  -> React + TypeScript frontend
  -> HTTP request to FastAPI
  -> route authorization and input validation
  -> SQLAlchemy session
  -> SQLite (local mode) or PostgreSQL (shared mode)

Meta test sender
  -> Meta webhook POST over HTTPS
  -> FastAPI webhook signature check and deduplication
  -> pending IntakeSubmission in the database
  -> coordinator reviews it in the frontend
  -> explicit approval creates a Response and optional Assignment
  -> timeline records who did what and when
```

Docker is one way to start independent services consistently. Python does not need a Docker-specific connection: the API uses a normal database driver and TCP connection. In Compose, Docker supplies a private network and the service name `db`; the API connects to `db:5432`. The browser does not connect to PostgreSQL.

CaseLoop is intended to complement existing coordination processes. It does not replace WhatsApp, an organization's authoritative systems, or human approval. A webhook draft is not an approved response. Use only a Meta test number and synthetic data for learning.

## 3. Plain-language technology glossary

| Term | Plain-language meaning in this project |
|---|---|
| API | A defined way for the frontend or an external provider to ask the backend to do something or return data. |
| Alembic | The migration tool that records deliberate database schema changes over time. |
| Authentication | Proving which account is making a request, such as signing in. |
| Authorization | Deciding what that signed-in account is allowed to do. A hidden button is not server-side authorization. |
| Backend | The Python/FastAPI process that validates requests, applies rules, and reads or writes data. |
| Build | Turning source code into runnable output; Vite builds the React app into static files. |
| CORS | A browser-enforced rule controlling which website origins may call an API. It is not a login system. |
| Container | An isolated process packaged with the files and runtime it needs. It can be replaced; its filesystem is not automatically durable storage. |
| Compose | A description for starting multiple containers, their configuration, networks, health checks, and volumes together. |
| Cookie | A browser-held value sent with matching requests. CaseLoop uses cookies for sessions and a CSRF token for state-changing requests. |
| CRUD | Create, read, update, and delete operations. Each action needs appropriate authorization and audit behavior. |
| CSRF | Cross-site request forgery: an unwanted state-changing request sent using a browser's existing credentials. |
| Database | An organized, durable store of records, constraints, and relationships. |
| Dependency | A library or service another piece of software relies on. Pinning and updating dependencies is part of maintenance. |
| DNS | The system that maps a human-readable domain name to an address. |
| Dockerfile | Build instructions for one image, such as the existing backend image or a future frontend image. |
| Endpoint | One address and HTTP method combination, such as `GET /api/responses/`. |
| Environment variable | A setting supplied to a process at runtime or build time. Its name does not make its value secret. |
| FastAPI | The Python framework that defines routes, validates HTTP input, and serves the CaseLoop API. |
| Fixture | Test setup that provides a controlled database, user, or request for a test. |
| Frontend | The React application rendered in the browser. It calls the API; it must not contain database credentials. |
| HTTP | The request/response protocol used between browser, API, and provider. HTTPS encrypts HTTP in transit. |
| HMAC signature | A cryptographic check that a webhook body was signed with the configured shared secret and was not altered. |
| Idempotency/deduplication | Making retries safe so the same provider message is not stored twice. |
| Image | A built template for containers. Running the image creates a container. |
| JSON | A text format commonly used for API request and response data. |
| ORM | Object-relational mapper. SQLAlchemy maps Python model objects to relational database rows. |
| Migration | A versioned instruction to move a database schema from one state to another. |
| Model | A backend class describing persisted data and relations; it is not the same thing as a frontend TypeScript type. |
| PostgreSQL | A relational database server used here for shared Compose development and possible hosting. |
| Proxy/reverse proxy | A public entry point that routes requests to internal services and can handle HTTPS. |
| React | A JavaScript UI library used to compose screens from components and state. |
| Role | A permission category such as responder, coordinator, or administrator. The backend must enforce it. |
| Route | Backend code that handles a matching HTTP method and URL. |
| Schema (Pydantic) | A validated shape for API input/output. This is separate from the database schema. |
| Schema (database) | The actual tables, columns, indexes, constraints, and relations installed in a database. |
| Seed | A script that inserts known sample records. Seeds should be synthetic and safe to rerun where intended. |
| Session | A database conversation managed by SQLAlchemy, or a browser login session; context determines which meaning applies. |
| SQLite | A database stored in a file or in-memory connection, useful for local practice and isolated tests. |
| SQL | The language used to query and change relational databases. |
| Static files | Browser-ready HTML, JavaScript, CSS, and images; the production React build is served this way. |
| Test double/override | A substitute dependency used to isolate a test from a real database or provider. |
| TypeScript | JavaScript with static type checking. Types help catch mismatches but do not validate untrusted server input by themselves. |
| Vite | The frontend development server and production bundler used by this React app. |
| Volume | Docker-managed storage outside a container's replaceable filesystem. It helps persist data but is not a separate backup. |
| Webhook | An HTTP request a provider sends to notify the app about an event. It can be retried and must be validated. |

Two overloaded words deserve special care: **model** can mean database model, AI model, or a conceptual model; **environment** can mean local/dev/production settings, a process's variables, or a Python virtual environment. Ask which one a sentence means.

## 4. File map: where to look first

### Browser application

| File | Responsibility |
|---|---|
| `frontend/src/main.tsx` | Browser entry point that mounts the React application. |
| `frontend/src/App.tsx` | Top-level application state and screen selection. |
| `frontend/src/layouts/MainLayout.tsx` | Shared responsive desktop/mobile navigation and page frame. |
| `frontend/src/services/api.ts` | API base URL, HTTP calls, session/CSRF handling, and response/error parsing. |
| `frontend/src/types/index.ts` | Shared TypeScript data shapes used by frontend features. |
| `frontend/src/features/auth/AuthGateway.tsx` | Login/registration and authentication presentation. |
| `frontend/src/features/workflow/WorkflowViews.tsx` | Intake review and related operational workflow screens. |
| `frontend/src/features/responses/ResponseRegister.tsx` | The response register view. |
| `frontend/src/features/assignments/AssignmentsManager.tsx` | Assignment-management UI. |
| `frontend/src/features/admin/AdminControl.tsx` | Admin sections and administrative management UI. |
| `frontend/src/features/profile/UserProfile.tsx` | User profile view. |

### Python API and database

| File or directory | Responsibility |
|---|---|
| `backend/app/main.py` | Creates the FastAPI app, initializes the database bootstrap, includes routers, configures CORS and CSRF middleware, and exposes `/`. |
| `backend/app/core/config.py` | Reads environment settings including `DATABASE_URL`, CORS origins, cookie mode, and WhatsApp values. |
| `backend/app/core/database.py` | Builds the SQLAlchemy engine/session factory and provides `get_db()`. |
| `backend/app/db_bootstrap.py` | On startup, upgrades an Alembic-managed database; for a genuinely empty database, creates metadata and stamps the current revision; refuses a non-empty DB without migration history. |
| `backend/app/core/auth.py` | Request dependencies and server-side role/session checks. |
| `backend/app/core/security.py` | Password/session security helpers. |
| `backend/app/models/models.py` | Persisted entities and relationships. |
| `backend/app/schemas/schemas.py` | Pydantic request/response validation shapes. |
| `backend/app/api/auth.py` | Sign-in, registration, current user, sign-out, and password endpoints. |
| `backend/app/api/responses.py` | Response register CRUD and timeline read paths. |
| `backend/app/api/assignments.py` | Team and assignment operations. |
| `backend/app/api/intakes.py` | Pending intake listing and coordinator approval/rejection. |
| `backend/app/api/webhooks.py` | Meta verification, signed-message validation, duplicate handling, and intake creation. |
| `backend/app/api/reports.py` | Summary, preview, and Word-export endpoints. |
| `backend/app/api/admin.py` | Admin-only management, status, and audit endpoints. |
| `backend/app/services/` | Reusable service logic separated from route wiring. |
| `backend/app/seed.py` | Synthetic demo records; requires an active admin/coordinator and avoids duplicate response reference codes. |
| `backend/app/create_admin.py` | Local administrator provisioning entry point; handle its output privately. |

### Database changes, tests, and runtime

| File or directory | Responsibility |
|---|---|
| `backend/alembic.ini` | Alembic configuration entry point. |
| `backend/alembic/env.py` | Supplies the project engine and model metadata to Alembic. |
| `backend/alembic/versions/` | Versioned schema changes. Each revision links to a predecessor. |
| `backend/tests/conftest.py` | Sets a SQLite default only if `DATABASE_URL` is unset, then creates/drops test tables around tests. |
| `backend/tests/test_main.py` | Main API behavior tests. |
| `backend/tests/test_database.py` | Database engine-related tests. |
| `backend/tests/test_assignments.py` | Assignment/intake/webhook integration coverage and explicit test database overrides. |
| `backend/Dockerfile` | Existing backend image build recipe. |
| `docker-compose.yml` | Local service topology, environment, private networking, port mappings, health checks, and database volume. |
| `.env.example` | Placeholder-only template. It is not an active secret store. |

Use a narrow search rather than browsing the whole repository every time. For a symptom, search first for the route, model, UI call, test, or setting named in the error. Read its direct callers and tests next.

## 5. Four complete feature paths

### A. Application startup and database selection

1. The process imports `backend/app/main.py`.
2. `core/config.py` reads `DATABASE_URL`; absent an override, it defaults to a local SQLite URL.
3. `core/database.py` parses that URL, creates the SQLAlchemy engine, then binds `SessionLocal` to it.
4. `main.py` calls `initialize_database()`.
5. A route receives a session through `Depends(get_db)`, which opens a session and closes it after the request.
6. `/` reports `engine.dialect.name`. This is a useful diagnostic for the process answering the request, not proof of every table or query.

In Compose, the API's environment supplies PostgreSQL settings and the hostname `db`. From a local Uvicorn process, the default is SQLite unless that process has a different environment variable. The frontend's `VITE_API_BASE_URL` selects an HTTP API address; it does not select the database.

### B. Browser API request

1. `main.tsx` mounts the app.
2. `App.tsx` chooses the current page/layout and gets user state.
3. A feature component calls a helper from `services/api.ts`.
4. `api.ts` sends `fetch()` with credentials; for state-changing requests it includes the CSRF header when a token is available.
5. The FastAPI route validates the request with a Pydantic schema.
6. Server-side dependencies check session and role where needed.
7. The route/service reads or changes SQLAlchemy models.
8. The route returns a schema-shaped JSON response or a deliberate HTTP error.
9. The UI displays the result or a visible error.

When a screen is blank or stale, inspect the browser network request and response first. Then correlate the URL/method to the API route, check server logs, and inspect the database only if the API evidence indicates persistence is involved.

### C. WhatsApp intake to response

1. Meta calls the HTTPS callback.
2. The GET verification route checks configured verification values and echoes the challenge only when valid.
3. On POST, the API checks configuration, size, signature over the original request bytes, JSON shape, supported text content, and provider message ID.
4. A duplicate message ID is not stored as a second intake.
5. An accepted text payload creates a pending intake record. It is not an approved response.
6. `api/intakes.py` returns pending items to authorized coordinators/admins.
7. Intake Review in `WorkflowViews.tsx` loads the API data; the current UI loads on open/actions, not through a push channel. Reopen or refresh to see an arrival while the page is already open.
8. A coordinator corrects and approves the draft. Approval creates the response and, if selected, linked assignment; timeline events retain the action.
9. A responder can use the permitted read-only view but cannot approve or administer records.

The webhook does not send outbound WhatsApp messages and does not read arbitrary WhatsApp groups. Never describe a synthetic test as a live Meta test.

### D. Report preview and export

1. A coordinator/admin opens Reports.
2. The frontend calls the summary or preview API with its chosen filters.
3. The backend computes deterministic summaries from structured records.
4. The preview is returned to the frontend for review.
5. The Word endpoint generates a document from the same structured records and filters.

Do not treat a generated summary as verified fact unless each source record is correct and reviewed. If analysis later uses AI, keep it advisory and human-reviewed. Report export is not a substitute for source validation or organizational approval.

## 6. Database choices and ORM basics

SQLite and PostgreSQL are separate database engines. They can support the same SQLAlchemy models, but they are not the same database and do not share data automatically.

| Question | SQLite local/test | PostgreSQL via Compose |
|---|---|---|
| Where is the server? | No separate server for a file DB; an in-memory URL can be test-only. | A separate `db` container/server. |
| How does the API reach it? | Local file/connection string. | TCP using the private Compose service name `db` and port `5432`. |
| Does the browser connect directly? | No. | No. The API is the only expected database client. |
| Is test data the Compose data? | Usually no; test fixtures isolate it. | Only if the API process is explicitly configured to use it. |
| Does switching URLs copy rows? | No. | No. A deliberate export/import or migration is required. |

A SQLAlchemy **engine** is the configured connection pool/dialect entry point. A **session** tracks a transaction and ORM objects during a unit of work. `get_db()` is a FastAPI dependency that supplies and closes a session. A **model** represents persisted Python data; a **schema** validates an API payload. A model change does not automatically alter an existing database.

## 7. The database, model, migration, seed, and UI must agree

A common mismatch chain looks like this:

```text
Frontend expects field A
  -> Pydantic schema accepts/returns field A
  -> route/service reads or writes model attribute A
  -> SQLAlchemy model declares column A
  -> database table must actually contain column A
  -> Alembic history must describe how the database got that column
  -> seed/test data must provide valid values for the same constraints
```

One layer can be changed while another stays stale. Symptoms include an `AttributeError` for a missing model field, a Pydantic validation error, a database “column does not exist” message, a unique/foreign-key constraint failure, or a frontend type/runtime mismatch.

### Safe diagnostic sequence

1. Capture the full first useful error, not only the last line.
2. Record which process returned it: browser, API, migration command, seed, or test.
3. Identify the exact environment and database URL without printing credentials.
4. Compare the database model, Pydantic schema, route, frontend type, and migration for the field involved.
5. Check migration state with `alembic current`, list declared heads with `alembic heads`, and inspect the revision chain with `alembic history` from the backend directory.
6. On a disposable database, run `alembic upgrade head` and the relevant tests; inspect generated SQL/schema before considering any real database.
7. If a model change is intended, create a focused revision with a descriptive message, review the generated migration, test both upgrade and downgrade where supported, and ensure the test exercises the new behavior.
8. If data must be transformed, write and review an explicit data migration; a schema change alone does not invent correct values.
9. Re-run seed only after confirming its preconditions and idempotency.
10. Verify the API response shape and the UI behavior after migration.

`backend/app/db_bootstrap.py` has a specific startup policy: if Alembic history exists it upgrades to head; if the database is truly empty it creates current model metadata and stamps the current head; if tables exist without Alembic history it refuses to initialize. That refusal is protective. Do not bypass it by editing `alembic_version`, manually adding columns, or stamping a database simply to make startup proceed. First determine the actual schema and migration lineage, then decide on a reviewed repair plan with a backup.

`seed.py` calls `Base.metadata.create_all()` and then inserts synthetic responses if their reference codes do not already exist. That makes seed data repeatable for the represented records; it does not turn `create_all()` into a production migration system. A seed can fail on a stale schema before its duplicate check, or violate new constraints if the fixture values are outdated.

### Commands are not magic repairs

- `alembic current`: observe the revision recorded by the selected database.
- `alembic heads`: observe declared current migration heads in the repository.
- `alembic history`: inspect revision order and parent links.
- `alembic upgrade head`: apply pending revisions to the database selected by the environment/configuration. It changes schema; use a disposable database first.
- `alembic revision --autogenerate -m "..."`: propose a migration based on model/schema comparison. The generated file is a draft and must be reviewed.
- `Base.metadata.create_all()`: create missing tables from current metadata; it is not a safe replacement for upgrading existing tables.
- `alembic stamp head`: change the migration marker without applying schema changes. Never use as a guessed fix.

Never run a migration against a valued database until the URL is positively identified, a restorable backup exists, the migration is reviewed, and a restoration path has been tested.

## 8. What the tests prove—and what they do not

`backend/tests/conftest.py` uses `os.environ.setdefault("DATABASE_URL", "sqlite://")`. `setdefault` means an existing process value wins. Its automatic fixture creates tables before a test and drops them after. Other tests may override `get_db` to use a dedicated in-memory SQLite engine. Read the fixture and the test; do not assume every test uses the same engine.

A safe PowerShell starting point is:

```powershell
Set-Location C:\Users\Admin\Documents\caseloop\backend
$env:DATABASE_URL = "sqlite://"
.\venv\Scripts\python.exe -m pytest -q
```

That setting applies to this PowerShell process and its child process. Do not paste a real connection string in a report or chat. The selected tests typically establish that a specific request, permission, and database behavior work with their fixtures. They do not prove that the local Compose database, Oracle network, TLS, Meta delivery, or production backup works.

For frontend verification:

```powershell
Set-Location C:\Users\Admin\Documents\caseloop\frontend
npm.cmd run build
```

This validates the configured TypeScript/Vite production build. It does not prove that the browser can reach a deployed API, that CORS/cookies are correct, or that a user flow is usable on a phone.

Record each check with: command, working directory, database/process selected, exact result, warning, and next step. A “pass” without the command and context is weak evidence.

## 9. Repeatable debugging for common failures

### API reports `sqlite` when you expected PostgreSQL

1. Call the exact API address shown in the browser or terminal.
2. Inspect the response's `database` field.
3. Check whether a local Uvicorn process and Compose API are both running.
4. Check `docker compose ps` and logs for the Compose API.
5. Verify the API container's environment variable names without printing secret values.
6. Resolve which process answered before changing `.env` or database contents.

### UI says offline or has no records

1. Check that the frontend server and API server are both running.
2. Use browser DevTools → Network: inspect request URL, method, status, and response.
3. Check `VITE_API_BASE_URL` and whether it is build-time or development configuration.
4. Check API logs, authentication state, role, and CORS response.
5. Only investigate DB persistence if the API itself reports a DB/query error.

### Migration says “already up to date,” but a column is missing

Likely possibilities: wrong database URL, migration history stamped too early, database was manually altered, migration was not included in the running image, or the column/model expectation is newer than the actual migration head. Compare `alembic current`, `heads`, `history`, model metadata, and the actual selected database. Do not immediately stamp or manually add a column.

### Seeding fails

Confirm the seed points to the intended synthetic database, an active coordinator/admin exists, schema migrations match the model, and required fields/constraints are satisfied. Read the exact traceback before rerunning. Seeding the wrong database can create real confusion even when records are synthetic.

### A test passes locally but UI fails

The test may use an in-memory dependency override while the UI calls another running API/database. Follow the actual browser request and compare that process's settings and data. A unit or integration test is evidence for its fixture, not every deployment.

### Webhook valid locally but provider cannot verify

Check public reachability, DNS, a trusted HTTPS certificate, callback path, challenge token match, and that the API process has the expected configuration. For POST failures, check exact raw-body signature verification, app secret, message format, size, and safe logs. Never disable signature checks to get a green test.

### Useful incident note template

```text
Date/time and environment:
Expected behavior:
Observed behavior:
Exact command/request and status:
First useful error:
Which database/process answered:
Files/layers inspected:
Hypothesis:
Smallest next experiment:
Result and follow-up:
```

## 10. Building the production frontend yourself

The current frontend is served by Vite during development. The backend already has a Dockerfile; the frontend Dockerfile, production web server/proxy, and Compose service are not yet present. The learning goal is to create these in small reviewable steps, not to paste a large opaque file.

### Before writing

1. Write acceptance criteria: a reproducible build serves the React app; browser routes fall back to `index.html`; API calls reach FastAPI; database remains private; only the edge proxy is published.
2. Inspect `frontend/package.json`, the lockfile, the current Vite build command, and `vite-env.d.ts`.
3. Inspect the backend Dockerfile and `docker-compose.yml` for established patterns.
4. Sketch the image stages and traffic flow on paper.

### Build-stage reasoning

The first image stage needs Node/npm, the lockfile, package metadata, and source. It should install the lockfile-pinned dependencies with `npm ci`, receive only the public API URL as a build argument/environment value, and run the existing production build. The output is a `dist` directory. The final runtime stage should be a small static server image that receives only `dist` and its server configuration—not Node development dependencies, Python, the database, or secret values.

### Runtime and proxy reasoning

A static server must serve normal files and return the single-page app entry point for client-side routes. The edge service should route `app.<domain>` to static files and `api.<domain>` to the internal `api:8000` service. Keep API and database out of public port mappings. Caddy can manage certificates when DNS and inbound connectivity are correct; persist the server's certificate/configuration data.

### Compose and browser settings

- Use `VITE_API_BASE_URL=https://api.<your-domain>/api` as a public build setting only.
- Set backend CORS to the exact browser origin, such as `https://app.<your-domain>`.
- Use production cookie security and verify CSRF/session behavior through HTTPS.
- Do not put database, Meta, or admin secrets in `VITE_` variables; Vite bundles those values into downloadable JavaScript.
- Publish only the reverse proxy's required web ports. Do not publish PostgreSQL's 5432.

### Small learning sequence

1. Build the image locally without deploying it.
2. Inspect build output and image logs for errors; do not print secret-bearing environment values.
3. Start only the frontend static server and check its HTML locally.
4. Add reverse-proxy routing and verify the API route from the local network.
5. Add the Compose frontend/proxy service and check `docker compose ps`/logs.
6. Test sign-in, a read, a permitted write, sign-out, and responsive phone layout.
7. Verify the database port is not published.
8. Only after local acceptance, prepare the cloud rehearsal.

When stuck, investigate the first failed layer: Docker build, static file serving, proxy DNS/routing, browser API URL, CORS/cookies, API, or database. Do not “fix” a frontend image by exposing the database or embedding server credentials.

## 11. Docker, networking, data, and recovery

| Docker concept | CaseLoop example | Operational meaning |
|---|---|---|
| Image | Backend image built from `backend/Dockerfile`. | Reproducible packaged template. |
| Container | Running API or PostgreSQL service. | Process instance; replaceable. |
| Compose service | `api` or `db`. | Named configuration and service-discovery identity. |
| Private network | Compose-created service network. | API can resolve `db` without exposing DB publicly. |
| Published port | Host-to-container mapping. | Makes a service reachable from the host/network; review before exposing. |
| Named volume | PostgreSQL data storage. | Survives container recreation; does not survive every host/disk failure. |
| Health check | Database readiness probe. | Signals readiness; not a backup or end-to-end feature test. |

`docker compose down` stops and removes Compose containers/networks but normally keeps named volumes. `docker compose down -v` removes named volumes and can delete the local database contents. Do not use the latter on data you want to retain.

A **backup** is a separately stored copy of recoverable data. A volume, snapshot on the same host, or `.env` file is not automatically a tested backup. A restore drill proves that the backup can be used. Before cloud use, document what is backed up, where it is stored, who can access it, how long it is retained, and how a restore is verified. For the learning deployment, use synthetic data.

Oracle Cloud does not require Docker. Docker is chosen for repeatable packaging. A VM still requires patching, firewall rules, HTTPS, access control, monitoring, backups, restore drills, and cost review. Free-tier labels and budget alerts do not guarantee zero cost or capacity.

## 12. Git and secret history

Git records selected file versions locally. GitHub receives commits only after a remote is configured and pushed. A private repository is not a password manager.

Before creating or publishing history:

1. Check `git status --short --branch`; confirm whether this folder is already a repository.
2. Inspect `.gitignore` and local file names.
3. Sanitize or exclude the known credential-bearing checkpoint and rotate any exposed credentials at their issuers.
4. Stage one reviewed set of files, not a blind whole-workspace add.
5. Inspect `git diff --cached --name-only`, `git diff --cached --check`, and the staged diff locally.
6. Commit only after confirming no `.env`, database, private key, credential, or real data is staged.
7. Push only after the history and remote visibility are understood.

If a credential reached Git history or another unintended location, editing the latest file does not revoke it. Rotate it first at the issuing service; history cleanup is a separate containment action. Never copy secrets from a checkpoint into comments, examples, reports, or a new file.

Useful everyday commands:

```text
git status
git diff
git diff --check
git add <reviewed-path>
git diff --cached
git commit -m "Describe one focused change"
git log --oneline
```

Learn what each command shows before using commands that rewrite history or delete files. A clean status is not proof the previous commit contains no secret; review the commit itself.

## 13. Credentials and safe configuration

Configuration describes how a service behaves. A secret grants access. `.env` can keep local settings out of Git when correctly ignored, but it is plain local text, not a vault.

Rotate at the issuer:

- CaseLoop account password: use the account password workflow.
- PostgreSQL role password: change it in PostgreSQL and update the API connection configuration in a coordinated way.
- Meta verify token: update the API and Meta configuration to the replacement.
- Meta app secret: generate/rotate it in Meta and update the API secret setting.
- Cloud SSH key: add a replacement public key, prove new access, then remove the old one.

Record identifier, issuer, date, reason, verification, old credential revocation, and responsible owner—not the credential value. Do not rotate a production database password by changing only `POSTGRES_PASSWORD` in `.env`; an already-initialized database keeps its existing role password.

## 14. WhatsApp and human review

The current integration accepts supported text through the official webhook path. It verifies the Meta challenge, checks a signed POST, rejects unsupported/malformed input safely, and deduplicates by provider message ID. Accepted items remain pending for a coordinator.

Learn the flow with tests before configuring a provider. Useful test cases include valid signature, invalid signature, malformed JSON, duplicate message ID, unsupported message type, no text, size boundary, unauthorized approval, and approval with/without an assignment. A retry should not create multiple drafts. An untrusted message must not trigger assignment or publication automatically.

A real provider test also depends on a public callback, trusted HTTPS, domain/DNS, Meta app configuration, an approved test recipient, and safely configured secrets. A localhost test does not prove any of those external pieces. This app does not read arbitrary existing group history; do not use scraping or unofficial workarounds.

## 15. Admin and responsive navigation

The main app has a desktop sidebar and a mobile **More** menu. Admin's internal sections currently use a separate horizontal row. It is not an iframe. Before changing it:

1. State the phone and desktop acceptance criteria.
2. Inspect `MainLayout.tsx` and `AdminControl.tsx` to find which component owns selected-section state.
3. Preserve role checks and browser navigation behavior.
4. Keep active-section feedback, keyboard access, and readable labels.
5. Test at a narrow viewport and desktop, with coordinator/admin roles.
6. Keep the existing row if users can operate it comfortably; do not refactor only for visual novelty.

This is a good self-directed exercise because it teaches state ownership, responsive layout, navigation, accessibility, and role-aware UI. The UI must never be treated as the authorization boundary; the API still decides.

## 16. How to write a useful report or issue summary

Do not start with a dramatic conclusion. Write a traceable account:

1. **Context:** app version/branch, local or deployed environment, and goal.
2. **Expected behavior:** one testable sentence.
3. **Actual behavior:** exact result, status, or user-visible symptom.
4. **Evidence:** safe command, test, log excerpt, screenshot, or request/response (redact secrets and personal data).
5. **Layer:** frontend, API, database, migration, Docker, provider, or unclear.
6. **Investigation:** files and checks actually performed.
7. **Root cause:** only after evidence supports it; otherwise say “not yet identified.”
8. **Change:** exact paths/behavior changed, with a small diff.
9. **Verification:** exact command and outcome, including warnings/failures.
10. **Limitations and next action:** what remains unverified, who owns it, and the next safe experiment.

For a database mismatch, explicitly state the selected database, Alembic current revision and heads, affected model/schema/table, and whether a backup/restore test exists. Never report that a migration “fixed it” based only on the server starting.

## 17. How to become independent without banning AI

For each task:

- First spend 15–20 minutes describing the behavior, reading the closest test/code, and making a prediction.
- Use local search, official documentation, and error messages next.
- Ask a person for a hint or compare your hypothesis with a peer.
- Use AI only if it is useful; ask for an explanation/test idea/review and omit secrets.
- Verify suggestions against code, tests, and observed behavior.
- Rewrite the explanation in your own words, and make the next similar attempt without help.

AI output is a proposal, not evidence. It can speed up boilerplate and search, but can introduce subtle bugs and review work. Manual practice builds durable mental models, but may be slower for routine tasks. Track the time saved versus time spent verifying and fixing; adapt based on your own results, not universal percentages or predictions about future pricing.

You do not need to memorize every file. You need to know how to locate the owning layer, trace a request, use tests to constrain a change, inspect a diff, recover safely, and ask a precise question when blocked.

## 18. Readiness gates

### Local learning gate

- You can start and stop API, frontend, and Compose without assistance.
- The API health response reports the database you intended.
- You can explain the browser → API → ORM → DB path.
- You can run focused tests and name their database fixture.
- You can make one small change, inspect the diff, and explain the result.

### Public demo gate

- Secret-bearing history is sanitized/excluded and affected credentials rotated.
- The production frontend and HTTPS proxy have been built and tested locally.
- CORS, secure cookies, session/CSRF, and role enforcement are verified.
- PostgreSQL is not publicly exposed.
- Backup/restore is tested and synthetic data is used.
- Phone and desktop browser flows work.
- Provider webhook uses official test configuration and keeps messages pending for review.
- You can clearly state what has not been tested or approved.

### Organizational use gate

A learning deployment is not approval for humanitarian operations. Obtain written organizational and university guidance on data ownership, consent, retention, access, incident handling, backups, availability, oversight, and whether the tool may be used at all. Never imply Red Cross endorsement or use protected marks without authorization.

## 19. Existing guides: use the right one

- [Completion roadmap](./caseloop-completion-roadmap.md): current gates and progress checklist.
- [Two-week learning lab](./caseloop-two-week-learning-lab.md): immediate session-by-session practice.
- [Independent learning program](./independent-learning-program.md): broader 12-week curriculum and offline-first approach.
- [Oracle and WhatsApp runbook](../deployment/oracle-whatsapp-learning-runbook.md): secrets, local PostgreSQL, GitHub preparation, Oracle, HTTPS, and Meta's test path.
- [Attachment logbook and report draft](./attachment-logbook-and-report-draft.md): dated evidence register, guide-aligned report structure, and assessment coordination.
- [Personal roadmap](./caseloop-personal-roadmap.md): bounded planning for placement, income, projects, and rest.
- [CaseLoop overview](../projects/caseloop/OVERVIEW.md): intended product workflow, implemented capability, and limits.
- [Implementation notes](../projects/caseloop/IMPLEMENTATION.md): implementation-specific record.
- [Design checklist](../design/checklist.md): product, deployment, and acceptance tasks.
- [Student Attachment Guide](./Student%20Attachment%20Guide%20updated%20Jan2021.pdf): academic logbook and report requirements. Confirm the current department's template and assessment rules.

## 20. Personal field notes

Use this blank form after each session:

```text
Date and duration:
Goal:
What I personally read, changed, or tested:
Expected / actual:
Evidence (command, test, or observation):
What I can now explain without notes:
What remains uncertain:
Next experiment:
```

Use this blank form after debugging:

```text
Symptom:
Reproduction:
First useful error:
Process/database/environment:
Evidence:
Hypothesis:
Experiment:
Result:
Regression check:
```

Keep the notes factual. Do not backfill hours or claim a live deployment, message, assessment, or test that did not occur.
