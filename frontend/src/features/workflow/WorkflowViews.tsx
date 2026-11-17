import React, { useEffect, useState } from 'react';
import {
  approveIntake,
  createIntake,
  downloadWordReport,
  getIntakes,
  getReportPreview,
  getTimelineFeed,
  getTeams,
  rejectIntake,
  ReportPreview,
  ReportOptions,
  ReportSummary,
  ReportTemplate,
  TimelineFeedEvent,
  Team,
} from '../../services/api';
import { fetchResponses } from '../../services/api';
import { ResponseCreatePayload, ResponseItem } from '../../types';

export function IntakeReview() {
  const [intakes, setIntakes] = useState<Awaited<ReturnType<typeof getIntakes>>>([]);
  const [selectedId, setSelectedId] = useState<number | null>(null);
  const [sourceText, setSourceText] = useState('');
  const [sourceChannel, setSourceChannel] = useState<'manual' | 'whatsapp_test'>('manual');
  const [referenceCode, setReferenceCode] = useState('');
  const [title, setTitle] = useState('');
  const [category, setCategory] = useState('Community assistance');
  const [priority, setPriority] = useState('normal');
  const [location, setLocation] = useState('');
  const [teams, setTeams] = useState<Team[]>([]);
  const [assignmentTeamId, setAssignmentTeamId] = useState(0);
  const [assignmentReference, setAssignmentReference] = useState('');
  const [assignmentDescription, setAssignmentDescription] = useState('');
  const [lastPublished, setLastPublished] = useState<{
    referenceCode: string;
    assigned: boolean;
    teamName?: string;
  } | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);

  const selected = intakes.find((item) => item.id === selectedId);

  const refresh = async () => {
    const data = await getIntakes();
    setIntakes(data);
    if (selectedId && !data.some((item) => item.id === selectedId)) {
      setSelectedId(null);
    }
  };

  useEffect(() => {
    Promise.all([refresh(), getTeams()])
      .then(([, teamRows]) => setTeams(teamRows))
      .catch((err: Error) => setError(err.message));
  }, []);

  const submitIntake = async (event: React.FormEvent) => {
    event.preventDefault();
    setBusy(true);
    setError(null);
    try {
      const saved = await createIntake({
        source_channel: sourceChannel,
        source_message_id:
          sourceChannel === 'whatsapp_test' ? `demo-${Date.now()}` : undefined,
        source_text: sourceText,
      });
      setSourceText('');
      setSelectedId(saved.id);
      setReferenceCode(`CR-KL-${new Date().getFullYear()}-${String(saved.id).padStart(3, '0')}`);
      setAssignmentReference(`ASN-${new Date().getFullYear()}-${String(saved.id).padStart(3, '0')}`);
      setTitle('');
      setLocation('');
      setLastPublished(null);
      await refresh();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to save intake.');
    } finally {
      setBusy(false);
    }
  };

  const approve = async (assignToTeam: boolean) => {
    if (!selected) return;
    if (assignToTeam && !assignmentTeamId) {
      setError('Select a response team before creating an assignment.');
      return;
    }
    setBusy(true);
    setError(null);
    const payload: ResponseCreatePayload = {
      reference_code: referenceCode,
      title,
      description: selected.source_text,
      category,
      priority,
      location,
    };
    try {
      await approveIntake(
        selected.id,
        payload,
        assignToTeam
          ? {
              reference_code: assignmentReference,
              team_id: assignmentTeamId,
              description: assignmentDescription || undefined,
            }
          : undefined,
      );
      setLastPublished({
        referenceCode,
        assigned: assignToTeam,
        teamName: teams.find((team) => team.id === assignmentTeamId)?.name,
      });
      setSelectedId(null);
      setAssignmentTeamId(0);
      await refresh();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Approval failed.');
    } finally {
      setBusy(false);
    }
  };

  const reject = async () => {
    if (!selected) return;
    setBusy(true);
    setError(null);
    try {
      await rejectIntake(selected.id);
      setSelectedId(null);
      await refresh();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Rejection failed.');
    } finally {
      setBusy(false);
    }
  };

  return (
    <div className="space-y-6">
      <div className="rounded-2xl border border-amber-300 bg-amber-50 p-4 text-sm text-amber-900">
        Manually entered test messages are synthetic only. A real Meta webhook message appears here as a draft
        after webhook setup; it still needs coordinator review before publishing or assigning.
      </div>
      {lastPublished && (
        <p role="status" className="rounded-xl border border-emerald-200 bg-emerald-50 p-3 text-sm text-emerald-900">
          Response {lastPublished.referenceCode} is now on the Response Register
          {lastPublished.assigned
            ? ` and assigned to ${lastPublished.teamName}.`
            : '. No team assignment was created; you can assign it from Teams & Assignments.'}
        </p>
      )}
      {error && <p role="alert" className="rounded-xl bg-red-50 p-3 text-sm text-red-700">{error}</p>}

      <section className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
        <h3 className="mb-4 text-lg font-bold">Capture incoming information</h3>
        <form onSubmit={submitIntake} className="space-y-4">
          <label className="block text-sm font-semibold">
            Source
            <select
              value={sourceChannel}
              onChange={(event) => setSourceChannel(event.target.value as 'manual' | 'whatsapp_test')}
              className="mt-1 block w-full rounded-lg border border-slate-300 p-2"
            >
              <option value="manual">Manual coordinator entry</option>
              <option value="whatsapp_test">WhatsApp test message (synthetic)</option>
            </select>
          </label>
          {sourceChannel === 'whatsapp_test' && (
            <button
              type="button"
              onClick={() => setSourceText(
                'TEST MESSAGE — Flood water is entering homes near the school. Two families need blankets and first aid. Reported at 08:15.',
              )}
              className="rounded-lg border border-slate-300 px-3 py-2 text-sm font-semibold"
            >
              Load synthetic WhatsApp test message
            </button>
          )}
          <label className="block text-sm font-semibold">
            Original message
            <textarea
              required
              maxLength={10000}
              rows={5}
              value={sourceText}
              onChange={(event) => setSourceText(event.target.value)}
              className="mt-1 block w-full rounded-lg border border-slate-300 p-3 font-normal"
              placeholder="Paste an unstructured message. It is saved as a draft and is not published automatically."
            />
          </label>
          <button disabled={busy} className="rounded-lg bg-red-600 px-4 py-2 font-semibold text-white disabled:opacity-50">
            Save draft for review
          </button>
        </form>
      </section>

      <div className="grid gap-6 lg:grid-cols-[minmax(0,1fr)_minmax(0,1.3fr)]">
        <section className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
          <h3 className="mb-4 text-lg font-bold">Pending drafts ({intakes.length})</h3>
          {intakes.length === 0 ? (
            <p className="text-sm text-slate-500">No drafts awaiting review.</p>
          ) : (
            <ul className="space-y-2">
              {intakes.map((item) => (
                <li key={item.id}>
                  <button
                    onClick={() => {
                      setSelectedId(item.id);
                      setReferenceCode(`CR-KL-${new Date().getFullYear()}-${String(item.id).padStart(3, '0')}`);
                      setAssignmentReference(`ASN-${new Date().getFullYear()}-${String(item.id).padStart(3, '0')}`);
                      setAssignmentTeamId(0);
                      setTitle('');
                    }}
                    className={`w-full rounded-xl border p-3 text-left text-sm ${
                      selectedId === item.id ? 'border-red-500 bg-red-50' : 'border-slate-200'
                    }`}
                  >
                    <span className="block font-bold">
                      {item.source_channel === 'whatsapp'
                        ? 'WhatsApp'
                        : item.source_channel === 'whatsapp_test'
                          ? 'WhatsApp test (synthetic)'
                          : 'Manual'} · Draft #{item.id}
                    </span>
                    <span className="mt-1 block truncate text-slate-600">{item.source_text}</span>
                  </button>
                </li>
              ))}
            </ul>
          )}
        </section>

        <section className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
          <h3 className="mb-4 text-lg font-bold">Coordinator review</h3>
          {!selected ? (
            <p className="text-sm text-slate-500">Select a pending draft to structure it.</p>
          ) : (
            <>
              <blockquote className="mb-4 whitespace-pre-wrap rounded-xl bg-slate-50 p-4 text-sm text-slate-700">
                {selected.source_text}
              </blockquote>
              <form onSubmit={(event) => { event.preventDefault(); void approve(false); }} className="grid gap-3 sm:grid-cols-2">
                <input required value={referenceCode} onChange={(e) => setReferenceCode(e.target.value)} placeholder="Reference code" className="rounded-lg border p-2 text-sm" />
                <input required value={title} onChange={(e) => setTitle(e.target.value)} placeholder="Response title" className="rounded-lg border p-2 text-sm" />
                <select value={category} onChange={(e) => setCategory(e.target.value)} className="rounded-lg border p-2 text-sm">
                  <option>Community assistance</option>
                  <option>Disaster response</option>
                  <option>Emergency support</option>
                  <option>Preparedness activity</option>
                </select>
                <select value={priority} onChange={(e) => setPriority(e.target.value)} className="rounded-lg border p-2 text-sm">
                  <option value="normal">Normal</option>
                  <option value="high">High</option>
                  <option value="urgent">Urgent</option>
                </select>
                <input value={location} onChange={(e) => setLocation(e.target.value)} placeholder="Location" className="rounded-lg border p-2 text-sm sm:col-span-2" />
                <div className="space-y-3 rounded-xl bg-slate-50 p-3 sm:col-span-2">
                  <p className="text-sm font-bold">Optional: assign a response team now</p>
                  <select
                    value={assignmentTeamId || ''}
                    onChange={(event) => setAssignmentTeamId(Number(event.target.value))}
                    className="w-full rounded-lg border p-2 text-sm"
                  >
                    <option value="">Publish without assigning</option>
                    {teams.map((team) => <option key={team.id} value={team.id}>{team.name}</option>)}
                  </select>
                  {assignmentTeamId !== 0 && (
                    <>
                      <input
                        required
                        value={assignmentReference}
                        onChange={(event) => setAssignmentReference(event.target.value)}
                        placeholder="Assignment reference"
                        className="w-full rounded-lg border p-2 text-sm"
                      />
                      <input
                        value={assignmentDescription}
                        onChange={(event) => setAssignmentDescription(event.target.value)}
                        placeholder="Task instructions (optional)"
                        className="w-full rounded-lg border p-2 text-sm"
                      />
                    </>
                  )}
                  {teams.length === 0 && (
                    <p className="text-xs text-slate-600">Create a response team before assigning this intake.</p>
                  )}
                </div>
                <div className="flex flex-wrap gap-2 sm:col-span-2">
                  <button disabled={busy} className="rounded-lg bg-emerald-700 px-4 py-2 text-sm font-semibold text-white disabled:opacity-50">
                    Approve and publish
                  </button>
                  <button
                    type="button"
                    disabled={busy || !assignmentTeamId}
                    onClick={() => void approve(true)}
                    className="rounded-lg bg-red-600 px-4 py-2 text-sm font-semibold text-white disabled:opacity-50"
                  >
                    Approve and assign team
                  </button>
                  <button type="button" disabled={busy} onClick={reject} className="rounded-lg border border-red-300 px-4 py-2 text-sm font-semibold text-red-700">
                    Reject draft
                  </button>
                </div>
              </form>
            </>
          )}
        </section>
      </div>
    </div>
  );
}

export function TimelineView() {
  const [responses, setResponses] = useState<ResponseItem[]>([]);
  const [selectedId, setSelectedId] = useState<number | null>(null);
  const [events, setEvents] = useState<TimelineFeedEvent[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [loadingResponses, setLoadingResponses] = useState(true);
  const [loadingEvents, setLoadingEvents] = useState(true);

  useEffect(() => {
    fetchResponses()
      .then(setResponses)
      .catch((err: Error) => setError(err.message))
      .finally(() => setLoadingResponses(false));
  }, []);

  useEffect(() => {
    setLoadingEvents(true);
    setError(null);
    getTimelineFeed(selectedId ?? undefined)
      .then(setEvents)
      .catch((err: Error) => setError(err.message))
      .finally(() => setLoadingEvents(false));
  }, [selectedId]);

  return (
    <section className="space-y-5 rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
      <div>
        <h3 className="text-lg font-black">Latest operational activity</h3>
        <p className="text-sm text-slate-500">Intake approvals, response changes, and team assignment updates across the operation.</p>
        <p className="mt-1 text-xs text-slate-500">Read-only audit history. Correct records through response or assignment management; their changes are recorded as new events.</p>
      </div>
      <label className="block max-w-lg text-sm font-semibold">
        Response
        <select
          value={selectedId ?? 'all'}
          onChange={(event) => setSelectedId(event.target.value === 'all' ? null : Number(event.target.value))}
          className="mt-1 block w-full rounded-lg border border-slate-300 p-2"
        >
          <option value="all">All responses</option>
          {responses.map((item) => <option key={item.id} value={item.id}>{item.reference_code} · {item.title}</option>)}
        </select>
      </label>
      {error && <p role="alert" className="text-sm text-red-700">{error}</p>}
      {loadingResponses || loadingEvents ? (
        <p className="text-sm text-slate-500">Loading operational activity…</p>
      ) : events.length === 0 ? (
        <div className="rounded-xl bg-slate-50 p-5 text-sm text-slate-600">
          {responses.length === 0
            ? 'No response records yet. Approved intake or a coordinator-created response will start the timeline.'
            : 'No activity recorded yet. Approving intake, creating a response, or creating and updating an assignment will add events here.'}
        </div>
      ) : (
        <ol className="space-y-4 border-l-2 border-red-200 pl-5">
          {events.map((event) => (
            <li key={event.id} className="relative">
              <span className="absolute -left-[1.65rem] top-1 h-3 w-3 rounded-full bg-red-600" />
              <p className="font-semibold">{event.event_type.replaceAll('_', ' ')}</p>
              <p className="text-xs font-semibold text-red-700">
                {event.response_reference} · {event.response_title}
              </p>
              <p className="text-sm text-slate-600">{event.details}</p>
              <p className="mt-1 flex flex-wrap gap-x-3 text-xs text-slate-400">
                <span>By {event.actor_name}</span>
                <time dateTime={event.timestamp}>{new Date(event.timestamp).toLocaleString()}</time>
              </p>
            </li>
          ))}
        </ol>
      )}
    </section>
  );
}

export function ReportsView() {
  const [preview, setPreview] = useState<ReportPreview | null>(null);
  const [showPreview, setShowPreview] = useState(true);
  const [teams, setTeams] = useState<Team[]>([]);
  const [filters, setFilters] = useState<ReportOptions>({ template: 'operational' });
  const [fromDate, setFromDate] = useState('');
  const [toDate, setToDate] = useState('');
  const [teamId, setTeamId] = useState('');
  const [template, setTemplate] = useState<ReportTemplate>('operational');
  const selectTemplate = (value: string) => {
    if (value === 'operational' || value === 'situation' || value === 'field') {
      setTemplate(value);
    }
  };
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const [busy, setBusy] = useState(false);

  useEffect(() => {
    Promise.all([getTeams(), getReportPreview()])
      .then(([teamRows, report]) => {
        setTeams(teamRows);
        setPreview(report);
      })
      .catch((err: Error) => setError(err.message))
      .finally(() => setLoading(false));
  }, []);

  const applyFilters = async (event: React.FormEvent) => {
    event.preventDefault();
    if (fromDate && toDate && fromDate > toDate) {
      setError('Start date must be on or before end date.');
      return;
    }
    const nextFilters: ReportOptions = {
      ...(fromDate ? { from_date: fromDate } : {}),
      ...(toDate ? { to_date: toDate } : {}),
      ...(teamId ? { team_id: Number(teamId) } : {}),
      template,
    };
    setBusy(true);
    setError(null);
    try {
      const report = await getReportPreview(nextFilters);
      setPreview(report);
      setFilters(nextFilters);
      setShowPreview(true);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unable to apply report filters.');
    } finally {
      setBusy(false);
    }
  };

  const clearFilters = async () => {
    setFromDate('');
    setToDate('');
    setTeamId('');
    setTemplate('operational');
    setBusy(true);
    setError(null);
    try {
      const report = await getReportPreview({ template: 'operational' });
      setPreview(report);
      setFilters({ template: 'operational' });
      setShowPreview(true);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unable to clear report filters.');
    } finally {
      setBusy(false);
    }
  };

  const download = async () => {
    setBusy(true);
    setError(null);
    try {
      await downloadWordReport(filters);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Report generation failed.');
    } finally {
      setBusy(false);
    }
  };

  const cards: Array<{
    label: string;
    key: 'total_responses' | 'active_responses' | 'resolved_responses' | 'unassigned_active_responses' | 'total_assignments' | 'active_assignments' | 'completed_assignments' | 'missing_location_responses';
  }> = [
    { label: 'Responses in period', key: 'total_responses' },
    { label: 'Active responses', key: 'active_responses' },
    { label: 'Resolved responses', key: 'resolved_responses' },
    { label: 'Active without assignment', key: 'unassigned_active_responses' },
    { label: 'Assignments in period', key: 'total_assignments' },
    { label: 'Active assignments', key: 'active_assignments' },
    { label: 'Completed assignments', key: 'completed_assignments' },
    { label: 'Responses without location', key: 'missing_location_responses' },
  ];
  const activeLocationBreakdown = (preview?.responses ?? [])
    .filter((item) => item.status === 'Active')
    .reduce<Record<string, number>>((counts, item) => {
      const location = item.location?.trim() || 'Location not recorded';
      counts[location] = (counts[location] ?? 0) + 1;
      return counts;
    }, {});
  const breakdowns: Array<{ title: string; values: Record<string, number> }> = preview
    ? preview.template === 'field'
      ? [{ title: 'Active responses by location', values: activeLocationBreakdown }]
      : preview.template === 'situation'
        ? [
          { title: 'By priority', values: preview.summary.priority_breakdown },
          { title: 'Coverage by location', values: preview.summary.location_breakdown },
        ]
        : [
          { title: 'By priority', values: preview.summary.priority_breakdown },
          { title: 'By category', values: preview.summary.category_breakdown },
          { title: 'By source', values: preview.summary.source_breakdown },
          { title: 'By location', values: preview.summary.location_breakdown },
        ]
    : [];
  const reportTitles: Record<ReportTemplate, string> = {
    operational: 'CaseLoop Operational Report',
    situation: 'CaseLoop Situation Report',
    field: 'CaseLoop Field Action Brief',
  };
  const weeklyActivity = preview?.summary.weekly_activity ?? [];
  const previousWeek = weeklyActivity.length > 1
    ? weeklyActivity[weeklyActivity.length - 2]
    : null;
  const latestWeek = weeklyActivity.length > 0
    ? weeklyActivity[weeklyActivity.length - 1]
    : null;
  const weeklyMaximum = Math.max(
    1,
    ...weeklyActivity.flatMap((week) => [week.responses_created, week.assignments_created]),
  );
  const responseRows = preview?.template === 'field'
    ? preview.responses.filter((item) => item.status === 'Active')
    : preview?.responses ?? [];
  const assignmentRows = preview?.template === 'operational'
    ? preview.assignments
    : preview?.assignments.filter((item) => !['Completed', 'Cancelled'].includes(item.status)) ?? [];

  return (
    <div className="space-y-6">
      {error && <p role="alert" className="rounded-xl bg-red-50 p-3 text-sm text-red-700">{error}</p>}
      <section className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
        <div className="mb-4">
          <h3 className="font-black">Build a report</h3>
          <p className="text-sm text-slate-500">Filter approved records, then choose a format for preview and export.</p>
        </div>
        <form onSubmit={applyFilters} className="grid gap-3 sm:grid-cols-2 xl:grid-cols-4">
          <label className="text-sm font-semibold">
            From
            <input type="date" value={fromDate} onChange={(event) => setFromDate(event.target.value)} className="mt-1 block w-full rounded-lg border border-slate-300 p-2" />
          </label>
          <label className="text-sm font-semibold">
            To
            <input type="date" value={toDate} onChange={(event) => setToDate(event.target.value)} className="mt-1 block w-full rounded-lg border border-slate-300 p-2" />
          </label>
          <label className="text-sm font-semibold">
            Team
            <select value={teamId} onChange={(event) => setTeamId(event.target.value)} className="mt-1 block w-full rounded-lg border border-slate-300 p-2">
              <option value="">All teams</option>
              {teams.map((team) => <option key={team.id} value={team.id}>{team.name}</option>)}
            </select>
          </label>
          <label className="text-sm font-semibold">
            Report format
            <select value={template} onChange={(event) => selectTemplate(event.target.value)} className="mt-1 block w-full rounded-lg border border-slate-300 p-2">
              <option value="operational">Operational report</option>
              <option value="situation">Situation report</option>
              <option value="field">Field action brief</option>
            </select>
          </label>
          <div className="flex items-end gap-2">
            <button type="submit" disabled={busy || loading} className="rounded-lg bg-slate-900 px-4 py-2 font-semibold text-white disabled:opacity-50">
              Apply filters
            </button>
            <button type="button" disabled={busy || loading} onClick={clearFilters} className="rounded-lg border border-slate-300 bg-white px-4 py-2 font-semibold disabled:opacity-50">
              Clear
            </button>
          </div>
        </form>
      </section>
      {loading ? (
        <p className="text-sm text-slate-500">Loading report data…</p>
      ) : preview ? (
        <>
          <section className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
            {cards.map(({ label, key }) => (
          <div key={key} className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
            <p className="text-sm text-slate-500">{label}</p>
            <p className="mt-2 text-3xl font-black text-slate-900">{preview.summary[key]}</p>
          </div>
            ))}
          </section>
          <div className="flex flex-wrap gap-3">
            <button
              disabled={busy || !preview}
              onClick={() => setShowPreview((visible) => !visible)}
              className="rounded-lg border border-slate-300 bg-white px-5 py-3 font-semibold disabled:opacity-50"
            >
              {showPreview ? 'Hide report preview' : 'Preview report'}
            </button>
            <button disabled={busy || !preview} onClick={download} className="rounded-lg bg-red-600 px-5 py-3 font-semibold text-white disabled:opacity-50">
              {busy ? 'Generating Word report…' : 'Download Word report (.docx)'}
            </button>
          </div>
        </>
      ) : null}
      {showPreview && preview && (
        <section className="space-y-5 rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
          <div className="flex flex-wrap items-end justify-between gap-2">
            <div>
              <p className="text-xs font-bold uppercase text-slate-500">Report preview</p>
              <h3 className="text-xl font-black">{reportTitles[preview.template]}</h3>
              <p className="text-sm text-slate-500">
                {preview.filters.from_date || preview.filters.to_date
                  ? `${preview.filters.from_date || 'Beginning'} to ${preview.filters.to_date || 'Present'}`
                  : 'All dates'}
                {' · '}{preview.filters.team_name || 'All teams'}
              </p>
            </div>
            <p className="text-xs text-slate-500">Generated {new Date(preview.generated_at).toLocaleString()}</p>
          </div>
          <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
            {breakdowns.map(({ title, values }) => {
              const rows = Object.entries(values);
              const largest = Math.max(1, ...rows.map(([, count]) => count));
              return (
                <section key={title} className="rounded-xl bg-slate-50 p-4">
                  <h4 className="mb-3 font-bold">{title}</h4>
                  {rows.length === 0 ? (
                    <p className="text-sm text-slate-500">No records.</p>
                  ) : (
                    <ul className="space-y-3">
                      {rows.map(([label, count]) => (
                        <li key={label}>
                          <div className="mb-1 flex justify-between gap-2 text-sm">
                            <span>{label}</span><span className="font-bold">{count}</span>
                          </div>
                          <div className="h-2 overflow-hidden rounded-full bg-slate-200">
                            <div className="h-full rounded-full bg-red-600" style={{ width: `${(count / largest) * 100}%` }} />
                          </div>
                        </li>
                      ))}
                    </ul>
                  )}
                </section>
              );
            })}
          </div>
          <section className="rounded-xl border border-slate-200 p-4">
            <div className="mb-3 flex flex-wrap items-end justify-between gap-2">
              <div>
                <h4 className="font-bold">Weekly activity trend</h4>
                <p className="text-xs text-slate-500">
                  Responses and assignments created per week from {preview.summary.weekly_activity_from} to {preview.summary.weekly_activity_to}.
                  {' '}The default trend contains eight weeks; longer date selections are capped at 26 weeks.
                </p>
              </div>
              {latestWeek && previousWeek && (
                <p className="text-xs text-slate-600">
                  Latest week: responses {latestWeek.responses_created - previousWeek.responses_created >= 0 ? '+' : ''}{latestWeek.responses_created - previousWeek.responses_created},
                  {' '}assignments {latestWeek.assignments_created - previousWeek.assignments_created >= 0 ? '+' : ''}{latestWeek.assignments_created - previousWeek.assignments_created} vs previous week
                </p>
              )}
            </div>
            {weeklyActivity.length === 0 ? (
              <p className="text-sm text-slate-500">No activity in the trend window.</p>
            ) : (
              <div className="space-y-3">
                {weeklyActivity.map((week) => (
                  <div key={week.week_start} className="grid gap-2 sm:grid-cols-[7rem_1fr] sm:items-center">
                    <p className="text-xs font-semibold text-slate-600">{week.week_start}</p>
                    <div className="space-y-1">
                      <div className="flex items-center gap-2 text-xs">
                        <span className="w-24 text-slate-500">Responses {week.responses_created}</span>
                        <div className="h-2 flex-1 rounded-full bg-slate-100">
                          <div className="h-2 rounded-full bg-red-600" style={{ width: `${(week.responses_created / weeklyMaximum) * 100}%` }} />
                        </div>
                      </div>
                      <div className="flex items-center gap-2 text-xs">
                        <span className="w-24 text-slate-500">Assignments {week.assignments_created}</span>
                        <div className="h-2 flex-1 rounded-full bg-slate-100">
                          <div className="h-2 rounded-full bg-blue-600" style={{ width: `${(week.assignments_created / weeklyMaximum) * 100}%` }} />
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </section>
          <p className="rounded-xl border border-amber-200 bg-amber-50 p-3 text-sm text-amber-900">
            {preview.summary.unassigned_active_responses === 0
              ? 'All active responses in this report have at least one team assignment.'
              : `${preview.summary.unassigned_active_responses} active response(s) in this report have no team assignment.`}
          </p>
          <div className="overflow-x-auto">
            <h4 className="mb-2 font-bold">{preview.template === 'field' ? 'Active responses' : 'Approved responses'}</h4>
            <table className="w-full text-left text-sm">
              <thead><tr className="border-b text-xs uppercase text-slate-500"><th className="p-2">Reference</th><th className="p-2">Response</th><th className="p-2">Category</th><th className="p-2">Priority</th><th className="p-2">Source</th><th className="p-2">Location</th><th className="p-2">Status</th></tr></thead>
              <tbody>
                {responseRows.length === 0 ? <tr><td colSpan={7} className="p-3 text-slate-500">No approved responses match this report format and filters.</td></tr> : responseRows.map((item) => (
                  <tr key={item.id} className="border-b last:border-0"><td className="p-2 font-mono">{item.reference_code}</td><td className="p-2 font-semibold">{item.title}</td><td className="p-2">{item.category || '—'}</td><td className="p-2 capitalize">{item.priority || '—'}</td><td className="p-2 capitalize">{item.source_channel.replaceAll('_', ' ')}</td><td className="p-2">{item.location || '—'}</td><td className="p-2">{item.status}</td></tr>
                ))}
              </tbody>
            </table>
          </div>
          <div className="overflow-x-auto">
            <h4 className="mb-2 font-bold">Assignments</h4>
            <table className="w-full text-left text-sm">
              <thead><tr className="border-b text-xs uppercase text-slate-500"><th className="p-2">Task</th><th className="p-2">Response</th><th className="p-2">Team</th><th className="p-2">Status</th><th className="p-2">Task details</th></tr></thead>
              <tbody>
                {assignmentRows.length === 0 ? <tr><td colSpan={5} className="p-3 text-slate-500">No assignments match this report format and filters.</td></tr> : assignmentRows.map((item) => (
                  <tr key={item.id} className="border-b last:border-0"><td className="p-2 font-mono">{item.reference_code || `#${item.id}`}</td><td className="p-2">{item.response_reference} · {item.response_title}</td><td className="p-2">{item.team_name}</td><td className="p-2">{item.status}</td><td className="p-2">{item.description || '—'}</td></tr>
                ))}
              </tbody>
            </table>
          </div>
        </section>
      )}
      <p className="text-sm text-slate-500">Counts and breakdowns use approved records. Location coverage is based on the recorded location text, not a map or geocoded coordinates. The Word download uses the same filters and format as this preview.</p>
    </div>
  );
}
