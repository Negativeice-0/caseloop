from fastapi.testclient import TestClient
from app.main import app
from app.core.database import engine

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    database = engine.dialect.name
    assert response.json() == {
        "app": "CaseLoop",
        "database": database,
        "mode": (
            "offline-first local database active"
            if database == "sqlite"
            else f"shared {database} database active"
        ),
        "status": "online",
    }