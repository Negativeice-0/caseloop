# CaseLoop Completion Roadmap

This page is the single progress map for learning, local verification, a synthetic hosted demo, and the attachment record. It distinguishes code that exists from work personally verified. Check an item only after you perform and record it.

## Current state at a glance

### Implemented in the codebase

- React 18 / TypeScript frontend and Python 3.11 / FastAPI API.
- SQLAlchemy database selection through backend `DATABASE_URL`.
- SQLite as the local default and PostgreSQL/API services in Docker Compose.
- Email/password access, roles, intake review, response register, assignments, timeline, reports, and admin controls.
- Official WhatsApp text webhook verification/signature checks, duplicate handling, and pending intake storage.
- Tests covering webhook verification, valid signed intake, duplicate delivery, approval, and assignment.
- Frontend intake review that loads drafts from the API.

### Not yet personally verified in the current learning sequence

- Starting Docker and confirming the API health response reports `postgresql`.
- Running the webhook tests and explaining their database fixtures.
- Verifying the UI against the Docker PostgreSQL API.
- Making and reviewing an independent code change.

### Not yet ready or configured for a live demo

- There is no `frontend/Dockerfile`, production frontend container, or HTTPS proxy configuration in the current Compose setup.
- No Oracle VM, DNS/TLS configuration, or live Meta webhook test has been completed.
- The UI does not push newly arriving webhook drafts to an already-open Intake Review page; reopen or refresh the view.
- Checkpoint 10 contains exposed credentials and must be redacted/excluded before GitHub; rotate the affected credentials at their issuers before deployment.
- Git is installed, but PowerShell needs Git's `cmd` directory on `PATH` or you can use Git Bash.

This is a functioning local product foundation, not a production-approved operational system. Do not enter real response or personal data into a learning deployment.

## Document map

| Document | Use it for |
| --- | --- |
| [README](../../README.md) | Current capabilities, stack, local startup, tests, and product boundaries. |
| [CaseLoop overview](../projects/caseloop/OVERVIEW.md) and [implementation notes](../projects/caseloop/IMPLEMENTATION.md) | Product purpose, current architecture, and intended workflow. |
| [Design pack index](../design/README.md), [workflow diagram](../design/workflow.mmd), [architecture diagram](../design/architecture.mmd), and [presentation](../design/CaseLoop_Stakeholder_Design_Brief.pptx) | Stakeholder explanation and editable system/design concepts. |
| [Design and operational checklist](../design/checklist.md) and [documentation plan](../design/documentation-plan.md) | Product acceptance, student attachment items, and future documentation needs. |
| [Deployment guide](../deployment/DEPLOYMENT.md) | Existing local setup, API details, WhatsApp limits, and the simpler Render/Neon alternative. |
| [Oracle and WhatsApp runbook](../deployment/oracle-whatsapp-learning-runbook.md) | Credential rotation, Docker PostgreSQL verification, safe GitHub preparation, Oracle architecture, HTTPS, and Meta's test flow. |
| [Independent learning program](./independent-learning-program.md) | Broader 12-week software-engineering curriculum. |
| [Two-week learning lab](./caseloop-two-week-learning-lab.md) | Immediate daily exercises that use the CaseLoop code and tests. |
| [Independent engineering handbook](./caseloop-independent-engineering-handbook.md) | Plain-language glossary, file connections, database/migration debugging, and production learning gates. |
| [Attachment logbook and report draft](./attachment-logbook-and-report-draft.md) | Eight-week dated register, honest placeholders, report structure, and assessment coordination. |
| [Dedicated attachment final report](./attachment-final-report-draft.md) | Report organized to match the final page of the Student Attachment Guide. |
| [Personal roadmap](./caseloop-personal-roadmap.md) | A bounded plan balancing placement, CaseLoop, sales, startup exploration, finance learning, and rest. |
| [Student Attachment Guide](./Student%20Attachment%20Guide%20updated%20Jan2021.pdf) | Logbook, weekly summary, and final attachment report expectations. |
| [Checkpoint 10](../projects/progress/chkpnt10.md) | Earlier project history only. It must not be published until the exposed credential values are redacted; rotate them before any live deployment. |

Use the two-week lab for daily work, this roadmap to track completion, the runbook for deployment operations, and the Student Attachment Guide for academic reporting. Do not use a checkpoint as a place to store credentials.

## Completion checklist

### Phase 1 — Safe starting point

- [ ] Choose one shell for the project: PowerShell with Git on `PATH`, or Git Bash. Avoid mixing Windows Git and WSL Git on the same working tree.
- [ ] Verify `git --version`, `docker version` (client and server), and `docker compose version`.
- [ ] Check whether a local `.env` already exists; never overwrite it blindly.
- [ ] Replace the `.env.example` placeholder only in a local ignored `.env`; do not commit real credentials.
- [ ] Redact exposed values from Checkpoint 10 or exclude that checkpoint from the initial repository.
- [ ] Rotate the exposed credentials at their issuing services. Replacing text in a file alone does not invalidate a credential.
- [ ] Review `.gitignore`; verify local `.env`, databases, `venv`, and `node_modules` will not be staged.
- [ ] Keep all learning records, screenshots, and tests synthetic.

**Gate:** No code change or GitHub push until secret handling is understood and the credential-bearing checkpoint is excluded or sanitized.

### Phase 2 — Run the complete local stack

- [ ] Start Docker Desktop's engine if it is not already running.
- [ ] Start Compose from the project root and inspect `docker compose ps` and service logs.
- [ ] Call `http://localhost:8000/` and confirm `database` is `postgresql`.
- [ ] Start Vite separately and open `http://127.0.0.1:5173`.
- [ ] Explain which process serves the UI, which serves the API, and which runs PostgreSQL.
- [ ] Stop with `docker compose down`; do not use `down -v` on data you want to keep.
- [ ] Explain that Compose configuration describes services, while the named volume stores PostgreSQL data; neither is a backup.

**Gate:** You can start, observe, and safely stop the app without an assistant operating the commands.

### Phase 3 — Trace, test, and improve one feature

- [ ] Trace `DATABASE_URL` from `config.py` to `engine`, `SessionLocal`, `get_db`, and a FastAPI route.
- [ ] Trace the webhook through `webhooks.py`, `IntakeSubmission`, the intake API, the frontend API client, and Intake Review.
- [ ] Run the focused webhook/intake tests with SQLite and describe which test database each fixture uses.
- [ ] Run the full backend suite and frontend build; record exact results.
- [ ] Add one focused test for a boundary case and explain its expected result.
- [ ] Make one small useful UI improvement yourself, such as a manual **Refresh drafts** control.
- [ ] Review the diff, run the focused verification, run the frontend build, and manually verify in the browser.
- [ ] Explain the change without reading an AI-generated explanation.

**Gate:** A test and a small change are both understandable and independently verified.

### Phase 4 — Responsive admin navigation exercise

The global navigation is responsive: desktop has a sidebar and mobile has a **More** menu. Admin's internal sections are currently a separate horizontally scrolling row; it is not an iframe. Decide on a design before coding:

- Desktop: keep the main sidebar and place admin subsections in a nested/expandable admin section or a narrow secondary navigation.
- Mobile: expose admin subsections in the **More** menu or an accessible menu opened from the admin view, not as seven cramped bottom-navigation buttons.
- Preserve role checks, visible active state, keyboard access, and browser back/forward expectations.

Then:

- [ ] Write the acceptance criteria and sketch desktop/mobile states.
- [ ] Inspect `MainLayout.tsx` and `AdminControl.tsx`; identify where active-section state currently lives.
- [ ] Make the smallest change that keeps the selected section synchronized with the responsive navigation.
- [ ] Verify at a narrow phone viewport and a desktop viewport, with keyboard navigation and both coordinator/admin roles.
- [ ] Keep the existing horizontal row if testing shows it is usable; do not refactor only to make the code look different.

This is a good learning feature because it teaches React state, responsive layout, navigation, and accessibility while improving a real interaction.

### Phase 5 — Safe local Git history and private GitHub

- [ ] Confirm the workspace is not already a repository before running `git init`.
- [ ] Stage only reviewed paths; do not use `git add .` as a first step.
- [ ] Ensure Checkpoint 10 is excluded or sanitized before staging.
- [ ] Inspect staged filenames and the complete staged diff locally; do not paste secret-bearing output into chat.
- [ ] Make a small local commit and inspect it with `git log`.
- [ ] Create a private GitHub repository only after the secret review.
- [ ] Push without putting a token in a URL, source file, or command history.
- [ ] If any secret is ever pushed, rotate it first; history cleanup is additional containment, not a substitute.

**Gate:** You can tell which files are in a commit and explain what GitHub will receive.

### Phase 6 — Production frontend and Oracle rehearsal

- [ ] Review Oracle resource pricing/tier labels and the region's capacity before creating resources.
- [ ] Create cost alerts while remembering they are soft alerts, not hard spending caps.
- [ ] Choose a domain/DNS plan; valid public HTTPS normally requires DNS and a trusted certificate.
- [ ] Create `frontend/Dockerfile`: use a Node build stage to run the Vite production build, then a static web server stage to serve `dist`.
- [ ] Configure the frontend build with `VITE_API_BASE_URL=https://api.<your-domain>/api`; this URL is public configuration, never put a database password or other secret in a `VITE_` variable.
- [ ] Add a production frontend/proxy service to Compose. One simple design uses Caddy to serve the built frontend for `app.<your-domain>` and proxy `api.<your-domain>` to `api:8000`.
- [ ] Persist Caddy's certificate/configuration data and publish only its HTTP/HTTPS ports; keep PostgreSQL private and the API off public interfaces.
- [ ] Configure the frontend's build-time API URL, backend exact CORS origin, production cookie security, and secret values.
- [ ] Keep API/database ports private; publish only the HTTPS proxy (and HTTP only as needed for certificate setup). Never expose port 5432 publicly.
- [ ] Check Docker image/dependency compatibility with the chosen VM architecture.
- [ ] Verify API health reports PostgreSQL through the public API hostname.
- [ ] Sign in on the PC and phone using synthetic data.
- [ ] Practise and verify a database backup/restore before treating the host as dependable.
- [ ] Check the OCI cost/usage view after provisioning and after changes.

**Gate:** Hosted login, session cookies, API requests, role permissions, and database access all work over HTTPS from two devices.

### Phase 7 — Live Meta test and end-to-end demo

- [ ] Create/configure Meta's WhatsApp developer app and its official test number.
- [ ] Add an approved test recipient.
- [ ] Configure the HTTPS callback and matching verify token; put the Meta app secret only in the API's secret environment.
- [ ] Verify the callback challenge and subscribe to the `messages` webhook field.
- [ ] Send a synthetic direct message to the test number.
- [ ] Confirm it appears as a pending intake, not automatically in the Response Register.
- [ ] Refresh Intake Review, review/correct the draft, and approve it.
- [ ] Confirm response, optional assignment, and timeline appear; verify responder read-only behavior in another browser.
- [ ] Test retries/duplicates, invalid signatures, unsupported messages, failure states, and role denial on disposable staging.
- [ ] Revoke temporary credentials/tunnels and review Oracle usage after the test.

**Gate:** You can explain and demonstrate every step from message receipt to human-reviewed publication without claiming arbitrary group scraping.

### Phase 8 — Attachment and stakeholder completion

- [ ] Keep the daily logbook factual: work done, skill learned, evidence, and next task.
- [ ] Add diagrams/screenshots only when appropriate and use synthetic information.
- [ ] Prepare the weekly summary and request supervisor feedback.
- [ ] Demonstrate the workflow and explain limitations, unresolved issues, and deployment costs honestly.
- [ ] Obtain organizational approval before operational or personal data is used.

## Founder-style AI policy for this project

There is no reliable universal percentage that predicts future developer productivity or AI pricing. Use this as a **two-week learning experiment**, not an industry statistic:

- **70%** of practice effort: you define behavior, read code/docs, write tests or code, and debug independently.
- **20%**: use AI for a targeted hint, explanation, test idea, or review after your attempt.
- **10%**: let AI draft repetitive boilerplate only when you can inspect and explain it.

Record whether AI saved time after review/fixes or created rework. Change the split based on your evidence. The lasting goal is not “never use AI”; it is being able to deliver and maintain the system if AI is unavailable, costly, wrong, or disallowed.
