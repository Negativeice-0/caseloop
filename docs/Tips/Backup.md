Here is your comprehensive **End-of-Session Tip Guide** containing all the practical troubleshooting notes, backup procedures, and configuration steps that belong outside the formal architecture checkpoint file.

You can use this to close out today's work with total peace of mind:

---

### 1. The SQLite Database Backup Guide

Because SQLite is a file-based database, keeping a snapshot of your state is essential before running experimental migrations.

* **How to Backup:** Stop your Uvicorn server, then run the following PowerShell command in your project root:
```powershell
Copy-Item "backend\caseloop.db" "backend\caseloop_backup.db"

```


* **Why:** This ensures you have a pristine restore point if any future Alembic migration drops a table or corrupts local state.

### 2. Troubleshooting Note: Router Imports & Class Naming

* **The Issue Encountered:** Python raised a `NameError` and `ImportError` when FastAPI tried to handle admin requests.
* **The Root Cause:** The API router (`backend/app/api/admin.py`) attempted to call `AdminService`, but the service file was explicitly named `admin_secret.py` and contained the class `AdminSecretService`.
* **The Permanent Rule:** Always ensure that when creating or refactoring backend modules, your imported class identifiers match the exact name defined in your service files.

### 3. Fixing the TypeScript CSS Import Warning (`vite-env.d.ts`)

* **The Issue:** TypeScript throws `Cannot find module or type declarations for side-effect import of './index.css'`.
* **The Fix:** Ensure a file named `src/vite-env.d.ts` exists inside your `frontend/` directory containing ambient Vite types:
```typescript
/// <reference types="vite/client" />

```


* **Rebuild Cache:** If the warning persists, restart your Vite development server with a force cache clear:
```bash
npm run dev -- --force

```



### 4. Responsive Mobile Navigation (Planned for Tomorrow)

* **The Pattern:** To implement YouTube-style navigation where the sidebar drops to a horizontal bottom bar on small screens and snaps back to a vertical sidebar on desktop (`md:` breakpoint), apply responsive Tailwind classes to your `<aside>` container:
```tsx
className="fixed bottom-0 left-0 w-full bg-white border-t border-slate-200 p-4 flex flex-row items-center justify-around z-20 shadow-lg md:relative md:w-72 md:h-screen md:border-t-0 md:border-r md:flex-col md:justify-between md:p-6"

```


* **When to Implement:** Integrate this directly into `Sidebar.tsx` during tomorrow's component decomposition phase.

---

Have a great evening! Whenever you return tomorrow, just bring your handover or checkpoint, and we will dive straight into modular component refactoring.