from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.models import (
    Assignment,
    ResponseEvent,
    ResponseItem,
    Team,
    TeamMembership,
    User,
)
from app.schemas.schemas import (
    AssignmentCreate,
    AssignmentDraftUpdate,
    AssignmentUpdate,
    TeamCreate,
)

def create_team_service(db: Session, team_data: TeamCreate):
    existing = db.query(Team).filter(Team.name == team_data.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Team name already exists.")
    
    new_team = Team(**team_data.model_dump())
    db.add(new_team)
    db.commit()
    db.refresh(new_team)
    return new_team

def list_teams_service(db: Session):
    return db.query(Team).all()

def create_assignment_service(db: Session, data: AssignmentCreate, actor: User):
    resp = db.query(ResponseItem).filter(ResponseItem.id == data.response_id).first()
    if not resp:
        raise HTTPException(status_code=404, detail="Parent response record not found.")
    
    team = db.query(Team).filter(Team.id == data.team_id).first()
    if not team:
        raise HTTPException(status_code=404, detail="Assigned team not found.")

    new_assignment = Assignment(**data.model_dump())
    db.add(new_assignment)
    db.flush()
    db.add(
        ResponseEvent(
            response_id=resp.id,
            actor_id=actor.id,
            event_type="ASSIGNMENT_CREATED",
            details=f"Assignment {new_assignment.reference_code} created for team {team.name}.",
        )
    )
    db.commit()
    db.refresh(new_assignment)
    return new_assignment


def update_draft_assignment_service(
    db: Session,
    assignment_id: int,
    data: AssignmentDraftUpdate,
    actor: User,
):
    assignment = db.query(Assignment).filter(Assignment.id == assignment_id).first()
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found.")
    if assignment.status != "Draft":
        raise HTTPException(
            status_code=409,
            detail="Only a draft assignment can be edited; preserve the active task history.",
        )

    duplicate = (
        db.query(Assignment)
        .filter(
            Assignment.reference_code == data.reference_code,
            Assignment.id != assignment_id,
        )
        .first()
    )
    if duplicate:
        raise HTTPException(status_code=409, detail="Assignment reference already exists.")

    response = db.query(ResponseItem).filter(ResponseItem.id == data.response_id).first()
    if not response:
        raise HTTPException(status_code=404, detail="Parent response record not found.")
    team = db.query(Team).filter(Team.id == data.team_id).first()
    if not team:
        raise HTTPException(status_code=404, detail="Assigned team not found.")

    previous_reference = assignment.reference_code
    previous_response_id = assignment.response_id
    changed = (
        assignment.reference_code != data.reference_code
        or assignment.response_id != data.response_id
        or assignment.team_id != data.team_id
        or assignment.description != data.description
    )
    if not changed:
        return assignment

    assignment.reference_code = data.reference_code
    assignment.response_id = data.response_id
    assignment.team_id = data.team_id
    assignment.description = data.description
    if previous_response_id != response.id:
        db.add(
            ResponseEvent(
                response_id=previous_response_id,
                actor_id=actor.id,
                event_type="DRAFT_ASSIGNMENT_UPDATED",
                details=f"Draft assignment {previous_reference} was moved to another response.",
            )
        )
    db.add(
        ResponseEvent(
            response_id=response.id,
            actor_id=actor.id,
            event_type="DRAFT_ASSIGNMENT_UPDATED",
            details=f"Draft assignment {previous_reference} was updated.",
        )
    )
    db.commit()
    db.refresh(assignment)
    return assignment


def list_assignments_service(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Assignment).offset(skip).limit(limit).all()

def update_assignment_status_service(
    db: Session,
    assignment_id: int,
    payload: AssignmentUpdate,
    current_user: User,
):
    assignment = db.query(Assignment).filter(Assignment.id == assignment_id).first()
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found.")
    if current_user.role == "responder":
        is_member = (
            db.query(TeamMembership)
            .filter(
                TeamMembership.team_id == assignment.team_id,
                TeamMembership.user_id == current_user.id,
            )
            .first()
        )
        if not is_member:
            raise HTTPException(
                status_code=403,
                detail="Responders can only update assignments for their team.",
            )
        if assignment.status == "Draft":
            raise HTTPException(
                status_code=403,
                detail="A coordinator must assign this task before a responder can acknowledge it.",
            )
        if payload.description is not None:
            raise HTTPException(
                status_code=403,
                detail="Responders may update task status, not assignment details.",
            )
    
    previous_status = assignment.status
    valid_transitions = {
        "Draft": "Assigned",
        "Assigned": "Acknowledged",
        "Acknowledged": "In Progress",
        "In Progress": "Completed",
    }
    if payload.status:
        expected_status = valid_transitions.get(previous_status)
        if payload.status != expected_status:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid status transition from {previous_status}.",
            )
        assignment.status = payload.status
    if payload.description:
        assignment.description = payload.description
        
    if payload.status:
        db.add(
            ResponseEvent(
                response_id=assignment.response_id,
                actor_id=current_user.id,
                event_type="ASSIGNMENT_STATUS_UPDATED",
                details=(
                    f"Assignment {assignment.reference_code} moved from "
                    f"{previous_status} to {assignment.status}."
                ),
            )
        )
    db.commit()
    db.refresh(assignment)
    return assignment