import hmac

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Request
from fastapi.responses import JSONResponse
from app.api import admin, responses, auth, assignments, intakes, reports
from app.api import webhooks
from app.core.auth import CSRF_COOKIE, CSRF_HEADER, SESSION_COOKIE
from app.core.config import settings
from app.core.database import engine
from app.db_bootstrap import initialize_database

if settings.APP_ENV == "production" and not settings.COOKIE_SECURE:
    raise RuntimeError("COOKIE_SECURE must be true when APP_ENV=production.")

initialize_database()

app = FastAPI(title="CaseLoop API", version="0.1.0")

app.include_router(admin.router)
app.include_router(auth.router)
app.include_router(responses.router)
app.include_router(assignments.router)
app.include_router(intakes.router)
app.include_router(reports.router)
app.include_router(webhooks.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)


@app.middleware("http")
async def protect_cookie_mutations(request: Request, call_next):
    if (
        request.method not in {"GET", "HEAD", "OPTIONS"}
        and request.cookies.get(SESSION_COOKIE)
        and request.url.path not in {
            "/api/auth/login",
            "/api/auth/register",
            "/api/webhooks/whatsapp",
        }
    ):
        cookie_token = request.cookies.get(CSRF_COOKIE, "")
        header_token = request.headers.get(CSRF_HEADER, "")
        if not cookie_token or not hmac.compare_digest(cookie_token, header_token):
            return JSONResponse(
                status_code=403, content={"detail": "CSRF token is missing or invalid."}
            )
    return await call_next(request)


@app.get("/")
def read_root():
    database = engine.dialect.name
    mode = (
        "offline-first local database active"
        if database == "sqlite"
        else f"shared {database} database active"
    )
    return {
        "app": "CaseLoop",
        "status": "online",
        "mode": mode,
        "database": database,
    }