CaseLoop Checkpoint 2: Master Architectural Record
Status: VERIFIED & LOCKED IN
Project: CaseLoop (Offline-First Red Cross Humanitarian Coordination Tool)
Target Environment: Red Cross Karen-Lang'ata Branch
Hardware & Language Runtime: Intel Core i3 Workstation, 8GB RAM, Python 3.11 Environment, Local Windows OS (`C:\Users\Admin\Documents\caseloop`)

1. Executive Summary & Foundational State
Checkpoint 2 represents the successful implementation and verification of the secure offline-first Admin Portal and real-time hardware monitoring subsystem. Operating entirely locally with zero cloud dependencies, the system monitors Core i3 workstation resources using Python's `psutil` library and enforces administrative security via a time-sensitive, single-use dynamic keyword authentication service (`AdminSecretService`) backed by SQLite persistence.
2. Pinpoint Dependency Baseline (Ground Truth)
A. Python 3.11 Backend Environment (`backend/requirements.txt`)

* FastAPI, Uvicorn, SQLAlchemy, Alembic, and `psutil` for hardware performance telemetry.

B. Frontend Manifest (`frontend/package.json`)

* React 18, Vite 5, TypeScript, Tailwind CSS, and `lucide-react` for enterprise UI components.

3. Directory Tree & Architecture Audit Verification

* **Backend Services:** Added `backend/app/services/admin_secret.py` and `backend/app/models/models.py` (AdminToken table) to manage single-use keys and expiration policies.
* **Backend API Routes:** Registered `/api/admin/system-status`, `/api/admin/request-keyword`, and `/api/admin/verify-keyword` inside `backend/app/api/admin.py`.
* **Frontend Modules:** Centralized types in `frontend/src/types/index.ts`, consolidated REST communication in `frontend/src/services/api.ts`, and encapsulated the resource monitor inside `frontend/src/features/admin/AdminControl.tsx`.

4. Official University Attachment Logbook Entry (Week Ending: November 6, 2026)
· **Activities Undertaken:**
5. Implemented backend system monitoring utilities using `psutil` to track CPU utilization and available RAM under workstation constraints.
6. Developed the `AdminSecretService` and `AdminToken` SQLite model to generate and verify secure, single-use, 5-minute time-sensitive access keywords.
7. Resolved FastAPI routing decorators, import mapping inconsistencies, and Alembic database migration dependencies.
8. Refactored the React frontend to establish a clean separation of concerns, integrating a secure admin unlock modal and live hardware metrics dashboard.
9. Professional Recommendations & Handover Notes

* **Recommendation 1 (Atomic Commits):** Commit code in small, logical increments after verifying feature behavior.
* **Recommendation 2 (Environment Isolation):** Always activate the Python virtual environment (`.\venv\Scripts\Activate`) before executing Uvicorn servers or running database commands.
* **Recommendation 3 (Local Data Backup):** Periodically back up `caseloop.db` prior to running experimental database migrations.

6. End-of-Day Wrap-Up Checklist