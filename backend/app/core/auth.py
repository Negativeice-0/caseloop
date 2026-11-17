import time
from collections.abc import Callable

from fastapi import Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import hash_session_token
from app.models.models import AuthSession, User

SESSION_COOKIE = "caseloop_session"
CSRF_COOKIE = "caseloop_csrf"
CSRF_HEADER = "X-CSRF-Token"


def get_current_session(
    request: Request, db: Session = Depends(get_db)
) -> AuthSession:
    token = request.cookies.get(SESSION_COOKIE)
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Sign in required."
        )
    session = (
        db.query(AuthSession)
        .filter(
            AuthSession.token_hash == hash_session_token(token),
            AuthSession.revoked_at.is_(None),
            AuthSession.expires_at > int(time.time()),
        )
        .first()
    )
    if not session:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Your session expired. Please sign in again.",
        )
    return session


def get_current_user(
    session: AuthSession = Depends(get_current_session),
    db: Session = Depends(get_db),
) -> User:
    user = db.query(User).filter(User.id == session.user_id).first()
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="This account is unavailable.",
        )
    return user


def require_roles(*roles: str) -> Callable:
    def role_dependency(user: User = Depends(get_current_user)) -> User:
        if user.role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Your account does not have permission for this action.",
            )
        return user

    return role_dependency
