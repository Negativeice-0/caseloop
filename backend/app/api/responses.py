# ----------------------------------------------------
# Copyright (c) 2026 Billy Gates Ochieng Osodo. All Rights Reserved.
# CaseLoop Humanitarian Coordination System - Responses API
# ----------------------------------------------------

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.core.auth import get_current_user, require_roles
from app.models import models
from app.schemas import schemas

router = APIRouter(
    prefix="/api/responses",
    tags=["Responses"],
    dependencies=[Depends(get_current_user)],
)

@router.post("/", response_model=schemas.ResponseOut, status_code=status.HTTP_201_CREATED)
def create_response(
    response_in: schemas.ResponseCreate,
    current_user: models.User = Depends(require_roles("admin", "coordinator")),
    db: Session = Depends(get_db),
):
    existing = db.query(models.ResponseItem).filter(models.ResponseItem.reference_code == response_in.reference_code).first()
    if existing:
        raise HTTPException(status_code=400, detail="Response with this reference code already exists.")
    
    try:
        db_response = models.ResponseItem(
            reference_code=response_in.reference_code,
            title=response_in.title,
            description=response_in.description,
            category=response_in.category,
            priority=response_in.priority,
            location=response_in.location,
            coordinator_id=current_user.id,
            status=models.ResponseStatus.ACTIVE
        )
        db.add(db_response)
        db.commit()
        db.refresh(db_response)

        # Record creation event in operational timeline
        event = models.ResponseEvent(
            response_id=db_response.id,
            actor_id=current_user.id,
            event_type="CREATED",
            details=f"Response record created with title: {db_response.title}"
        )
        db.add(event)
        db.commit()
        return db_response
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database transaction failed: {str(e)}")

@router.get("/", response_model=List[schemas.ResponseOut])
def list_responses(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.ResponseItem).offset(skip).limit(limit).all()


@router.get("/timeline", response_model=List[schemas.TimelineFeedOut])
def get_timeline_feed(
    response_id: int | None = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    query = (
        db.query(models.ResponseEvent, models.ResponseItem, models.User)
        .join(models.ResponseItem, models.ResponseItem.id == models.ResponseEvent.response_id)
        .outerjoin(models.User, models.User.id == models.ResponseEvent.actor_id)
    )
    if response_id is not None:
        query = query.filter(models.ResponseEvent.response_id == response_id)
    rows = (
        query.order_by(
            models.ResponseEvent.timestamp.desc(),
            models.ResponseEvent.id.desc(),
        )
        .offset(max(skip, 0))
        .limit(min(max(limit, 1), 200))
        .all()
    )
    return [
        schemas.TimelineFeedOut(
            id=event.id,
            response_id=response.id,
            response_reference=response.reference_code,
            response_title=response.title,
            actor_id=event.actor_id,
            actor_name=(user.full_name or user.email) if user else "System",
            event_type=event.event_type,
            details=event.details,
            timestamp=event.timestamp,
        )
        for event, response, user in rows
    ]


@router.get("/{response_id}", response_model=schemas.ResponseOut)
def get_response(response_id: int, db: Session = Depends(get_db)):
    response = db.query(models.ResponseItem).filter(models.ResponseItem.id == response_id).first()
    if not response:
        raise HTTPException(status_code=404, detail="Response not found.")
    return response

@router.put("/{response_id}", response_model=schemas.ResponseOut)
def update_response(
    response_id: int,
    response_in: schemas.ResponseCreate,
    current_user: models.User = Depends(require_roles("admin", "coordinator")),
    db: Session = Depends(get_db),
):
    db_response = db.query(models.ResponseItem).filter(models.ResponseItem.id == response_id).first()
    if not db_response:
        raise HTTPException(status_code=404, detail="Response not found.")
    
    try:
        db_response.reference_code = response_in.reference_code
        db_response.title = response_in.title
        db_response.description = response_in.description
        db_response.category = response_in.category
        db_response.priority = response_in.priority
        db_response.location = response_in.location

        db.commit()
        db.refresh(db_response)

        event = models.ResponseEvent(
            response_id=db_response.id,
            actor_id=current_user.id,
            event_type="UPDATED",
            details=f"Response record updated: {db_response.title}"
        )
        db.add(event)
        db.commit()
        return db_response
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database update failed: {str(e)}")

@router.delete("/{response_id}")
def delete_response(
    response_id: int,
    current_user: models.User = Depends(require_roles("admin")),
    db: Session = Depends(get_db),
):
    db_item = db.query(models.ResponseItem).filter(models.ResponseItem.id == response_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Response record not found")
    if db_item.assignments:
        raise HTTPException(
            status_code=409,
            detail="This response has assignments. Complete or remove them before deleting it.",
        )
    if (
        db.query(models.IntakeSubmission)
        .filter(models.IntakeSubmission.response_id == response_id)
        .first()
    ):
        raise HTTPException(
            status_code=409,
            detail="This response is linked to an intake record and cannot be deleted.",
        )
    
    try:
        # CASCADING DELETION FIX: Delete all related child ResponseEvent records first
        db.query(models.ResponseEvent).filter(models.ResponseEvent.response_id == response_id).delete()
        
        # Now delete parent ResponseItem safely
        db.add(
            models.AuditLog(
                user_id=current_user.id,
                action="RESPONSE_DELETED",
                details=f"Deleted response {db_item.reference_code}.",
            )
        )
        db.delete(db_item)
        db.commit()
        return {"status": "success", "message": "Record and associated events deleted successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to delete response record: {str(e)}")

@router.get("/{response_id}/timeline", response_model=List[schemas.EventOut])
def get_response_timeline(response_id: int, skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    return db.query(models.ResponseEvent)\
        .filter(models.ResponseEvent.response_id == response_id)\
        .order_by(models.ResponseEvent.timestamp.desc())\
        .offset(skip)\
        .limit(limit)\
        .all()