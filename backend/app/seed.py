import sys
import os
from dotenv import load_dotenv

# Force loading the root .env file
root_env = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '.env'))
load_dotenv(root_env)
print(f"📁 Loaded environment for seeding from: {root_env}")

from app.core.database import SessionLocal, engine, Base
from app.core.security import hash_password  # <-- Use the exact app security hasher!
from app.models import models

def seed_database():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    try:
        print("🌱 Starting database seeding into fresh Docker PostgreSQL...")

        # 1. Admin/Coordinator User
        admin_email = "chago@redcross.org.ke"
        coordinator = db.query(models.User).filter(models.User.email == admin_email).first()
        
        if not coordinator:
            print(f"Creating default coordinator/admin: {admin_email}")
            coordinator = models.User(
                username="chago",
                email=admin_email,
                full_name="Faith",
                hashed_password=hash_password("chagoKRCklb#2026"),  # <-- Uses exact app hashing
                role="admin",
                is_active=1
            )
            db.add(coordinator)
            db.commit()
            db.refresh(coordinator)

        # 2. Regular User
        user_email = "llybisetga@gmail.com"
        regular_user = db.query(models.User).filter(models.User.email == user_email).first()
        
        if not regular_user:
            print(f"Creating regular user: {user_email}")
            regular_user = models.User(
                username="lsetga",
                email=user_email,
                full_name="Lsetga",
                hashed_password=hash_password("123456789Ten"),  # <-- Uses exact app hashing
                role="user",
                is_active=1
            )
            db.add(regular_user)
            db.commit()

        db.commit()
        print("🎉 Database seeding completed successfully with identical app hashing!")

    except Exception as e:
        db.rollback()
        print(f"❌ Error seeding database: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()