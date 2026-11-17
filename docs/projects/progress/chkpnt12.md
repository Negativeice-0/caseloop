# CaseLoop Engineering: Master Session Handover & Architecture Blueprint

This comprehensive document serves as your definitive end-to-end engineering handover for the CaseLoop project. It consolidates your project status, technical architecture, debugging history, root-cause post-mortems, professional engineering standards, and future scaling blueprints into a single reference guide.

---

## 1. Master Project Status Checklist

| Milestone / Task | Status | Details & Technical Scope |
| --- | --- | --- |
| **Environment & Config** | $\checkmark$ **Done** | Fixed root `.env` path resolution (`../../.env`), routing Alembic and FastAPI configuration directly to Docker PostgreSQL. |
| **Dependency Stack** | $\checkmark$ **Done** | Aligned requirements, managing core libraries (`fastapi`, `sqlalchemy`, `psycopg`, `uvicorn`, `pydantic`) without version drift. |
| **Database & Seeding** | $\checkmark$ **Done** | Fixed SQLAlchemy keyword arguments (`full_name`) and executed deterministic Python seeders with correct bcrypt hashing. |
| **Backend API & Transport** | $\checkmark$ **Done** | Verified FastAPI boots cleanly, interactive Swagger documentation renders at `/docs`, and local socket transport is healthy. |
| **Alembic State Sync** | $\checkmark$ **Done** | Synchronized migration history using `alembic stamp head` to satisfy strict non-empty database safety checks. |
| **Frontend-Backend Bridge** | ⚠️ **In Progress** | Validating frontend API calls (`api.ts`), session cookie management, and authentication response handling. |
| **WhatsApp Feature** | ⏳ **Remaining** | Integrating Meta/Twilio webhook messaging streams into backend intake triggers. |
| **Cloud Hosting / Deployment** | ⏳ **Remaining** | Orchestrating containerized database, FastAPI backend, and React frontend for production deployment. |

---

## 2. Technical Architecture & Current State

### Environment & Infrastructure Alignment

* **Docker PostgreSQL:** Isolated securely on port `5432` (`caseloop-db-1`) utilizing persistent Docker volumes (`docker compose up -d db`).
* **Path Resolution:** Environment loaders explicitly anchor to the project root (`caseloop/.env`), ensuring seeders, migration scripts, and backend instances share identical connection strings.
* **Port Management:** Local port `8000` is dedicated exclusively to the Uvicorn hot-reloading development server, separating containerized data persistence from application compute.

### Security & Authentication Pipeline

* **Bcrypt Hashing:** Verified that user records (`chago@redcross.org.ke` / `llybisetga@gmail.com`) use native app security functions (`app.core.security`) for robust password hashing and verification.
* **Session Management:** Secure `httponly` cookies (`SESSION_COOKIE`, `CSRF_COOKIE`) handle state between the FastAPI backend and the React frontend client (`api.ts`).

---

## 3. Post-Mortem: Debugging History & Root Causes

Understanding the hurdles encountered today provides a vital mental model for maintaining system stability moving forward:

| Incident / Bug | Root Cause | Preventive Engineering Rule |
| --- | --- | --- |
| **1. Split `.env` Path Trap** | `seed.py` inside `backend/app/` used relative paths (`..`) that missed the project root, falling back to empty states or local SQLite files. | **Single Source of Truth:** Environment files must reside at the root; initialization scripts must explicitly resolve paths relative to that root. |
| **2. Port 8000 Ghost Processes (`WinError 10013`)** | Abrupt terminal closures left background Uvicorn workers and Python sockets bound to the host network stack, blocking subsequent boots. | **Explicit Port Hygiene:** Never assume a port frees automatically. Audit TCP bindings (`Get-NetTCPConnection`) before starting local servers. |
| **3. Docker vs. Local Port Collisions** | Running FastAPI inside Docker *and* locally via Uvicorn simultaneously caused both to fight for host port `8000`. | **Separation of Concerns:** Docker manages infrastructure services (PostgreSQL), while application code runs locally on the host for rapid hot-reloading. |
| **4. Alembic Non-Empty Database Panic** | Wiping Docker volumes dropped physical tables while leaving Alembic version tables out of sync, triggering startup safety locks. | **Migration Synchronization:** When pre-seeding pre-existing tables, always run `alembic stamp head` to align version metadata. |

---

## 4. The Google Staff Engineer Blueprint

To scale this architecture to enterprise standards, a senior engineering approach enforces:

1. **12-Factor Environment Validation:** Implement strict Pydantic `BaseSettings` validation on application startup. If critical environment variables or database connections fail, the application halts immediately with a clear diagnostic error before initializing connection pools.
2. **Container Development Parity:** Use explicit Docker Compose profiles separating development (`docker-compose.dev.yml`) from production, complete with health checks that delay dependent service execution until databases are fully accepting traffic.
3. **Idempotent Database Seeders:** Seed scripts must utilize `UPSERT` semantics or existence checks so they can run repeatedly without throwing integrity constraint violations or requiring manual volume wipes.

---

## 5. Real-World Walkthrough: Ingesting Data Science & YouTube Shorts Metrics

Imagine a data scientist delivers a new dataset containing trending YouTube Shorts performance metrics (engagement rates, audio track IDs, regional impressions) that must be ingested and visualized in CaseLoop:

* **Step 1: Schema Extension:** Define a new SQLAlchemy model in `backend/app/models/models.py` (e.g., `YouTubeShortsMetric`) linking to existing operational responses or campaigns.
* **Step 2: Migration Generation:** Generate and apply a clean Alembic migration:
```powershell
python -m alembic revision --autogenerate -m "add youtube shorts metrics table"
python -m alembic upgrade head

```


* **Step 3: Ingestion Pipeline:** Create a validated FastAPI router (`backend/app/api/shorts.py`) using Pydantic schemas to ingest batch payloads from the data science pipeline.
* **Step 4: Frontend Sync:** Update `types.ts` and `api.ts` to fetch and render the new metrics inside your React analytics dashboard.

---

## 6. Immediate Action Plan & Next Steps

When you return to the codebase, follow this exact sequence before tackling WhatsApp webhooks or cloud deployment:

1. **Start PostgreSQL Container:**
```powershell
docker compose up -d db

```


2. **Launch Uvicorn Backend:**
```powershell
cd backend
python -m uvicorn app.main:app --reload --port 8000

```


3. **Audit API Modules:** Review route handlers (`responses.py`, `assignments.py`, `intakes.py`, `reports.py`, `admin.py`) to ensure all raw queries adhere strictly to SQLAlchemy PostgreSQL sessions.

---

## 7. Official Session Logbook Entry

**Work Done:** Synchronized Docker PostgreSQL with FastAPI backend, resolved Uvicorn socket lockouts (WinError 10013), and aligned Alembic migration states. **Rating:** 8/10. **Reason:** High persistence through complex local environment conflicts. **Skills Applied:** Container orchestration, database state management. **Problems Solved:** Eliminated hidden background process port blocks and credential hash mismatches.

Here is a quick recap of everything we accomplished and fixed during our session today:

### 1. Docker & Database Alignment

* **Cleaned Slate:** Successfully cleared and re-seeded your Dockerized PostgreSQL database with your core users (`chago@redcross.org.ke` as admin) without needing to tear down or wipe the container volume.
* **Database Resilience:** Confirmed your SQLAlchemy configuration (`pool_pre_ping=True`) is keeping the connection healthy and responsive.

### 2. Solving the Cookie & CORS Authentication Trap

* **The Root Cause:** Identified that modern browsers treat `localhost:5173` and `127.0.0.1:8000` as cross-site origins, which causes security rules to automatically strip authentication cookies.
* **Vite Proxy Integration:** Configured Vite's dev server proxy to seamlessly forward `/api` requests to your FastAPI backend, allowing your frontend and backend to share the exact same origin.
* **`api.ts` Refinement:** Updated your API client base URL to default to relative paths (`/api`), ensuring cookies, credentials, and tokens attach smoothly on every request.

### 3. Current Status

* **Login Functionality:** Authentication is fully working, and your login sessions are sticking properly.
* **Next Steps for Later:** The minor root health-check route mismatch (`/` vs `/api/...`) has been isolated and can be polished whenever you're ready.