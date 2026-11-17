# CaseLoop 🌐🚑
## Master Project Charter & Technical Deep-Dive Blueprint
**Target Institution:** Kenya Red Cross Society (Karen-Lang'ata Field Unit / Branch)  
**Framework:** Karen-Lang'ata Digital Innovation Lab  
**Lead Architect:** Billy Gates Ochieng Osodo  
**Document Status:** Historical charter; current implementation is tracked in Checkpoint 6 and the project README  
**Last Updated:** November 11, 2026  

---

## Current Architecture and Status (November 13, 2026)

This status supersedes older checklists and setup instructions in the historical charter sections below. See [Checkpoint 6](../progress/chkpnt6.md) for what changed in this milestone.

- **SQLAlchemy stays.** SQLAlchemy remains the ORM. SQLite is the local, offline, single-workstation option; PostgreSQL is the shared-database option.
- **Docker Compose is local development/demo infrastructure.** It runs PostgreSQL and the API on this machine with a persistent Docker volume. It is not a public host and does not migrate the SQLite database.
- **Authentication and access control are implemented:** email/password accounts, PBKDF2 password hashes, revocable server-side sessions, CSRF checks, role enforcement, account provisioning/reset, team memberships, and administrative activity records. Independent security/privacy review and login abuse protection are still needed before public access.
- **Intake and reporting are implemented:** coordinator-reviewed source text, a protected response board, assignment lifecycle and user-attributed timeline, report preview, and Word download. Reporting is deterministic, not AI-generated.
- **WhatsApp adapter is implemented, not live-connected:** official Meta webhook challenge/HMAC verification, text-only intake, and duplicate-message handling create pending drafts only. It cannot read arbitrary chat/group histories, send messages, approve intakes, or create assignments. A Meta app, secrets, approved test recipient, and public HTTPS callback are not configured.
- **Hosting is not ready or configured:** no Git remote, provider account, public host, public DNS name, security/privacy approval, or production backup/restore process is in place. Use synthetic data only.
- **Windows runtimes:** the project virtual environment is Python 3.11.9, and the frontend manifest uses React 18.2 with Vite/TypeScript. See the root README for repeatable commands.
- **Product boundary:** CaseLoop is a coordination aid that complements existing Red Cross workflows; it is not an officially approved Red Cross system unless and until the organization authorizes it.

## Architecture Decision Addendum (November 13, 2026)

- **Offline-first remains the design goal.** Keep SQLite for local single-workstation work; choose PostgreSQL when multiple authorized users need a shared database.
- **Human review is mandatory.** Preserve original unstructured source text, let a coordinator correct and approve it, then create the response; inbound WhatsApp messages remain drafts.
- **Keep deterministic report content traceable to approved structured data.** Any future AI is advisory and may not silently publish or dispatch.
- **Deployment sequence:** complete organizational approval, security/privacy and migration review, login abuse protection, HTTPS/secrets/CORS configuration, backup and restore drills, and provider readiness before introducing real data or public access.

The remainder of this charter includes historical architectural plans and checklists. They record project intent but are not a statement that every item remains open or that its old command/credential is safe to use.

## 1. Executive Overview & Foundational Thesis

**CaseLoop** is an offline-first operational notebook, coordination platform, and intelligence companion engineered specifically for local humanitarian response units operating under real-world resource constraints. 

In humanitarian branch operations—such as the Karen-Lang'ata Red Cross unit—incident response begins with high-velocity communication across WhatsApp groups, emergency phone calls, and dispatch messages. While messaging channels are ideal for real-time alerting, they break down when managing operational continuity, task accountability, and executive reporting. Critical information becomes fragmented across chat histories, coordinators spend hours manually compiling weekend situation reports (SitReps), and cloud-dependent platforms fail when local power grid or network outages strike.

CaseLoop addresses this structural gap by acting as a **non-disruptive, offline-first operational companion**. It operates 100% locally on standard workstation hardware (Intel Core i3, 8GB RAM) using a lightweight Python FastAPI and SQLite architecture. It does not attempt to replace WhatsApp or force volunteers to adopt complex enterprise interfaces during active field emergencies; instead, it provides branch leadership and team leaders with a structured intake, assignment lifecycle engine, automated audit trail, and instant report generation platform.

---

## 2. Core Problem Statement & Strategic Value Addition

### 2.1 The Problem Statement
1. **Information Fragmentation:** Emergency details, location tags, deployed personnel rosters, and status updates are buried across unstructured chat streams.
2. **Administrative Friction:** Branch Governors and Coordinators spend 3 to 5 hours weekly re-keying chat messages into manual spreadsheets and Word documents for headquarters reporting.
3. **Infrastructure Vulnerability:** Cloud-only response tools stall during local power disruption or cellular network congestion in field locations.
4. **Audit & Accountability Deficit:** Lack of timestamped, immutable logging makes post-incident reviews (after-action reviews) reliance on memory rather than data.

### 2.2 Strategic Value Addition
* **Zero Cloud & Zero LLM Overhead:** Operates with zero internet dependence. Excludes resource-heavy AI models (Ollama/Llama 3 permanently removed) in favor of deterministic, hyper-fast Python utilities (`psutil`, `difflib`, SQLite FTS5).
* **Automated SitRep & CSV Export:** Generates executive KPI summaries, structured branch reports, and plain-text WhatsApp SitReps with a single click.
* **Strict Role Security Boundary:** Prevents data corruption by isolating administrative creation/deletion tools from volunteer task execution feeds.
* **Student Succession & Low TCO:** Modular monolith structure built with clean separation of concerns, enabling incoming software engineering attachment students to inherit, maintain, and extend the system without expensive technical debt.

---

## 3. User Personas, Role Separation & Security Boundaries

A primary design mandate of CaseLoop is respecting the authority structure of the Red Cross branch while minimizing friction for field personnel.

```
                  ┌──────────────────────────────────────────────┐
                  │            AUTHENTICATION GATEWAY            │
                  │   (Session Token / Single-Use Admin Gate)    │
                  └──────────────────────┬───────────────────────┘
                                         │
                   ┌─────────────────────┴─────────────────────┐
                   ▼                                           ▼
   ┌───────────────────────────────┐           ┌───────────────────────────────┐
   │     RESPONDER / FIELD ROLE    │           │   ADMIN / GOVERNOR ROLE       │
   │  (Volunteers / Team Leaders)  │           │   (Branch Leadership)         │
   └───────────────┬───────────────┘           └───────────────┬───────────────┘
                   │                                           │
  [READ-ONLY] View Incident Feed              [FULL CRUD] Create/Delete Incidents
  [WRITE-ONLY] Lifecycle Transitions          [FULL CRUD] Manage Team Rosters
               - Draft → Assigned             [FULL CRUD] Workstation Telemetry
               - Assigned → Acknowledged      [FULL CRUD] Dynamic Security Tokens
               - Acknowledged → In Progress   [EXECUTIVE] CSV & WhatsApp Exports
               - In Progress → Completed
```

### Role Matrix

| Action / Capability | Field Responder / Volunteer | Team Leader | Branch Governor / Admin |
| :--- | :---: | :---: | :---: |
| **View Active Incident Feed** | ✅ (Read-Only) | ✅ (Read-Only) | ✅ (Full Access) |
| **Log New Operational Response** | ❌ | ❌ | ✅ (Full Access) |
| **Delete / Archive Incident** | ❌ | ❌ | ✅ (Full Access) |
| **Assign Team to Incident** | ❌ | ❌ | ✅ (Full Access) |
| **Update Assignment Lifecycle Status** | ❌ | ✅ (State-Restricted) | ✅ (Full Access) |
| **Manage Team Roster (Add/Remove Staff)** | ❌ | ❌ | ✅ (Full Access) |
| **Generate & Verify Dynamic Secret Token** | ❌ | ❌ | ✅ (Full Access) |
| **View Hardware Resource Telemetry (`psutil`)** | ❌ | ❌ | ✅ (Full Access) |
| **Export Branch CSV / WhatsApp SitRep** | ❌ | ✅ (Read-Only Export) | ✅ (Full Access) |

---

## 4. End-to-End Operational Workflow

```
1. INTAKE & CREATION [Admin / Governor]
   │ Emergency alert arrives via phone call or WhatsApp group chat.
   └─► Admin opens Response Register -> Enters Reference (e.g. CR-KL-2026-004), Title, Category, Priority, and Location.

2. RESOURCE ALLOCATION & TEAM ASSIGNMENT [Admin / Governor]
   │ Coordinator evaluates available branch units in Team Roster Manager.
   └─► Issues assignment (ASN-001) linked to Response Record -> Sets expected completion parameters.

3. FIELD ACKNOWLEDGEMENT & EXECUTION [Team Leader / Responder]
   │ Deployed team logs into CaseLoop on workstation/mobile portal.
   ├─► Views assigned operational tasks in read-only register.
   ├─► Clicks "Acknowledge Task" (Status: Draft/Assigned ──► Acknowledged).
   ├─► Clicks "Begin Execution" (Status: Acknowledged ──► In Progress).
   └─► Clicks "Mark Completed" (Status: In Progress ──► Completed).

4. AUTOMATED AUDIT TRAIL [System Engine / SQLite]
   │ Every lifecycle transition triggers backend event service.
   └─► Appends immutable timestamped entry to `ResponseEvent` log (`caseloop.db`).

5. REVIEW, SITREP & EXECUTIVE REPORTING [Admin / Governor]
   │ Operational cycle closes or periodic reporting period arrives.
   ├─► Governor checks dashboard KPIs (Total Incidents, Overdue Tasks, Active Units).
   ├─► Clicks "Copy WhatsApp SitRep" for instant posting back to group communication.
   └─► Clicks "Export Official CSV Report" for Red Cross HQ administrative filing.
```

---

## 5. Checkpoint-by-Checkpoint History (Checkpoints 1 – 5)

### 📌 Checkpoint 1: Core Monolith Architecture & Round-Trip Persistence
* **Status:** LOCKED IN & VERIFIED
* **Key Achievements:**
  1. Established Python 3.11 backend with FastAPI and SQLAlchemy ORM.
  2. Integrated SQLite database (`caseloop.db`) with FTS5 search index capabilities.
  3. Formatted initial React 18 / Vite 5 / Tailwind CSS frontend boilerplate.
  4. Configured CORS middleware allowing asynchronous REST calls between Vite frontend and FastAPI backend.
  5. Tested full round-trip persistence (creating data in UI, persisting to local disk, reloading upon server restart).

### 📌 Checkpoint 2: Hardware Telemetry & Security Gate
* **Status:** LOCKED IN & VERIFIED
* **Key Achievements:**
  1. Integrated Python `psutil` library in `backend/app/services/system_monitor.py` to track Core i3 CPU utilization and available RAM without system spikes.
  2. Implemented `AdminSecretService` and `AdminToken` model generating 5-minute single-use dynamic security keys (`CR-KL-XXXXXX`).
  3. Built `AdminControl.tsx` frontend modal featuring live workstation hardware metrics and key verification.

### 📌 Checkpoint 3: Authentication Gateway & Frontend Decoupling
* **Status:** LOCKED IN & VERIFIED
* **Key Achievements:**
  1. Built `AuthGateway.tsx` supporting user registration and session login.
  2. Implemented backend routes (`/api/auth/register`, `/api/auth/login`) storing coordinator credentials securely in SQLite.
  3. Standardized API base routing (`http://localhost:8000`) resolving double `/api/api/` prefix 404 bugs.
  4. Embedded the 5-click hidden administrative access trigger inside `UserProfile.tsx`.

### 📌 Checkpoint 4: Response Register CRUD & Foreign-Key Integrity
* **Status:** LOCKED IN & VERIFIED
* **Key Achievements:**
  1. Extracted monolithic inline code from `App.tsx` into modular feature components (`src/features/responses/ResponseRegister.tsx`).
  2. Completed full CRUD operations for response records (Create, Read, Search Filter, Delete).
  3. Resolved cascading deletion bugs in SQLite, ensuring removing a response safely cleans up or disassociates dependent timeline events.

### 📌 Checkpoint 5: Assignments Manager & Status Lifecycles
* **Status:** LOCKED IN & VERIFIED
* **Key Achievements:**
  1. Created `AssignmentsManager.tsx` and backend services (`assignment_service.py`).
  2. Implemented team creation and assignment allocation linked to parent responses.
  3. Drafted initial lifecycle statuses (`Draft`, `Assigned`, `Acknowledged`, `In Progress`, `Completed`).

---

## 6. Checkpoint 6 Execution Roadmap & Outstanding Work

Checkpoint 6 completes the primary architectural MVP, shifting focus entirely to administrative intelligence, reporting automation, and deployment readiness.

```
                                 CHECKPOINT 6 TARGETS
                                           │
  ┌───────────────────┬────────────────────┼────────────────────┬───────────────────┐
  ▼                   ▼                    ▼                    ▼                   ▼
[Team Roster    [Executive Reports   [Chronological Audit  [WhatsApp SitRep    [Auto-Backup &
 Controls]       & CSV Export]        Timeline Feed]        Exporter]           Docker Deployment]
```

### 📋 Outstanding Feature Execution Breakdown

#### 1. Coordinator Team Membership Roster (`TeamMembershipManager.tsx`)
* **Objective:** Allow admins to dynamically add, view, and revoke staff members assigned to specific response units.
* **Backend Inferred Endpoints:**
  * `GET /api/teams/{team_id}/members` -> Fetch member list for a team.
  * `POST /api/teams/{team_id}/members` -> Add responder user ID to team.
  * `DELETE /api/teams/{team_id}/members/{user_id}` -> Revoke team membership.

#### 2. Strict Uni-Directional Lifecycle Enforcement
* **Objective:** Refactor `AssignmentsManager.tsx` to remove generic `<select>` dropdowns for status switching. Replace with context-aware action buttons:
  * Current: `Assigned` ──► Button: **"Acknowledge Task"** ──► Next: `Acknowledged`
  * Current: `Acknowledged` ──► Button: **"Begin Execution"** ──► Next: `In Progress`
  * Current: `In Progress` ──► Button: **"Mark Completed"** ──► Next: `Completed`
* **Backend Inferred Endpoint:**
  * `PATCH /api/assignments/{id}/status` -> Validates transition, updates state, and invokes `event_service.create_event()`.

#### 3. Chronological Audit Event Timeline (`TimelineView.tsx`)
* **Objective:** Render an immutable log feed of `ResponseEvent` records so the Governor can audit every operational action by timestamp.
* **Backend Inferred Endpoint:**
  * `GET /api/responses/{response_id}/events` -> Fetch chronological event log.

#### 4. Executive Analytical Dashboard & CSV Exporter (`ReportsView.tsx`)
* **Objective:** Provide visual KPI metric cards and a single-click CSV file download engine for Red Cross HQ filing.
* **Backend Inferred Endpoints:**
  * `GET /api/reports/summary` -> Aggregate counts (Total Responses, Active Assignments, Overdue Tasks, Completed Responses).
  * `GET /api/reports/export/csv` -> Stream formatted `.csv` buffer for local disk saving.

#### 5. WhatsApp "SitRep" Formatter
* **Objective:** One-click clipboard utility converting structured incident data into plain-text formatted Situation Reports ready to paste into chat groups.
* **Format:**
  ```text
  🚨 *RED CROSS KAREN-LANG'ATA SITREP* 🚨
  *Ref:* CR-KL-2026-004 | *Title:* Medical Camp Support
  *Category:* Community Assistance | *Priority:* HIGH
  *Status:* IN PROGRESS
  *Assigned Team:* Alpha Response Unit
  *Timeline Log:* 
   - 08:30: Response Created
   - 09:05: Team Acknowledged
  -----------------------------------------
  *Generated via CaseLoop Local Station*
  ```

#### 6. SQLite Automated Backup Daemon
* **Objective:** A background daemon thread in FastAPI (`backend/app/services/backup_service.py`) that copies `caseloop.db` to `backend/backups/caseloop_backup_YYYYMMDD_HHMM.db` every 30 minutes to prevent data loss during power outages.

#### 7. Production Docker Containerization (DigitalOcean / Local Server)
* **Objective:** Provide production multi-stage `Dockerfile` and `docker-compose.yml` for containerized execution.

---

## 7. Pinpoint Dependency Baseline (Ground Truth)

To prevent breaking changes or version drift across environments, developers must adhere to these exact pinned versions:

### 🐍 Python 3.11 Backend Environment (`backend/requirements.txt`)
```text
alembic==1.13.1
annotated-types==0.8.0
anyio==4.15.1
certifi==2026.10.23
click==8.5.0
colorama==0.4.6
fastapi==0.115.0
greenlet==3.5.6
h11==0.16.0
httpcore==1.0.9
httptools==0.9.0
httpx==0.27.0
idna==3.20
iniconfig==2.3.1
Mako==1.4.3
MarkupSafe==3.0.4
packaging==26.3
pluggy==1.7.0
psutil==5.9.8
pydantic==2.6.4
pydantic_core==2.16.3
pytest==8.2.0
python-dotenv==1.0.1
PyYAML==6.0.3
sniffio==1.3.1
SQLAlchemy==2.0.23
starlette==0.38.6
typing_extensions==4.16.0
uvicorn==0.30.0
watchfiles==1.3.0
websockets==17.3
```

### ⚛️ Frontend Manifest (`frontend/package.json`)
```json
{
  "name": "caseloop-frontend",
  "private": true,
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "lucide-react": "^0.344.0",
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^7.18.5"
  },
  "devDependencies": {
    "@types/react": "^18.2.66",
    "@types/react-dom": "^18.2.22",
    "@vitejs/plugin-react": "^4.2.1",
    "autoprefixer": "^10.6.2",
    "postcss": "^8.5.32",
    "tailwindcss": "^3.4.19",
    "typescript": "^5.2.2",
    "vite": "^5.1.6"
  }
}
```

---

## 8. Current Installation and Account Setup

For authoritative commands, see the root [README](../../../README.md). The following are the current Windows commands; do not use legacy seed accounts.

### 8.1 Backend Setup (Windows PowerShell)
```powershell
Set-Location C:\Users\Admin\Documents\caseloop\backend
.\venv\Scripts\python.exe -m uvicorn app.main:app --reload --port 8000
.\venv\Scripts\python.exe -m app.create_admin
```

### 8.2 Frontend Setup
```powershell
Set-Location C:\Users\Admin\Documents\caseloop\frontend
npm.cmd run dev -- --host 127.0.0.1
```

There are no default test credentials or public sign-up. The interactive CLI prompts for the initial administrator's email, name, and password. Admin-provisioned accounts receive a one-time temporary password that must be changed.

Optional synthetic response examples can be added after creating an admin with `python -m app.seed`; the seeder no longer creates a placeholder account.

---

## 9. SQLite Database Schema Architecture

```
┌─────────────────────────────────┐       ┌─────────────────────────────────┐
│             USERS               │       │             TEAMS               │
├─────────────────────────────────┤       ├─────────────────────────────────┤
│ id (PK, Integer)                │       │ id (PK, Integer)                │
│ username (String, Unique)       │       │ name (String, Unique)           │
│ hashed_password (String)        │       │ description (String)            │
│ role (String: admin/coordinator)│       └────────────────┬────────────────┘
│ created_at (DateTime)           │                        │ 1
└────────────────┬────────────────┘                        │
                 │ 1                                       │
                 │                                         │
                 │ N                                       │ N
┌────────────────┴────────────────┐       ┌────────────────┴────────────────┐
│           RESPONSES             │       │           ASSIGNMENTS           │
├─────────────────────────────────┤       ├─────────────────────────────────┤
│ id (PK, Integer)                │1     N│ id (PK, Integer)                │
│ reference_code (String, Unique) ├───────┤ reference_code (String, Unique) │
│ title (String)                  │       │ response_id (FK -> responses.id)│
│ description (Text)              │       │ team_id (FK -> teams.id)        │
│ category (String)               │       │ status (String: Draft/Assigned/ │
│ priority (String: normal/high)  │       │   Acknowledged/InProgress/Done) │
│ location (String)               │       │ description (Text)              │
│ created_at (DateTime)           │       └─────────────────────────────────┘
└────────────────┬────────────────┘
                 │ 1
                 │
                 │ N
┌────────────────┴────────────────┐       ┌─────────────────────────────────┐
│        RESPONSE_EVENTS          │       │           ADMIN_TOKENS          │
├─────────────────────────────────┤       ├─────────────────────────────────┤
│ id (PK, Integer)                │       │ id (PK, Integer)                │
│ response_id (FK -> responses.id)│       │ keyword (String, Unique)        │
│ event_type (String)             │       │ expires_at (DateTime)           │
│ message (Text)                  │       │ is_used (Boolean)               │
│ created_at (DateTime)           │       └─────────────────────────────────┘
└─────────────────────────────────┘
```

---

## 10. DigitalOcean & Production Containerization Blueprint

For remote or central deployment on a DigitalOcean Droplet ($6/mo Basic Droplet, 1GB RAM, 1 vCPU, Ubuntu 24.04 LTS):

### 10.1 Backend Dockerfile (`backend/Dockerfile`)
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Prevent Python from writing pyc files and buffering stdout
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies required for SQLite and compilation
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    sqlite3 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 10.2 Frontend Dockerfile (`frontend/Dockerfile`)
```dockerfile
# Build Stage
FROM node:18-alpine AS build
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Production Stage (NGINX Web Server)
FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

### 10.3 Orchestration (`docker-compose.yml`)
```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    restart: always
    ports:
      - "8000:8000"
    volumes:
      - caseloop_db_data:/app/data
    environment:
      - DATABASE_URL=sqlite:////app/data/caseloop.db

  frontend:
    build: ./frontend
    restart: always
    ports:
      - "80:80"
    depends_on:
      - backend

volumes:
  caseloop_db_data:
```

---

## 11. Interactive Master Project Checklist

```markdown
### 🟢 Checkpoint 1 – 5 Foundation (Verified & Locked)
- [x] Python 3.11 + FastAPI + SQLAlchemy with SQLite and PostgreSQL modes
- [x] Email/password sign-in, hashed passwords, revocable sessions, CSRF checks, and server-side role authorization
- [x] Admin account/team management, response/assignment workflow, reviewed intake, and attributed timeline
- [x] Report summary, preview, and Word download
- [x] Optional signed Meta text webhook that creates pending intake drafts only
- [x] Docker Compose PostgreSQL/API local development environment

### 🟡 Remaining deployment gates (not a public launch checklist)
- [ ] Organizational security/privacy approval and independent application review
- [ ] Login abuse protection and operational monitoring
- [ ] Production HTTPS, secret management, CORS, private database networking, backups, and tested restore
- [ ] Migration/rollback rehearsal against SQLite and PostgreSQL
- [ ] Real WhatsApp test after setting up the Meta test number, approved recipient, secrets, and HTTPS callback
```



### Summary of What Was Generated

comprehensive Master Project Charter and Deep-Dive Blueprint for CaseLoop in a dedicated markdown document

1. **`docs/caseloop_master_charter.md`:** A deep-dive master charter that integrates:
* **Problem & Value Addition:** Clarifying why we build primarily for the **Branch Governor and Coordinators** (eliminating administrative friction and automating SitReps) while giving volunteers a simple situational view.
* **Security Boundary & Role Matrix:** Explicitly detailing read-only vs. full CRUD permissions across Responders, Team Leaders, and the Governor.
* **Checkpoint History (1 – 5):** Complete sequential history documenting your architectural progress to date.
* **Checkpoint 6 Roadmap:** Concrete plans for Team Roster Controls, Uni-Directional Lifecycle Enforcement, Chronological Event Feeds, Executive CSV Reports, WhatsApp SitRep Exporter, and SQLite Backup Daemon.
* **Pinpoint Dependency Specifications:** Pinned dependency lists for Python 3.11, FastAPI `0.115.0`, SQLAlchemy `2.0.23`, React `18.2.0`, Vite `5.1.6`, TypeScript `5.2.2`, and Tailwind CSS `3.4.19`.
* **Database Schema Diagram & Installation Steps:** Visual entity-relationship diagram, setup commands, and seeding instructions.
* **Production Containerization Blueprint:** Complete multi-stage `Dockerfile` and `docker-compose.yml` configurations for DigitalOcean or offline server deployment.
* **Interactive Checklist:** Master tracker to keep your development focused.

