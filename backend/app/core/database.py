from sqlalchemy import create_engine
from sqlalchemy.engine import Engine, make_url
from sqlalchemy.orm import declarative_base, sessionmaker
from .config import settings

def create_database_engine(database_url: str) -> Engine:
    url = make_url(database_url)
    
    # Optional: Automatically handle driver adjustments if needed
    if (
        url.get_backend_name() == "postgresql"
        and url.get_driver_name() == "psycopg2"
    ):
        url = url.set(drivername="postgresql+psycopg")

    # SQLite needs check_same_thread=False for FastAPI concurrency
    connect_args = (
        {"check_same_thread": False} if url.get_backend_name() == "sqlite" else {}
    )
    
    # pool_pre_ping=True is vital for Docker environments to prevent stale connections
    return create_engine(
        url, 
        connect_args=connect_args,
        pool_pre_ping=True
    )

# Pulls DATABASE_URL directly from your Settings class (which loaded the .env file)
engine = create_database_engine(settings.DATABASE_URL)

# Session factory for database operations
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for SQLAlchemy models
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()