```markdown
## Common Setup & Environment Troubleshooting

### 1. Node.js & npm Connection Resets (`ECONNRESET` / `-4077`)
* **Symptom:** `npm install` hangs indefinitely or fails immediately with `npm error code ECONNRESET` or `errno -4077`.
* **Root Cause:** Strict ISP routing, firewall restrictions, or local network bottlenecks dropping socket connections to the primary npm registry.
* **Resolution:** 
  Configure npm to use a stable, regionally optimized mirror and increase the socket timeout threshold:
  ```powershell
  npm config set registry [https://registry.npmmirror.com](https://registry.npmmirror.com)
  npm config set fetch-retry-maxtimeout 120000
  npm config set fetch-retries 5

```

### 2. Python 3.11 & Virtual Environment Configuration

* **Symptom:** Package installation stalls or dependency compilation fails when setting up the FastAPI backend on Python 3.11.
* **Root Cause:** Outdated `pip` index caches or SSL certificate verification blocks on corporate/restricted networks.
* **Resolution:**
Upgrade pip and use a clean virtual environment initialization:
```powershell
python -m venv venv
source venv/bin/activate  # Or venv\Scripts\activate on Windows
python -m pip install --upgrade pip
pip install -r requirements.txt

```