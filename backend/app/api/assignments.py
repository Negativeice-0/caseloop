from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.auth import get_current_user, require_roles
from app.core.database import get_db
from app.models.models import (
    Assignment,
    AuditLog,
    ResponseEvent,
    Team,
    TeamMembership,
    User,
)
from app.schemas.schemas import (
    AssignmentCreate,
    AssignmentDraftUpdate,
    AssignmentUpdate,
    AssignmentResponse,
    TeamCreate,
    TeamResponse,
)
from app.services.assignment_service import (
    create_team_service,
    list_teams_service,
    create_assignment_service,
    update_draft_assignment_service,
    update_assignment_status_service
)

router = APIRouter(
    prefix="/api/assignments",
    tags=["Assignments"],
    dependencies=[Depends(get_current_user)],
)

@router.post("/teams", response_model=TeamResponse, status_code=status.HTTP_201_CREATED)
def create_team(
    team_data: TeamCreate,
    _: User = Depends(require_roles("admin", "coordinator")),
    db: Session = Depends(get_db),
):
    return create_team_service(db, team_data)

@router.get("/teams", response_model=List[TeamResponse])
def list_teams(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if current_user.role == "responder":
        return (
            db.query(Team)
            .join(TeamMembership, TeamMembership.team_id == Team.id)
            .filter(TeamMembership.user_id == current_user.id)
            .order_by(Team.name)
            .all()
        )
    return list_teams_service(db)


@router.put("/teams/{team_id}", response_model=TeamResponse)
def update_team(
    team_id: int,
    team_data: TeamCreate,
    current_user: User = Depends(require_roles("admin", "coordinator")),
    db: Session = Depends(get_db),
):
    team = db.query(Team).filter(Team.id == team_id).first()
    if not team:
        raise HTTPException(status_code=404, detail="Team not found.")
    duplicate = db.query(Team).filter(
        Team.name == team_data.name, Team.id != team_id
    ).first()
    if duplicate:
        raise HTTPException(status_code=409, detail="Team name already exists.")
    team.name = team_data.name
    team.description = team_data.description
    db.add(
        AuditLog(
            user_id=current_user.id,
            action="TEAM_UPDATED",
            details=f"Updated team {team.name}.",
        )
    )
    db.commit()
    db.refresh(team)
    return team


@router.delete("/teams/{team_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_team(
    team_id: int,
    current_user: User = Depends(require_roles("admin")),
    db: Session = Depends(get_db),
):
    team = db.query(Team).filter(Team.id == team_id).first()
    if not team:
        raise HTTPException(status_code=404, detail="Team not found.")
    if team.assignments:
        raise HTTPException(
            status_code=409,
            detail="This team has assignment history and cannot be deleted.",
        )
    db.add(
        AuditLog(
            user_id=current_user.id,
            action="TEAM_DELETED",
            details=f"Deleted team {team.name}.",
        )
    )
    db.delete(team)
    db.commit()

@router.post("", response_model=AssignmentResponse, status_code=status.HTTP_201_CREATED, include_in_schema=False)
@router.post("/", response_model=AssignmentResponse, status_code=status.HTTP_201_CREATED)
def create_assignment(
    data: AssignmentCreate,
    current_user: User = Depends(require_roles("admin", "coordinator")),
    db: Session = Depends(get_db),
):
    return create_assignment_service(db, data, current_user)


@router.put("/{assignment_id}", response_model=AssignmentResponse)
def update_draft_assignment(
    assignment_id: int,
    data: AssignmentDraftUpdate,
    current_user: User = Depends(require_roles("admin", "coordinator")),
    db: Session = Depends(get_db),
):
    return update_draft_assignment_service(db, assignment_id, data, current_user)


@router.get("", response_model=List[AssignmentResponse], include_in_schema=False)
@router.get("/", response_model=List[AssignmentResponse])
def list_assignments(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    query = db.query(Assignment)
    if current_user.role == "responder":
        query = query.join(
            TeamMembership, TeamMembership.team_id == Assignment.team_id
        ).filter(TeamMembership.user_id == current_user.id)
    return query.order_by(Assignment.created_at.desc()).offset(skip).limit(limit).all()

@router.patch("/{assignment_id}/status", response_model=AssignmentResponse)
def update_assignment_status(
    assignment_id: int,
    payload: AssignmentUpdate,
    current_user: User = Depends(require_roles("admin", "coordinator", "responder")),
    db: Session = Depends(get_db),
):
    return update_assignment_status_service(db, assignment_id, payload, current_user)


@router.delete("/{assignment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_draft_assignment(
    assignment_id: int,
    current_user: User = Depends(require_roles("admin")),
    db: Session = Depends(get_db),
):
    assignment = db.query(Assignment).filter(Assignment.id == assignment_id).first()
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found.")
    if assignment.status != "Draft":
        raise HTTPException(
            status_code=409,
            detail="Only a draft assignment can be deleted; preserve the active task history.",
        )
    db.add(
        ResponseEvent(
            response_id=assignment.response_id,
            actor_id=current_user.id,
            event_type="DRAFT_ASSIGNMENT_DELETED",
            details=f"Draft assignment {assignment.reference_code} was removed.",
        )
    )
    db.add(
        AuditLog(
            user_id=current_user.id,
            action="DRAFT_ASSIGNMENT_DELETED",
            details=f"Deleted draft assignment {assignment.reference_code}.",
        )
    )
    db.delete(assignment)
    db.commit()