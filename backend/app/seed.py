import sys
import os
from dotenv import load_dotenv

# 1. Force loading the root .env file so it targets Docker PostgreSQL
root_env = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '.env'))
load_dotenv(root_env)
print(f"📁 Loaded environment for seeding from: {root_env}")

from passlib.context import CryptContext
from app.core.database import SessionLocal, engine, Base
from app.models import models

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def seed_database():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    try:
        print("🌱 Starting database seeding into Docker PostgreSQL...")

        # 1. Ensure Default Admin/Coordinator Exists (Faith)
        admin_email = "chago@redcross.org.ke"
        coordinator = db.query(models.User).filter(models.User.email == admin_email).first()
        
        if not coordinator:
            print(f"Creating default coordinator/admin: {admin_email}")
            coordinator = models.User(
                email=admin_email,
                full_name="Faith",
                hashed_password=get_password_hash("chagoKRCklb#2026"),
                role="admin",
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

        db.commit()
        print("🎉 Database seeding completed successfully into PostgreSQL!")

    except Exception as e:
        db.rollback()
        print(f"❌ Error seeding database: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()