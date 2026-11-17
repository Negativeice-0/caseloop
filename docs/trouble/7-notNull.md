# Backend Database & API Troubleshooting Guide: FastAPI, SQLAlchemy & Alembic

## Executive Technical Summary

This document captures a comprehensive root-cause analysis and resolution walkthrough for a critical database-model divergence issue encountered during backend development for the **CaseLoop** platform.

Over a multi-hour debugging session, the team resolved a persistent HTTP 500 Internal Server Error (`sqlite3.IntegrityError: NOT NULL constraint failed: assignments.assignee_name`) during dynamic entity creation via automated PowerShell test suites. The issue was resolved in a zero-downtime, non-destructive manner without resetting or deleting the active production/development database.

---

## 1. Comprehensive Session Timeline & Analysis

### 1.1 The Context & Objective
The primary objective was to automate assignment creation and verification end-to-end using a custom PowerShell test script (`test_assignment.ps1`), connecting to a FastAPI application backed by SQLAlchemy ORM and an SQLite database managed through Alembic migrations.

### 1.2 The Bug Manifestation
When sending a `POST /api/assignments/` request, the server returned an HTTP 500 error with the following traceback snippet:

```text
sqlite3.IntegrityError: NOT NULL constraint failed: assignments.assignee_name
[SQL: INSERT INTO assignments (reference_code, response_id, team_id, status, description, updated_at) VALUES (?, ?, ?, ?, ?, ?) RETURNING id, created_at]
[parameters: ('CR-KL-2026-TST-132005', 1, 1, 'Active', 'Automated test assignment deployment', None)]
```

### 1.3 Key Technical Paradoxes Discovered
1. **Model & Schema Alignment:** `assignee_name` had been explicitly removed from both the Pydantic request schema (`AssignmentCreate`) and the SQLAlchemy ORM definition (`Assignment`).
2. **Database Schema Lag:** The underlying physical SQLite table (`assignments`) inside `caseloop.db` retained a legacy column (`assignee_name`) configured with a `NOT NULL` constraint from an earlier version.
3. **Database File Ambiguity:** Two database files (`caseloop.db` and `sql_app.db`) existed in the backend directory. The application was explicitly mapped to `caseloop.db` via `Settings.DATABASE_URL`, but initial quick-fix scripts targeted `sql_app.db`, returning `sqlite3.OperationalError: no such table: assignments`.
4. **Memory State Caching:** In-memory Uvicorn server states and SQLite connection handles held onto stale schema definitions across migration attempts until process reboots were forced.

---

## 2. Deep Dive: Why SQLite Column Dropping Required Special Handling

In standard relational database management systems (RDBMS) such as PostgreSQL or MySQL, altering a table to drop a column is straightforward:
$$\text{ALTER TABLE } \text{assignments} \text{ DROP COLUMN } \text{assignee\_name};$$

However, SQLite’s architecture handles Schema Definition Language (DDL) modifications with strict limitations:

### Historical Constraints & Table Rebuilding
* Legacy versions of SQLite (< 3.35.0) do **not** natively support `ALTER TABLE DROP COLUMN`. 
* Historically, dropping a column required a complex multi-step table rewrite:
  1. Create a new temporary table (`assignments_rg_temp`) with the desired column structure.
  2. Copy data from the old table to the temporary table ($\text{INSERT INTO temp SELECT ...}$).
  3. Drop the original table (`DROP TABLE assignments`).
  4. Rename the temporary table to the original name (`ALTER TABLE assignments_rg_temp RENAME TO assignments`).
  5. Recreate all indexes, foreign keys, and triggers.

### Alembic Batch Operations Mode
Alembic accommodates this SQLite limitation via its **batch operation context** (`with op.batch_alter_table(...)`). In migration script `85daa8c7a156`, Alembic defined the column drop, but because migrations were not executed directly against the active `caseloop.db` file, the physical table structure remained out of sync.

### The Non-Destructive Production Direct Fix
Since modern SQLite (3.35.0+) supports inline column drops, the issue was resolved directly on `caseloop.db` without wiping existing data tables (`users`, `responses`, `teams`, etc.):

```python
import sqlite3

conn = sqlite3.connect('caseloop.db')
cursor = conn.cursor()
cursor.execute('ALTER TABLE assignments DROP COLUMN assignee_name;')
conn.commit()
conn.close()
```

---

## 3. Four-Layer Framework for System Integration Troubleshooting

To prevent similar multi-hour roadblocks, follow this **4-Layer Boundary Debugging Protocol**:

```
[ Layer 1: Client Payload ]  ==> JSON body sent from PowerShell/Frontend
           ||
[ Layer 2: Validation Schema] ==> Pydantic models (schemas.py)
           ||
[ Layer 3: ORM Domain Model ] ==> SQLAlchemy declarative classes (models.py)
           ||
[ Layer 4: Physical Database] ==> SQLite / PostgreSQL storage engine (.db)
```

### Layer Verification Steps:
1. **Payload vs. Schema:** Ensure the incoming JSON keys match the Pydantic fields exactly.
2. **Schema vs. ORM Model:** Verify that attributes passed to `Model(**schema.dict())` are defined as `Column(...)` in SQLAlchemy.
3. **ORM Model vs. Database Table:** Query SQLite system tables directly (`SELECT name FROM sqlite_master WHERE type='table';` and `PRAGMA table_info(assignments);`) to verify column names, data types, and `NOT NULL` constraints.
4. **Environment Isolation:** Confirm that `DATABASE_URL` matches the target file being altered during migration executions.

---

## 4. University Logbook & Attachment Report Entry

### Weekly Activity & Problem-Solving Log

* **Task Description:** Automated database integration testing for FastAPI backend endpoints using PowerShell scripts and standardized SQLAlchemy/Alembic migration workflows.
* **Problem Encountered:** Intermittent HTTP 500 exceptions triggered by `sqlite3.IntegrityError` (`NOT NULL constraint failed: assignments.assignee_name`). Schema validation and SQLAlchemy models indicated the field had been deprecated, yet database insertions failed.
* **Root-Cause Analysis:** Identified a multi-faceted divergence between the physical database file (`caseloop.db`), the Alembic migration history, and the ORM domain definitions. Secondary confusion arose from multiple local database files (`sql_app.db` vs `caseloop.db`) and Uvicorn memory caching.
* **Solution Implemented:** 
  1. Traced active database bindings in `app/core/config.py`.
  2. Executed non-destructive direct DDL column removal on `caseloop.db` to align physical storage with current ORM models without data loss.
  3. Cleaned PowerShell test payloads and verified automated POST (`201 Created`) and GET (`200 OK`) workflows.
* **Key Learning:** Mastered production-grade zero-downtime database migration techniques, SQLite DDL batch operations, and structured boundary testing across client, schema, ORM, and database layers.

---

## 5. Verification & Test Execution Results

Following step-by-step remediation, the test script executed with complete success:

```text
==========================================
🚀 TESTING ASSIGNMENT CREATION FLOW
==========================================
📝 Using Response ID: 1
📝 Using Team ID: 1
📝 Generated Reference Code: CR-KL-2026-TST-151706

Posting assignment request...
✅ Assignment Created Successfully! ID: 1

📋 Listing All Assignments in Database:

id reference_code        team_id response_id status
-- --------------        ------- ----------- ------
 1 CR-KL-2026-TST-151706       1           1 Active
```