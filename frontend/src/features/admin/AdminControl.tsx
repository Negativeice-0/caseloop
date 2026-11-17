import React, { useEffect, useState } from 'react';
import { AlertCircle, CheckCircle2, Clipboard, UsersRound } from 'lucide-react';
import ResponseRegister from '../responses/ResponseRegister';
import { AssignmentsManager } from '../assignments/AssignmentsManager';
import { IntakeReview, ReportsView, TimelineView } from '../workflow/WorkflowViews';
import {
  addTeamMember,
  createAdminUser,
  createTeam,
  CurrentUser,
  deleteTeam,
  fetchSystemStatus,
  getAdminAudit,
  getAdminUsers,
  getIntakes,
  getReportSummary,
  getTeamMembers,
  getTeams,
  removeTeamMember,
  ReportSummary,
  resetUserPassword,
  setUserActive,
  Team,
  TeamMember,
  updateAdminUser,
  updateTeam,
  updateTeamMemberRole,
} from '../../services/api';

type AdminSection = 'overview' | 'responses' | 'assignments' | 'intake' | 'timeline' | 'reports' | 'people';

interface AdminControlProps {
  currentUser: CurrentUser;
}

export const AdminControl: React.FC<AdminControlProps> = ({ currentUser }) => {
  const [section, setSection] = useState<AdminSection>('overview');
  const [users, setUsers] = useState<CurrentUser[]>([]);
  const [teams, setTeams] = useState<Team[]>([]);
  const [members, setMembers] = useState<TeamMember[]>([]);
  const [summary, setSummary] = useState<ReportSummary | null>(null);
  const [pendingCount, setPendingCount] = useState(0);
  const [whatsappReady, setWhatsappReady] = useState(false);
  const [database, setDatabase] = useState('—');
  const [audit, setAudit] = useState<Awaited<ReturnType<typeof getAdminAudit>>>([]);
  const [error, setError] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);
  const [newUser, setNewUser] = useState<{ email: string; full_name: string; role: CurrentUser['role'] }>({
    email: '',
    full_name: '',
    role: 'responder',
  });
  const [initialPassword, setInitialPassword] = useState('');
  const [passwordRecipient, setPasswordRecipient] = useState('');
  const [newTeam, setNewTeam] = useState({ name: '', description: '' });
  const [membership, setMembership] = useState({
    team_id: 0,
    user_id: 0,
    member_role: 'member' as 'leader' | 'member',
  });

  const refresh = async () => {
    setError(null);
    try {
      const [userRows, teamRows, memberRows, metrics, intakes, status, auditRows] =
        await Promise.all([
          getAdminUsers(),
          getTeams(),
          getTeamMembers(),
          getReportSummary(),
          getIntakes(),
          fetchSystemStatus(),
          getAdminAudit(),
        ]);
      setUsers(userRows);
      setTeams(teamRows);
      setMembers(memberRows);
      setSummary(metrics);
      setPendingCount(intakes.length);
      setWhatsappReady(status.whatsapp_webhook_configured);
      setDatabase(status.database);
      setAudit(auditRows);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unable to load administration data.');
    }
  };

  useEffect(() => {
    void refresh();
  }, []);

  const runAction = async (action: () => Promise<void>) => {
    setBusy(true);
    setError(null);
    try {
      await action();
      await refresh();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'The requested change failed.');
    } finally {
      setBusy(false);
    }
  };

  const submitUser = async (event: React.FormEvent) => {
    event.preventDefault();
    await runAction(async () => {
      const result = await createAdminUser(newUser);
      setInitialPassword(result.initial_password);
      setPasswordRecipient(newUser.email.trim().toLowerCase());
      setNewUser({ email: '', full_name: '', role: 'responder' });
    });
  };

  const submitTeam = async (event: React.FormEvent) => {
    event.preventDefault();
    await runAction(async () => {
      await createTeam(newTeam);
      setNewTeam({ name: '', description: '' });
    });
  };

  const submitMembership = async (event: React.FormEvent) => {
    event.preventDefault();
    await runAction(async () => {
      await addTeamMember(membership.team_id, membership.user_id, membership.member_role);
      setMembership({ team_id: 0, user_id: 0, member_role: 'member' });
    });
  };

  const copyInitialPassword = async () => {
    try {
      await navigator.clipboard.writeText(initialPassword);
      setInitialPassword('');
    } catch {
      setError('Clipboard access is unavailable. Select and copy the temporary password before leaving this page.');
    }
  };

  const editTeam = async (team: Team) => {
    const name = window.prompt('Team name', team.name);
    if (name === null) return;
    const description = window.prompt('Team description', team.description || '');
    if (description === null) return;
    await runAction(async () => {
      await updateTeam(team.id, { name, description });
    });
  };

  const removeTeam = async (team: Team) => {
    if (!window.confirm(`Delete "${team.name}"? Teams with assignment history cannot be deleted.`)) return;
    await runAction(() => deleteTeam(team.id));
  };

  const nav: Array<[AdminSection, string]> = [
    ['overview', 'Overview'],
    ['responses', 'Response records'],
    ['assignments', 'Teams & assignments'],
    ['intake', `Intake review${pendingCount ? ` (${pendingCount})` : ''}`],
    ['timeline', 'Operational timeline'],
    ['reports', 'Reports'],
    ['people', 'People & access'],
  ];

  return (
    <div className="space-y-6">
      <p className="text-sm text-slate-500">
        Administrator workspace · {currentUser.full_name || currentUser.email}
      </p>
      <nav aria-label="Administration sections" className="flex gap-2 overflow-x-auto rounded-xl bg-white p-2 shadow-sm">
        {nav.map(([key, label]) => (
          <button
            key={key}
            onClick={() => setSection(key)}
            className={`shrink-0 rounded-lg px-3 py-2 text-sm font-bold ${
              section === key ? 'bg-slate-900 text-white' : 'text-slate-600 hover:bg-slate-100'
            }`}
          >
            {label}
          </button>
        ))}
      </nav>
      {error && (
        <p role="alert" className="flex items-center gap-2 rounded-xl border border-red-200 bg-red-50 p-3 text-sm text-red-700">
          <AlertCircle className="h-4 w-4" /> {error}
        </p>
      )}

      {section === 'overview' && (
        <>
          <section className="grid gap-3 sm:grid-cols-2 xl:grid-cols-4">
            {[
              ['Approved responses', summary?.total_responses ?? '—'],
              ['Active responses without assignment', summary?.unassigned_active_responses ?? '—'],
              ['Assignments in progress', summary?.active_assignments ?? '—'],
              ['Awaiting coordinator review', pendingCount],
              ['Responses without location', summary?.missing_location_responses ?? '—'],
              ['Database', database],
            ].map(([label, value]) => (
              <div key={label} className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
                <p className="text-xs font-bold uppercase text-slate-500">{label}</p>
                <p className="mt-2 text-2xl font-black capitalize">{value}</p>
              </div>
            ))}
          </section>
          <section className="grid gap-3 sm:grid-cols-2">
            {nav.slice(1).map(([key, label]) => (
              <button
                key={key}
                onClick={() => setSection(key)}
                className="rounded-xl border border-slate-200 bg-white px-4 py-4 text-left font-bold shadow-sm hover:border-red-300"
              >
                {label}
              </button>
            ))}
          </section>
          <section className="flex flex-wrap items-center justify-between gap-3 rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
            <div className="flex items-center gap-2">
              {whatsappReady ? <CheckCircle2 className="h-5 w-5 text-emerald-600" /> : <AlertCircle className="h-5 w-5 text-amber-600" />}
              <div>
                <p className="font-bold">Official WhatsApp webhook</p>
                <p className="text-xs text-slate-500">
                  {whatsappReady
                    ? 'Webhook secrets are present; Meta callback verification and a live test are still required.'
                    : 'Setup required: Meta app credentials and a public HTTPS callback.'}
                </p>
              </div>
            </div>
            <span className="rounded-full bg-slate-100 px-3 py-1 text-xs font-bold">
              {whatsappReady ? 'Secrets present' : 'Not connected'}
            </span>
          </section>
        </>
      )}

      {section === 'responses' && <ResponseRegister userRole="admin" mode="admin" />}
      {section === 'assignments' && <AssignmentsManager userRole="admin" />}
      {section === 'intake' && <IntakeReview />}
      {section === 'timeline' && <TimelineView />}
      {section === 'reports' && <ReportsView />}

      {section === 'people' && (
        <>
          <section className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
            <div className="mb-4 flex items-center justify-between gap-3">
              <div>
                <h3 className="text-lg font-black">Accounts and access</h3>
                <p className="text-sm text-slate-500">Accounts are named and role-based; no shared passwords.</p>
              </div>
              <UsersRound className="h-6 w-6 text-red-600" />
            </div>
            {initialPassword && (
              <div className="mb-4 flex flex-wrap items-center justify-between gap-3 rounded-xl border border-amber-300 bg-amber-50 p-4">
                <div>
                  <p className="font-bold text-amber-900">Temporary password for {passwordRecipient} — shown once</p>
                  <code className="break-all text-sm text-amber-950">{initialPassword}</code>
                  <p className="mt-1 text-xs text-amber-800">Share securely. The user must change it at first sign-in.</p>
                </div>
                <button onClick={copyInitialPassword} className="inline-flex items-center gap-2 rounded-lg bg-white px-3 py-2 text-sm font-bold">
                  <Clipboard className="h-4 w-4" /> Copy and hide
                </button>
              </div>
            )}
            <form onSubmit={submitUser} className="mb-5 grid gap-3 md:grid-cols-4">
              <input required type="email" placeholder="Email" value={newUser.email} onChange={(e) => setNewUser({ ...newUser, email: e.target.value })} className="rounded-lg border p-2 text-sm" />
              <input required placeholder="Full name" value={newUser.full_name} onChange={(e) => setNewUser({ ...newUser, full_name: e.target.value })} className="rounded-lg border p-2 text-sm" />
              <select value={newUser.role} onChange={(e) => setNewUser({ ...newUser, role: e.target.value as CurrentUser['role'] })} className="rounded-lg border p-2 text-sm">
                <option value="responder">Responder</option><option value="coordinator">Coordinator</option><option value="admin">Administrator</option>
              </select>
              <button disabled={busy} className="rounded-lg bg-red-600 px-4 py-2 text-sm font-bold text-white disabled:opacity-50">Create account</button>
            </form>
            <div className="overflow-x-auto">
              <table className="w-full text-left text-sm">
                <thead><tr className="border-b text-xs uppercase text-slate-500"><th className="py-2">Name / email</th><th>Role</th><th>Status</th><th>Actions</th></tr></thead>
                <tbody>
                  {users.map((user) => (
                    <tr key={user.id} className="border-b last:border-0">
                      <td className="py-3"><span className="block font-semibold">{user.full_name || user.email}</span><span className="text-xs text-slate-500">{user.email}</span></td>
                      <td>
                        <select
                          aria-label={`Role for ${user.email}`}
                          value={user.role}
                          onChange={(e) => { const role = e.target.value as CurrentUser['role']; void runAction(() => updateAdminUser(user.id, { full_name: user.full_name || user.email, role }).then(() => undefined)); }}
                          className="rounded border p-1 text-xs"
                        >
                          <option value="responder">Responder</option><option value="coordinator">Coordinator</option><option value="admin">Administrator</option>
                        </select>
                      </td>
                      <td>{user.is_active ? 'Active' : 'Inactive'}</td>
                      <td className="text-right">
                        {user.id !== currentUser.id && (
                          <button
                            disabled={busy}
                            onClick={() => {
                              if (!window.confirm(`Reset the password for ${user.email}? Their current sessions will be revoked.`)) return;
                              void runAction(async () => {
                                const result = await resetUserPassword(user.id);
                                setInitialPassword(result.initial_password);
                                setPasswordRecipient(user.email);
                              });
                            }}
                            className="mr-3 font-semibold text-slate-700 hover:underline disabled:opacity-50"
                          >
                            Reset password
                          </button>
                        )}
                        <button disabled={busy || user.id === currentUser.id} onClick={() => runAction(() => setUserActive(user.id, !user.is_active).then(() => undefined))} className="font-semibold text-red-700 hover:underline disabled:opacity-50">
                          {user.is_active ? 'Deactivate' : 'Reactivate'}
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </section>

          <section className="grid gap-6 lg:grid-cols-2">
            <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
              <h3 className="mb-3 text-lg font-black">Response teams</h3>
              <form onSubmit={submitTeam} className="mb-4 grid gap-2 sm:grid-cols-[1fr_1fr_auto]">
                <input required placeholder="Team name" value={newTeam.name} onChange={(e) => setNewTeam({ ...newTeam, name: e.target.value })} className="rounded-lg border p-2 text-sm" />
                <input placeholder="Description" value={newTeam.description} onChange={(e) => setNewTeam({ ...newTeam, description: e.target.value })} className="rounded-lg border p-2 text-sm" />
                <button disabled={busy} className="rounded-lg bg-slate-900 px-3 py-2 text-sm font-bold text-white">Add team</button>
              </form>
              <ul className="space-y-2">
                {teams.map((team) => (
                  <li key={team.id} className="rounded-lg bg-slate-50 p-3">
                    <p className="font-bold">{team.name}</p><p className="text-xs text-slate-500">{team.description || 'No description'}</p>
                    <div className="mt-2 flex gap-3">
                      <button onClick={() => editTeam(team)} className="text-xs font-bold text-slate-700 hover:underline">Edit</button>
                      <button onClick={() => removeTeam(team)} className="text-xs font-bold text-red-700 hover:underline">Delete</button>
                    </div>
                  </li>
                ))}
              </ul>
            </div>

            <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
              <h3 className="mb-3 text-lg font-black">Team membership and chain of command</h3>
              <form onSubmit={submitMembership} className="mb-4 grid gap-2">
                <select required value={membership.team_id || ''} onChange={(e) => setMembership({ ...membership, team_id: Number(e.target.value) })} className="rounded-lg border p-2 text-sm">
                  <option value="" disabled>Select team</option>{teams.map((team) => <option key={team.id} value={team.id}>{team.name}</option>)}
                </select>
                <select required value={membership.user_id || ''} onChange={(e) => setMembership({ ...membership, user_id: Number(e.target.value) })} className="rounded-lg border p-2 text-sm">
                  <option value="" disabled>Select active account</option>{users.filter((user) => user.is_active).map((user) => <option key={user.id} value={user.id}>{user.full_name || user.email} · {user.email}</option>)}
                </select>
                <select value={membership.member_role} onChange={(e) => setMembership({ ...membership, member_role: e.target.value as 'leader' | 'member' })} className="rounded-lg border p-2 text-sm">
                  <option value="leader">Team leader</option><option value="member">Team member</option>
                </select>
                <button disabled={busy || !teams.length || !users.length} className="rounded-lg bg-slate-900 px-3 py-2 text-sm font-bold text-white">Add to team</button>
              </form>
              <ul className="space-y-2">
                {members.map((member) => (
                  <li key={member.id} className="flex items-center justify-between gap-3 rounded-lg bg-slate-50 p-3">
                    <span><span className="block font-semibold">{member.user_name}</span><span className="text-xs text-slate-500">{member.team_name}</span></span>
                    <div className="flex items-center gap-2">
                      <select aria-label={`Role for ${member.user_email}`} value={member.member_role} onChange={(e) => runAction(() => updateTeamMemberRole(member.id, e.target.value as TeamMember['member_role']).then(() => undefined))} className="rounded border p-1 text-xs">
                        <option value="leader">Leader</option><option value="member">Member</option>
                      </select>
                      <button onClick={() => runAction(() => removeTeamMember(member.id))} className="text-xs font-bold text-red-700 hover:underline">Remove</button>
                    </div>
                  </li>
                ))}
              </ul>
            </div>
          </section>

          <section className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
            <h3 className="mb-3 text-lg font-black">Recent administrative activity</h3>
            {audit.length === 0 ? <p className="text-sm text-slate-500">No administrative changes recorded.</p> : (
              <div className="overflow-x-auto">
                <table className="w-full text-left text-sm">
                  <thead><tr className="border-b text-xs uppercase text-slate-500"><th className="p-2">When</th><th className="p-2">Action</th><th className="p-2">By</th><th className="p-2">Details</th></tr></thead>
                  <tbody>{audit.map((entry) => <tr key={entry.id} className="border-b last:border-0"><td className="p-2 whitespace-nowrap">{new Date(entry.timestamp).toLocaleString()}</td><td className="p-2 font-semibold">{entry.action.replaceAll('_', ' ')}</td><td className="p-2">{entry.actor}</td><td className="p-2">{entry.details}</td></tr>)}</tbody>
                </table>
              </div>
            )}
          </section>
        </>
      )}
    </div>
  );
};
