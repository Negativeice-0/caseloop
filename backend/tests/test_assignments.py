import pytest
import json
import hashlib
import hmac
from pathlib import Path
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool  # <--- Import StaticPool

from app.main import app
from app.core.database import Base, get_db
from app.core.security import hash_password
from app.core.config import settings
from app.models.models import Assignment, ResponseItem, Team, TeamMembership, User

# =============================================================================
# === Isolated In-Memory Test Setup ===
# =============================================================================
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,  # <--- Forces all connections to share the exact same in-memory database
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 1. Override the application's get_db dependency so endpoints use our in-memory DB
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)
TEST_ADMIN_EMAIL = "coord@caseloop.test"
TEST_ADMIN_PASSWORD = "test-admin-password-123"
TEST_ADMIN_HASH = hash_password(TEST_ADMIN_PASSWORD)


@pytest.fixture(autouse=True)
def setup_database():
    """Create fresh tables for each test and seed initial required data."""
    client.cookies.clear()
    client.headers.pop("X-CSRF-Token", None)
    # Create all tables on the in-memory test engine
    Base.metadata.create_all(bind=engine)
    
    # Pre-seed a dummy user and response item for foreign key constraints
    db = TestingSessionLocal()
    user = User(
        username=TEST_ADMIN_EMAIL,
        email=TEST_ADMIN_EMAIL,
        hashed_password=TEST_ADMIN_HASH,
        role="admin"
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    response_item = ResponseItem(
        reference_code="RESP-2026-TEST",
        title="Test Flood Incident",
        description="Testing response linkage",
        coordinator_id=user.id
    )
    db.add(response_item)
    db.commit()
    db.close()
    login = client.post(
        "/api/auth/login",
        json={"email": TEST_ADMIN_EMAIL, "password": TEST_ADMIN_PASSWORD},
    )
    assert login.status_code == 200
    client.headers["X-CSRF-Token"] = login.json()["csrf_token"]

    yield
    
    # Drop tables after the test finishes
    Base.metadata.drop_all(bind=engine)
    client.cookies.clear()
    client.headers.pop("X-CSRF-Token", None)


# =============================================================================
# === Test Cases ===
# =============================================================================

def test_create_and_list_team():
    """Verify team creation and retrieval."""
    team_payload = {"name": "Karen Alpha Team", "description": "Rapid Response"}
    response = client.post("/api/assignments/teams", json=team_payload)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Karen Alpha Team"
    assert "id" in data

    response = client.get("/api/assignments/teams")
    assert response.status_code == 200
    teams = response.json()
    assert len(teams) == 1
    assert teams[0]["name"] == "Karen Alpha Team"


def test_create_assignment_success():
    """Verify linking an assignment to a response and team."""
    team_res = client.post("/api/assignments/teams", json={"name": "Langata Unit B"})
    team_id = team_res.json()["id"]

    assignment_payload = {
        "reference_code": "ASN-2026-001",
        "response_id": 1,
        "team_id": team_id,
        "status": "Draft",
        "description": "Initial deployment to sector 4"
    }

    res = client.post("/api/assignments/", json=assignment_payload)
    assert res.status_code == 201
    data = res.json()
    assert data["reference_code"] == "ASN-2026-001"
    assert data["status"] == "Draft"
    assert data["team_id"] == team_id


def test_assignment_invalid_team_or_response():
    """Verify 404 behavior when response or team does not exist."""
    payload = {
        "reference_code": "ASN-FAIL-01",
        "response_id": 1,
        "team_id": 999,
        "status": "Draft"
    }
    res = client.post("/api/assignments/", json=payload)
    assert res.status_code == 404
    assert res.json()["detail"] == "Assigned team not found."


def test_draft_assignment_can_be_edited_and_records_a_timeline_event():
    first_team = client.post(
        "/api/assignments/teams", json={"name": "Draft Editing Unit A"}
    ).json()
    second_team = client.post(
        "/api/assignments/teams", json={"name": "Draft Editing Unit B"}
    ).json()
    created = client.post("/api/assignments/", json={
        "reference_code": "ASN-DRAFT-EDIT-001",
        "response_id": 1,
        "team_id": first_team["id"],
        "status": "Draft",
        "description": "Original draft details",
    })
    assert created.status_code == 201

    updated = client.put(f"/api/assignments/{created.json()['id']}", json={
        "reference_code": "ASN-DRAFT-EDIT-002",
        "response_id": 1,
        "team_id": second_team["id"],
        "description": "Corrected draft details",
    })
    assert updated.status_code == 200
    assert updated.json()["reference_code"] == "ASN-DRAFT-EDIT-002"
    assert updated.json()["team_id"] == second_team["id"]
    assert updated.json()["description"] == "Corrected draft details"

    events = client.get("/api/responses/1/timeline").json()
    assert any(event["event_type"] == "DRAFT_ASSIGNMENT_UPDATED" for event in events)

    assigned = client.patch(
        f"/api/assignments/{created.json()['id']}/status",
        json={"status": "Assigned"},
    )
    assert assigned.status_code == 200
    locked = client.put(f"/api/assignments/{created.json()['id']}", json={
        "reference_code": "ASN-DRAFT-EDIT-002",
        "response_id": 1,
        "team_id": second_team["id"],
        "description": "Attempt to rewrite active history",
    })
    assert locked.status_code == 409


def test_update_assignment_status_lifecycle():
    """Verify the assignment lifecycle emits timeline events at each step."""
    team_res = client.post("/api/assignments/teams", json={"name": "Delta Support"})
    team_id = team_res.json()["id"]

    asn_res = client.post("/api/assignments/", json={
        "reference_code": "ASN-2026-LIFECYCLE",
        "response_id": 1,
        "team_id": team_id,
        "status": "Draft"
    })
    asn_id = asn_res.json()["id"]

    for next_status in ("Assigned", "Acknowledged", "In Progress", "Completed"):
        patch_res = client.patch(
            f"/api/assignments/{asn_id}/status", json={"status": next_status}
        )
        assert patch_res.status_code == 200
        assert patch_res.json()["status"] == next_status

    timeline = client.get("/api/responses/1/timeline")
    assert timeline.status_code == 200
    events = timeline.json()
    assert [event["event_type"] for event in events].count("ASSIGNMENT_STATUS_UPDATED") == 4
    assert all(event["actor_id"] == 1 for event in events)
    feed = client.get("/api/responses/timeline")
    assert feed.status_code == 200
    assert len(feed.json()) == 5
    assert all(event["response_reference"] == "RESP-2026-TEST" for event in feed.json())
    assert all(event["actor_name"] == TEST_ADMIN_EMAIL for event in feed.json())


def test_assignment_rejects_skipped_lifecycle_transition():
    team_res = client.post("/api/assignments/teams", json={"name": "Foxtrot Unit"})
    assignment = client.post("/api/assignments/", json={
        "reference_code": "ASN-2026-SKIP",
        "response_id": 1,
        "team_id": team_res.json()["id"],
        "status": "Draft",
    })
    response = client.patch(
        f"/api/assignments/{assignment.json()['id']}/status",
        json={"status": "Completed"},
    )
    assert response.status_code == 400


def test_whatsapp_intake_requires_review_before_response_creation():
    fixture_path = Path(__file__).parent / "fixtures" / "whatsapp_intake.json"
    payload = json.loads(fixture_path.read_text(encoding="utf-8"))
    intake = client.post("/api/intakes/", json=payload)
    assert intake.status_code == 201
    assert intake.json()["status"] == "pending"
    assert client.get("/api/responses/").json() == [
        client.get("/api/responses/1").json()
    ]

    duplicate = client.post("/api/intakes/", json=payload)
    assert duplicate.status_code == 409

    approval_payload = {"response": {
            "reference_code": "RESP-FROM-INTAKE-001",
            "title": "Flood support request",
            "description": intake.json()["source_text"],
            "category": "Disaster response",
            "priority": "high",
            "location": "School area",
        }}
    approved = client.post(
        f"/api/intakes/{intake.json()['id']}/approve", json=approval_payload
    )
    assert approved.status_code == 200
    assert approved.json()["title"] == "Flood support request"
    assert len(client.get("/api/responses/").json()) == 2
    duplicate_approval = client.post(
        f"/api/intakes/{intake.json()['id']}/approve", json=approval_payload
    )
    assert duplicate_approval.status_code == 409


def test_word_report_is_a_docx_download():
    response = client.get("/api/reports/word")
    assert response.status_code == 200
    assert response.headers["content-type"].startswith(
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )
    assert response.content.startswith(b"PK")


def test_report_summary_counts_responses_and_assignments():
    summary = client.get("/api/reports/summary")
    assert summary.status_code == 200
    assert summary.json()["total_responses"] == 1
    assert summary.json()["total_assignments"] == 0
    preview = client.get("/api/reports/preview")
    assert preview.status_code == 200
    assert preview.json()["responses"][0]["reference_code"] == "RESP-2026-TEST"
    assert preview.json()["assignments"] == []


def test_report_filters_analysis_and_word_export_use_the_same_records():
    from datetime import datetime
    from io import BytesIO
    from docx import Document
    from app.models.models import IntakeSubmission

    db = TestingSessionLocal()
    team = Team(name="Report Team")
    db.add(team)
    db.flush()
    response = ResponseItem(
        reference_code="RESP-REPORT-001",
        title="Synthetic health support",
        description="Synthetic report test record.",
        category="Health",
        priority="high",
        status="Active",
        location="Example location",
        coordinator_id=1,
    )
    old_response = ResponseItem(
        reference_code="RESP-REPORT-OLD",
        title="Old synthetic record",
        category="Shelter",
        priority="normal",
        status="Resolved",
        coordinator_id=1,
        created_at=datetime(2000, 1, 1),
    )
    db.add_all([response, old_response])
    db.flush()
    db.add_all([
        Assignment(
            reference_code="ASN-REPORT-001",
            response_id=response.id,
            team_id=team.id,
            status="Assigned",
            description="Coordinate synthetic support.",
        ),
        IntakeSubmission(
            source_channel="whatsapp",
            source_text="TEST ONLY: synthetic health support",
            status="approved",
            response_id=response.id,
            reviewed_at=datetime.utcnow(),
        ),
    ])
    team_id = team.id
    db.commit()
    db.close()

    params = {
        "from_date": "2020-01-01",
        "to_date": "2100-01-01",
        "team_id": team_id,
    }
    preview = client.get("/api/reports/preview", params=params)
    assert preview.status_code == 200
    report = preview.json()
    assert [item["reference_code"] for item in report["responses"]] == [
        "RESP-REPORT-001"
    ]
    assert report["filters"]["team_name"] == "Report Team"
    assert report["summary"]["priority_breakdown"] == {"High": 1}
    assert report["summary"]["category_breakdown"] == {"Health": 1}
    assert report["summary"]["source_breakdown"] == {"Whatsapp": 1}
    assert report["summary"]["unassigned_active_responses"] == 0

    word_report = client.get("/api/reports/word", params=params)
    assert word_report.status_code == 200
    document = Document(BytesIO(word_report.content))
    document_text = "\n".join(paragraph.text for paragraph in document.paragraphs)
    document_text += "\n" + "\n".join(
        cell.text
        for table in document.tables
        for row in table.rows
        for cell in row.cells
    )
    assert "Report Team" in document_text
    assert "Responses by source" in document_text
    assert "RESP-REPORT-001" in document_text
    assert "RESP-2026-TEST" not in document_text

    invalid_range = client.get(
        "/api/reports/preview",
        params={"from_date": "2026-12-01", "to_date": "2026-11-01"},
    )
    assert invalid_range.status_code == 422


def test_report_weekly_activity_and_location_coverage():
    from datetime import datetime

    db = TestingSessionLocal()
    team = Team(name="Trend Test Team")
    db.add(team)
    db.flush()
    first = ResponseItem(
        reference_code="RESP-WEEK-001",
        title="First synthetic response",
        description="Synthetic weekly report test.",
        category="Health",
        priority="high",
        location="North sector",
        coordinator_id=1,
        created_at=datetime(2024, 1, 2, 12),
    )
    second = ResponseItem(
        reference_code="RESP-WEEK-002",
        title="Second synthetic response",
        description="Synthetic weekly report test.",
        category="Shelter",
        priority="normal",
        status="Resolved",
        location="",
        coordinator_id=1,
        created_at=datetime(2024, 1, 9, 12),
    )
    db.add_all([first, second])
    db.flush()
    db.add_all([
        Assignment(
            reference_code="ASN-WEEK-001",
            response_id=first.id,
            team_id=team.id,
            status="Assigned",
            created_at=datetime(2024, 1, 3, 12),
        ),
        Assignment(
            reference_code="ASN-WEEK-002",
            response_id=second.id,
            team_id=team.id,
            status="Completed",
            created_at=datetime(2024, 1, 10, 12),
        ),
    ])
    team_id = team.id
    db.commit()
    db.close()

    response = client.get(
        "/api/reports/summary",
        params={
            "from_date": "2024-01-01",
            "to_date": "2024-01-14",
            "team_id": team_id,
        },
    )
    assert response.status_code == 200
    summary = response.json()
    assert summary["location_breakdown"] == {
        "Location not recorded": 1,
        "North sector": 1,
    }
    assert summary["missing_location_responses"] == 1
    assert [
        (
            week["week_start"],
            week["responses_created"],
            week["assignments_created"],
        )
        for week in summary["weekly_activity"]
    ] == [("2024-01-01", 1, 1), ("2024-01-08", 1, 1)]
    assert summary["weekly_activity_from"] == "2024-01-01"
    assert summary["weekly_activity_to"] == "2024-01-14"


def test_report_trend_window_caps_at_eight_or_twenty_six_weeks():
    from datetime import date, timedelta

    default_summary = client.get("/api/reports/summary")
    assert default_summary.status_code == 200
    assert len(default_summary.json()["weekly_activity"]) == 8

    end_date = date(2024, 1, 1)
    long_range_summary = client.get(
        "/api/reports/summary",
        params={"from_date": "2000-01-01", "to_date": end_date.isoformat()},
    )
    assert long_range_summary.status_code == 200
    summary = long_range_summary.json()
    latest_week = end_date - timedelta(days=end_date.weekday())
    first_week = latest_week - timedelta(weeks=25)
    assert len(summary["weekly_activity"]) == 26
    assert summary["weekly_activity"][0]["week_start"] == first_week.isoformat()
    assert summary["weekly_activity_from"] == first_week.isoformat()


@pytest.mark.parametrize(
    ("template", "expected_title", "expected_section"),
    [
        ("operational", "CaseLoop Operational Report", "Responses by category"),
        ("situation", "CaseLoop Situation Report", "Situation overview"),
        ("field", "CaseLoop Field Action Brief", "Active field responses"),
    ],
)
def test_report_templates_match_preview_and_word_export(
    template, expected_title, expected_section
):
    from io import BytesIO
    from docx import Document

    preview = client.get("/api/reports/preview", params={"template": template})
    assert preview.status_code == 200
    assert preview.json()["template"] == template

    word_report = client.get("/api/reports/word", params={"template": template})
    assert word_report.status_code == 200
    document = Document(BytesIO(word_report.content))
    assert document.paragraphs[0].text == expected_title
    assert expected_section in [paragraph.text for paragraph in document.paragraphs]


def test_api_requires_session_and_rejects_missing_csrf_header():
    unauthenticated = TestClient(app)
    assert unauthenticated.get("/api/responses/").status_code == 401

    csrf_token = client.headers["X-CSRF-Token"]
    client.headers.pop("X-CSRF-Token")
    response = client.post("/api/assignments/teams", json={"name": "Missing CSRF"})
    assert response.status_code == 403
    client.headers["X-CSRF-Token"] = csrf_token


def test_admin_sign_in_rejects_responder_accounts_without_creating_a_session():
    db = TestingSessionLocal()
    responder = User(
        username="responder-login@example.test",
        email="responder-login@example.test",
        hashed_password=hash_password("responder-login-password-2026"),
        role="responder",
    )
    db.add(responder)
    db.commit()
    db.close()

    responder_client = TestClient(app)
    rejected = responder_client.post("/api/auth/login", json={
        "email": "responder-login@example.test",
        "password": "responder-login-password-2026",
        "audience": "admin",
    })
    assert rejected.status_code == 403
    assert responder_client.get("/api/auth/me").status_code == 401

    regular_login = responder_client.post("/api/auth/login", json={
        "email": "responder-login@example.test",
        "password": "responder-login-password-2026",
    })
    assert regular_login.status_code == 200
    assert regular_login.json()["user"]["role"] == "responder"

    administrator_client = TestClient(app)
    administrator_login = administrator_client.post("/api/auth/login", json={
        "email": TEST_ADMIN_EMAIL,
        "password": TEST_ADMIN_PASSWORD,
        "audience": "admin",
    })
    assert administrator_login.status_code == 200
    assert administrator_login.json()["user"]["role"] == "admin"


def test_admin_provisioned_account_must_change_password():
    created = client.post("/api/admin/users", json={
        "email": "new.responder@example.test",
        "full_name": "New Responder",
        "role": "responder",
    })
    assert created.status_code == 201
    body = created.json()
    assert body["user"]["must_change_password"] is True
    assert body["show_password_once"] is True

    responder = TestClient(app)
    login = responder.post("/api/auth/login", json={
        "email": "new.responder@example.test",
        "password": body["initial_password"],
    })
    assert login.status_code == 200
    assert "access_token" not in login.json()
    assert sum(
        "httponly" in cookie.lower()
        for cookie in login.headers.get_list("set-cookie")
    ) == 2
    responder.headers["X-CSRF-Token"] = login.json()["csrf_token"]
    assert login.json()["user"]["must_change_password"] is True

    changed = responder.post("/api/auth/password", json={
        "current_password": body["initial_password"],
        "new_password": "responder-own-password-2026",
    })
    assert changed.status_code == 200
    assert changed.json()["must_change_password"] is False
    assert responder.get("/api/auth/me").status_code == 200


def test_admin_password_reset_revokes_sessions_and_requires_password_change():
    created = client.post("/api/admin/users", json={
        "email": "reset.responder@example.test",
        "full_name": "Reset Responder",
        "role": "responder",
    })
    assert created.status_code == 201
    user_id = created.json()["user"]["id"]
    previous_password = created.json()["initial_password"]

    responder = TestClient(app)
    login = responder.post("/api/auth/login", json={
        "email": "reset.responder@example.test",
        "password": previous_password,
    })
    assert login.status_code == 200
    responder.headers["X-CSRF-Token"] = login.json()["csrf_token"]

    reset = client.post(f"/api/admin/users/{user_id}/reset-password")
    assert reset.status_code == 200
    assert reset.json()["show_password_once"] is True
    assert responder.get("/api/auth/me").status_code == 401
    assert responder.post("/api/auth/login", json={
        "email": "reset.responder@example.test",
        "password": previous_password,
    }).status_code == 401

    new_login = responder.post("/api/auth/login", json={
        "email": "reset.responder@example.test",
        "password": reset.json()["initial_password"],
    })
    assert new_login.status_code == 200
    assert new_login.json()["user"]["must_change_password"] is True


def test_demo_seed_requires_an_existing_coordinator_or_admin(monkeypatch):
    from app import seed as seed_module

    seed_engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=seed_engine)
    seed_sessions = sessionmaker(bind=seed_engine)
    monkeypatch.setattr(seed_module, "engine", seed_engine)
    monkeypatch.setattr(seed_module, "SessionLocal", seed_sessions)
    with pytest.raises(RuntimeError, match="Create an active administrator"):
        seed_module.seed_database()
    seed_engine.dispose()


def test_responder_only_sees_and_updates_their_team_assignments():
    db = TestingSessionLocal()
    responder = User(
        username="field@example.test",
        email="field@example.test",
        full_name="Field Responder",
        hashed_password=hash_password("field-password-2026"),
        role="responder",
    )
    assigned_team = Team(name="Assigned Unit")
    other_team = Team(name="Other Unit")
    db.add_all([responder, assigned_team, other_team])
    db.commit()
    db.refresh(responder)
    db.refresh(assigned_team)
    db.refresh(other_team)
    db.add(TeamMembership(team_id=assigned_team.id, user_id=responder.id))
    assigned = Assignment(
        reference_code="ASN-RESPONDER-OWN",
        response_id=1,
        team_id=assigned_team.id,
        status="Draft",
    )
    outside = Assignment(
        reference_code="ASN-RESPONDER-OTHER",
        response_id=1,
        team_id=other_team.id,
        status="Assigned",
    )
    db.add_all([assigned, outside])
    db.commit()
    db.refresh(assigned)
    assigned_id = assigned.id
    outside_id = outside.id
    db.close()

    field_client = TestClient(app)
    login = field_client.post("/api/auth/login", json={
        "email": "field@example.test",
        "password": "field-password-2026",
    })
    assert login.status_code == 200
    field_client.headers["X-CSRF-Token"] = login.json()["csrf_token"]

    assert field_client.delete("/api/responses/1").status_code == 403
    visible = field_client.get("/api/assignments/").json()
    assert [item["reference_code"] for item in visible] == ["ASN-RESPONDER-OWN"]
    assert field_client.patch(
        f"/api/assignments/{assigned_id}/status", json={"status": "Assigned"}
    ).status_code == 403
    assert field_client.patch(
        f"/api/assignments/{outside_id}/status", json={"status": "Acknowledged"}
    ).status_code == 403

    assigned_by_coordinator = client.patch(
        f"/api/assignments/{assigned_id}/status", json={"status": "Assigned"}
    )
    assert assigned_by_coordinator.status_code == 200
    acknowledged = field_client.patch(
        f"/api/assignments/{assigned_id}/status", json={"status": "Acknowledged"}
    )
    assert acknowledged.status_code == 200
    assert acknowledged.json()["status"] == "Acknowledged"


def test_session_logout_revokes_the_server_session():
    response = client.post("/api/auth/logout")
    assert response.status_code == 204
    assert client.get("/api/auth/me").status_code == 401


def test_public_registration_creates_an_authenticated_responder_only_account():
    public_client = TestClient(app)
    registration = {
        "email": "new.responder@example.test",
        "full_name": "New Responder",
        "password": "secure-responder-password",
    }

    created = public_client.post("/api/auth/register", json=registration)

    assert created.status_code == 201
    assert created.json()["user"]["role"] == "responder"
    assert created.json()["user"]["is_active"] == 1
    assert public_client.get("/api/auth/me").status_code == 200
    assert public_client.get("/api/admin/users").status_code == 403
    assert public_client.post(
        "/api/intakes/",
        json={"source_channel": "manual", "source_text": "Restricted action"},
    ).status_code == 403

    duplicate = public_client.post("/api/auth/register", json=registration)
    assert duplicate.status_code == 409


def test_public_registration_rejects_role_override_and_short_password():
    public_client = TestClient(app)
    registration = {
        "email": "role.override@example.test",
        "full_name": "Role Override",
        "password": "secure-responder-password",
        "role": "admin",
    }
    assert public_client.post("/api/auth/register", json=registration).status_code == 422

    registration.pop("role")
    registration["password"] = "too-short"
    assert public_client.post("/api/auth/register", json=registration).status_code == 422


def test_meta_webhook_verification_and_signed_intake_are_draft_only(monkeypatch):
    monkeypatch.setattr(settings, "WHATSAPP_VERIFY_TOKEN", "test-verify-token")
    monkeypatch.setattr(settings, "WHATSAPP_APP_SECRET", "test-meta-app-secret")

    verification = client.get("/api/webhooks/whatsapp", params={
        "hub.mode": "subscribe",
        "hub.verify_token": "test-verify-token",
        "hub.challenge": "challenge-123",
    })
    assert verification.status_code == 200
    assert verification.text == "challenge-123"

    payload = {
        "object": "whatsapp_business_account",
        "entry": [{
            "changes": [{
                "field": "messages",
                "value": {
                    "messages": [{
                        "id": "wamid.TEST-WEBHOOK-001",
                        "from": "15551234567",
                        "type": "text",
                        "text": {"body": "TEST ONLY: need water near Example Ward 4"},
                    }]
                },
            }]
        }],
    }
    raw_body = json.dumps(payload).encode("utf-8")
    signature = "sha256=" + hmac.new(
        b"test-meta-app-secret", raw_body, hashlib.sha256
    ).hexdigest()

    received = client.post(
        "/api/webhooks/whatsapp",
        content=raw_body,
        headers={"X-Hub-Signature-256": signature},
    )
    assert received.status_code == 200
    assert received.json() == {"status": "ok", "accepted": 1, "duplicates": 0}
    pending = client.get("/api/intakes/?intake_status=pending").json()
    assert len(pending) == 1
    assert pending[0]["source_channel"] == "whatsapp"
    assert pending[0]["status"] == "pending"
    assert client.get("/api/responses/").json()

    duplicate = client.post(
        "/api/webhooks/whatsapp",
        content=raw_body,
        headers={"X-Hub-Signature-256": signature},
    )
    assert duplicate.json() == {"status": "ok", "accepted": 0, "duplicates": 1}

    team = client.post(
        "/api/assignments/teams",
        json={"name": "WhatsApp Intake Team"},
    ).json()
    approved = client.post(
        f"/api/intakes/{pending[0]['id']}/approve",
        json={
            "response": {
                "reference_code": "RESP-WHATSAPP-001",
                "title": "Synthetic water support request",
                "description": pending[0]["source_text"],
                "category": "Disaster response",
                "priority": "high",
                "location": "Example Ward 4",
            },
            "assignment": {
                "reference_code": "ASN-WHATSAPP-001",
                "team_id": team["id"],
                "description": "Review and coordinate the synthetic request.",
            },
        },
    )
    assert approved.status_code == 200
    response_rows = client.get("/api/responses/").json()
    assert any(row["reference_code"] == "RESP-WHATSAPP-001" for row in response_rows)
    assignment_rows = client.get("/api/assignments/").json()
    linked_assignment = next(
        row for row in assignment_rows if row["reference_code"] == "ASN-WHATSAPP-001"
    )
    assert linked_assignment["response_id"] == approved.json()["id"]
    assert linked_assignment["team_id"] == team["id"]
    assert linked_assignment["status"] == "Assigned"
    linked_events = client.get(
        f"/api/responses/{approved.json()['id']}/timeline"
    ).json()
    assert {event["event_type"] for event in linked_events} == {
        "CREATED_FROM_INTAKE",
        "ASSIGNMENT_CREATED",
    }


def test_meta_webhook_rejects_invalid_signatures_and_malformed_payloads(monkeypatch):
    monkeypatch.setattr(settings, "WHATSAPP_APP_SECRET", "test-meta-app-secret")
    bad_signature = client.post(
        "/api/webhooks/whatsapp",
        content=b'{"object":"whatsapp_business_account"}',
        headers={"X-Hub-Signature-256": "sha256=invalid"},
    )
    assert bad_signature.status_code == 401

    raw_body = b"{not-json"
    signature = "sha256=" + hmac.new(
        b"test-meta-app-secret", raw_body, hashlib.sha256
    ).hexdigest()
    malformed = client.post(
        "/api/webhooks/whatsapp",
        content=raw_body,
        headers={"X-Hub-Signature-256": signature},
    )
    assert malformed.status_code == 400