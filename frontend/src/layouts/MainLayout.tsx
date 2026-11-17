/* ----------------------------------------------------
   Copyright (c) 2026 Billy Gates Ochieng Osodo. All Rights Reserved.
   CaseLoop Humanitarian Coordination System - Main Layout
   ---------------------------------------------------- */

import React from 'react';
import { 
  HeartPulse,
  Activity, 
  Users, 
  Clock, 
  Settings, 
  Home, 
  FolderKanban,
  User,
  MessageSquareText,
  FileText,
  MoreHorizontal,
  LogOut,
} from 'lucide-react';
import { CurrentUser } from '../services/api';

export type TabType = 'responses' | 'assignments' | 'timeline' | 'intake' | 'reports' | 'admin' | 'profile';

interface MainLayoutProps {
  children: React.ReactNode;
  activeTab: TabType;
  setActiveTab: (tab: TabType) => void;
  backendStatus: 'online' | 'offline';
  databaseMode: 'sqlite' | 'postgresql' | 'unknown';
  currentUser: CurrentUser;
  onLogout: () => void;
}

export const MainLayout: React.FC<MainLayoutProps> = ({
  children,
  activeTab,
  setActiveTab,
  backendStatus,
  databaseMode,
  currentUser,
  onLogout,
}) => {
  const [moreOpen, setMoreOpen] = React.useState(false);
  const homeTab: TabType = currentUser.role === 'admin' ? 'admin' : 'responses';
  const selectTab = (tab: TabType) => {
    setActiveTab(tab);
    setMoreOpen(false);
  };

  return (
    <div className="min-h-screen bg-slate-100 text-slate-900 flex flex-col md:flex-row font-sans selection:bg-red-600 selection:text-white">
      
      {/* MOBILE TOP HEADER */}
      <header className="md:hidden bg-white border-b border-slate-200 px-4 py-3 flex items-center justify-between sticky top-0 z-40 shadow-sm flex-shrink-0">
        <button type="button" aria-label="CaseLoop home" onClick={() => selectTab(homeTab)} className="flex items-center gap-2.5 text-left">
          <div className="bg-red-600 p-2 rounded-xl text-white shadow-md shadow-red-600/30">
            <HeartPulse className="h-5 w-5" />
          </div>
          <div>
            <h1 className="font-black text-base tracking-tight text-slate-900">
              Case<span className="text-red-600">Loop</span>
            </h1>
            <p className="text-[10px] text-slate-500 font-medium">Karen-Lang'ata Operations</p>
          </div>
        </button>
        
        <div className="flex items-center gap-1.5 text-[11px] font-semibold bg-slate-50 border border-slate-200 px-2.5 py-1 rounded-full">
          <span className={`w-2 h-2 rounded-full ${backendStatus === 'online' ? 'bg-emerald-500 animate-ping' : 'bg-amber-500'}`}></span>
          <span className="text-slate-700 capitalize">{backendStatus}</span>
        </div>
      </header>

      {/* DESKTOP SIDEBAR */}
      <aside className="hidden md:flex flex-col justify-between w-72 bg-white border-r border-slate-200 p-6 sticky top-0 h-screen shadow-sm flex-shrink-0 z-30">
        <div>
          <button type="button" aria-label="CaseLoop home" onClick={() => selectTab(homeTab)} className="mb-8 flex items-center gap-3 text-left">
            <div className="bg-red-600 p-3 rounded-2xl text-white shadow-lg shadow-red-600/30">
              <HeartPulse className="h-6 w-6" />
            </div>
            <div>
              <h1 className="font-black text-xl tracking-tight text-slate-900">
                Case<span className="text-red-600">Loop</span>
              </h1>
              <p className="text-xs font-medium text-slate-500">Karen-Lang'ata Operations</p>
            </div>
          </button>

          <nav className="space-y-2">
            <button
              onClick={() => setActiveTab('responses')}
              className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-semibold transition-all ${
                activeTab === 'responses' ? 'bg-red-600 text-white shadow-md shadow-red-600/25' : 'text-slate-600 hover:bg-slate-100'
              }`}
            >
              <Activity className="w-4 h-4" /> Response Register
            </button>
            
            <button
              onClick={() => setActiveTab('assignments')}
              className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-semibold transition-all ${
                activeTab === 'assignments' ? 'bg-red-600 text-white shadow-md shadow-red-600/25' : 'text-slate-600 hover:bg-slate-100'
              }`}
            >
              <Users className="w-4 h-4" /> Assignments & Teams
            </button>

            <button
              onClick={() => setActiveTab('timeline')}
              className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-semibold transition-all ${
                activeTab === 'timeline' ? 'bg-red-600 text-white shadow-md shadow-red-600/25' : 'text-slate-600 hover:bg-slate-100'
              }`}
            >
              <Clock className="w-4 h-4" /> Operational Timeline
            </button>

            {currentUser.role !== 'responder' && (
              <>
                <button
                  onClick={() => setActiveTab('intake')}
                  className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-semibold transition-all ${
                    activeTab === 'intake' ? 'bg-red-600 text-white shadow-md shadow-red-600/25' : 'text-slate-600 hover:bg-slate-100'
                  }`}
                >
                  <MessageSquareText className="w-4 h-4" /> Intake Review
                </button>

                <button
                  onClick={() => setActiveTab('reports')}
                  className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-semibold transition-all ${
                    activeTab === 'reports' ? 'bg-red-600 text-white shadow-md shadow-red-600/25' : 'text-slate-600 hover:bg-slate-100'
                  }`}
                >
                  <FileText className="w-4 h-4" /> Reports & Analysis
                </button>
              </>
            )}

            {/* Added Officer Profile Navigation Button */}
            <button
              onClick={() => setActiveTab('profile')}
              className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-semibold transition-all ${
                activeTab === 'profile' ? 'bg-red-600 text-white shadow-md shadow-red-600/25' : 'text-slate-600 hover:bg-slate-100'
              }`}
            >
              <User className="w-4 h-4" /> Officer Profile
            </button>

            {currentUser.role === 'admin' && (
              <button
                onClick={() => setActiveTab('admin')}
                className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-semibold transition-all ${
                  activeTab === 'admin' ? 'bg-slate-900 text-white shadow-md shadow-slate-900/25' : 'text-slate-600 hover:bg-slate-100'
                }`}
              >
                <Settings className="w-4 h-4" /> Admin & System Control
              </button>
            )}
          </nav>
        </div>

        <div className="bg-slate-50 border border-slate-200 p-4 rounded-2xl space-y-2.5 shadow-inner">
          <div className="flex items-center justify-between text-xs font-semibold">
            <span className="text-slate-500">System Mode</span>
            <span className="text-emerald-600 bg-emerald-50 px-2 py-0.5 rounded-full border border-emerald-200">
              {databaseMode === 'sqlite' ? 'SQLite · offline' : databaseMode === 'postgresql' ? 'PostgreSQL · shared' : 'Unknown'}
            </span>
          </div>
          <div className="flex items-center justify-between text-xs text-slate-600 pt-2 border-t border-slate-200 font-medium">
            <span>FastAPI Backend:</span>
            <span className={backendStatus === 'online' ? 'text-emerald-600 font-bold uppercase' : 'text-amber-600 font-bold uppercase'}>
              {backendStatus}
            </span>
          </div>
          <div className="border-t border-slate-200 pt-3">
            <p className="truncate text-xs font-bold">{currentUser.full_name || currentUser.email}</p>
            <p className="text-[11px] capitalize text-slate-500">{currentUser.role}</p>
            <button onClick={onLogout} className="mt-2 text-xs font-bold text-red-700 hover:underline">Sign out</button>
          </div>
        </div>
      </aside>

      {/* MAIN VIEWPORT */}
      <main className="flex-1 p-5 md:p-10 overflow-y-auto bg-slate-50 pb-36 md:pb-10">
        <div className="max-w-6xl mx-auto w-full">
          {children}
        </div>
      </main>

      {/* MOBILE BOTTOM NAVIGATION */}
      <nav 
        aria-label="Mobile Navigation" 
        style={{ position: 'fixed', bottom: 0, left: 0, right: 0, zIndex: 9999 }}
        className="relative flex md:hidden w-full items-center justify-around border-t border-slate-800 bg-slate-900 px-2 py-2 shadow-[0_-4px_20px_rgba(0,0,0,0.3)]"
      >
        <button
          onClick={() => selectTab('responses')}
          className={`flex flex-col items-center justify-center py-2 rounded-xl transition-all ${
            activeTab === 'responses' ? 'bg-red-600/30 text-red-400 font-bold' : 'text-slate-400 hover:text-slate-200'
          }`}
        >
          <Home className="w-5 h-5 mb-1" />
          <span className="text-[10px] tracking-wide">Register</span>
        </button>

        <button
          onClick={() => selectTab('assignments')}
          className={`flex flex-col items-center justify-center py-2 rounded-xl transition-all ${
            activeTab === 'assignments' ? 'bg-red-600/30 text-red-400 font-bold' : 'text-slate-400 hover:text-slate-200'
          }`}
        >
          <FolderKanban className="w-5 h-5 mb-1" />
          <span className="text-[10px] tracking-wide">Teams</span>
        </button>

        <button
          onClick={() => selectTab('timeline')}
          className={`flex flex-col items-center justify-center py-2 rounded-xl transition-all ${
            activeTab === 'timeline' ? 'bg-red-600/30 text-red-400 font-bold' : 'text-slate-400 hover:text-slate-200'
          }`}
        >
          <Clock className="w-5 h-5 mb-1" />
          <span className="text-[10px] tracking-wide">Timeline</span>
        </button>

        <button
          aria-expanded={moreOpen}
          aria-controls="mobile-more-menu"
          onClick={() => setMoreOpen((open) => !open)}
          className={`flex flex-col items-center justify-center rounded-xl py-2 transition-all ${
            moreOpen || ['intake', 'reports', 'profile', 'admin'].includes(activeTab)
              ? 'bg-red-600/30 font-bold text-red-400'
              : 'text-slate-400 hover:text-slate-200'
          }`}
        >
          <MoreHorizontal className="mb-1 h-5 w-5" />
          <span className="text-[10px] tracking-wide">More</span>
        </button>

        {moreOpen && (
          <div id="mobile-more-menu" className="absolute bottom-full right-2 mb-2 w-72 rounded-2xl border border-slate-200 bg-white p-2 text-slate-900 shadow-xl">
            {currentUser.role !== 'responder' ? (
              <>
                <button onClick={() => selectTab('intake')} className="flex w-full items-center gap-3 rounded-xl px-3 py-3 text-left text-sm font-semibold hover:bg-slate-100">
                  <MessageSquareText className="h-4 w-4" /> Intake review
                </button>
                <button onClick={() => selectTab('reports')} className="flex w-full items-center gap-3 rounded-xl px-3 py-3 text-left text-sm font-semibold hover:bg-slate-100">
                  <FileText className="h-4 w-4" /> Reports &amp; Analysis
                </button>
              </>
            ) : (
              <p className="px-3 py-3 text-xs leading-relaxed text-slate-500">
                Reports and Admin require a coordinator or administrator account. Sign out to switch accounts.
              </p>
            )}
            <button onClick={() => selectTab('profile')} className="flex w-full items-center gap-3 rounded-xl px-3 py-3 text-left text-sm font-semibold hover:bg-slate-100">
              <User className="h-4 w-4" /> Officer Profile
            </button>
            {currentUser.role === 'admin' && (
              <button onClick={() => selectTab('admin')} className="flex w-full items-center gap-3 rounded-xl px-3 py-3 text-left text-sm font-semibold hover:bg-slate-100">
                <Settings className="h-4 w-4" /> Admin &amp; System Control
              </button>
            )}
            <div className="my-1 border-t border-slate-200" />
            <button onClick={onLogout} className="flex w-full items-center gap-3 rounded-xl px-3 py-3 text-left text-sm font-semibold text-red-700 hover:bg-red-50">
              <LogOut className="h-4 w-4" /> Sign out / switch account
            </button>
          </div>
        )}
      </nav>

    </div>
  );
};