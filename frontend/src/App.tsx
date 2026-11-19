import React, { useEffect, useState } from 'react';
import { AlertCircle, RefreshCw } from 'lucide-react';
import { AdminControl } from './features/admin/AdminControl';
import { AuthGateway } from './features/auth/AuthGateway';
import { AssignmentsManager } from './features/assignments/AssignmentsManager';
import { PasswordChangeForm, UserProfile } from './features/profile/UserProfile';
import ResponseRegister from './features/responses/ResponseRegister';
import { IntakeReview, ReportsView, TimelineView } from './features/workflow/WorkflowViews';
import { MainLayout, TabType } from './layouts/MainLayout';
import {
  checkBackendHealth,
  CurrentUser,
  getCurrentUser,
  logoutUser,
} from './services/api';

export default function App() {
  const isAdminEntry = window.location.pathname === '/admin';
  const [currentUser, setCurrentUser] = useState<CurrentUser | null>(null);
  const [sessionChecked, setSessionChecked] = useState(false);
  const [activeTab, setActiveTab] = useState<TabType>(isAdminEntry ? 'admin' : 'responses');
  const [backendStatus, setBackendStatus] = useState<'online' | 'offline'>('offline');
  const [databaseMode, setDatabaseMode] = useState<'sqlite' | 'postgresql' | 'unknown'>('unknown');
  const [error, setError] = useState<string | null>(null);
  const canCoordinate = currentUser?.role !== 'responder';

  useEffect(() => {
    getCurrentUser()
      .then(setCurrentUser)
      .catch(() => setCurrentUser(null))
      .finally(() => setSessionChecked(true));
  }, []);

const checkStatus = async () => {
    try {
      const health = await checkBackendHealth();
      
      if (health.status === 'online') {
        setBackendStatus('online');
        
        // Handle database mode safely whether admin data or regular fallback is returned
        if (health.database) {
          setDatabaseMode(health.database.toLowerCase().includes('postgres') ? 'postgresql' : 'sqlite');
        }
        
        setError(null);
      }
    } catch (err) {
      // Only triggered if the backend is truly unreachable / offline
      setBackendStatus('offline');
      setDatabaseMode('unknown');
      setError('Backend is unreachable. Start the API and refresh.');
    }
  };

  useEffect(() => {
    if (currentUser) void checkStatus();
  }, [currentUser]);

  useEffect(() => {
    if (!canCoordinate && ['intake', 'reports', 'admin'].includes(activeTab)) {
      setActiveTab('responses');
    }
  }, [activeTab, canCoordinate]);

  const handleLogout = async () => {
    try {
      await logoutUser();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Sign out failed.');
      return;
    }
    setCurrentUser(null);
    setActiveTab('responses');
  };

  if (!sessionChecked) {
    return <div className="flex min-h-screen items-center justify-center text-sm text-slate-500">Checking secure session…</div>;
  }
  if (!currentUser) {
    return <AuthGateway onLoginSuccess={setCurrentUser} adminEntry={isAdminEntry} />;
  }
  if (isAdminEntry && currentUser.role !== 'admin') {
    return (
      <div className="flex min-h-screen items-center justify-center bg-slate-50 p-4">
        <section className="w-full max-w-lg rounded-2xl border border-slate-200 bg-white p-6 text-center shadow-sm">
          <h1 className="text-xl font-black">Administrator access required</h1>
          <p className="mt-2 text-sm text-slate-600">
            This account has {currentUser.role} access. Sign out, then use an administrator account to continue.
          </p>
          {error && <p role="alert" className="mt-3 text-sm text-red-700">{error}</p>}
          <button onClick={handleLogout} className="mt-5 rounded-lg bg-slate-900 px-4 py-2 font-semibold text-white">
            Sign out and switch account
          </button>
        </section>
      </div>
    );
  }
  if (currentUser.must_change_password) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-slate-50 p-4">
        <div className="w-full max-w-xl">
          <div className="mb-4 rounded-xl border border-amber-300 bg-amber-50 p-4 text-sm text-amber-900">
            Your administrator created a temporary sign-in. Change it before using the workspace.
          </div>
          <PasswordChangeForm
            currentUser={currentUser}
            required
            onPasswordChanged={setCurrentUser}
          />
        </div>
      </div>
    );
  }

  return (
    <MainLayout
      activeTab={activeTab}
      setActiveTab={setActiveTab}
      backendStatus={backendStatus}
      databaseMode={databaseMode}
      currentUser={currentUser}
      onLogout={handleLogout}
    >
      <header className="mb-8 flex flex-col justify-between gap-4 border-b border-slate-200 pb-6 md:flex-row md:items-center">
        <div>
          <h2 className="text-2xl font-black capitalize tracking-tight text-slate-900">
            {activeTab === 'responses' && 'Operational Response Register'}
            {activeTab === 'assignments' && 'Team Assignment Management'}
            {activeTab === 'timeline' && 'Chronological Operational Timeline'}
            {activeTab === 'intake' && 'Incoming Information Review'}
            {activeTab === 'reports' && 'Operational Analysis & Reports'}
            {activeTab === 'admin' && 'Administration & Team Readiness'}
            {activeTab === 'profile' && 'Account & Security'}
          </h2>
        </div>
        <button
          onClick={checkStatus}
          className="self-start rounded-xl border border-slate-200 bg-white p-2.5 text-slate-700 shadow-sm hover:bg-slate-100 md:self-auto"
          title="Refresh system status"
        >
          <RefreshCw className="h-4 w-4" />
        </button>
      </header>

      {error && (
        <div role="alert" className="mb-6 flex items-center gap-3 rounded-2xl border border-amber-200 bg-amber-50 p-4 text-sm text-amber-800">
          <AlertCircle className="h-5 w-5 shrink-0 text-amber-600" />
          <span>{error}</span>
        </div>
      )}

      {activeTab === 'responses' && <ResponseRegister userRole={currentUser.role} />}
      {activeTab === 'assignments' && <AssignmentsManager userRole={currentUser.role} />}
      {activeTab === 'intake' && canCoordinate && <IntakeReview />}
      {activeTab === 'timeline' && <TimelineView />}
      {activeTab === 'reports' && canCoordinate && <ReportsView />}
      {activeTab === 'profile' && (
        <UserProfile currentUser={currentUser} onPasswordChanged={setCurrentUser} />
      )}
      {activeTab === 'admin' && currentUser.role === 'admin' && (
        <AdminControl currentUser={currentUser} />
      )}
    </MainLayout>
  );
}
