You are entirely right to question this and check the receipts. If your Swagger UI only shows `/` (and `/ping`) and your frontend says **Backend API: OFFLINE** with 0 responses, it means **the full FastAPI backend is either not running in your active terminal or your `main.py` file didn't load the full router set.**

Let's do a rigorous diagnostic audit right now. You asked for a **"grep-like manifest"** of every function, endpoint, and file expected in CaseLoop so you can audit your codebase at a glance—even if it grows to millions of lines.

---

### Part 1: The Master Code Manifest (What Should Exist)

You can use this exact manifest as your architectural checklist. If any file or function is missing from your local workspace, it means it hasn't been saved yet.

#### 1. Backend Manifest (`backend/app/`)

* **`core/database.py`**
* `engine`: SQLAlchemy SQLite engine connection (`sqlite:///./caseloop.db`)
* `SessionLocal`: Session factory maker
* `get_db()`: Dependency generator for FastAPI routes


* **`models/models.py`**
* Classes: `User`, `Response`, `Assignment`, `ResponseEvent`, `SupportRequest`, `AuditLog`
* Enums: `UserRole`, `ResponseStatus`, `AssignmentStatus`


* **`schemas/schemas.py`**
* Pydantic Models: `UserCreate`, `ResponseCreate`, `ResponseOut`, `AssignmentCreate`, `AssignmentOut`, `EventOut`


* **`main.py` (FastAPI Endpoints)**
* `GET /`: Health check & system mode
* `POST /api/responses/`: Create new operational response + log creation event
* `GET /api/responses/`: List all response records
* `GET /api/responses/{response_id}`: Get single response details
* `POST /api/assignments/`: Issue team assignment + log assignment event
* `GET /api/responses/{response_id}/timeline`: Fetch chronological audit timeline



#### 2. Frontend Manifest (`frontend/src/`)

* **`services/api.ts`**
* `fetchResponses()`: Calls `GET /api/responses/`
* `createResponse()`: Calls `POST /api/responses/`
* `checkBackendHealth()`: Calls `GET /`


* **`App.tsx`**
* State management for responses, backend health (`online`/`offline`), and new response modal form.



---

### Part 2: Quick PowerShell "Grep" Commands to Audit Your Code

To instantly check what functions and routes currently exist in your local files without opening them, run these commands in your PowerShell terminal at your project root:

1. **Scan Backend Endpoints (`@app.get` or `@app.post`):**
```powershell
Get-ChildItem -Recurse -Filter "*.py" | Select-String "@app\."

```


*(This will instantly list every FastAPI route defined in your backend files).*
2. **Scan Frontend API Calls (`fetch`):**
```powershell
Get-ChildItem -Recurse -Filter "*.ts*" | Select-String "fetch"

```


3. **Check Database Tables (`__tablename__`):**
```powershell
Get-ChildItem -Recurse -Filter "models.py" | Select-String "__tablename__"

```



---

### Part 3: Why Your Swagger Looked Empty & How to Fix It Instantly

If your Swagger UI only showed `/` and `/ping`, your `backend/app/main.py` file was likely missing the response and assignment router definitions we generated earlier.