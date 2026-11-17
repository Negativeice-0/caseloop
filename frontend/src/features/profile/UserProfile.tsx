import React, { useState } from 'react';
import { ChevronDown, KeyRound, UserRound } from 'lucide-react';
import { changePassword, CurrentUser } from '../../services/api';

interface UserProfileProps {
  currentUser: CurrentUser;
  onPasswordChanged: (user: CurrentUser) => void;
}

export function PasswordChangeForm({
  currentUser,
  onPasswordChanged,
  required = false,
}: UserProfileProps & { required?: boolean }) {
  const [currentPassword, setCurrentPassword] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [confirmation, setConfirmation] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState(false);
  const [busy, setBusy] = useState(false);

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    setError(null);
    setSuccess(false);
    if (newPassword !== confirmation) {
      setError('The new passwords do not match.');
      return;
    }
    setBusy(true);
    try {
      const user = await changePassword({
        current_password: currentPassword,
        new_password: newPassword,
      });
      setCurrentPassword('');
      setNewPassword('');
      setConfirmation('');
      setSuccess(true);
      onPasswordChanged(user);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unable to change password.');
    } finally {
      setBusy(false);
    }
  };

  return (
    <section className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
      <div className="mb-4 flex items-center gap-3">
        <KeyRound className="h-5 w-5 text-red-600" />
        <div>
          <h3 className="font-bold">{required ? 'Set your password' : 'Change password'}</h3>
          {required && <p className="text-sm text-slate-500">Set a personal password before continuing.</p>}
        </div>
      </div>
      {error && <p role="alert" className="mb-3 rounded-lg bg-red-50 p-3 text-sm text-red-700">{error}</p>}
      {success && <p className="mb-3 rounded-lg bg-emerald-50 p-3 text-sm text-emerald-700">Password updated.</p>}
      <form onSubmit={handleSubmit} className="grid gap-3 sm:grid-cols-2">
        <label className="text-sm font-semibold sm:col-span-2">
          Current password
          <input
            type="password"
            autoComplete="current-password"
            required
            value={currentPassword}
            onChange={(event) => setCurrentPassword(event.target.value)}
            className="mt-1 w-full rounded-lg border border-slate-300 p-2"
          />
        </label>
        <label className="text-sm font-semibold">
          New password
          <input
            type="password"
            autoComplete="new-password"
            minLength={12}
            required
            value={newPassword}
            onChange={(event) => setNewPassword(event.target.value)}
            className="mt-1 w-full rounded-lg border border-slate-300 p-2"
          />
        </label>
        <label className="text-sm font-semibold">
          Confirm new password
          <input
            type="password"
            autoComplete="new-password"
            minLength={12}
            required
            value={confirmation}
            onChange={(event) => setConfirmation(event.target.value)}
            className="mt-1 w-full rounded-lg border border-slate-300 p-2"
          />
        </label>
        <p className="text-xs text-slate-500 sm:col-span-2">Use at least 12 characters. Avoid reusing an organizational or personal password.</p>
        <button disabled={busy} className="justify-self-start rounded-lg bg-slate-900 px-4 py-2 font-semibold text-white disabled:opacity-50">
          {busy ? 'Saving…' : 'Update password'}
        </button>
      </form>
    </section>
  );
}

export function UserProfile({ currentUser, onPasswordChanged }: UserProfileProps) {
  const [showPasswordForm, setShowPasswordForm] = useState(false);

  return (
    <div className="mx-auto max-w-3xl space-y-6">
      <section className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
        <div className="flex items-center gap-4">
          <div className="flex h-14 w-14 items-center justify-center rounded-2xl bg-red-600 text-white">
            <UserRound className="h-7 w-7" />
          </div>
          <div>
            <h2 className="text-xl font-black">{currentUser.full_name || currentUser.email}</h2>
            <p className="text-sm text-slate-500">{currentUser.email}</p>
          </div>
        </div>
        <dl className="mt-6 grid gap-3 sm:grid-cols-2">
          <div className="rounded-xl bg-slate-50 p-4">
            <dt className="text-xs font-bold uppercase text-slate-500">Role</dt>
            <dd className="mt-1 font-semibold capitalize">{currentUser.role}</dd>
          </div>
          <div className="rounded-xl bg-slate-50 p-4">
            <dt className="text-xs font-bold uppercase text-slate-500">Account</dt>
            <dd className="mt-1 font-semibold">{currentUser.is_active ? 'Active' : 'Inactive'}</dd>
          </div>
        </dl>
      </section>
      <section className="overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-sm">
        <button
          type="button"
          aria-expanded={showPasswordForm}
          aria-controls="profile-password-form"
          onClick={() => setShowPasswordForm((visible) => !visible)}
          className="flex w-full items-center gap-4 p-5 text-left transition hover:bg-slate-50"
        >
          <span className="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl bg-slate-100 text-slate-700">
            <KeyRound className="h-5 w-5" />
          </span>
          <span className="min-w-0 flex-1">
            <span className="block font-bold">Change password</span>
            <span className="mt-1 block text-sm text-slate-500">Update your sign-in password and keep your account secure.</span>
          </span>
          <ChevronDown className={`h-5 w-5 shrink-0 text-slate-500 transition-transform ${showPasswordForm ? 'rotate-180' : ''}`} />
        </button>
        {showPasswordForm && (
          <div id="profile-password-form" className="border-t border-slate-200 p-5">
            <PasswordChangeForm currentUser={currentUser} onPasswordChanged={onPasswordChanged} />
          </div>
        )}
      </section>
    </div>
  );
}
