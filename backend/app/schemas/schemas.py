# backend/app/schemas/schemas.py
from datetime import date, datetime
from typing import Optional, List, Literal
from pydantic import BaseModel, Field
from typing import Literal

# --- USER SCHEMAS ---
class UserBase(BaseModel):
    email: str
    full_name: Optional[str] = None
    role: str = "responder"

class UserOut(UserBase):
    id: int
    is_active: int
    must_change_password: bool
    created_at: datetime

    class Config:
        from_attributes = True


class AdminUserCreate(BaseModel):
    email: str = Field(min_length=5, max_length=254)
    full_name: str = Field(min_length=1, max_length=200)
    role: Literal["admin", "coordinator", "responder"]


class AdminUserUpdate(BaseModel):
    full_name: str = Field(min_length=1, max_length=200)
    role: Literal["admin", "coordinator", "responder"]


class UserSessionOut(BaseModel):
    user: UserOut
    csrf_token: str


class AuthCredentials(BaseModel):
    email: str = Field(min_length=5, max_length=254)
    password: str = Field(min_length=1, max_length=128)
    audience: Literal["workspace", "admin"] = "workspace"


class PublicRegistration(BaseModel):
    model_config = {"extra": "forbid"}

    email: str = Field(min_length=5, max_length=254)
    full_name: str = Field(min_length=1, max_length=200)
    password: str = Field(min_length=12, max_length=128)


class PasswordChange(BaseModel):
    current_password: str = Field(min_length=1, max_length=128)
    new_password: str = Field(min_length=12, max_length=128)


class UserStatusUpdate(BaseModel):
    is_active: bool

# --- RESPONSE SCHEMAS ---
class ResponseCreate(BaseModel):
    reference_code: str
    title: str
    description: Optional[str] = None
    category: Optional[str] = None
    priority: Optional[str] = "normal"
    location: Optional[str] = None
    coordinator_id: Optional[int] = None

class ResponseOut(ResponseCreate):
    id: int
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# =============================================================================
# === NEW FOR CHECKPOINT 5: TEAM SCHEMAS ===
# =============================================================================
class TeamBase(BaseModel):
    name: str
    description: Optional[str] = None

class TeamCreate(TeamBase):
    pass

class TeamResponse(TeamBase):
    id: int

    class Config:
        from_attributes = True


class TeamMemberCreate(BaseModel):
    user_id: int
    member_role: Literal["leader", "member"] = "member"


class TeamMemberUpdate(BaseModel):
    member_role: Literal["leader", "member"]


class TeamMemberOut(BaseModel):
    id: int
    team_id: int
    user_id: int
    member_role: str
    user_email: str
    user_name: str
    team_name: str

# =============================================================================
# === NEW FOR CHECKPOINT 5: ASSIGNMENT SCHEMAS ===
# Supports status tracking: Draft, Assigned, Acknowledged, In Progress, Completed
# =============================================================================
class AssignmentCreate(BaseModel):
    reference_code: str
    response_id: int
    team_id: int
    status: Literal["Draft"] = "Draft"
    description: Optional[str] = None


class AssignmentDraftUpdate(BaseModel):
    reference_code: str = Field(min_length=1, max_length=100)
    response_id: int
    team_id: int
    description: Optional[str] = Field(default=None, max_length=2000)


class AssignmentUpdate(BaseModel):
    status: Optional[str] = None
    description: Optional[str] = None

class AssignmentResponse(BaseModel):
    id: int
    reference_code: str
    response_id: int
    team_id: int
    status: str
    description: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# --- TIMELINE EVENT SCHEMAS ---
class EventOut(BaseModel):
    id: int
    response_id: int
    actor_id: Optional[int] = None
    event_type: str
    details: Optional[str] = None
    timestamp: datetime

    class Config:
        from_attributes = True


class TimelineFeedOut(BaseModel):
    id: int
    response_id: int
    response_reference: str
    response_title: str
    actor_id: Optional[int] = None
    actor_name: str
    event_type: str
    details: Optional[str] = None
    timestamp: datetime


class IntakeCreate(BaseModel):
    source_channel: Literal["manual", "whatsapp_test", "whatsapp"] = "manual"
    source_message_id: Optional[str] = Field(default=None, max_length=255)
    source_text: str = Field(min_length=1, max_length=10000)


class IntakeOut(BaseModel):
    id: int
    source_channel: str
    source_message_id: Optional[str]
    source_text: str
    status: str
    created_at: datetime
    reviewed_at: Optional[datetime]
    response_id: Optional[int]

    class Config:
        from_attributes = True


class IntakeAssignment(BaseModel):
    reference_code: str = Field(min_length=1, max_length=100)
    team_id: int
    description: Optional[str] = Field(default=None, max_length=2000)


class IntakeApproval(BaseModel):
    response: ResponseCreate
    assignment: Optional[IntakeAssignment] = None


class ReportWeek(BaseModel):
    week_start: date
    responses_created: int
    assignments_created: int


class ReportSummary(BaseModel):
    total_responses: int
    active_responses: int
    resolved_responses: int
    total_assignments: int
    active_assignments: int
    completed_assignments: int
    unassigned_active_responses: int
    priority_breakdown: dict[str, int]
    category_breakdown: dict[str, int]
    source_breakdown: dict[str, int]
    location_breakdown: dict[str, int]
    missing_location_responses: int
    weekly_activity_from: date
    weekly_activity_to: date
    weekly_activity: list[ReportWeek]


class ReportFilters(BaseModel):
    from_date: Optional[date]
    to_date: Optional[date]
    team_id: Optional[int]
    team_name: Optional[str]


class ReportPreviewResponse(BaseModel):
    id: int
    reference_code: str
    title: str
    category: Optional[str]
    priority: Optional[str]
    source_channel: str
    status: str
    location: Optional[str]
    created_at: datetime


class ReportPreviewAssignment(BaseModel):
    id: int
    reference_code: Optional[str]
    response_reference: str
    response_title: str
    team_name: str
    status: str
    description: Optional[str]
    created_at: datetime


class ReportPreview(BaseModel):
    generated_at: datetime
    template: Literal["operational", "situation", "field"]
    filters: ReportFilters
    summary: ReportSummary
    responses: list[ReportPreviewResponse]
    assignments: list[ReportPreviewAssignment]