import React, { useEffect, useState } from 'react';
import { getAssignments, getTeams, createAssignment, createTeam, deleteDraftAssignment, updateAssignmentStatus, updateDraftAssignment, Assignment, Team, fetchResponses } from '../../services/api';
import { ResponseItem } from '../../types';

interface AssignmentsManagerProps {
  userRole: 'admin' | 'coordinator' | 'responder';
}

export const AssignmentsManager: React.FC<AssignmentsManagerProps> = ({ userRole }) => {
  const [assignments, setAssignments] = useState<Assignment[]>([]);
  const [teams, setTeams] = useState<Team[]>([]);
  const [responses, setResponses] = useState<ResponseItem[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  
  // Form state for new assignment
  const [referenceCode, setReferenceCode] = useState('');
  const [responseId, setResponseId] = useState<number>(0);
  const [teamId, setTeamId] = useState<number>(0);
  const [description, setDescription] = useState('');
  const [editingAssignment, setEditingAssignment] = useState<Assignment | null>(null);
  const [teamName, setTeamName] = useState('');
  const [teamDescription, setTeamDescription] = useState('');

  const fetchData = async () => {
    try {
      setLoading(true);
      const [assignmentsData, teamsData, responsesData] = await Promise.all([getAssignments(), getTeams(), fetchResponses()]);
      setAssignments(assignmentsData);
      setTeams(teamsData);
      setResponses(responsesData);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load assignment data.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const handleCreateAssignment = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const payload = {
        reference_code: referenceCode,
        response_id: responseId,
        team_id: teamId,
        description: description || undefined,
      };
      if (editingAssignment) {
        await updateDraftAssignment(editingAssignment.id, payload);
      } else {
        await createAssignment({ ...payload, status: 'Draft' });
      }
      clearAssignmentForm();
      await fetchData();
    } catch (err) {
      alert(err instanceof Error ? err.message : 'Unable to create assignment.');
    }
  };

  const clearAssignmentForm = () => {
    setReferenceCode('');
    setResponseId(0);
    setTeamId(0);
    setDescription('');
    setEditingAssignment(null);
  };

  const editDraft = (assignment: Assignment) => {
    setEditingAssignment(assignment);
    setReferenceCode(assignment.reference_code);
    setResponseId(assignment.response_id);
    setTeamId(assignment.team_id);
    setDescription(assignment.description || '');
  };

  const handleCreateTeam = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await createTeam({ name: teamName, description: teamDescription });
      setTeamName('');
      setTeamDescription('');
      await fetchData();
    } catch (err) {
      alert(err instanceof Error ? err.message : 'Failed to create team.');
    }
  };

  const handleStatusChange = async (id: number, newStatus: string) => {
    try {
      await updateAssignmentStatus(id, newStatus);
      await fetchData();
    } catch (err) {
      alert(err instanceof Error ? err.message : 'Unable to update assignment status.');
    }
  };

  const handleDeleteDraft = async (assignment: Assignment) => {
    if (!window.confirm(`Delete draft ${assignment.reference_code}?`)) return;
    try {
      await deleteDraftAssignment(assignment.id);
      await fetchData();
    } catch (err) {
      alert(err instanceof Error ? err.message : 'Unable to delete draft assignment.');
    }
  };

  const statusColors: Record<string, string> = {
    "Draft": "bg-gray-200 text-gray-800",
    "Assigned": "bg-blue-100 text-blue-800",
    "Acknowledged": "bg-yellow-100 text-yellow-800",
    "In Progress": "bg-purple-100 text-purple-800",
    "Completed": "bg-green-100 text-green-800"
  };
  const nextStatus: Record<string, string> = {
    Draft: 'Assigned',
    Assigned: 'Acknowledged',
    Acknowledged: 'In Progress',
    'In Progress': 'Completed',
  };

  return (
    <div className="p-6 max-w-7xl mx-auto space-y-8">
      <div className="flex justify-between items-center border-b pb-4">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Teams & Assignments Manager</h1>
          <p className="text-sm text-gray-500">Karen-Lang'ata Field Unit • Operational Task Coordination</p>
        </div>
      </div>

      {error && <p role="alert" className="rounded-lg bg-red-50 p-3 text-sm text-red-700">{error}</p>}

      {userRole !== 'responder' && <div className="bg-white shadow rounded-lg p-6">
        <h2 className="text-lg font-semibold mb-4">Manage response teams</h2>
        <form onSubmit={handleCreateTeam} className="mb-6 grid grid-cols-1 md:grid-cols-3 gap-3">
          <input value={teamName} onChange={(e) => setTeamName(e.target.value)} placeholder="Team name" className="border rounded px-3 py-2 text-sm" required />
          <input value={teamDescription} onChange={(e) => setTeamDescription(e.target.value)} placeholder="Team description (optional)" className="border rounded px-3 py-2 text-sm" />
          <button type="submit" className="bg-slate-800 text-white font-medium px-4 py-2 rounded hover:bg-slate-700 text-sm">Add team</button>
        </form>
        <h2 className="text-lg font-semibold mb-4">{editingAssignment ? 'Edit draft assignment' : 'Issue New Field Assignment'}</h2>
        <form onSubmit={handleCreateAssignment} className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <input
            type="text"
            placeholder="Reference Code (e.g., ASN-001)"
            value={referenceCode}
            onChange={(e) => setReferenceCode(e.target.value)}
            className="border rounded px-3 py-2 text-sm"
            required
          />
          <select value={responseId} onChange={(e) => setResponseId(Number(e.target.value))} className="border rounded px-3 py-2 text-sm" required>
            <option value={0} disabled>Select response</option>
            {responses.map((response) => <option key={response.id} value={response.id}>{response.reference_code} · {response.title}</option>)}
          </select>
          <select
            value={teamId}
            onChange={(e) => setTeamId(Number(e.target.value))}
            className="border rounded px-3 py-2 text-sm"
            required
          >
            <option value={0} disabled>Select team</option>
            {teams.map((t) => (
              <option key={t.id} value={t.id}>{t.name}</option>
            ))}
          </select>
          <input value={description} onChange={(e) => setDescription(e.target.value)} placeholder="Assignment details" className="border rounded px-3 py-2 text-sm" />
          <div className="flex items-center gap-2">
            <button type="submit" className="bg-green-600 text-white font-medium px-4 py-2 rounded hover:bg-green-700 text-sm">
              {editingAssignment ? 'Save draft' : 'Create Assignment'}
            </button>
            {editingAssignment && (
              <button type="button" onClick={clearAssignmentForm} className="rounded border px-4 py-2 text-sm font-medium">
                Cancel
              </button>
            )}
          </div>
        </form>
      </div>}

      {/* Assignments Table */}
      <div className="bg-white shadow rounded-lg overflow-hidden">
        <div className="px-6 py-4 border-b">
          <h3 className="font-semibold text-gray-800">Assignments and lifecycle</h3>
        </div>
        {loading ? (
          <p className="p-6 text-gray-500">Loading assignments...</p>
        ) : assignments.length === 0 ? (
          <p className="p-6 text-gray-500">No active assignments recorded yet.</p>
        ) : (
          <table className="min-w-full divide-y divide-gray-200 text-left text-sm">
            <thead className="bg-gray-50 text-gray-700 uppercase font-semibold">
              <tr>
                <th className="px-6 py-3">Reference</th>
                <th className="px-6 py-3">Response</th>
                <th className="px-6 py-3">Team</th>
                <th className="px-6 py-3">Status</th>
                <th className="px-6 py-3">Actions / Lifecycle</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200">
              {assignments.map((asn) => (
                <tr key={asn.id} className="hover:bg-gray-50">
                  <td className="px-6 py-4 font-medium text-gray-900">{asn.reference_code}</td>
                  <td className="px-6 py-4 text-gray-600">{responses.find((item) => item.id === asn.response_id)?.reference_code || `#${asn.response_id}`}</td>
                  <td className="px-6 py-4 text-gray-600">{teams.find((item) => item.id === asn.team_id)?.name || `Team #${asn.team_id}`}</td>
                  <td className="px-6 py-4">
                    <span className={`px-2.5 py-1 rounded-full text-xs font-semibold ${statusColors[asn.status] || 'bg-gray-100 text-gray-800'}`}>
                      {asn.status}
                    </span>
                  </td>
                  <td className="px-6 py-4 space-x-2">
                    {userRole !== 'responder' && asn.status === 'Draft' && (
                      <button onClick={() => editDraft(asn)} className="text-xs font-semibold text-slate-700 hover:underline">
                        Edit draft
                      </button>
                    )}
                    {nextStatus[asn.status] && (userRole !== 'responder' || asn.status !== 'Draft') && (
                      <button
                        onClick={() => handleStatusChange(asn.id, nextStatus[asn.status])}
                        className="rounded bg-slate-900 px-3 py-1.5 text-xs font-semibold text-white"
                      >
                        {asn.status === 'Draft' ? 'Assign' : `Move to ${nextStatus[asn.status]}`}
                      </button>
                    )}
                    {userRole === 'admin' && asn.status === 'Draft' && (
                      <button onClick={() => handleDeleteDraft(asn)} className="ml-2 text-xs font-semibold text-red-700 hover:underline">
                        Delete draft
                      </button>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
};