## Backend Pytest Troubleshooting & Verification Guide: FastAPI & SQLAlchemy

---

### 1. Final Session Summary

During test suite configuration for the **CaseLoop** backend, execution evolved from environment configuration blocks to full test isolation success.

* **Milestone Achieved:** Successfully executed `pytest tests/test_assignments.py`, resulting in all 4 test cases passing cleanly (`4 passed in 0.67s`).
* **Key Challenges Overcome:**
1. **Python Path Resolution (`PYTHONPATH`):** Fixed `ModuleNotFoundError` by explicitly ensuring Python recognizes the local workspace as a root package source.
2. **Database Schema Initialization:** Resolved `OperationalError` (missing tables like `teams` and `responses`) by replacing default in-memory behavior with a shared-connection model using SQLAlchemy's `StaticPool`.


3. **Dependency Mocking:** Aligned FastAPI's `get_db` dependency override with the test suite's temporary SQLite session.





---

### 2. How to Read Pytest Errors (With Examples)

When tests fail, Pytest provides a detailed trace traceback. Here is how to break down common error messages:

#### A. Import & Collection Errors (`ModuleNotFoundError`)

* **What it looks like:**
```text
E   ModuleNotFoundError: No module named 'app'

```


* **How to read it:** Python cannot locate your source directory packages (`app/`) because the terminal's execution context lacks the project root path.
* **The Fix:** Set the environment path before running pytest: `$env:PYTHONPATH="."`.

#### B. Database Schema Errors (`OperationalError: no such table`)

* **What it looks like:**
```text
E   sqlalchemy.exc.OperationalError: (sqlite3.OperationalError) no such table: teams

```


* **How to read it:** The FastAPI endpoint code executed a SQL query against a database table (`teams`) that hasn't been created yet, or the test client is hitting a separate, isolated database connection from the one where tables were generated.


* **The Fix:** Ensure your test configuration uses an engine configured with `poolclass=StaticPool` so that all threads and connections share the same in-memory tables.



#### C. Assertion Failures (`AssertionError`)

* **What it looks like:**
```text
E   AssertionError: assert {'status': 'online'} == {'status': 'active'}

```


* **How to read it:** The test ran successfully end-to-end, but the JSON payload or status code returned by your API endpoint did not match the expected value hardcoded in your test file's `assert` statement.
* **The Fix:** Update either your endpoint code logic or your test assertions to match expected business rules.

---

### 3. What to Expect for Verification

When your testing environment is fully healthy, your terminal output will confirm successful test collection, execution, and summary metrics.

* **Successful Execution Output:**
```powershell
(venv) PS C:\Users\Admin\Documents\caseloop\backend> $env:PYTHONPATH="."
(venv) PS C:\Users\Admin\Documents\caseloop\backend> pytest tests/test_assignments.py
============================= test session starts ==============================
platform win32 -- Python 3.11.9, pytest-8.2.0, pluggy-1.7.0
rootdir: C:\Users\Admin\Documents\caseloop\backend
plugins: anyio-4.15.1
collected 4 items                                                               

tests\test_assignments.py ....                                            [100%]

======================== 4 passed, 6 warnings in 0.67s =========================

```


* **Indicators of Success:**
* **Dots (`....`):** Each dot represents a passing test function inside `test_assignments.py`.
* **Summary line (`4 passed`):** Indicates 100% green test execution.
* **Deprecation warnings:** Pydantic V2/Starlette warnings are normal third-party library notices and do not block code execution or deployment.



---

### 4. Final Thoughts

Testing asynchronous web frameworks like FastAPI alongside relational ORMs like SQLAlchemy often feels tricky at first because of boundary management—keeping your production files untouched while spinning up fast, isolated data layers in memory.

By utilizing **`TestClient`**, explicit **dependency overrides (`get_db`)**, and a **`StaticPool` in-memory SQLite setup**, you now have a professional, deterministic test pipeline. Your tests can run in under a second without needing Uvicorn servers or touching external database files, giving you instant feedback as you build out the rest of CaseLoop!