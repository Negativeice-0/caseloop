# CaseLoop Checkpoint 8 — Discoverable Admin and Deployment Guidance

**Date:** November 13, 2026  
**Status:** Implemented and locally verified.

## What changed

- Confirmed the open browser session is a responder account. Reports and Admin are intentionally role-gated; the responder UI now explains this in the mobile **More** menu.
- Added a dedicated `/admin` sign-in entry. It uses the existing email/password session and backend role authorization; responder/coordinator credentials cannot enter the admin-only sign-in.
- Reworked mobile navigation to expose **More**, with Intake, Reports, Profile, Admin (when authorized), and Sign out/switch-account actions.
- Made the report preview open by default so weekly trends, recorded-location coverage, missing-location counts, and report-template selection are visible when a coordinator/admin opens Reports.
- Added Timeline to Admin. It remains immutable/read-only audit history; corrections are made through response or assignment management and recorded as new events.
- Added edit support for draft assignments. Once a task is assigned, its details cannot be rewritten; lifecycle status changes continue to append timeline events. Response CRUD stays in Admin → Response records.
- Added `backend\.python-version` to preserve Python 3.11 for Render and documented a Render Static Site/Web Service + Neon Free Postgres demo deployment, including cookies, CORS, secrets, admin provisioning, and WhatsApp test setup.

## Verification

- Backend suite: **29 passed** with 7 existing dependency deprecation warnings.
- Frontend TypeScript check and production build: **passed**.
- Docker API rebuilt and healthy against PostgreSQL 16; the Vite UI returned HTTP 200.
- Browser check confirmed the current signed-in role is `responder`, and the mobile **More** menu now states why Reports/Admin are hidden and offers sign-out/switch-account.

## Operational notes

- Provision an administrator through `docker compose exec api python -m app.create_admin`; use a dedicated admin email if possible. No admin credentials were created in this task.
- Public hosting and Meta WhatsApp delivery are not active. The runbook gives a provider setup path, but GitHub/Render/Neon accounts and Meta credentials must be supplied by the owner.
- The WhatsApp integration is an official webhook for the configured Business/test number, not a crawler for personal chats or arbitrary groups.
- Use synthetic data only. Free hosting is for preview/testing, not operational Red Cross data or a service-availability commitment.

## References

- [Deployment and hosting guide](../../deployment/DEPLOYMENT.md)
- [Implementation notes](../caseloop/IMPLEMENTATION.md)
- [Project overview](../caseloop/OVERVIEW.md)
