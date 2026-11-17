That “Preparing metadata (pyproject.toml …)” step you’re seeing with pip is normal — it happens when packages use **PEP 517/518 builds**. Some libraries (like SQLAlchemy or Alembic) need to build wheels from source, which can take a while depending on your machine and network. If it feels stuck, give it a few minutes; if it hangs indefinitely, you can try:

```powershell
pip install --upgrade pip setuptools wheel
```

and then rerun:
```powershell
pip install -r requirements.txt
```

That usually speeds things up.

---

### ⚛️ Installing Vite (Frontend)

You don’t need to copy‑paste `package.json` manually. Instead, run this in your **frontend root** (not `src`):

```powershell
npm create vite@latest
```

Choose `React + TypeScript` when prompted. This generates a `package.json` and scaffolds the project. Then:

```powershell
cd frontend
npm install
npm run dev
```

👉 Always run npm commands from the **frontend root** (where `package.json` lives), not inside `src`.

---

### 🧩 Dlang Fullstack Path

If you pivot to Dlang later, here’s how it fits:

- **Backend**: Use `arsd` modules (`arsd.cgi` for REST APIs, `arsd.web` for UI).
- **Frontend/UI**: You can serve HTML directly from Dlang or still use React if you prefer.
- **Database**: Connect to Postgres via `arsd.database` or `dpq2` (D bindings for libpq).
- **Workflow**: Dlang compiles to native binaries, so you’d skip Python/Node entirely. Deployment is simpler (just ship the binary + Postgres).

This is a good long‑term plan if you want systems‑level control and less runtime overhead.

---

### 🐳 Ollama on Windows

Right now Ollama doesn’t install like a Python venv — it’s a **system‑level runtime**. On Windows:

- Download the installer from [ollama.com/download](https://ollama.com/download).
- It sets up a background service and CLI (`ollama run mistral`).
- Models are stored in `%LOCALAPPDATA%\Ollama\models`.

There isn’t a “portable venv‑style” Ollama yet. The closest is projects like **ollama‑rucksack** (bootable ISO with Ollama preinstalled) or running Ollama inside Docker. But on Windows, the official installer is the cleanest way.

---

### 🧭 What You’re Forgetting

- **Alembic config**: You’ll need to edit `alembic.ini` to point to your DB (`DATABASE_URL`).
- **Environment management**: Use `.env` files for secrets and DB URLs.
- **Docs**: You already have `README.md`, but add `DEPLOYMENT.md` and `TROUBLESHOOTING.md` early.
- **Frontend tooling**: Tailwind CSS and ESLint/Prettier for clean UI dev.
- **GitHub Actions (later)**: For CI/CD when you move to DigitalOcean.

---

👉 My recommendation:  
- Finish pip install (upgrade pip if slow).  
- Run `npm create vite@latest` in `frontend`.  
- Install Ollama globally on Windows (don’t fight for a venv‑style install).  
- Keep SQLite locally, but start learning Alembic → Postgres migration for DigitalOcean.  
- If you later switch to Dlang, you’ll rebuild backend logic but keep the same DB and docs.  

Would you like me to draft a **TROUBLESHOOTING.md template** now so you’re covered when pip/npm inevitably throw their first errors?