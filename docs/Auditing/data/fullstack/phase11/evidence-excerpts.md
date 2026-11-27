# Evidence Excerpts

## api-router-registration.txt

backend\app\main.py:21: app.include_router(admin.router)
backend\app\main.py:22: app.include_router(auth.router)
backend\app\main.py:23: app.include_router(responses.router)
backend\app\main.py:24: app.include_router(assignments.router)
backend\app\main.py:25: app.include_router(intakes.router)


## entry-path-source.txt

frontend\src\App.tsx:18: const isAdminEntry = window.location.pathname === '/admin';
frontend\src\App.tsx:21: const [activeTab, setActiveTab] = useState<TabType>(isAdminEntry ? 'admin' : 'responses');
frontend\src\App.tsx:81: return <AuthGateway onLoginSuccess={setCurrentUser} adminEntry={isAdminE

## runtime-entry-tests.txt

Runtime UI checks using isolated test database and synthetic accounts (no credentials recorded):

Responder desktop: Register, Assignments & Teams, Operational Timeline, Officer Profile. Intake Review, Reports & Analysis, and Admin & System Control absent.
Responder mobile More menu: no Intake Re

## tab-disposition-source.txt

frontend\src\layouts\MainLayout.tsx:23: export type TabType = 'responses' | 'assignments' | 'timeline' | 'intake' | 'reports' | 'admin' | 'profile';
frontend\src\layouts\MainLayout.tsx:56: <button type="button" aria-label="CaseLoop home" onClick={() => selectTab(homeTab)} className="flex items-cent
