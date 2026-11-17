import os
import secrets
from datetime import datetime, timedelta
from pathlib import Path
import psutil
from sqlalchemy.orm import Session
from app.models.models import AdminToken

class AdminSecretService:
    @staticmethod
    def generate_admin_token(db: Session) -> dict:
        """Generates a secure, single-use, time-sensitive keyword valid for 5 minutes."""
        raw_keyword = f"CR-KL-{secrets.token_hex(3).upper()}"
        expires = datetime.utcnow() + timedelta(minutes=5)
        
        db_token = AdminToken(keyword=raw_keyword, expires_at=expires, is_used=False)
        db.add(db_token)
        db.commit()
        
        return {
            "message": "Dynamic admin keyword generated successfully.",
            "keyword": raw_keyword,
            "expires_in_minutes": 5
        }

    @staticmethod
    def verify_admin_token(db: Session, entered_keyword: str) -> bool:
        """Validates and consumes a dynamic admin keyword."""
        clean_keyword = entered_keyword.strip()
        
        token_record = db.query(AdminToken).filter(
            AdminToken.keyword == clean_keyword,
            AdminToken.is_used == False
        ).first()
        
        if not token_record:
            return False
            
        if datetime.utcnow() > token_record.expires_at:
            return False
            
        # Enforce single-use security policy
        token_record.is_used = True
        db.commit()
        return True