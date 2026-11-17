import os
from passlib.context import CryptContext
from app.core.database import SessionLocal, engine, Base
from app.models import models

# Password hashing setup (matches standard FastAPI security patterns)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def seed_database():
    # Ensure all tables exist
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    try:
        print("🌱 Starting database seeding...")

        # 1. Ensure Default Admin/Coordinator Exists (Faith)
        admin_email = "chago@redcross.org.ke"
        coordinator = db.query(models.User).filter(models.User.email == admin_email).first()
        
        if not coordinator:
            print(f"Creating default coordinator/admin: {admin_email}")
            coordinator = models.User(
                email=admin_email,
                name="Faith",
                hashed_password=get_password_hash("chagoKRCklb#2026"),
                role="admin",  # or "coordinator" depending on your model choices
                is_active=1
            )
            db.add(coordinator)
            db.commit()
            db.refresh(coordinator)
        else:
            print(f"Coordinator already exists: {admin_email}")

        # 2. Ensure Regular User Exists (Lsetga)
        user_email = "llybisetga@gmail.com"
        regular_user = db.query(models.User).filter(models.User.email == user_email).first()
        
        if not regular_user:
            print(f"Creating regular user: {user_email}")
            regular_user = models.User(
                email=user_email,
                name="Lsetga",
                hashed_password=get_password_hash("123456789Ten"),
                role="user",
                is_active=1
            )
            db.add(regular_user)
            db.commit()
        else:
            print(f"Regular user already exists: {user_email}")

        # 3. Seed Synthetic CaseLoop Demo Responses
        print("Seeding synthetic CaseLoop demo responses...")
        responses_data = [
            {
                "reference_code": "CR-KL-2026-001",
                "title": "Karen Community Health & Hygiene Camp",
                "description": "Providing basic health screening, hygiene kits, and community sensitization.",
                "category": "Community assistance",
                "priority": "normal",
                "location": "Karen Sub-County Hall",
                "coordinator_id": coordinator.id,
            },
            {
                "reference_code": "CR-KL-2026-002",
                "title": "Lang'ata Flash Flood Assessment & Relief",
                "description": "Assessing affected households following heavy seasonal downpours and distributing emergency blankets.",
                "category": "Disaster response",
                "priority": "urgent",
                "location": "Lang'ata Ward 6",
                "coordinator_id": coordinator.id,
            },
            {
                "reference_code": "CR-KL-2026-003",
                "title": "First Aid Preparedness Training Exercise",
                "description": "Training volunteer response teams on rapid triage and basic life support protocols.",
                "category": "Preparedness activity",
                "priority": "high",
                "location": "Branch Training Grounds",
                "coordinator_id": coordinator.id,
            },
        ]

        for response_data in responses_data:
            exists = (
                db.query(models.ResponseItem)
                .filter(models.ResponseItem.reference_code == response_data["reference_code"])
                .first()
            )
            if exists:
                continue
            response = models.ResponseItem(**response_data)
            db.add(response)
            db.flush()
            db.add(
                models.ResponseEvent(
                    response_id=response.id,
                    actor_id=coordinator.id,
                    event_type="CREATED",
                    details=f"Initialized synthetic response: {response.title}",
                )
            )
        db.commit()
        print("🎉 Database seeding completed successfully!")

    except Exception as e:
        db.rollback()
        print(f"❌ Error seeding database: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()