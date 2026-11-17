import { ResponseItem, ResponseCreatePayload, SystemStatus } from '../types';

// If VITE_API_BASE_URL is not defined (local dev), default to "/api" 
// so it hits the Vite proxy and shares the same origin (localhost:5173).
// In production, you can set VITE_API_BASE_URL in your build environment.
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "/api";
const API_ROOT_URL = API_BASE_URL.replace(/\/api\/?$/, "");
// 👉 ADD THIS LINE TO DEBUG:
console.log("🔍 Resolved API_BASE_URL:", API_BASE_URL);
let csrfToken = '';

async function apiFetch(input: RequestInfo | URL, init: RequestInit = {}): Promise<Response> {
  const headers = new Headers(init.headers);
  const method = (init.method || 'GET').toUpperCase();
  if (!['GET', 'HEAD', 'OPTIONS'].includes(method) && csrfToken) {
    headers.set('X-CSRF-Token', csrfToken);
  }
  return fetch(input, { ...init, headers, credentials: 'include' });
}

export async function checkBackendHealth() {
  // Instead of hitting the unproxied root '/', hit a valid API endpoint 
  // that goes through the Vite proxy, such as system status or intakes
  const res = await apiFetch(`${API_BASE_URL}/admin/system-status`);
  if (!res.ok) throw new Error('Backend health check failed');
  return res.json();
}

export interface CurrentUser {
  id: number;
  email: string;
  full_name: string | null;
  role: 'admin' | 'coordinator' | 'responder';
  is_active: number;
  must_change_password: boolean;
  created_at: string;
}

interface SessionResponse {
  user: CurrentUser;
  csrf_token: string;
}

export async function loginUser(credentials: {
  email: string;
  password: string;
  audience?: 'workspace' | 'admin';
}): Promise<CurrentUser> {
  const res = await apiFetch(`${API_BASE_URL}/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(credentials),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || 'Authentication failed');
  }
  const session: SessionResponse = await res.json();
  csrfToken = session.csrf_token;
  return session.user;
}

export async function registerUser(data: {
  email: string;
  full_name: string;
  password: string;
}): Promise<CurrentUser> {
  const res = await apiFetch(`${API_BASE_URL}/auth/register`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || 'Registration failed.');
  }
  const session: SessionResponse = await res.json();
  csrfToken = session.csrf_token;
  return session.user;
}

export async function getCurrentUser(): Promise<CurrentUser> {
  const res = await apiFetch(`${API_BASE_URL}/auth/me`);
  if (!res.ok) throw new Error('Sign in required.');
  const session: SessionResponse = await res.json();
  csrfToken = session.csrf_token;
  return session.user;
}

export async function logoutUser(): Promise<void> {
  const res = await apiFetch(`${API_BASE_URL}/auth/logout`, { method: 'POST' });
  if (!res.ok) throw new Error('Unable to sign out. Please try again.');
  csrfToken = '';
}

export async function changePassword(credentials: {
  current_password: string;
  new_password: string;
}): Promise<CurrentUser> {
  const res = await apiFetch(`${API_BASE_URL}/auth/password`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(credentials),
  });
  if (!res.ok) {
    const error = await res.json().catch(() => ({}));
    throw new Error(error.detail || 'Unable to update password.');
  }
  return res.json();
}

export async function fetchSystemStatus(): Promise<SystemStatus> {
  const response = await apiFetch(`${API_BASE_URL}/admin/system-status`);
  if (!response.ok) throw new Error('Failed to fetch system metrics');
  return response.json();
}

export async function getAdminUsers(): Promise<CurrentUser[]> {
  const response = await apiFetch(`${API_BASE_URL}/admin/users`);
  if (!response.ok) throw new Error('Failed to load user accounts.');
  return response.json();
}

export async function createAdminUser(data: {
  email: string;
  full_name: string;
  role: CurrentUser['role'];
}): Promise<{ user: CurrentUser; initial_password: string; show_password_once: boolean }> {
  const response = await apiFetch(`${API_BASE_URL}/admin/users`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });
  if (!response.ok) {
    const error = await response.json().catch(() => ({}));
    throw new Error(error.detail || 'Failed to create user account.');
  }
  return response.json();
}

export async function setUserActive(userId: number, is_active: boolean): Promise<CurrentUser> {
  const response = await apiFetch(`${API_BASE_URL}/admin/users/${userId}/status`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ is_active }),
  });
  if (!response.ok) {
    const error = await response.json().catch(() => ({}));
    throw new Error(error.detail || 'Failed to update user account.');
  }
  return response.json();
}

export async function resetUserPassword(
  userId: number,
): Promise<{ initial_password: string; show_password_once: boolean }> {
  const response = await apiFetch(`${API_BASE_URL}/admin/users/${userId}/reset-password`, {
    method: 'POST',
  });
  if (!response.ok) {
    const error = await response.json().catch(() => ({}));
    throw new Error(error.detail || 'Failed to reset user password.');
  }
  return response.json();
}

export async function updateAdminUser(
  userId: number,
  data: { full_name: string; role: CurrentUser['role'] },
): Promise<CurrentUser> {
  const response = await apiFetch(`${API_BASE_URL}/admin/users/${userId}`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });
  if (!response.ok) {
    const error = await response.json().catch(() => ({}));
    throw new Error(error.detail || 'Failed to update user account.');
  }
  return response.json();
}

export async function getAdminAudit(): Promise<Array<{
  id: number;
  action: string;
  details: string | null;
  timestamp: string;
  actor: string;
}>> {
  const response = await apiFetch(`${API_BASE_URL}/admin/audit`);
  if (!response.ok) throw new Error('Failed to load administration history.');
  return response.json();
}

export async function fetchResponses(): Promise<ResponseItem[]> {
  const res = await apiFetch(`${API_BASE_URL}/responses/`);
  if (!res.ok) throw new Error("Failed to fetch responses from local backend.");
  return res.json();
}

export async function createResponse(payload: ResponseCreatePayload): Promise<ResponseItem> {
  const res = await apiFetch(`${API_BASE_URL}/responses/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!res.ok) {
    const err = await res.json();
    throw new Error(err.detail || "Failed to create response record.");
  }
  return res.json();
}

export async function updateResponse(
  id: number,
  payload: ResponseCreatePayload,
): Promise<ResponseItem> {
  const response = await apiFetch(`${API_BASE_URL}/responses/${id}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });
  if (!response.ok) {
    const error = await response.json().catch(() => ({}));
    throw new Error(error.detail || 'Failed to update response record.');
  }
  return response.json();
}

export async function deleteResponse(id: number) {
  const res = await apiFetch(`${API_BASE_URL}/responses/${id}`, {
    method: 'DELETE',
  });
  if (!res.ok) throw new Error('Failed to delete response');
  return true;
}

export interface Team {
  id: number;
  name: string;
  description?: string;
}

export interface TeamMember {
  id: number;
  team_id: number;
  user_id: number;
  member_role: 'leader' | 'member';
  user_email: string;
  user_name: string;
  team_name: string;
}

export async function updateTeam(
  teamId: number,
  data: { name: string; description?: string },
): Promise<Team> {
  const response = await apiFetch(`${API_BASE_URL}/assignments/teams/${teamId}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });
  if (!response.ok) {
    const error = await response.json().catch(() => ({}));
    throw new Error(error.detail || 'Failed to update team.');
  }
  return response.json();
}

export async function deleteTeam(teamId: number): Promise<void> {
  const response = await apiFetch(`${API_BASE_URL}/assignments/teams/${teamId}`, {
    method: 'DELETE',
  });
  if (!response.ok) {
    const error = await response.json().catch(() => ({}));
    throw new Error(error.detail || 'Failed to delete team.');
  }
}

export interface AdminSystemStatus {
  status: string;
  database: string;
  whatsapp_webhook_configured: boolean;
  environment: string;
}

export async function getTeamMembers(): Promise<TeamMember[]> {
  const response = await apiFetch(`${API_BASE_URL}/admin/team-memberships`);
  if (!response.ok) throw new Error('Failed to load team membership.');
  return response.json();
}

export async function addTeamMember(
  teamId: number,
  userId: number,
  memberRole: TeamMember['member_role'],
): Promise<TeamMember> {
  const response = await apiFetch(`${API_BASE_URL}/admin/teams/${teamId}/members`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ user_id: userId, member_role: memberRole }),
  });
  if (!response.ok) {
    const error = await response.json().catch(() => ({}));
    throw new Error(error.detail || 'Failed to add team member.');
  }
  return response.json();
}

export async function removeTeamMember(membershipId: number): Promise<void> {
  const response = await apiFetch(`${API_BASE_URL}/admin/team-memberships/${membershipId}`, {
    method: 'DELETE',
  });
  if (!response.ok) {
    const error = await response.json().catch(() => ({}));
    throw new Error(error.detail || 'Failed to remove team member.');
  }
}

export async function updateTeamMemberRole(
  membershipId: number,
  memberRole: TeamMember['member_role'],
): Promise<TeamMember> {
  const response = await apiFetch(`${API_BASE_URL}/admin/team-memberships/${membershipId}`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ member_role: memberRole }),
  });
  if (!response.ok) {
    const error = await response.json().catch(() => ({}));
    throw new Error(error.detail || 'Failed to update team role.');
  }
  return response.json();
}

export interface Assignment {
  id: number;
  reference_code: string;
  response_id: number;
  team_id: number;
  status: string;
  description?: string;
  created_at: string;
}

export interface IntakeSubmission {
  id: number;
  source_channel: 'manual' | 'whatsapp_test' | 'whatsapp';
  source_message_id?: string;
  source_text: string;
  status: 'pending' | 'approved' | 'rejected';
  created_at: string;
  reviewed_at?: string;
  response_id?: number;
}

export interface TimelineEvent {
  id: number;
  response_id: number;
  actor_id?: number;
  event_type: string;
  details?: string;
  timestamp: string;
}

export interface TimelineFeedEvent extends TimelineEvent {
  response_reference: string;
  response_title: string;
  actor_name: string;
}

export interface ReportSummary {
  total_responses: number;
  active_responses: number;
  resolved_responses: number;
  total_assignments: number;
  active_assignments: number;
  completed_assignments: number;
  unassigned_active_responses: number;
  priority_breakdown: Record<string, number>;
  category_breakdown: Record<string, number>;
  source_breakdown: Record<string, number>;
  location_breakdown: Record<string, number>;
  missing_location_responses: number;
  weekly_activity_from: string;
  weekly_activity_to: string;
  weekly_activity: Array<{
    week_start: string;
    responses_created: number;
    assignments_created: number;
  }>;
}

export interface ReportFilters {
  from_date?: string;
  to_date?: string;
  team_id?: number;
}

export type ReportTemplate = 'operational' | 'situation' | 'field';

export interface ReportOptions extends ReportFilters {
  template?: ReportTemplate;
}

export interface ReportPreview {
  generated_at: string;
  template: ReportTemplate;
  filters: {
    from_date: string | null;
    to_date: string | null;
    team_id: number | null;
    team_name: string | null;
  };
  summary: ReportSummary;
  responses: Array<{
    id: number;
    reference_code: string;
    title: string;
    category: string | null;
    priority: string | null;
    source_channel: string;
    status: string;
    location: string | null;
    created_at: string;
  }>;
  assignments: Array<{
    id: number;
    reference_code: string | null;
    response_reference: string;
    response_title: string;
    team_name: string;
    status: string;
    description: string | null;
    created_at: string;
  }>;
}

function reportQuery(filters: ReportOptions): string {
  const params = new URLSearchParams();
  if (filters.from_date) params.set('from_date', filters.from_date);
  if (filters.to_date) params.set('to_date', filters.to_date);
  if (filters.team_id) params.set('team_id', String(filters.team_id));
  if (filters.template) params.set('template', filters.template);
  const query = params.toString();
  return query ? `?${query}` : '';
}

export async function getReportPreview(filters: ReportOptions = {}): Promise<ReportPreview> {
  const response = await apiFetch(`${API_BASE_URL}/reports/preview${reportQuery(filters)}`);
  if (!response.ok) throw new Error('Failed to load report preview.');
  return response.json();
}

export async function createIntake(data: {
  source_channel: 'manual' | 'whatsapp_test';
  source_message_id?: string;
  source_text: string;
}): Promise<IntakeSubmission> {
  const response = await apiFetch(`${API_BASE_URL}/intakes/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });
  if (!response.ok) {
    const error = await response.json().catch(() => ({}));
    throw new Error(error.detail || 'Failed to save intake draft.');
  }
  return response.json();
}

export async function getIntakes(): Promise<IntakeSubmission[]> {
  const response = await apiFetch(`${API_BASE_URL}/intakes/?intake_status=pending`);
  if (!response.ok) throw new Error('Failed to load pending intake drafts.');
  return response.json();
}

export async function approveIntake(
  id: number,
  responseData: ResponseCreatePayload,
  assignment?: { reference_code: string; team_id: number; description?: string },
): Promise<ResponseItem> {
  const response = await apiFetch(`${API_BASE_URL}/intakes/${id}/approve`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ response: responseData, assignment }),
  });
  if (!response.ok) {
    const error = await response.json().catch(() => ({}));
    throw new Error(error.detail || 'Failed to approve intake.');
  }
  return response.json();
}

export async function rejectIntake(id: number): Promise<IntakeSubmission> {
  const response = await apiFetch(`${API_BASE_URL}/intakes/${id}/reject`, { method: 'POST' });
  if (!response.ok) {
    const error = await response.json().catch(() => ({}));
    throw new Error(error.detail || 'Failed to reject intake.');
  }
  return response.json();
}

export async function getTimeline(responseId: number): Promise<TimelineEvent[]> {
  const response = await apiFetch(`${API_BASE_URL}/responses/${responseId}/timeline`);
  if (!response.ok) throw new Error('Failed to load the operational timeline.');
  return response.json();
}

export async function getTimelineFeed(responseId?: number): Promise<TimelineFeedEvent[]> {
  const query = responseId === undefined ? '' : `?response_id=${responseId}`;
  const response = await apiFetch(`${API_BASE_URL}/responses/timeline${query}`);
  if (!response.ok) throw new Error('Failed to load the operational timeline.');
  return response.json();
}

export async function getReportSummary(filters: ReportFilters = {}): Promise<ReportSummary> {
  const response = await apiFetch(`${API_BASE_URL}/reports/summary${reportQuery(filters)}`);
  if (!response.ok) throw new Error('Failed to load report summary.');
  return response.json();
}

export async function downloadWordReport(filters: ReportOptions = {}): Promise<void> {
  const response = await apiFetch(`${API_BASE_URL}/reports/word${reportQuery(filters)}`);
  if (!response.ok) throw new Error('Failed to generate the Word report.');
  const file = await response.blob();
  const url = URL.createObjectURL(file);
  const link = document.createElement('a');
  link.href = url;
  link.download = 'caseloop-report.docx';
  document.body.appendChild(link);
  link.click();
  link.remove();
  window.setTimeout(() => URL.revokeObjectURL(url), 30_000);
}

// Teams
export async function getTeams(): Promise<Team[]> {
  const res = await apiFetch(`${API_BASE_URL}/assignments/teams`);
  if (!res.ok) throw new Error('Failed to fetch teams');
  return res.json();
}

export async function createTeam(data: { name: string; description?: string }): Promise<Team> {
  const res = await apiFetch(`${API_BASE_URL}/assignments/teams`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || 'Failed to create team');
  }
  return res.json();
}

// Assignments
export async function getAssignments(): Promise<Assignment[]> {
  const res = await apiFetch(`${API_BASE_URL}/assignments/`);
  if (!res.ok) throw new Error('Failed to fetch assignments');
  return res.json();
}

export async function createAssignment(data: Omit<Assignment, 'id' | 'created_at'>): Promise<Assignment> {
  const res = await apiFetch(`${API_BASE_URL}/assignments/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || 'Failed to create assignment');
  }
  return res.json();
}

export async function updateDraftAssignment(
  id: number,
  data: Pick<Assignment, 'reference_code' | 'response_id' | 'team_id' | 'description'>,
): Promise<Assignment> {
  const response = await apiFetch(`${API_BASE_URL}/assignments/${id}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });
  if (!response.ok) {
    const error = await response.json().catch(() => ({}));
    throw new Error(error.detail || 'Failed to update draft assignment.');
  }
  return response.json();
}

export async function updateAssignmentStatus(id: number, status: string): Promise<Assignment> {
  const res = await apiFetch(`${API_BASE_URL}/assignments/${id}/status`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ status }),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || 'Failed to update assignment status');
  }
  return res.json();
}

export async function deleteDraftAssignment(id: number): Promise<void> {
  const response = await apiFetch(`${API_BASE_URL}/assignments/${id}`, {
    method: 'DELETE',
  });
  if (!response.ok) {
    const error = await response.json().catch(() => ({}));
    throw new Error(error.detail || 'Failed to delete draft assignment.');
  }
}