from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.auth import get_current_user, require_roles
from app.models.models import (
    AuditLog,
    Assignment,
    IntakeSubmission,
    ResponseEvent,
    ResponseItem,
    Team,
    User,
)
from app.schemas.schemas import IntakeApproval, IntakeCreate, IntakeOut, ResponseOut

router = APIRouter(
    prefix="/api/intakes",
    tags=["Intake"],
    dependencies=[Depends(get_current_user)],
)


@router.post("/", response_model=IntakeOut, status_code=status.HTTP_201_CREATED)
def create_intake(
    payload: IntakeCreate,
    _: User = Depends(require_roles("admin", "coordinator")),
    db: Session = Depends(get_db),
):
    if payload.source_channel == "whatsapp":
        raise HTTPException(
            status_code=400,
            detail="WhatsApp-originated drafts are accepted only from the verified webhook.",
        )
    intake = IntakeSubmission(
        source_channel=payload.source_channel,
        source_message_id=payload.source_message_id,
        source_text=payload.source_text.strip(),
    )
    if not intake.source_text:
        raise HTTPException(status_code=422, detail="Source text cannot be blank.")
    db.add(intake)
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="This source message has already been received.",
        ) from exc
    db.refresh(intake)
    return intake


@router.get("/", response_model=list[IntakeOut])
def list_intakes(
    intake_status: str | None = None,
    skip: int = 0,
    limit: int = 100,
    _: User = Depends(require_roles("admin", "coordinator")),
    db: Session = Depends(get_db),
):
    query = db.query(IntakeSubmission)
    if intake_status:
        query = query.filter(IntakeSubmission.status == intake_status)
    return query.order_by(IntakeSubmission.created_at.desc()).offset(skip).limit(limit).all()


@router.post("/{intake_id}/approve", response_model=ResponseOut)
def approve_intake(
    intake_id: int,
    payload: IntakeApproval,
    current_user: User = Depends(require_roles("admin", "coordinator")),
    db: Session = Depends(get_db),
):
    intake = (
        db.query(IntakeSubmission)
        .filter(IntakeSubmission.id == intake_id)
        .with_for_update()
        .first()
    )
    if not intake:
        raise HTTPException(status_code=404, detail="Intake not found.")
    if intake.status != "pending":
        raise HTTPException(status_code=409, detail="Intake has already been reviewed.")

    response_data = payload.response
    existing = (
        db.query(ResponseItem)
        .filter(ResponseItem.reference_code == response_data.reference_code)
        .first()
    )
    if existing:
        raise HTTPException(status_code=409, detail="Response reference already exists.")
    team = None
    if payload.assignment:
        team = (
            db.query(Team)
            .filter(Team.id == payload.assignment.team_id)
            .first()
        )
        if not team:
            raise HTTPException(status_code=404, detail="Assigned team not found.")
        if db.query(Assignment).filter(
            Assignment.reference_code == payload.assignment.reference_code
        ).first():
            raise HTTPException(
                status_code=409, detail="Assignment reference already exists."
            )

    response = ResponseItem(
        reference_code=response_data.reference_code,
        title=response_data.title,
        description=response_data.description,
        category=response_data.category,
        priority=response_data.priority,
        location=response_data.location,
        coordinator_id=current_user.id,
    )
    db.add(response)
    db.flush()
    intake.status = "approved"
    intake.reviewed_at = datetime.utcnow()
    intake.response_id = response.id
    db.add(
        ResponseEvent(
            response_id=response.id,
            actor_id=current_user.id,
            event_type="CREATED_FROM_INTAKE",
            details=f"Coordinator approved intake {intake.id} and created this response.",
        )
    )
    if payload.assignment and team:
        assignment = Assignment(
            reference_code=payload.assignment.reference_code,
            response_id=response.id,
            team_id=team.id,
            status="Assigned",
            description=payload.assignment.description,
        )
        db.add(assignment)
        db.add(
            ResponseEvent(
                response_id=response.id,
                actor_id=current_user.id,
                event_type="ASSIGNMENT_CREATED",
                details=(
                    f"Assignment {assignment.reference_code} created for "
                    f"team {team.name} from intake {intake.id}."
                ),
            )
        )
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="The response or assignment reference already exists.",
        ) from exc
    db.refresh(response)
    return response


@router.post("/{intake_id}/reject", response_model=IntakeOut)
def reject_intake(
    intake_id: int,
    current_user: User = Depends(require_roles("admin", "coordinator")),
    db: Session = Depends(get_db),
):
    intake = db.query(IntakeSubmission).filter(IntakeSubmission.id == intake_id).first()
    if not intake:
        raise HTTPException(status_code=404, detail="Intake not found.")
    if intake.status != "pending":
        raise HTTPException(status_code=409, detail="Intake has already been reviewed.")
    intake.status = "rejected"
    intake.reviewed_at = datetime.utcnow()
    db.add(
        AuditLog(
            user_id=current_user.id,
            action="INTAKE_REJECTED",
            details=f"Rejected intake {intake.id}.",
        )
    )
    db.commit()
    db.refresh(intake)
    return intake
