# Evidence Excerpts

## entry-point-evidence.txt

frontend\src\App.tsx:18: const isAdminEntry = window.location.pathname === '/admin';
frontend\src\App.tsx:21: const [activeTab, setActiveTab] = useState<TabType>(isAdminEntry ? 'admin' : 'responses');
frontend\src\App.tsx:62: setActiveTab('responses');
frontend\src\App.tsx:74: setActiveTab('respo

## frontend-test-capability.txt

Frontend test scripts:
None declared in frontend/package.json.

Frontend source test files:
No .test. or .spec. files found under frontend/src.


## ui-role-test-results.txt

Runtime UI checks using isolated test database and synthetic accounts (no credentials recorded):

Responder desktop: Register, Assignments & Teams, Operational Timeline, Officer Profile. Intake Review, Reports & Analysis, and Admin & System Control absent.
Responder mobile More menu: no Intake Re

## visibility-source-evidence.txt

Role visibility and entry-point source matches:
[app] frontend\src\App.tsx:18: const isAdminEntry = window.location.pathname === '/admin';
[app] frontend\src\App.tsx:21: const [activeTab, setActiveTab] = useState<TabType>(isAdminEntry ? 'admin' : 'responses');
[app] frontend\src\App.tsx:25: const
