# Evidence Excerpts

## auth-path-references.txt

frontend\src\App.tsx:18: const isAdminEntry = window.location.pathname === '/admin';
frontend\src\features\auth\AuthGateway.tsx:55: <button type="button" aria-label="CaseLoop authentication home" onClick={() => window.location.assign('/')} className="flex items-center gap-3 text-left">
frontend\sr

## router-package-reference.txt

frontend\package.json:15: "react-router-dom": "^7.18.5"


## router-source-references.txt

No react-router-dom references found in first-party frontend source files.


## tab-reference-matrix.txt

Frontend tab-token references (first-party source only):
TAB: responses | source match count: 14
  frontend\src\App.tsx:21: const [activeTab, setActiveTab] = useState<TabType>(isAdminEntry ? 'admin' : 'responses');
  frontend\src\App.tsx:62: setActiveTab('responses');
  frontend\src\App.tsx:74:
