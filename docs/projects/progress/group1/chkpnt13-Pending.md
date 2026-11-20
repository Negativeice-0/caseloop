Here is your complete, step-by-step master guide and deep dive to execute every single task from your checklist.

---

## Phase 1: Fixing 403 Errors & Securing Permissions

### 1. Root Cause Analysis

You are getting `403 Forbidden` across `/api/admin/*`, `/api/reports/preview`, and `/api/intakes/` because FastAPI or your middleware layer recognizes your session cookie (`caseloop_session`), but **the underlying account associated with that session lacks administrative privileges**, or **global router-level dependencies** are blocking non-admin user roles.

### 2. How to Implement the Fix

* **Step A: Inspect your Router Declarations (`main.py` or router files)**. Look for where `reports` and `intakes` routers are included. If they have a global dependency like `dependencies=[Depends(get_admin_user)]`, regular users will always be hit with a 403.
* **Step B: Separate Admin vs. Regular Endpoints**. Move your admin-restricted routes into a dedicated prefix (`/api/admin/intakes`, `/api/admin/reports`) or write explicit role-checking dependencies per endpoint rather than locking down entire functional domains.

```python
# Example of a granular role-checking dependency in FastAPI
from fastapi import Depends, HTTPException, status

def verify_admin_role(current_user = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required to access this resource."
        )
    return current_user

# Apply only to routes meant for admins
@router.get("/intakes/")
def get_admin_intakes(admin = Depends(verify_admin_role)):
    ...

```

---

## Phase 2: WhatsApp API Integration & Oracle Cloud Hosting

### 1. Implementing WhatsApp API Calls

To send WhatsApp messages programmatically using the official Cloud API:

1. Set up a Meta Developer Account and obtain a permanent or temporary **Access Token**, a **Phone Number ID**, and your recipient's phone number.
2. Create a utility function inside your backend (e.g., `whatsapp.py`) using `httpx`:

```python
import httpx
from app.core.config import settings

async def send_whatsapp_notification(phone_number: str, message_body: str):
    url = f"https://graph.facebook.com/v17.0/{settings.WHATSAPP_PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {settings.WHATSAPP_ACCESS_TOKEN}",
        "Content-Type": "application/json",
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": phone_number,
        "type": "text",
        "text": {"body": message_body},
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload, headers=headers)
        return response.json()

```

### 2. Hosting on Oracle Cloud Infrastructure (OCI) Free Tier

1. **Provision an Instance**: Spin up an Ubuntu 22.04 or 24.04 ARM-based Ampere instance (`VM.Standard.A1.Flex`).
2. **Configure OCI Security Lists & Firewall**:
* Open ports `80` (HTTP), `443` (HTTPS), and `8000` (or your app port) in your OCI Cloud Console Virtual Cloud Network (VCN) Security List.
* Configure local `ufw` on the server:
```bash
sudo ufw allow OpenSSH
sudo ufw allow 'Nginx Full'
sudo ufw enable

```




3. **Set up Nginx + Uvicorn via Systemd**:
* Clone your repository to `/var/www/caseloop` and create a Python virtual environment.
* Create a systemd service file at `/etc/systemd/system/caseloop.service`:
```ini
[Unit]
Description=Caseloop FastAPI Application
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/var/www/caseloop
ExecStart=/var/www/caseloop/venv/bin/uvicorn main:app --host 127.0.0.1 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target

```


* Enable and start the service: `sudo systemctl daemon-reload && sudo systemctl enable --now caseloop`.
* Set up an Nginx reverse proxy block pointing to `[http://127.0.0.1:8000](http://127.0.0.1:8000)`.



---

## Phase 3: Component & UI Restructuring (`UsersTeams`)

To strip out CRUD capabilities for regular users and keep code clean:

1. **Create a New Component**: Build `UsersTeams.jsx` (or `.tsx`) specifically for standard users to view team structures in a read-only format.
2. **Conditionally Render or Split Views**:
```jsx
// In your main dashboard view router or parent layout
import UsersTeams from './UsersTeams';
import AdminTeamsManager from './AdminTeamsManager';

export default function TeamsPage({ user }) {
  // If the user is an admin, show the full CRUD manager; otherwise show read-only
  return user.is_admin ? <AdminTeamsManager /> : <UsersTeams />;
}

```


3. **Inside `UsersTeams.jsx**`: Remove all forms, mutation hooks (`useMutation`), delete buttons, and edit modals. Render only clean tables or lists mapping out the team metadata.

---

## Phase 4: Breaking Down Admin Dashboard into Independent Windows

To move away from a cramped single-page application tab group where everything shares state:

1. **Define Dedicated Routes in Frontend Router (e.g., React Router)**:
* `/admin/system-status` → Renders system health metrics window.
* `/admin/intakes` → Renders intake queues and monitoring.
* `/admin/reports` → Renders analytics and report previews.


2. **Refactor Navigation Elements**: Turn your sidebar tabs into native links (`<Link to="/admin/intakes">`) or use window management / popup drawers if you want distinct floating desktop-like app panes.
3. **Isolate State**: Fetch data independently inside each component layout using isolated API calls rather than fetching a massive monolithic admin payload upfront.

---

## Final Recommendations

1. **Lock In Your Leverage:** Do not wait for standard hiring portals. Take the client conversations or pipeline data you’ve built, package them into a clean one-page brief, and present them directly to a decision-maker as a turnkey revenue asset.
2. **Execute the Delphi MVP:** While waiting or during downtime, use Delphi's form designer to build your local lead-tracker. It gives you immediate utility and insulates your skillset.
3. **Keep Your Checklist Active:** Use your master checklist to methodically tackle Phase 1 (Auth fixes) and Phase 2 (WhatsApp API) next.
