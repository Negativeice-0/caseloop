# CaseLoop overview

CaseLoop is an offline-first coordination notebook for humanitarian response teams. Its intended value is practical administrative relief for coordinators: turn unstructured reports into reviewed response records, assign teams, track a clear chain of responsibility, and prepare traceable operational reports. Responders get a focused situational board and can update only the work assigned to their team.

CaseLoop complements existing communication channels; it does not replace WhatsApp, Red Cross systems, or organizational approval. Never use real operational or beneficiary data until the organization has approved the system and data-handling practices.

## Intended workflow

1. Capture source text from a coordinator or supported channel.
2. Keep the original text and have a coordinator review, correct, and approve it.
3. Publish the approved response to the response board.
4. Assign a team and move its task through the enforced status lifecycle.
5. Attribute timeline events to the acting user.
6. Preview the report and download a Word document from approved structured data.

On approval, the coordinator can publish the response alone or choose a team and create its linked assignment atomically. Both actions are visible in the operational timeline. The timeline defaults to all responses and can be filtered to one response.

## Current implementation

- Named email/password accounts, server-side roles, hashed passwords, revocable sessions, CSRF protection, a dedicated `/admin` sign-in entry, admin account and team management, temporary-password onboarding/reset, and admin audit activity. Public registration creates responder-only accounts; coordinators and admins are provisioned by an administrator.
- Response records, coordinator-reviewed manual intake, response/team/assignment management, team membership, and assignment lifecycle/timeline.
- Main-navigation Reports & Analysis for coordinators and admins, with date/team filters, operational/situation/field report formats, weekly activity trends, recorded-location coverage and missing-location counts, an automatically open preview, and matching Word exports.
- Admin workspace has direct sections for response records, draft/active assignments, intake review, read-only timeline, reports, and account/team management. Draft assignments can be edited; later lifecycle changes are preserved in the audit timeline.
- Optional Meta WhatsApp webhook: verifies Meta's challenge and HMAC signature, deduplicates messages, and saves supported text-only messages as pending drafts. It does not send outbound messages, inspect arbitrary existing groups, approve drafts, or create assignments. Meta's separate Groups API is not implemented.
- SQLite is the local single-workstation/offline mode; PostgreSQL is the shared-database mode. Docker Compose provides a local PostgreSQL/API setup. SQLAlchemy remains the ORM in both modes.

## Limits and open gates

- No live Meta credentials, public HTTPS webhook, or real WhatsApp test is configured. A synthetic webhook test is not a provider test.
- CaseLoop does not currently accept Groups API payloads. Meta's official Groups API is limited to eligible Official Business Accounts and invite-only groups of up to 8 participants; it is not an API for reading arbitrary existing group history.
- No Git remote, provider account, public deployment, or public hosting is configured. A local Docker Compose setup is not hosting.
- Password hashing and session authorization are implemented, but public deployment still needs independent security/privacy review, registration/login abuse protection, an appropriate email-verification or invite policy, monitored operations, tested backups/restores, and organizational approval.
- Migration/bootstrap history should be reviewed and tested on SQLite and PostgreSQL before a production data upgrade. SQLite data is not automatically transferred to PostgreSQL.
- Report analysis is deterministic and based on structured records; optional AI must remain advisory and human-reviewed.
- No specific VMS product or integration was identified. CaseLoop is intended to complement a VMS: the VMS remains the authoritative source for volunteer identity, eligibility, and lifecycle; CaseLoop handles incident operations and only the minimum team assignment data required. No roster import/sync exists.

## Recommended next increments

1. Make Admin operationally useful at a glance: pending intakes, open/unassigned/overdue assignments, recent changes, and direct links to resolve each queue.
2. Run the official Meta Cloud API test-number flow end to end. Preserve the source message, deduplicate webhook retries, extract only draft fields, and require coordinator correction/approval before publishing or assigning.
3. If the organization has Meta Official Business Account eligibility, assess the Groups API for small, invite-only, consent-based groups; otherwise use direct messages to the official intake number or voluntary forwarding. Preserve human review and source traceability.
4. Add comparisons across user-selected periods while preserving the separation between approved facts and analysis.
5. Add signup abuse controls and the organization's chosen email verification or invitation policy before any public deployment.
6. Add documented backup/restore and retention workflows before using anything beyond synthetic data.

## Technical baseline

- Python 3.11, FastAPI, SQLAlchemy, Alembic.
- React 18, TypeScript, Vite.
- SQLite for local/offline use; PostgreSQL for shared deployments.
- Docker Compose for local PostgreSQL/API development, not as a substitute for public hosting.

## Authoritative references

- [Project setup and test commands](../../../README.md)
- [Implementation notes](IMPLEMENTATION.md)
- [Deployment, hosting gates, and Meta webhook setup](../../deployment/DEPLOYMENT.md)
- [Stakeholder design pack and project checklist](../../design/README.md)
- [Project charter](caseloop_master_project_charter.md)
- [Checkpoint 6: secure access and admin workflow](../progress/chkpnt6.md)
- [Checkpoint 8: discoverable admin and deployment guidance](../progress/chkpnt8.md)
- [Checkpoint 9: brand navigation and hosting/WhatsApp guidance](../progress/chkpnt9.md)
- [Checkpoint 10: first admin, auth layout, hosting and learning plan](../progress/chkpnt10.md)
