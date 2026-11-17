import React, { useState } from 'react';
import { ArrowRight, HeartPulse, LogIn } from 'lucide-react';
import { CurrentUser, loginUser, registerUser } from '../../services/api';

interface AuthGatewayProps {
  onLoginSuccess: (user: CurrentUser) => void;
  adminEntry?: boolean;
}

export const AuthGateway: React.FC<AuthGatewayProps> = ({ onLoginSuccess, adminEntry = false }) => {
  const [screen, setScreen] = useState<'landing' | 'login' | 'admin-login' | 'register'>(
    adminEntry ? 'admin-login' : 'landing',
  );
  const [fullName, setFullName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleLogin = async (event: React.FormEvent) => {
    event.preventDefault();
    setLoading(true);
    setError(null);
    try {
      const user = await loginUser({
        email,
        password,
        ...(screen === 'admin-login' ? { audience: 'admin' as const } : {}),
      });
      onLoginSuccess(user);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Sign-in failed.');
    } finally {
      setLoading(false);
    }
  };

  const handleRegister = async (event: React.FormEvent) => {
    event.preventDefault();
    setLoading(true);
    setError(null);
    try {
      const user = await registerUser({ full_name: fullName, email, password });
      onLoginSuccess(user);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Registration failed.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900 flex flex-col justify-between p-6 font-sans">
      <nav className="w-full flex items-center justify-between py-4">
        <button type="button" aria-label="CaseLoop authentication home" onClick={() => window.location.assign('/')} className="flex items-center gap-3 text-left">
          <div className="bg-red-600 p-2.5 rounded-2xl text-white shadow-lg shadow-red-600/30">
            <HeartPulse className="h-6 w-6" />
          </div>
          <div>
            <h1 className="font-black text-xl tracking-tight">Case<span className="text-red-600">Loop</span></h1>
            <p className="text-[10px] text-slate-500 font-medium">Karen-Lang'ata Operations</p>
          </div>
        </button>
        {screen === 'landing' && (
          <button
            onClick={() => setScreen('login')}
            className="inline-flex items-center gap-2 bg-white border border-slate-200 hover:bg-slate-100 text-slate-700 font-bold px-4 py-2.5 rounded-xl shadow-sm text-xs"
          >
            <LogIn className="w-4 h-4" /> Sign In
          </button>
        )}
      </nav>

      <main className="max-w-6xl mx-auto w-full flex items-center justify-center my-auto py-12">
        {screen === 'landing' ? (
          <div className="text-center space-y-6 max-w-2xl">
            <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-white border border-slate-200 text-red-600 text-xs font-semibold">
              Coordinator workspace
            </div>
            <h2 className="text-4xl md:text-5xl font-black tracking-tight leading-tight">
              Field information, <span className="text-red-600">clear assignments.</span>
            </h2>
            <p className="text-slate-600 text-sm md:text-base leading-relaxed max-w-xl mx-auto">
              Review incoming information, publish approved response records, coordinate teams, and prepare traceable operational reports.
            </p>
            <button
              onClick={() => setScreen('register')}
              className="inline-flex items-center gap-2 bg-red-600 hover:bg-red-700 text-white font-black px-8 py-3.5 rounded-xl shadow-xl text-sm"
            >
              Launch Dispatch Portal <ArrowRight className="w-4 h-4" />
            </button>
            <p>
              <button
                onClick={() => window.location.assign('/admin')}
                className="text-sm font-bold text-slate-600 underline decoration-slate-300 underline-offset-4 hover:text-red-700"
              >
                Administrator sign-in
              </button>
            </p>
          </div>
        ) : screen === 'login' || screen === 'admin-login' ? (
          <div className="bg-white border border-slate-200 max-w-md w-full p-8 rounded-3xl shadow-2xl">
            <div className="text-center mb-6">
              <div className="inline-flex p-3 bg-red-50 text-red-600 rounded-2xl border border-red-100 mb-3">
                <LogIn className="w-6 h-6" />
              </div>
              <h3 className="text-xl font-black">
                {screen === 'admin-login' ? 'Administrator sign-in' : 'Sign in to CaseLoop'}
              </h3>
              <p className="text-xs text-slate-500 mt-1">
                {screen === 'admin-login'
                  ? 'Use an administrator account. Coordinator and responder accounts cannot enter Admin.'
                  : 'Use your email address and password.'}
              </p>
            </div>
            {error && <p role="alert" className="mb-4 p-3 bg-red-50 border border-red-200 rounded-xl text-sm text-red-700">{error}</p>}
            <form onSubmit={handleLogin} className="space-y-4">
              <label className="block text-xs font-bold text-slate-700">
                Email
                <input
                  type="email"
                  autoComplete="username"
                  required
                  value={email}
                  onChange={(event) => setEmail(event.target.value)}
                  className="mt-1 w-full px-4 py-3 rounded-xl bg-slate-50 border border-slate-300 text-sm focus:outline-none focus:ring-2 focus:ring-red-600"
                />
              </label>
              <label className="block text-xs font-bold text-slate-700">
                Password
                <input
                  type="password"
                  autoComplete="current-password"
                  required
                  value={password}
                  onChange={(event) => setPassword(event.target.value)}
                  className="mt-1 w-full px-4 py-3 rounded-xl bg-slate-50 border border-slate-300 text-sm focus:outline-none focus:ring-2 focus:ring-red-600"
                />
              </label>
              <button
                type="submit"
                disabled={loading}
                className="w-full py-3.5 bg-red-600 hover:bg-red-700 text-white font-bold rounded-xl disabled:opacity-50"
              >
                {loading ? 'Signing in…' : 'Sign In'}
              </button>
              <p className="text-xs text-slate-500 text-center">
                {screen === 'login' && (
                  <>
                    Need an account?{' '}
                    <button type="button" onClick={() => { setError(null); setScreen('register'); }} className="font-semibold text-red-700 hover:text-red-800">
                      Register
                    </button>
                  </>
                )}
              </p>
              {screen === 'login' ? (
                <button
                  type="button"
                  onClick={() => window.location.assign('/admin')}
                  className="w-full text-xs font-semibold text-slate-600 hover:text-red-700"
                >
                  Administrator? Use the Admin sign-in page
                </button>
              ) : (
                <p className="text-center text-xs text-slate-500">
                  Admin accounts are provisioned by an administrator or the local setup command.
                </p>
              )}
              <button
                type="button"
                onClick={() => {
                  setError(null);
                  if (screen === 'admin-login') window.location.assign('/');
                  else setScreen('landing');
                }}
                className="w-full text-xs font-semibold text-slate-500 hover:text-slate-900"
              >
                {screen === 'admin-login' ? 'Back to dispatch portal' : 'Back'}
              </button>
            </form>
          </div>
        ) : (
          <div className="bg-white border border-slate-200 max-w-md w-full p-8 rounded-3xl shadow-2xl">
            <div className="text-center mb-6">
              <div className="inline-flex p-3 bg-red-50 text-red-600 rounded-2xl border border-red-100 mb-3">
                <HeartPulse className="h-6 w-6" />
              </div>
              <h3 className="text-xl font-black">Register for CaseLoop</h3>
              <p className="text-xs text-slate-500 mt-1">Create an account to join the response team.</p>
            </div>
            {error && <p role="alert" className="mb-4 p-3 bg-red-50 border border-red-200 rounded-xl text-sm text-red-700">{error}</p>}
            <form onSubmit={handleRegister} className="space-y-4">
              <label className="block text-xs font-bold text-slate-700">
                Full name
                <input
                  type="text"
                  autoComplete="name"
                  maxLength={200}
                  required
                  value={fullName}
                  onChange={(event) => setFullName(event.target.value)}
                  className="mt-1 w-full px-4 py-3 rounded-xl bg-slate-50 border border-slate-300 text-sm focus:outline-none focus:ring-2 focus:ring-red-600"
                />
              </label>
              <label className="block text-xs font-bold text-slate-700">
                Email
                <input
                  type="email"
                  autoComplete="email"
                  maxLength={254}
                  required
                  value={email}
                  onChange={(event) => setEmail(event.target.value)}
                  className="mt-1 w-full px-4 py-3 rounded-xl bg-slate-50 border border-slate-300 text-sm focus:outline-none focus:ring-2 focus:ring-red-600"
                />
              </label>
              <label className="block text-xs font-bold text-slate-700">
                Password
                <input
                  type="password"
                  autoComplete="new-password"
                  minLength={12}
                  maxLength={128}
                  required
                  value={password}
                  onChange={(event) => setPassword(event.target.value)}
                  className="mt-1 w-full px-4 py-3 rounded-xl bg-slate-50 border border-slate-300 text-sm focus:outline-none focus:ring-2 focus:ring-red-600"
                />
              </label>
              <p className="text-xs text-slate-500">
                New accounts start with responder access. An administrator manages access to coordinator and admin features.
              </p>
              <button
                type="submit"
                disabled={loading}
                className="w-full py-3.5 bg-red-600 hover:bg-red-700 text-white font-bold rounded-xl disabled:opacity-50"
              >
                {loading ? 'Creating account…' : 'Create Account'}
              </button>
              <p className="text-xs text-slate-500 text-center">
                Already registered?{' '}
                <button type="button" onClick={() => { setError(null); setScreen('login'); }} className="font-semibold text-red-700 hover:text-red-800">
                  Sign In
                </button>
              </p>
              <button type="button" onClick={() => { setError(null); setScreen('landing'); }} className="w-full text-xs font-semibold text-slate-500 hover:text-slate-900">
                Back
              </button>
            </form>
          </div>
        )}
      </main>
      <footer className="max-w-6xl mx-auto w-full text-center py-4 border-t border-slate-200 text-[11px] text-slate-400">
        Human-reviewed coordination • Synthetic data only until approved for operations
      </footer>
    </div>
  );
};
