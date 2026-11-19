# CaseLoop: Master Handover Document & Attachment Blueprint
**Humanitarian Response Coordination & Operational Intelligence System**  
*Karen-Lang'ata Digital Innovation Lab · Red Cross Attachment Project*

> **Direction update (November 13, 2026):** This handover contains historical plans and examples; do not use its old seeded credentials or mark its old checklist as current. For current status and commands, see [Implementation](IMPLEMENTATION.md), [Deployment](../../deployment/DEPLOYMENT.md), the [Master Project Charter](caseloop_master_project_charter.md), and [Checkpoint 6](../progress/chkpnt6.md). SQLAlchemy remains the ORM; SQLite is the offline option and Docker Compose PostgreSQL is the local shared-database option. Current code has reviewed intake, role-based email/password access, event timeline, report preview/Word output, and a Meta webhook that creates pending text drafts only. There is no live WhatsApp connection or public hosting.

---

## 1. Daily Logbook Entry (Wednesday, November 4, 2026)

* **Date:** Wednesday, 4th November 2026
* **Time Duration:** 8 Hours (08:00 - 17:00)
* **Activity:** Researched local AI integration using Ollama; successfully installed Ollama for Windows, diagnosed local TCP socket/port binding issues, and mapped modular RAG architecture.
* **Effectiveness:** 9/10
* **Reason for Rating:** Successfully diagnosed system-level ports and ensured smooth AI service fallback without blocking core database operations.
* **Knowledge Learned:** Local LLM daemon architecture, port binding resolution, and offline AI fallback design.
* **Interactions:** Solo debugging, technical documentation review, and architectural mentor feedback.
* **Skills Applied:** PowerShell diagnostic scripting, network socket analysis, and local AI runtime configuration.
* **Problems & Solutions:** Resolved Ollama `bind: 127.0.0.1:11434` port conflict by verifying background daemon execution in Windows task tray.

---

## 2. Command Refresher & Local Environment Verification

Keep this quick command cheatsheet handy to launch and verify all layers of CaseLoop.

### A. Backend (FastAPI + SQLite + SQLAlchemy)
From the root directory `caseloop/`:
```bash
# Navigate to backend and activate virtual environment
cd backend
source venv/bin/activate  # On Windows PowerShell: venv\Scripts\activate

# Use the existing Python 3.11 virtual environment and pinned dependencies
.\venv\Scripts\python.exe -m pip install -r requirements.txt

# Create the initial administrator through the interactive CLI
python -m app.create_admin

# Launch FastAPI application server with auto-reload
uvicorn app.main:app --reload --port 8000
```
* **API Documentation (Swagger UI):** `http://127.0.0.1:8000/docs`
* **Alternative API Documentation (ReDoc):** `http://127.0.0.1:8000/redoc`
* **Health Check Endpoint:** `http://127.0.0.1:8000/`

### B. Schema Migrations (Alembic)
```bash
# Create a new migration script after modifying models.py
alembic revision --autogenerate -m "describe_changes"

# Apply pending migrations to SQLite database
alembic upgrade head
```

### C. Frontend (React + Vite + Tailwind CSS)
From the root directory `caseloop/`:
```bash
# Navigate to frontend and install dependencies
cd frontend
npm ci

# Launch Vite development server
npm run dev
```
* **Frontend Web Application:** `http://localhost:5173`

### D. Local AI Engine (Ollama)
```bash
# Check if Ollama service is running and list downloaded models
ollama list

# Pull lightweight model for offline summarization
ollama pull qwen2.5:1.5b  # or llama3:8b

# Run interactive terminal session with the model
ollama run qwen2.5:1.5b
```

---

## 3. Deep Dive: "The Data-First Backbone Approach"

### What is the Data-First Backbone Approach?
In web application development, engineers often debate between **UI-Driven (Top-Down)** design and **Data-First Backbone (Bottom-Up)** architecture.

In CaseLoop, we selected the **Data-First Backbone Approach**. This means:
1. **Core Domain Entities First:** We define database models (`User`, `Response`, `Assignment`, `ResponseEvent`, `SupportRequest`) and relationships first.
2. **Schema & Validation Layer:** We construct strict Pydantic schemas for input validation and serialized outputs.
3. **Interactive API Verification:** We expose these entities through FastAPI endpoints. Because FastAPI automatically generates interactive OpenAPI/Swagger documentation (`/docs`), we gain a live, testable API *before* frontend development finishes.
4. **UI Integration:** The React frontend connects directly to validated backend contracts, eliminating double work caused by mismatched mock interfaces.

### Architectural Diagram (Data Flow)
```text
  ┌─────────────────────────────────────────────────────────┐
  │                 React + Vite Frontend                   │
  │   (Response Register, Dashboard Shell, Task Lists)     │
  └───────────────────────────┬─────────────────────────────┘
                              │ HTTP / REST APIs
                              ▼
  ┌─────────────────────────────────────────────────────────┐
  │                   FastAPI Controller                    │
  │          (Pydantic Input/Output Schemas)               │
  └───────────────────────────┬─────────────────────────────┘
                              │ ORM Calls
                              ▼
  ┌─────────────────────────────────────────────────────────┐
  │                 SQLAlchemy Engine                       │
  │               (Alembic Migration Pipelines)             │
  └───────────────────────────┬─────────────────────────────┘
                              │ Local Persistence
                              ▼
  ┌───────────────────────────┴─────────────────────────────┐
  │                SQLite Database File                     │
  │                    (caseloop.db)                        │
  └─────────────────────────────────────────────────────────┘
```

---

## 4. Master Checklist for Attachment & Project Completion

### A. Technical Deliverables (CaseLoop MVP)
- [x] Backend database layer (`caseloop.db`, SQLAlchemy ORM).
- [x] Alembic migration pipeline configured for SQLite batch mode.
- [x] Synthetic demo data seeding script (`app/seed.py`).
- [x] Operational Response Register CRUD endpoints.
- [x] React + Vite + Tailwind CSS frontend dashboard shell.
- [ ] Assignment Management module (Assign team, acknowledge, update status).
- [ ] Operational Timeline view (chronological activity stream).
- [ ] CSV report export engine.
- [ ] Optional local Ollama summarization integration.

### B. University Attachment Deliverables
- [x] Logbook entries for Week 1 (Monday to Friday).
- [x] Logbook entry for Week 2 Monday (Database Core).
- [x] Logbook entry for Week 2 Tuesday (AI Research & Ollama Installation).
- [x] Logbook entry for Week 2 Wednesday (Ollama Port Debugging & Pipeline Mapping).
- [ ] Weekly Logbook entries for Weeks 3–8.
- [ ] Final University Attachment Report (Organization summary, technical contribution, theoretical-to-practical translation, personal fulfillment statement).

### C. Karen-Lang'ata Digital Innovation Lab Deliverables
- [x] Founding Project Document (`CASE-LOOP_RED-CROSS_CONSIDERATION.docx`).
- [x] Project directory tree and modular monolith layout.
- [ ] Innovation Lab Handover Directory (`docs/handover/`).
- [ ] Student Onboarding & Succession Guide.
- [ ] Executive Presentation Deck (10 slides for Branch Management/HQ).

---

## 5. Strategic Recommendations: University Alignment, Lab Leadership & Commercialization

### A. Aligning with University Evaluation Criteria
Academic evaluators prioritize:
1. **Application of Theoretical Knowledge:** Emphasize how software design patterns (MVC, Modular Monoliths, ORM abstractions) solved real-world administrative inefficiencies.
2. **Methodology:** Document your iterative development lifecycle (Requirements $\rightarrow$ Database Design $\rightarrow$ API Implementation $\rightarrow$ UI Integration $\rightarrow$ Offline Testing).
3. **Problem-Solving Skills:** Detail concrete technical obstacles you resolved (e.g., handling SQLite schema alteration constraints using Alembic batch mode).

### B. Positioning the Karen-Lang'ata Digital Innovation Lab
To position yourself as the head/initiator of a Digital Innovation Lab at the branch:
* Frame CaseLoop as **"Project #001"** of the lab rather than a single standalone student exercise.
* Provide clean handover templates so future attachment students can build additional modules (e.g., inventory tracking, community message triage).
* Present the lab to branch leadership as a **zero-cost, high-impact innovation engine** powered by structured student attachments.

### C. Commercialization & Software Sales Strategy
* **Maintain Intellectual Property Boundaries:** Keep your personal startup codebase distinct from branch operational data.
* **The "Open Core" Business Model:** Offer the basic response notebook as open source for community humanitarian groups, while offering hosted cloud infrastructure, multi-branch syncing, custom security roles, and enterprise SLA contracts to larger NGOs.
* **Networking via Red Cross:** Leverage your attachment to present CaseLoop at civic tech meetups, humanitarian technology conferences, and social innovation grants (e.g., Google for Startups, Mozilla Open Source Grants).

---

## 6. Sequential Prompts for Future Chat Sessions

To prevent session degradation or context loss, copy and paste these exact prompts into new chat sessions as you progress through each remaining phase.

### Prompt 1: Phase 2 — Assignment Management UI & Status Workflow
```text
I am resuming work on CaseLoop (Offline-First Humanitarian Response App). 
Context Snapshot:
- Stack: FastAPI, SQLite, SQLAlchemy, React, Vite, Tailwind CSS.
- Current State: Response register DB models, seed scripts, and React dashboard shell are complete.

Task: Let's implement the Assignment Management module.
1. Update FastAPI endpoints to support updating assignment statuses (ASSIGNED -> ACKNOWLEDGED -> IN_PROGRESS -> COMPLETED) with completion notes.
2. Build the React component for issuing assignments and managing task statuses on the frontend.
3. Provide production-grade, heavily commented code following our modular monolith structure.
```

### Prompt 2: Phase 2 — Operational Timeline & Audit Trail UI
```text
I am resuming work on CaseLoop (Offline-First Humanitarian Response App).
Context Snapshot:
- Stack: FastAPI, SQLite, SQLAlchemy, React, Vite, Tailwind CSS.
- Current State: Response register and Assignment management are fully operational.

Task: Let's build the Operational Timeline UI view.
1. Connect the `/api/responses/{id}/timeline` endpoint to the React frontend.
2. Display a chronological stream of events (Response Created, Assignment Issued, Status Updated) with visual icons and actor badges.
3. Ensure offline performance and responsive UI using Tailwind CSS.
```

### Prompt 3: Phase 3 — CSV Export Engine & Local Ollama AI Summarization
```text
I am resuming work on CaseLoop (Offline-First Humanitarian Response App).
Context Snapshot:
- Stack: FastAPI, SQLite, SQLAlchemy, React, Vite, Tailwind CSS, Ollama.
- Current State: Core response tracking, assignments, and timeline are complete.

Task: Let's build the Reporting & Local AI Summarization module.
1. Add a backend utility to generate exportable CSV reports of response registers and assignments.
2. Build a python service wrapper using `requests` that connects to local Ollama (`http://localhost:11434/api/generate`) to draft operational case summaries.
3. Ensure AI failure fallback so the system remains 100% functional even if Ollama is offline.
```

### Prompt 4: Phase 4 — University Final Report & Attachment Documentation
```text
I am preparing my University Attachment Final Report for CaseLoop at the Red Cross Karen-Lang'ata Branch.
Please generate a comprehensive, academic-grade final report structure including:
1. Executive Summary & Organizational Overview (Type, Structure, Humanitarian Mission).
2. Critical Administrative Challenge (Information fragmentation across chat channels and the CaseLoop solution).
3. Theoretical Knowledge Translation to Practical Skills (Software engineering, ORM, offline database design).
4. Summary of Overall Career Lessons & Personal Fulfillment Statement.
5. Student Handover & Digital Innovation Lab Succession Plan.
```