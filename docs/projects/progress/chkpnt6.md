# CaseLoop Checkpoint 6 — Secure Access and Coordinator Workflow

**Date:** November 13, 2026  
**Status:** Implemented and verified locally; manual signed-in UI workflow remains available after administrator provisioning.  
**Purpose:** Turn the project from a role-gated prototype into a useful coordinator/admin workflow while retaining offline operation and requiring human review.

## What changed

- Replaced the old keyword/weak-token access pattern with named email/password accounts, PBKDF2-HMAC-SHA256 password hashes, opaque revocable server sessions, HttpOnly cookies, CSRF checks, and server-side role dependencies.
- Initially removed self-registration. The first admin is created with `python -m app.create_admin`; admins provision accounts with one-time temporary passwords and can reset another user's password. Temporary accounts must change their password at first sign-in.
- Added coordinator/admin permissions for response CRUD, intake review, reports, account status/roles, team CRUD, memberships, and administrative activity. Responders have limited response visibility and can move only their own team's assignments through allowed lifecycle transitions.
- Added user attribution to assignment lifecycle events. Team and account changes create admin activity records.
- Added a practical admin workspace with operational sections, response/assignment/intake/report access, account provisioning/reset, team membership and roles, and system status.
- Added report preview beside the Word report download.
- Added a Meta WhatsApp Cloud API webhook with challenge verification, HMAC signature checks, text-only intake, and duplicate-message handling. It creates pending drafts only; there is no sending, arbitrary group-history reading, approval, or automatic assignment.
- Coordinators can now approve an intake into the Response Register and optionally choose a team to create its linked assignment in the same transaction. The timeline records both actions.
- The timeline now loads a global event feed by default, supports per-response filtering, identifies the response and actor, and explains how to generate activity when the feed is empty.
- Expanded Reports & Analysis in the main navigation with date/team filters, response priority/category/source breakdowns, unassigned-active-response signals, filtered preview, and a matching Word export. The same report view remains available as an Admin shortcut.
- The everyday Response Register is read-only. Create/edit/delete controls are confined to Admin → Response records; the API still restricts deletion to administrators.
- Restored the original landing-page CTA behavior: “Launch Dispatch Portal” opens a registration form, while the top navigation remains the sign-in entry point.
- Enabled public registration for active responder-only accounts. The server rejects role selection, assigns the responder role, and signs the new account in; coordinator/admin privileges remain admin-provisioned.
- Moved the normal profile password form behind an expandable “Change password” security card. Required temporary-password changes remain mandatory before workspace access.
- Added the Alembic revision `83af72d6d204` for auth sessions, required-password-change state, and team memberships.
- Clarified SQLite vs. PostgreSQL: SQLAlchemy remains the ORM; Docker Compose provides local PostgreSQL/API, not hosting or SQLite migration.

## Verification

- Backend suite: **22 passed** using `.\venv\Scripts\python.exe -m pytest -q` from `backend` (7 dependency deprecation warnings).
- Frontend type-check and production build: **passed after the profile-card change** using `npm.cmd run build` from `frontend`.
- Rebuilt Docker API is online against PostgreSQL 16; report preview and Word export routes are registered, Alembic revision `83af72d6d204` is confirmed as head, and the root health endpoint reports PostgreSQL.
- Vite returned HTTP 200 on `http://127.0.0.1:5173`; the browser confirmed “Launch Dispatch Portal” opens the registration form and the sign-in entry remains available. The React 18.3.1 and Vite 5.4.21 packages are installed from the frontend lockfile/manifest.
- A same-Wi-Fi phone-preview configuration was tested from the PC, including frontend-to-API CORS access. The active Wi-Fi profile is marked Public, so the LAN listeners were shut down and Docker restored to `127.0.0.1:8000`; relaunch only after using a trusted Private network.
- Sign-in and end-user operation have automated API test coverage. No administrator was provisioned during this task, so the authenticated browser workflow still needs a local admin account.

## Local test setup

For SQLite, start the API from `backend` and create an admin using the interactive CLI:

```powershell
Set-Location backend
.\venv\Scripts\python.exe -m uvicorn app.main:app --reload --port 8000
.\venv\Scripts\python.exe -m app.create_admin
```

For PostgreSQL, run `docker compose up --build -d` from the project root and then `docker compose exec api python -m app.create_admin`. Start Vite from `frontend` with `npm.cmd run dev -- --host 127.0.0.1`. No default credentials are provided or committed.

## Not yet complete / operational gates

- No Meta developer app credentials, approved recipient, public HTTPS endpoint, or live provider test are configured. The test fixture is synthetic and proves only local webhook code.
- CaseLoop is intended to complement a Volunteer Management System (VMS), not replace its volunteer identity, eligibility, or lifecycle records. No named VMS product or integration was supplied or implemented.
- No Git remote, hosting account, public deployment, or public DNS name is configured. Candidate low-cost demo providers are not selected or confirmed against current quotas.
- Do not use real beneficiary or operational data until the organization authorizes the system and data handling. Public deployment still requires independent security/privacy review, login abuse protection, monitoring, exact HTTPS/CORS/secret configuration, migration testing, backups, and a restore drill.
- The Compose database does not import the local SQLite database. Review and test migration history on both engines before real data.
- Report metrics are deterministic. AI-assisted extraction or summarization, if later added, must remain advisory and human-reviewed.

## Recommended next sequence

1. Run the interactive admin-provisioning command in the root README, sign in, and manually exercise account/team administration, password change, report preview/download, and assignment workflow.
2. Keep the WhatsApp fixture test as a synthetic test. Only begin a real Meta test after setting up the Meta test number/recipient and a temporary HTTPS callback with synthetic traffic.
3. Decide an approved demo/organizational host and privacy owner before publishing. Do not treat free-tier availability as operational readiness.

## References

- [Project setup and verification commands](../../../README.md)
- [Implementation notes](../caseloop/IMPLEMENTATION.md)
- [Deployment and WhatsApp setup](../../deployment/DEPLOYMENT.md)
- [Updated product overview](../caseloop/OVERVIEW.md)
