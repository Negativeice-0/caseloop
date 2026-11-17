from sqlalchemy.orm import Session
from app.models import models
from app.schemas import schemas
from fastapi import HTTPException

def create_response_record(db: Session, response_in: schemas.ResponseCreate, coordinator_id: int = 1):
    existing = db.query(models.ResponseItem).filter(models.ResponseItem.reference_code == response_in.reference_code).first()
    if existing:
        raise HTTPException(status_code=400, detail="Response with this reference code already exists.")
    
    db_response = models.ResponseItem(
        reference_code=response_in.reference_code,
        title=response_in.title,
        description=response_in.description,
        category=response_in.category,
        priority=response_in.priority,
        location=response_in.location,
        coordinator_id=coordinator_id,
        status=models.ResponseStatus.ACTIVE
    )
    db.add(db_response)
    db.commit()
    db.refresh(db_response)

    event = models.ResponseEvent(
        response_id=db_response.id,
        actor_id=coordinator_id,
        event_type="CREATED",
        details=f"Response record created with title: {db_response.title}"
    )
    db.add(event)
    db.commit()
    return db_response

def get_all_responses(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.ResponseItem).offset(skip).limit(limit).all()