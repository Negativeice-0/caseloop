# tests/conftest.py
import os

os.environ.setdefault("DATABASE_URL", "sqlite://")

import pytest
from app.core.database import Base, engine

@pytest.fixture(autouse=True)
def setup_database():
    # Create tables before each test
    Base.metadata.create_all(bind=engine)
    yield
    # Drop tables after each test
    Base.metadata.drop_all(bind=engine)