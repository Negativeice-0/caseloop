CaseLoop Checkpoint 1: Master Architectural Record
Status: VERIFIED & LOCKED IN
Project: CaseLoop (Offline-First Red Cross Humanitarian Coordination Tool)
Target Environment: Red Cross Karen-Lang'ata Branch
Hardware & Language Runtime: Intel Core i3 Workstation, 8GB RAM, Python 3.11 Environment, Local Windows OS (C:\Users\Admin\Documents\caseloop)

1. Executive Summary & Foundational State
Checkpoint 1 represents the complete build and verification of the Core Monolith Architecture & Round-Trip Data Persistence. The system operates 100% locally with zero cloud dependencies and zero local LLM overhead (Llama 3 / Ollama are permanently excluded due to hardware constraints).
All intelligence and analytical features are powered natively by Python 3.11 utilities (psutil, difflib, SQLite FTS5). All core data operations pass asynchronously from the React UI through FastAPI down to local SQLite storage.

2. Pinpoint Dependency Baseline (Ground Truth)
A. Python 3.11 Backend Environment (backend/requirements.txt)
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

B. Frontend Manifest (frontend/package.json)
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
    "react-dom": "^18.2.0"
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


3. Directory Tree Audit Verification
Verified via .\scripts\audit_tree.ps1 (60 Total Files Accounted For):
C:\Users\Admin\Documents\caseloop
├── Makefile
├── README.md
├── setup.ps1
├── backend/
│   ├── alembic.ini
│   ├── caseloop.db
│   ├── requirements.txt
│   ├── alembic/
│   │   ├── env.py
│   │   └── versions/ (1b86f570ca4e, 63fb95653be7, cda7af70145b)
│   └── app/
│       ├── main.py
│       ├── seed.py
│       ├── api/ (admin.py)
│       ├── core/ (config.py, database.py)
│       ├── models/ (models.py)
│       ├── schemas/ (schemas.py)
│       └── services/ (system_monitor.py)
├── docs/
│   ├── master_platform_checklist.md
│   ├── master_prompt_template.md
│   ├── projects/
│   │   ├── yesterday.md
│   │   ├── progress/ (chkpnt1_v2.md)
│   │   └── caseloop/ (1- CASE-LOOP_RED-CROSS_CONSIDERATION.txt)
│   └── trouble/ (1-setup.md, 2-dbIssues.md, 3-poweshell.md)
├── frontend/
│   ├── index.html
│   ├── package.json
│   ├── postcss.config.js
│   ├── tailwind.config.js
│   └── src/
│       ├── App.tsx
│       ├── index.css
│       ├── main.tsx
│       ├── features/dashboard/Dashboard.tsx
│       └── services/api.ts
└── scripts/
    ├── audit_tree.ps1
    └── test_ollama.ps1


4. Official University Attachment Logbook Entry
Copy and paste directly into your university logbook for the week ending November 6, 2026:
·	Week Ending: November 6, 2026
·	Department: Software Engineering & Operations Support (Red Cross Karen-Lang'ata Branch)
·	Activities Undertaken:
1.	Audited and structured the FastAPI backend data models (ResponseItem, Assignments, Events) with Python 3.11 and Pydantic v2 validation schemas.
2.	Resolved ES module scope configuration conflicts in frontend build tools by configuring PostCSS CommonJS support (postcss.config.js).
3.	Configured Cross-Origin Resource Sharing (CORS) middleware in FastAPI to enable real-time asynchronous REST calls from the React 18 / Vite 5 frontend.
4.	Tested round-trip data persistence, verifying that operational state changes correctly save to the local SQLite database (caseloop.db).

5. Architectural Rules & Core i3 / Python 3.11 Directives
1.	Local LLM Abandonment: Ollama and Llama 3 are permanently removed from development plans. The Core i3 / 8GB system cannot support model inference.
2.	Python-Native Analytics: Operational summaries, audit logs, and status analytics must be built using deterministic Python 3.11 modules (psutil hardware monitoring, difflib fuzzy search, and SQLite FTS5 index queries).
3.	Frontend Separation of Concerns: Monolithic App.tsx will be broken down into modular UI components (Sidebar.tsx, TopHeader.tsx, ResponseRegister.tsx, ProfileView.tsx, AdminDashboard.tsx) in Phase 2.
4.	Role Separation: General users view their personal operational tasks in "Profile"; administrative metrics and system resource controls remain in "Admin & System Control".

6. Transition to Checkpoint 2 (Master Checklist Target)
Development moves directly to Phase 2: Operational Visibility & System Health:
·	Step A: Refactor App.tsx into modular components (Sidebar.tsx, TopHeader.tsx, ResponseRegister.tsx).
·	Step B: Implement backend/app/services/system_monitor.py using psutil to track hardware usage without load spikes.
·	Step C: Expose GET /api/admin/system-status in FastAPI.
·	Step D: Render the system monitor hardware card in the React Admin panel.
·	Step E: Build the responder Profile View tab.
