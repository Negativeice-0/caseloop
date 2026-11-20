Use a controlled “inventory → baseline → navigation surgery → authorization audit → refactor → cleanup” sequence. Do not begin by deleting files or redesigning every component. Your README already describes a meaningful product boundary, but it appears to mix current behavior, planned behavior, learning material, deployment guidance, and security warnings; the first audit should separate those categories and identify contradictions.

The operating standard I recommend
Use these standards for CaseLoop:

Trunk-based Git workflow with short-lived branches — one focused change per branch and pull request.

Small pull requests — ideally one concern, such as navigation removal or route documentation.

Test pyramid — unit tests for rules and utilities, API tests for permissions and workflows, a smaller number of browser tests for critical journeys.

Role matrix — explicitly document what admin, coordinator, responder, and unauthenticated users can see and do.

Feature ownership — organize code around product capabilities, not only technical layers.

Static analysis plus human review — scanners identify candidates; you decide what is safe.

Synthetic data only — especially important because CaseLoop concerns humanitarian operations and personal information.

No destructive cleanup without a reversible commit — use git rm only after the file has been classified and tested.

CaseLoop cleanup checklist
Use this as the master checklist. Do not check an item merely because a command ran; check it when the result has been inspected and recorded.

Phase 0 — Freeze the starting point
 Confirm the repository is clean.

Powershell

Copy
git status --short
 Create a safety branch.

Powershell

Copy
git switch -c chore/caseloop-ui-audit
 Create a baseline tag or commit reference.

Powershell

Copy
git add -A
git commit -m "chore: record baseline before UI audit"
 Record the current versions.

Powershell

Copy
python --version
node --version
npm --version
docker --version
git --version
 Run the existing backend tests.

Powershell

Copy
Set-Location backend
.\venv\Scripts\python.exe -m pytest -q
 Run the frontend build.

Powershell

Copy
Set-Location ..\frontend
npm.cmd run build
 Record failures before changing anything.

Create:

Text

Copy
docs/audits/baseline.md
Include:

Date.

Commands run.

Passing checks.

Failing checks.

Warnings.

Environment assumptions.

Whether SQLite or PostgreSQL was used.

Phase 1 — Create the application map
Create this directory:

Text

Copy
docs/audits/
Add these files:

Text

Copy
docs/audits/
  baseline.md
  route-inventory.md
  role-permission-matrix.md
  connection-map.md
  readme-audit.md
  deletion-candidates.md
  ui-component-map.md
 List all top-level files.

Powershell

Copy
Get-ChildItem -Force
Get-ChildItem -Recurse -File |
  Select-Object FullName |
  Out-File docs\audits\file-inventory.txt
 List frontend source files.

Powershell

Copy
Get-ChildItem frontend\src -Recurse -File |
  Select-Object FullName |
  Out-File docs\audits\frontend-files.txt
 List backend source files.

Powershell

Copy
Get-ChildItem backend\app -Recurse -File |
  Select-Object FullName |
  Out-File docs\audits\backend-files.txt
 List tests.

Powershell

Copy
Get-ChildItem -Recurse -File |
  Where-Object {
    $_.Name -match "test|spec" -or $_.DirectoryName -match "tests"
  } |
  Select-Object FullName |
  Out-File docs\audits\test-files.txt
Phase 2 — Build the route inventory
Search for route definitions, links, labels, and navigation arrays:

Powershell

Copy
rg -n -i `
  "createBrowserRouter|BrowserRouter|Routes|Route|navigate\(|Link|NavLink|href=|path:|navItems|menuItems|sidebar|bottom.?nav|more" `
  frontend\src
Search specifically for the redundant entries:

Powershell

Copy
rg -n -i `
  "intake review|reports.?analysis|intake-review|reports-analysis" `
  frontend backend tests docs
For every route, record:

Route	Component	Entry points	Allowed roles	API calls	
Keep?

/users	UsersPage	Sidebar, mobile nav	Admin/coordinator	User API	
Yes

/admin	Admin entry	Login page	Admin	Auth API	
Yes

/intake-review	Unknown	Sidebar or direct URL	Coordinator/admin	Intake API	
Decide

/reports	Unknown	Sidebar	Coordinator/admin	Reports API	
Decide

Do not assume “remove from navigation” means “delete the route.” You have three distinct choices:

Hide from navigation but retain the route — useful for backward compatibility.

Redirect the old route — useful if the feature has been replaced.

Delete the route and component — appropriate only after confirming it is retired.

For your case, I would initially remove the two entries from visible navigation while retaining their routes temporarily, unless you have confirmed that the underlying features are no longer part of the product vision.

Phase 3 — Build the role and permission audit
Your README claims that:

Administrators manage accounts, teams, memberships, roles, deactivation, and password resets.

Coordinators review submitted text and publish responses.

Responders have read-only response access and can advance assignments only for their own team.

Server-side roles enforce permissions.

Turn that into a testable matrix:

Markdown

Copy
# CaseLoop role and permission matrix

| Capability | Anonymous | Responder | Coordinator | Admin | UI location | API endpoint | Test |
|---|---:|---:|---:|---:|---|---|---|
| Register | Yes | N/A | N/A | N/A | Landing page | POST /... | Yes/No |
| Review intake | No | No | Yes | Yes | Intake page | PATCH /... | Yes/No |
| Manage users | No | No | No | Yes | Admin page | GET/POST /... | Yes/No |
| Assign own team | No | Yes | Yes | Yes | Assignment page | PATCH /... | Yes/No |
| View reports | No | No/Yes | Yes | Yes | Reports page | GET /... | Yes/No |
For every capability:

 Confirm the frontend hides or disables inappropriate actions.

 Confirm the backend rejects inappropriate requests.

 Confirm direct URL access is protected.

 Confirm API tests exist.

 Confirm the UI does not rely on hiding alone for security.

The backend must be authoritative. A user who manually visits /admin or sends an API request should receive a denial even if the frontend has hidden the link.

Phase 4 — Build the connection map
Create docs/audits/connection-map.md with this format:

Markdown

Copy
# CaseLoop connection map

## Browser to frontend

- Browser
  - Vite development server
  - React application
  - Router
  - Auth/session state
  - API client

## Frontend to backend

- Users page
  - API client
  - User endpoints
  - Role guard
- Intake review
  - API client
  - Intake endpoints
  - Coordinator/admin guard
- Reports
  - API client
  - Report endpoints
  - Coordinator/admin guard

## Backend to database

- FastAPI route
  - Service or domain logic
  - SQLAlchemy model
  - SQLite or PostgreSQL
  - Alembic migration

## External integration

- Meta WhatsApp webhook
  - Signature verification
  - Pending intake creation
  - No automatic approval
  - No automatic assignment

## Docker

- frontend development server
- api service
- postgres service
- postgres_data volume
Search for connections with:

Powershell

Copy
rg -n -i `
  "fetch\(|axios|baseURL|/api/|http://|https://|DATABASE_URL|POSTGRES|SQLITE|WHATSAPP|docker compose|depends_on|ports:|volumes:|networks:" `
  frontend backend docker-compose.yml .env.example .github docs
For each frontend API call, record:

Text

Copy
UI component
→ API client function
→ HTTP method and path
→ backend route
→ service function
→ database model
→ authorization rule
→ test file
This is the most useful form of “full connection route” because it connects visible behavior to data and permissions.

Phase 5 — Audit the README and related documentation
From the README you pasted, these files are explicitly related:

Text

Copy
README.md
docs/deployment/oracle-whatsapp-learning-runbook.md
docs/deployment/DEPLOYMENT.md
docs/design/README.md
docs/training/independent-learning-program.md
docs/training/caseloop-two-week-learning-lab.md
docs/training/caseloop-completion-roadmap.md
docs/projects/caseloop/IMPLEMENTATION.md
docs/projects/caseloop/OVERVIEW.md
docs/projects/progress/chkpnt6.md
.env.example
docker-compose.yml
The README also refers to:

Meta WhatsApp Cloud API documentation.

A VMS boundary comparison.

Local SQLite setup.

Docker PostgreSQL setup.

Render and Neon hosting.

Oracle and WhatsApp learning deployment.

Frontend and backend verification commands.

Admin creation and synthetic seeding.

Offline-first behavior.

Reports and analysis.

Intake review.

Role-based permissions.

Find all documentation references automatically:

Powershell

Copy
rg -n -i `
  "\[[^\]]+\]\([^)]+\)|README|readme|docs/|documentation|runbook|guide|overview|implementation|checkpoint|roadmap" `
  README.md docs .github
Find all README files:

Powershell

Copy
Get-ChildItem -Recurse -File -Filter README.md |
  Select-Object FullName |
  Out-File docs\audits\readme-files.txt
Find all deployment and configuration files:

Powershell

Copy
Get-ChildItem -Recurse -File |
  Where-Object {
    $_.Name -match "docker|compose|env|config|deploy|workflow|pipeline|makefile"
  } |
  Select-Object FullName |
  Out-File docs\audits\deployment-files.txt
README audit questions
For every claim in the README, mark it:

Verified — confirmed in current code and tested.

Partially verified — code exists but behavior differs.

Stale — no longer true.

Planned — described as direction, not current capability.

Unclear — needs investigation.

The most suspicious areas in the supplied README are:

It says reports are available, while you are considering removing “Reports & Analysis.”

It says users can review incoming reports, but you may be changing the navigation around intake review.

It describes multiple deployment paths, although no public deployment is configured.

It includes extensive training and learning links that may not describe the current application.

It says “current capabilities” while also describing product direction and future operational readiness.

It includes security claims that should be verified by tests rather than accepted from prose.

I would split the README into:

What CaseLoop is.

Current verified capabilities.

Local development.

Testing.

Architecture and routes.

Security and operational limitations.

Deployment guides.

Product direction.

Training material.

That separation will make future drift much easier to detect.

Phase 6 — UI teardown and separation of concerns
Do this only after the route and role inventories exist.

Target structure
Text

Copy
frontend/src/
  app/
    App.tsx
    router.tsx
    providers/
      AuthProvider.tsx
      QueryProvider.tsx

  layout/
    AppShell.tsx
    Sidebar.tsx
    MobileBottomNav.tsx
    MoreMenu.tsx
    PageHeader.tsx

  navigation/
    navigationConfig.ts
    navigationTypes.ts
    navigationVisibility.ts

  features/
    auth/
      pages/
      components/
      authApi.ts
      authTypes.ts
      auth.test.ts

    users/
      pages/
      components/
      usersApi.ts
      usersTypes.ts
      users.test.ts

    intake/
      pages/
      components/
      intakeApi.ts
      intakeTypes.ts
      intake.test.ts

    responses/
      pages/
      components/
      responsesApi.ts
      responsesTypes.ts

    assignments/
      pages/
      components/
      assignmentsApi.ts
      assignmentsTypes.ts

    reports/
      pages/
      components/
      reportsApi.ts
      reportsTypes.ts

  shared/
    components/
    hooks/
    utils/
    types/
Separation rules
layout/ knows how the application is arranged, not how an intake is approved.

navigation/ knows labels, paths, icons, and visibility rules.

features/ owns business behavior.

shared/ contains genuinely reusable code with no feature-specific assumptions.

API functions should not be embedded directly inside visual components.

A component should not decide security permissions by itself; it may consume an authorization result supplied by the auth layer.

A feature should not import another feature’s internal files unless that relationship is intentional and documented.

Refactor order
 Extract the shared navigation configuration.

 Make desktop sidebar and mobile navigation consume that configuration.

 Add tests for visible entries by role.

 Remove “Intake Review” and “Reports & Analysis” from the configuration.

 Confirm both desktop and mobile navigation update.

 Decide whether old routes remain reachable.

 Extract API calls from page components.

 Extract repeated buttons, tables, loading states, and error states.

 Move feature-specific code into feature folders.

 Remove unused imports.

 Run type-check, build, backend tests, and browser tests.

 Update README and route documentation only after behavior is final.

Phase 7 — Testing you should add
Backend tests
Add tests for:

Unauthenticated access to protected endpoints.

Responder access to coordinator-only endpoints.

Coordinator access to admin-only endpoints.

Responder assignment changes limited to their own team.

Intake approval creating the expected response record.

Assignment and approval producing timeline events.

Deactivated users being rejected.

Password reset behavior.

CSRF protection.

WhatsApp signature validation.

Duplicate webhook delivery handling.

Database behavior in SQLite and PostgreSQL where their behavior differs.

Frontend tests
Add tests for:

Admin sees admin navigation.

Coordinator sees coordinator navigation.

Responder does not see admin controls.

Removed navigation entries do not appear on desktop.

Removed navigation entries do not appear in the mobile “More” menu.

Direct route access shows an authorization or not-found state as intended.

Loading, empty, and error states.

Session expiration and redirect behavior.

Browser tests
Use a small number of end-to-end journeys:

Admin signs in and manages a user.

Coordinator reviews and publishes an intake.

Responder views permitted responses and updates an allowed assignment.

Unauthorized user attempts a restricted route.

Mobile user opens the bottom navigation and “More” menu.

WhatsApp synthetic webhook is accepted or rejected correctly.

# Prompt to guide me through the work one step at a time
Copy and paste this as a reusable instruction in a future turn:

Text

Copy
Act as my senior software-maintenance guide for the CaseLoop repository.

Take me through the CaseLoop cleanup checklist one operation at a time. Do not jump ahead, batch destructive commands, or assume a result. Before each operation:

1. State the purpose in plain language.
2. Explain what could go wrong.
3. Give the exact PowerShell 5.1 command or exact file edit.
4. Tell me what output I should expect.
5. Ask me to paste the result.
6. Inspect my result before giving the next operation.

Project context:
- Backend: Python 3.11, FastAPI, SQLAlchemy, Alembic.
- Frontend: React 18, TypeScript, Vite.
- Local database: SQLite.
- Shared database option: PostgreSQL through Docker Compose.
- Roles: anonymous, responder, coordinator, admin.
- Important product flow: intake review → approved response → assignment