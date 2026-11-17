import enum
from datetime import datetime
from sqlalchemy.sql import func
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship
from ..core.database import Base


class UserRole(str, enum.Enum):
    COORDINATOR = "coordinator"
    RESPONDER = "responder"
    ADMIN = "admin"

class ResponseStatus(str, enum.Enum):
    ACTIVE = "Active"
    RESOLVED = "Resolved"
    PENDING = "Pending"

class AdminToken(Base):
    __tablename__ = "admin_tokens"

    id = Column(Integer, primary_key=True, index=True)
    keyword = Column(String, unique=True, index=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=False)
    is_used = Column(Boolean, default=False)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=True)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default=UserRole.COORDINATOR)
    is_active = Column(Integer, default=1)
    must_change_password = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    responses = relationship("ResponseItem", back_populates="coordinator")
    team_memberships = relationship("TeamMembership", back_populates="user")


class AuthSession(Base):
    __tablename__ = "auth_sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    token_hash = Column(String(64), unique=True, nullable=False, index=True)
    csrf_hash = Column(String(64), nullable=False)
    expires_at = Column(Integer, nullable=False, index=True)
    created_at = Column(Integer, nullable=False)
    revoked_at = Column(Integer, nullable=True)

    user = relationship("User")


class ResponseItem(Base):
    __tablename__ = "responses"

    id = Column(Integer, primary_key=True, index=True)
    reference_code = Column(String, unique=True, index=True, nullable=False)
    title = Column(String, index=True, nullable=False)
    description = Column(Text, nullable=True)
    category = Column(String, nullable=True)
    priority = Column(String, default="normal")
    status = Column(String, default=ResponseStatus.ACTIVE)
    location = Column(String, nullable=True)
    coordinator_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    coordinator = relationship("User", back_populates="responses")
    events = relationship("ResponseEvent", back_populates="response")
    assignments = relationship("Assignment", back_populates="response")


class IntakeSubmission(Base):
    __tablename__ = "intake_submissions"

    id = Column(Integer, primary_key=True, index=True)
    source_channel = Column(String, nullable=False, default="manual")
    source_message_id = Column(String, unique=True, nullable=True, index=True)
    source_text = Column(Text, nullable=False)
    status = Column(String, nullable=False, default="pending")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    reviewed_at = Column(DateTime, nullable=True)
    response_id = Column(Integer, ForeignKey("responses.id"), nullable=True)


class ResponseEvent(Base):
    __tablename__ = "response_events"

    id = Column(Integer, primary_key=True, index=True)
    response_id = Column(Integer, ForeignKey("responses.id"), nullable=False)
    actor_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    event_type = Column(String, nullable=False)
    details = Column(Text, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)

    response = relationship("ResponseItem", back_populates="events")


class Team(Base):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(Text, unique=True, index=True)
    description = Column(Text, nullable=True)

    assignments = relationship("Assignment", back_populates="assigned_team")
    memberships = relationship(
        "TeamMembership", back_populates="team", cascade="all, delete-orphan"
    )


class TeamMembership(Base):
    __tablename__ = "team_memberships"
    __table_args__ = (
        UniqueConstraint("team_id", "user_id", name="uq_team_membership"),
    )

    id = Column(Integer, primary_key=True, index=True)
    team_id = Column(Integer, ForeignKey("teams.id"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    member_role = Column(String, nullable=False, default="member")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    team = relationship("Team", back_populates="memberships")
    user = relationship("User", back_populates="team_memberships")


class Assignment(Base):
    __tablename__ = "assignments"

    id = Column(Integer, primary_key=True, index=True)
    reference_code = Column(Text, unique=True, index=True)
    response_id = Column(Integer, ForeignKey("responses.id"), nullable=False)
    team_id = Column(Integer, ForeignKey("teams.id"), nullable=False)
    
    # Status tracking: Draft, Assigned, Acknowledged, In Progress, Completed
    status = Column(Text, default="Draft")
    description = Column(Text, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    response = relationship("ResponseItem", back_populates="assignments")
    assigned_team = relationship("Team", back_populates="assignments")


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    action = Column(String, nullable=False)
    details = Column(Text, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)