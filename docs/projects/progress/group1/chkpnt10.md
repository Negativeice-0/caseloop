# Checkpoint 10: First Admin, Auth Layout, Hosting, and Learning Plan

**Date:** November 13, 2026  
**Status:** Implemented and locally verified.

## What changed

- Removed the duplicate Administrator sign-in button next to Sign In. The landing page keeps the administrator link beneath **Launch Dispatch Portal**.
- Let the auth navigation span the available page width, placing the CaseLoop mark at the left and Sign In at the right on wide screens.
- Bootstrapped the first administrator in the Docker-backed PostgreSQL database. The account is active and has the admin role; personal account details and password are intentionally omitted here. The Windows non-TTY pipe did not work with Python `getpass`, so the account was created in Docker using the project's password-hashing function and User model after confirming the email was unused and there were no admins.
- Required a password change at the first admin sign-in because the bootstrap password had been shared in chat. The account will show the password-change screen before entering the workspace.
- Expanded the deployment guide with the least-complex Render + Neon path, the reason not to host the local Compose database as a free-tier production database, the consent-based WhatsApp Groups API flow, and a beginner learning plan.

## WhatsApp group workflow and limits

- The target flow is official WhatsApp message webhook → source-preserving pending intake draft → explicit branch tag such as `KLB` → coordinator review → response register and optional linked assignment → audit timeline → branch-filtered reports.
- Meta documents group ID, message ID, participant business-scoped ID, text, and provider timestamp in group message webhooks. Sender identity can be mapped to an authorized person; text claims about who completed work still need review.
- This requires an eligible Official Business Account and Groups API-created, invite-only groups, capped at 8 participants. It cannot read history from arbitrary existing WhatsApp groups. CaseLoop's current webhook does not yet support Groups API payloads.

## Hosting recommendation and learning

- Recommended first public synthetic demo: Render Static Site + Render Python Web Service + Neon Free Postgres. Keep Docker Compose for local development; use managed Postgres for hosted persistence. Render's Python runtime avoids adding Docker deployment complexity for the first hosted version.
- The deployment guide now includes a staged learning path through Git, request tracing, React/TypeScript, FastAPI/Python, SQL/Postgres, testing/debugging, Docker/deployment, and webhook security. The central practice is to explain a feature's path, inspect Copilot's diff, and run a focused test before accepting the change.

## Verification and remaining setup

- Frontend TypeScript check and Vite production build passed.
- Docker API and PostgreSQL were healthy. The first admin was verified active with role `admin`, and `must_change_password` is enabled.
- The failed non-TTY `getpass` attempt made no account changes; the successful bootstrap was then verified in PostgreSQL.
- No public deployment or live Meta webhook test was performed; hosting/provider accounts and Meta credentials remain unconfigured.

The admin record is:

- **Name:** Faith
- **Email:** `chago@redcross.org.ke`
- current/new password -- `chagoKRCklb#2026`

The regular record is:
Name: Lsetga
Emial: `llybisetga@gmail.com`
Initial pass: `123456789Ten`

The database stores a password hash, not the plaintext. I enabled a required password change at first sign-in; use these credentials at [http://127.0.0.1:5173/admin](http://127.0.0.1:5173/admin), then choose a new password before exploring the dashboard. <- **Initial password:** chago-klbl2026>


Today I bootstrapped CaseLoop's first local administrator and verified the role. I required a password change. I removed the duplicate Admin sign-in button and widened the auth header. I documented hosting and WhatsApp constraints and added a deployment and learning plan. No public hosting or live WhatsApp integration was completed.