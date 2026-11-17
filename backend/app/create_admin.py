import getpass
import re
import sys

from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.core.security import hash_password
from app.db_bootstrap import initialize_database
from app.models.models import User


def main() -> None:
    initialize_database()
    email = input("Administrator email: ").strip().lower()
    full_name = input("Administrator name: ").strip()
    password = getpass.getpass("Password (12+ characters): ")
    confirmation = getpass.getpass("Confirm password: ")

    if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
        sys.exit("Enter a valid email address.")
    if not full_name:
        sys.exit("Name cannot be blank.")
    if len(password) < 12:
        sys.exit("Use a password of at least 12 characters.")
    if password != confirmation:
        sys.exit("Passwords do not match.")

    db: Session = SessionLocal()
    try:
        existing = db.query(User).filter(User.email == email).first()
        if existing:
            existing.username = email
            existing.full_name = full_name
            existing.role = "admin"
            existing.hashed_password = hash_password(password)
            existing.must_change_password = False
            existing.is_active = 1
            admin = existing
        else:
            admin = User(
                username=email,
                email=email,
                full_name=full_name,
                role="admin",
                hashed_password=hash_password(password),
                must_change_password=False,
                is_active=1,
            )
            db.add(admin)
        db.commit()
        print(f"Administrator account created for {email}.")
    finally:
        db.close()


if __name__ == "__main__":
    main()
