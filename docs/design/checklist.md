# CaseLoop project checklist

Use synthetic data until the organization approves the deployment and data handling. `Done` means locally implemented/verified, not approved for operational use.

## Product and interface

- [x] Keep the main workflow clear: intake, review, response register, assignments, timeline, reports.
- [x] Keep responder-facing response records read-only; place administrative CRUD behind Admin.
- [x] Keep the timeline as an attributed audit history.
- [x] Separate administrator sign-in from public responder registration.
- [x] Provide report preview and Word export from structured records.
- [x] Show the CaseLoop brand and responsive sign-in layout.
- [ ] Review admin subsection navigation on phone and desktop; consider moving admin sections into the desktop sidebar and mobile More menu.
- [ ] Review the SVG concepts with a coordinator and student attachment supervisor.
- [ ] Confirm role/permission matrix and field names with the organization.

## Local technical baseline

- [x] Python 3.11 / FastAPI API.
- [x] React 18 / TypeScript frontend.
- [x] PostgreSQL 16 in Docker Compose for shared local development.
- [x] Persist PostgreSQL data with a named volume.
- [x] Require password change for the bootstrapped local administrator.
- [ ] Add `frontend/Dockerfile` with a production build/static-server stage.
- [ ] Add a production frontend/HTTPS proxy Compose service (the current Compose file contains API and database services only).
- [ ] Add repeatable backup and restore checks for PostgreSQL.
- [ ] Verify all Docker images and Python dependencies on ARM64 before OCI deployment.

## Oracle Cloud zero-cost guardrails

- [ ] Confirm the tenancy remains on the Free Tier; do not upgrade to Pay As You Go for this demo.
- [ ] Create only resources explicitly labelled **Always Free** and stay within published quotas.
- [ ] Set compartment quotas and budget alerts; remember budgets are soft alerts, not hard spending caps.
- [ ] Select an Always Free eligible VM and storage only; confirm region capacity before building the deployment around it.
- [ ] Restrict ingress to HTTPS and narrowly scoped SSH; never expose PostgreSQL port 5432 publicly.
- [ ] Configure HTTPS, secrets, and exact allowed origins; do not put credentials in Git, slides, screenshots, or chat.
- [ ] Keep an off-VM backup and test restoration; assume an idle free VM may be reclaimed.
- [ ] Check usage/cost views after provisioning and after each infrastructure change.
- [ ] Use synthetic records only; no beneficiary or operational data on a free demo.

## WhatsApp integration (later phase)

- [ ] First test the official Cloud API test-number direct-message webhook.
- [ ] Confirm the callback is HTTPS, signatures are validated, retries are deduplicated, and source timestamps/IDs are retained.
- [ ] Route messages into pending intake drafts only.
- [ ] Parse explicit branch labels such as `KLB`; never infer a branch solely from ambiguous prose.
- [ ] Map provider sender IDs to authorized people; treat quoted claims about another person as unverified.
- [ ] Require coordinator correction/approval before publishing and assigning.
- [ ] Consider Groups API only if the organization qualifies for an Official Business Account and accepts its invite-only, 8-participant limit.
- [ ] Record participant notice/consent, retention, access, and escalation procedures before any live group test.

## Acceptance before showing a live demo

- [ ] A new administrator can sign in and complete the forced password change.
- [ ] A responder can view the register but cannot perform admin CRUD.
- [ ] A coordinator can review a synthetic intake, correct it, publish it, and optionally create an assignment.
- [ ] Assignment lifecycle changes appear in the timeline with actor and time.
- [ ] Branch/team/date filters affect report preview and Word export consistently.
- [ ] A backup can be restored to a clean test database.
- [ ] HTTPS, cookie settings, CORS, and logout work from both phone and PC.

## Student attachment record

Follow the [Student Attachment Guide](../training/Student%20Attachment%20Guide%20updated%20Jan2021.pdf) and confirm any department-specific requirements with the supervisor.

- [ ] At the end of each workday, record tasks completed and skills learned in the logbook; keep the logbook at the placement workplace.
- [ ] Record daily work clearly and include sketches/diagrams where applicable.
- [ ] Prepare a weekly summary of the work covered and obtain the supervisor's review/comments.
- [ ] Build the final report from verified work: organization background, assigned tasks, skills/lessons, challenges, and recommendations.
- [ ] Confirm submission requirements and attachment dates with the university coordinator.
