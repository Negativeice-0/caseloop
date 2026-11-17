import re
import secrets
import time

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.auth import require_roles
from app.core.config import settings
from app.core.database import engine, get_db
from app.core.security import hash_password
from app.models.models import (
    AuditLog,
    AuthSession,
    Team,
    TeamMembership,
    User,
)
from app.schemas.schemas import (
    AdminUserCreate,
    AdminUserUpdate,
    TeamMemberCreate,
    TeamMemberOut,
    TeamMemberUpdate,
    UserOut,
    UserStatusUpdate,
)

router = APIRouter(
    prefix="/api/admin",
    tags=["Administration"],
    dependencies=[Depends(require_roles("admin"))],
)


def _record_admin_action(db: Session, user_id: int, action: str, details: str) -> None:
    db.add(AuditLog(user_id=user_id, action=action, details=details))


def _valid_email(value: str) -> bool:
    return bool(re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", value))


@router.get("/system-status")
def get_system_status():
    return {
        "status": "online",
        "database": engine.dialect.name,
        "whatsapp_webhook_configured": bool(
            settings.WHATSAPP_VERIFY_TOKEN and settings.WHATSAPP_APP_SECRET
        ),
        "environment": settings.APP_ENV,
    }


@router.get("/audit")
def list_recent_audit_events(limit: int = 50, db: Session = Depends(get_db)):
    limit = min(max(limit, 1), 200)
    rows = (
        db.query(AuditLog, User)
        .outerjoin(User, User.id == AuditLog.user_id)
        .order_by(AuditLog.timestamp.desc())
        .limit(limit)
        .all()
    )
    return [
        {
            "id": event.id,
            "action": event.action,
            "details": event.details,
            "timestamp": event.timestamp,
            "actor": user.email if user else "System",
        }
        for event, user in rows
    ]


@router.get("/users", response_model=list[UserOut])
def list_users(db: Session = Depends(get_db)):
    return db.query(User).order_by(User.created_at.desc()).all()


@router.post("/users", status_code=status.HTTP_201_CREATED)
def create_user(
    payload: AdminUserCreate,
    admin: User = Depends(require_roles("admin")),
    db: Session = Depends(get_db),
):
    email = payload.email.strip().lower()
    full_name = payload.full_name.strip()
    if not _valid_email(email):
        raise HTTPException(status_code=422, detail="Enter a valid email address.")
    if not full_name:
        raise HTTPException(status_code=422, detail="Name cannot be blank.")
    if db.query(User).filter(User.email == email).first():
        raise HTTPException(status_code=409, detail="That email address already exists.")

    initial_password = secrets.token_urlsafe(18)
    user = User(
        username=email,
        email=email,
        full_name=full_name,
        role=payload.role,
        hashed_password=hash_password(initial_password),
        must_change_password=True,
        is_active=1,
    )
    db.add(user)
    _record_admin_action(
        db, admin.id, "USER_CREATED", f"Created {payload.role} account {email}."
    )
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(
            status_code=409, detail="That email address already exists."
        ) from exc
    db.refresh(user)
    return {
        "user": UserOut.model_validate(user),
        "initial_password": initial_password,
        "show_password_once": True,
    }


@router.patch("/users/{user_id}/status", response_model=UserOut)
def update_user_status(
    user_id: int,
    payload: UserStatusUpdate,
    admin: User = Depends(require_roles("admin")),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    if user.id == admin.id and not payload.is_active:
        raise HTTPException(status_code=400, detail="You cannot deactivate your own account.")
    if user.role == "admin" and user.is_active and not payload.is_active:
        other_admins = db.query(User).filter(
            User.role == "admin", User.is_active == 1, User.id != user.id
        ).count()
        if other_admins == 0:
            raise HTTPException(
                status_code=400, detail="Create another administrator before deactivating this account."
            )
    user.is_active = int(payload.is_active)
    if not payload.is_active:
        db.query(AuthSession).filter(
            AuthSession.user_id == user.id,
            AuthSession.revoked_at.is_(None),
        ).update({AuthSession.revoked_at: int(time.time())})
    _record_admin_action(
        db,
        admin.id,
        "USER_STATUS_UPDATED",
        f"Set {user.email} active={payload.is_active}.",
    )
    db.commit()
    db.refresh(user)
    return user


@router.patch("/users/{user_id}", response_model=UserOut)
def update_user(
    user_id: int,
    payload: AdminUserUpdate,
    admin: User = Depends(require_roles("admin")),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    if user.id == admin.id and payload.role != "admin":
        raise HTTPException(status_code=400, detail="You cannot remove your own administrator role.")
    if user.role == "admin" and user.is_active and payload.role != "admin":
        other_admins = db.query(User).filter(
            User.role == "admin", User.is_active == 1, User.id != user.id
        ).count()
        if other_admins == 0:
            raise HTTPException(
                status_code=400,
                detail="Create another administrator before changing this role.",
            )
    user.full_name = payload.full_name.strip()
    user.role = payload.role
    _record_admin_action(
        db,
        admin.id,
        "USER_UPDATED",
        f"Updated {user.email} to role {user.role}.",
    )
    db.commit()
    db.refresh(user)
    return user


@router.post("/users/{user_id}/reset-password")
def reset_user_password(
    user_id: int,
    admin: User = Depends(require_roles("admin")),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    if user.id == admin.id:
        raise HTTPException(
            status_code=400, detail="Use your account profile to change your own password."
        )
    initial_password = secrets.token_urlsafe(18)
    user.hashed_password = hash_password(initial_password)
    user.must_change_password = True
    db.query(AuthSession).filter(
        AuthSession.user_id == user.id,
        AuthSession.revoked_at.is_(None),
    ).update({AuthSession.revoked_at: int(time.time())})
    _record_admin_action(
        db, admin.id, "USER_PASSWORD_RESET", f"Reset password for {user.email}."
    )
    db.commit()
    return {"initial_password": initial_password, "show_password_once": True}


@router.get("/team-memberships", response_model=list[TeamMemberOut])
def list_team_memberships(db: Session = Depends(get_db)):
    rows = (
        db.query(TeamMembership, Team, User)
        .join(Team, Team.id == TeamMembership.team_id)
        .join(User, User.id == TeamMembership.user_id)
        .order_by(Team.name, User.full_name)
        .all()
    )
    return [
        TeamMemberOut(
            id=membership.id,
            team_id=team.id,
            user_id=user.id,
            member_role=membership.member_role,
            user_email=user.email,
            user_name=user.full_name or user.email,
            team_name=team.name,
        )
        for membership, team, user in rows
    ]


@router.post(
    "/teams/{team_id}/members",
    response_model=TeamMemberOut,
    status_code=status.HTTP_201_CREATED,
)
def add_team_member(
    team_id: int,
    payload: TeamMemberCreate,
    admin: User = Depends(require_roles("admin")),
    db: Session = Depends(get_db),
):
    team = db.query(Team).filter(Team.id == team_id).first()
    user = db.query(User).filter(User.id == payload.user_id).first()
    if not team or not user:
        raise HTTPException(status_code=404, detail="Team or user not found.")
    if not user.is_active:
        raise HTTPException(status_code=400, detail="An inactive user cannot join a team.")
    if db.query(TeamMembership).filter(
        TeamMembership.team_id == team_id,
        TeamMembership.user_id == user.id,
    ).first():
        raise HTTPException(status_code=409, detail="This user is already on that team.")
    membership = TeamMembership(
        team_id=team_id, user_id=user.id, member_role=payload.member_role
    )
    db.add(membership)
    _record_admin_action(
        db,
        admin.id,
        "TEAM_MEMBER_ADDED",
        f"Added {user.email} to {team.name} as {payload.member_role}.",
    )
    db.commit()
    db.refresh(membership)
    return TeamMemberOut(
        id=membership.id,
        team_id=team.id,
        user_id=user.id,
        member_role=membership.member_role,
        user_email=user.email,
        user_name=user.full_name or user.email,
        team_name=team.name,
    )


@router.delete("/team-memberships/{membership_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_team_member(
    membership_id: int,
    admin: User = Depends(require_roles("admin")),
    db: Session = Depends(get_db),
):
    membership = (
        db.query(TeamMembership).filter(TeamMembership.id == membership_id).first()
    )
    if not membership:
        raise HTTPException(status_code=404, detail="Team membership not found.")
    team = db.query(Team).filter(Team.id == membership.team_id).first()
    user = db.query(User).filter(User.id == membership.user_id).first()
    _record_admin_action(
        db,
        admin.id,
        "TEAM_MEMBER_REMOVED",
        f"Removed {user.email if user else membership.user_id} from "
        f"{team.name if team else membership.team_id}.",
    )
    db.delete(membership)
    db.commit()


@router.patch("/team-memberships/{membership_id}", response_model=TeamMemberOut)
def update_team_member_role(
    membership_id: int,
    payload: TeamMemberUpdate,
    admin: User = Depends(require_roles("admin")),
    db: Session = Depends(get_db),
):
    membership = (
        db.query(TeamMembership).filter(TeamMembership.id == membership_id).first()
    )
    if not membership:
        raise HTTPException(status_code=404, detail="Team membership not found.")
    membership.member_role = payload.member_role
    team = db.query(Team).filter(Team.id == membership.team_id).first()
    user = db.query(User).filter(User.id == membership.user_id).first()
    _record_admin_action(
        db,
        admin.id,
        "TEAM_MEMBER_ROLE_UPDATED",
        f"Set {user.email if user else membership.user_id} as {membership.member_role} "
        f"for {team.name if team else membership.team_id}.",
    )
    db.commit()
    db.refresh(membership)
    return TeamMemberOut(
        id=membership.id,
        team_id=membership.team_id,
        user_id=membership.user_id,
        member_role=membership.member_role,
        user_email=user.email if user else "",
        user_name=(user.full_name or user.email) if user else "",
        team_name=team.name if team else "",
    )
