# CaseLoop

CaseLoop is an offline-first coordination notebook for humanitarian response teams. It helps coordinators review incoming reports, publish response records, assign teams, track a timestamped operational timeline, and prepare reports. It complements WhatsApp and does not replace Red Cross systems. Organizational approval is still required before any operational data is entered.

> **Want to host the full Docker stack for a synthetic demo?** Follow the [Oracle and WhatsApp learning runbook](docs/deployment/oracle-whatsapp-learning-runbook.md). For a simpler hosted demo, see the [Render and Neon guide](docs/deployment/DEPLOYMENT.md#hosting-guide-live-demo-with-render-and-neon).
>
> **Preparing a project presentation?** Open the [CaseLoop design pack](docs/design/README.md) for editable slides, Figma-importable mockups, diagrams, a checklist, and documentation plan.
>
> **Learning to maintain CaseLoop independently?** Follow the [offline-first, learn-by-doing program](docs/training/independent-learning-program.md), with practical testing, debugging, WhatsApp, and hosting exercises.
>
> **Ready for hands-on practice?** Use the [two-week CaseLoop learning lab](docs/training/caseloop-two-week-learning-lab.md) to trace, test, and improve one workflow yourself.
>
> **Want one completion checklist for the project and training?** Follow the [CaseLoop Completion Roadmap](docs/training/caseloop-completion-roadmap.md).
>
## Current capabilities

- Email/password sign-in with revocable server-side sessions, password hashing, CSRF protection, and role-based API permissions.
- A separate `/admin` sign-in entry for administrator accounts; coordinator and admin access is still enforced by server-side roles.
- Administrators provision accounts and teams, manage team memberships and roles, deactivate accounts, and reset passwords. Temporary passwords are displayed once and require a change at first sign-in.
- Coordinators review submitted text before it becomes an operational response. Responders have read-only response access and can advance assignments only for their own team.
- Responses and assignments produce a timestamped event timeline. Assignment transitions are enforced by the API.
- Coordinators and admins can open Reports & Analysis from the main navigation. Reports include weekly activity trends, recorded-location coverage and missing-location counts, three report formats, and matching Word exports.
- An optional official Meta WhatsApp Cloud API webhook accepts signed, text-only inbound messages as pending intake drafts. It does not read arbitrary group history, send messages, approve intakes, or create assignments.

This is a demo/development foundation, not a production-approved system. Use synthetic data until security, privacy, retention, recovery, and organizational reviews are complete.

## Stack and data modes

- Backend: Python 3.11, FastAPI, SQLAlchemy, Alembic.
- Frontend: React 18, TypeScript, Vite.
- SQLite is the local, single-workstation/offline option.
- PostgreSQL is the shared-database option. Docker Compose runs PostgreSQL and the API locally with a persistent Docker volume.
- SQLAlchemy is the ORM in both database modes. PostgreSQL did not replace SQLAlchemy.

## Local setup (Windows PowerShell)

Use the existing project virtual environment and `frontend/node_modules` when available.

```powershell
# Terminal 1: API using local SQLite
Set-Location backend
.\venv\Scripts\python.exe -m uvicorn app.main:app --reload --port 8000

# Terminal 2: React development server
Set-Location frontend
npm.cmd run dev -- --host 127.0.0.1
```

Open `http://127.0.0.1:5173`. Create the first local administrator in another terminal:

```powershell
Set-Location backend
.\venv\Scripts\python.exe -m app.create_admin
```

The CLI prompts for the administrator's email, name, and a password of at least 12 characters. It can also reset/promote an existing account by email. The landing page's **Launch Dispatch Portal** button opens public registration; new accounts are limited to the responder role. Coordinator and administrator accounts remain provisioned by an administrator. The CLI setup does not require default credentials.

Do not run `.\venv\Scripts\python.exe -m app.seed` or `docker compose exec api python -m app.seed`. The current seeder creates built-in default accounts, contrary to its existing guard test, which currently fails. Use the UI or isolated test fixtures for synthetic data until the seeder is corrected and re-verified.

## Local PostgreSQL with Docker

Docker Desktop must be installed and running. From the project root:

```powershell
Copy-Item .env.example .env
# Replace the example local-only database password in .env.
docker compose up --build -d
docker compose exec api python -m app.create_admin
```

The API is at `http://localhost:8000`; OpenAPI docs are at `http://localhost:8000/docs`. Run the Vite command above in a separate terminal for the UI. The regular sign-in is at `http://127.0.0.1:5173/`; the dedicated admin entry is `http://127.0.0.1:5173/admin`. PostgreSQL data persists in the `postgres_data` volume. `docker compose down` stops containers but preserves that volume; do not use `down -v` unless you intend to delete its data. Do not expose port 5432 to the internet.

The Compose setup does not migrate the local SQLite database into PostgreSQL and does not publish the app to the internet.

For a phone preview on the same trusted Wi-Fi, see the [same-Wi-Fi instructions](docs/deployment/DEPLOYMENT.md#same-wi-fi-phone-preview-not-public-hosting). This is not a public deployment.

## Verification

```powershell
# Backend tests
Set-Location backend
.\venv\Scripts\python.exe -m pytest -q

# Frontend type-check and production build
Set-Location ..\frontend
npm.cmd run build
```

## WhatsApp test path

The code supports Meta's webhook verification challenge and `X-Hub-Signature-256` validation. To receive a real test message, configure a Meta developer app with the WhatsApp product and its provided test number, add an approved test recipient, configure a publicly reachable HTTPS callback ending in `/api/webhooks/whatsapp`, set the `messages` webhook field, and set `WHATSAPP_VERIFY_TOKEN` plus `WHATSAPP_APP_SECRET` as environment secrets. Never commit secrets or use real beneficiary information for setup tests.

Meta's test number and recipient are the correct first integration test. A local-only callback is not reachable by Meta; any temporary HTTPS tunnel must be explicitly opened, limited to synthetic test traffic, and shut down after testing. No public callback or live WhatsApp test has been verified in this workspace.

See Meta's [Cloud API getting-started guide](https://developers.facebook.com/documentation/business-messaging/whatsapp/get-started) and [webhook setup guide](https://developers.facebook.com/docs/graph-api/webhooks/getting-started).

## Hosting and operational readiness

An `origin` Git remote is configured, but no public deployment or live WhatsApp connection has been verified in this workspace. A possible synthetic demo stack is a static frontend host, a container-capable API host, and managed PostgreSQL; free-tier availability and limits change and must be confirmed at deployment time. Do not put real humanitarian or personal data on an unapproved free tier.

Before any public or organizational deployment: apply and test schema migrations on a restored copy; add login abuse protection and operational monitoring; configure HTTPS, secure cookies, exact CORS origins, secret management, backups and restore drills; define data retention and access procedures; and obtain the organization's approval. For cookie-based auth across separate hosts, use same-site custom subdomains and explicitly allow the frontend origin.

For a step-by-step synthetic demo deployment, see the [deployment and hosting guide](docs/deployment/DEPLOYMENT.md).

## Product direction

Keep the human-reviewed flow: original unstructured text → coordinator review and correction → approved response board → team assignment → accountable timeline → traceable report. Deterministic reporting is the default; optional AI may suggest fields but must never silently approve or dispatch. WhatsApp is an intake channel, not an unrestricted group-history feed.

When a coordinator approves an intake, it is published to the Response Register. They can either publish it without an assignment or select a team and create the linked assignment in the same reviewed action. The assignment and approval appear in the timeline.

## How CaseLoop complements a VMS

Assuming VMS means a volunteer management system, CaseLoop should complement it rather than duplicate it:

| Volunteer management system | CaseLoop |
| --- | --- |
| Authoritative volunteer profiles, recruitment, credentials, training, availability, and volunteer lifecycle | Incident/intake review, response records, operational team assignments, status history, and situation reports |
| Owns volunteer identity and eligibility data | Uses only the minimum team membership needed to route and track response work |
| May provide a roster source if approved | Does not currently integrate with a VMS |

Keep the VMS as the source of truth for people. Before any integration or roster import, agree with the organization on the specific VMS, data owner, access, retention, and approved API/export. No particular VMS product was supplied, so this is a boundary comparison, not a feature-by-feature vendor assessment.

See [deployment guide](docs/deployment/DEPLOYMENT.md), [implementation notes](docs/projects/caseloop/IMPLEMENTATION.md), [product overview](docs/projects/caseloop/OVERVIEW.md), and [Checkpoint 6](docs/projects/progress/chkpnt6.md).

---

### README and logbook timing
Do not wait until Oracle hosting and WhatsApp are complete. Maintain:

A small current README now.

An audit file for uncertain or stale claims.

Deployment and WhatsApp documentation as separate guides.

A final readiness update only after live hosting and integration testing.

For the logbook, wait until the end of the workday or a natural stopping point. Your previous summary supports an estimated eight-hour session, but record that as estimated unless you tracked exact time. The sub-50-word template is suitable; use it after each completed session, not after every interaction.
