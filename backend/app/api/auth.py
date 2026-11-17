import re
import time

from fastapi import APIRouter, Depends, HTTPException, Request, Response
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.auth import (
    CSRF_COOKIE,
    SESSION_COOKIE,
    get_current_session,
    get_current_user,
)
from app.core.config import settings
from app.core.database import get_db
from app.core.security import hash_password, hash_session_token, new_session_secret, verify_password
from app.models.models import AuditLog, AuthSession, User, UserRole
from app.schemas.schemas import (
    AuthCredentials,
    PasswordChange,
    PublicRegistration,
    UserOut,
    UserSessionOut,
)

router = APIRouter(prefix="/api/auth", tags=["Authentication"])


def valid_email(email: str) -> bool:
    return bool(re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email))


def session_payload(user: User, csrf_token: str) -> UserSessionOut:
    return UserSessionOut(user=user, csrf_token=csrf_token)


def set_session_cookies(response: Response, token: str, csrf_token: str) -> None:
    cookie_options = {
        "secure": settings.COOKIE_SECURE,
        "samesite": "lax",
        "path": "/",
        "max_age": settings.SESSION_TTL_SECONDS,
    }
    response.set_cookie(
        SESSION_COOKIE, token, httponly=True, **cookie_options
    )
    response.set_cookie(
        CSRF_COOKIE, csrf_token, httponly=True, **cookie_options
    )


def create_session(user: User, db: Session, response: Response) -> UserSessionOut:
    token = new_session_secret()
    csrf_token = new_session_secret()
    now = int(time.time())
    db.add(
        AuthSession(
            user_id=user.id,
            token_hash=hash_session_token(token),
            csrf_hash=hash_session_token(csrf_token),
            created_at=now,
            expires_at=now + settings.SESSION_TTL_SECONDS,
        )
    )
    db.commit()
    set_session_cookies(response, token, csrf_token)
    return session_payload(user, csrf_token)


@router.post("/login", response_model=UserSessionOut)
def login(
    payload: AuthCredentials,
    response: Response,
    db: Session = Depends(get_db),
):
    email = payload.email.strip().lower()
    password = payload.password
    if not valid_email(email) or not password:
        raise HTTPException(status_code=401, detail="Invalid email or password.")

    user = db.query(User).filter(User.email == email).first()
    if not user or not user.is_active or not verify_password(
        password, user.hashed_password
    ):
        raise HTTPException(status_code=401, detail="Invalid email or password.")
    if payload.audience == "admin" and user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="This sign-in page is for administrator accounts.",
        )

    return create_session(user, db, response)


@router.post("/register", response_model=UserSessionOut, status_code=201)
def register(
    payload: PublicRegistration,
    response: Response,
    db: Session = Depends(get_db),
):
    email = payload.email.strip().lower()
    full_name = payload.full_name.strip()
    if not valid_email(email):
        raise HTTPException(status_code=422, detail="Enter a valid email address.")
    if not full_name:
        raise HTTPException(status_code=422, detail="Name cannot be blank.")
    if db.query(User).filter(User.email == email).first():
        raise HTTPException(status_code=409, detail="That email address already exists.")

    user = User(
        username=email,
        email=email,
        full_name=full_name,
        role=UserRole.RESPONDER,
        hashed_password=hash_password(payload.password),
        is_active=1,
        must_change_password=False,
    )
    db.add(user)
    try:
        db.flush()
        db.add(
            AuditLog(
                user_id=user.id,
                action="USER_SELF_REGISTERED",
                details="Created a public responder account.",
            )
        )
        return create_session(user, db, response)
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(
            status_code=409, detail="That email address already exists."
        ) from exc


@router.get("/me", response_model=UserSessionOut)
def current_user(
    request: Request,
    user: User = Depends(get_current_user),
    session: AuthSession = Depends(get_current_session),
):
    csrf_token = request.cookies.get(CSRF_COOKIE, "")
    from app.core.security import hash_session_token

    if not csrf_token or hash_session_token(csrf_token) != session.csrf_hash:
        raise HTTPException(status_code=401, detail="Session validation failed.")
    return session_payload(user, csrf_token)


@router.post("/logout")
def logout(
    session: AuthSession = Depends(get_current_session),
    db: Session = Depends(get_db),
):
    session.revoked_at = int(time.time())
    db.commit()
    response = Response(status_code=204)
    response.delete_cookie(
        SESSION_COOKIE, path="/", secure=settings.COOKIE_SECURE, samesite="lax"
    )
    response.delete_cookie(
        CSRF_COOKIE, path="/", secure=settings.COOKIE_SECURE, samesite="lax"
    )
    return response


@router.post("/password", response_model=UserOut)
def change_password(
    payload: PasswordChange,
    user: User = Depends(get_current_user),
    current_session: AuthSession = Depends(get_current_session),
    db: Session = Depends(get_db),
):
    if not verify_password(payload.current_password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Current password is incorrect.")
    if payload.current_password == payload.new_password:
        raise HTTPException(
            status_code=400, detail="Choose a password different from the current one."
        )
    user.hashed_password = hash_password(payload.new_password)
    user.must_change_password = False
    db.query(AuthSession).filter(
        AuthSession.user_id == user.id,
        AuthSession.revoked_at.is_(None),
        AuthSession.id != current_session.id,
    ).update({AuthSession.revoked_at: int(time.time())}, synchronize_session=False)
    db.add(
        AuditLog(
            user_id=user.id,
            action="PASSWORD_CHANGED",
            details="Account password changed.",
        )
    )
    db.commit()
    db.refresh(user)
    return user
