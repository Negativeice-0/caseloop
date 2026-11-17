from collections import Counter
from datetime import date, datetime, timedelta
from io import BytesIO
from typing import Literal

from docx import Document
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import StreamingResponse
from sqlalchemy import func, select
from sqlalchemy.orm import Session, joinedload

from app.core.auth import require_roles
from app.core.database import get_db
from app.models.models import Assignment, IntakeSubmission, ResponseItem, Team
from app.schemas.schemas import (
    ReportFilters,
    ReportPreview,
    ReportPreviewAssignment,
    ReportPreviewResponse,
    ReportSummary,
    ReportWeek,
)

router = APIRouter(
    prefix="/api/reports",
    tags=["Reports"],
    dependencies=[Depends(require_roles("admin", "coordinator"))],
)


def _collect_report_data(
    db: Session,
    from_date: date | None,
    to_date: date | None,
    team_id: int | None,
):
    report_end = to_date or date.today()
    if from_date and from_date > report_end:
        raise HTTPException(
            status_code=422, detail="Start date must be on or before end date."
        )

    team = db.get(Team, team_id) if team_id is not None else None
    if team_id is not None and team is None:
        raise HTTPException(status_code=404, detail="Team not found.")

    response_query = db.query(ResponseItem)
    if from_date:
        response_query = response_query.filter(
            func.date(ResponseItem.created_at) >= from_date.isoformat()
        )
    if to_date:
        response_query = response_query.filter(
            func.date(ResponseItem.created_at) <= to_date.isoformat()
        )
    if team_id is not None:
        team_response_ids = (
            select(Assignment.response_id)
            .where(Assignment.team_id == team_id)
            .distinct()
        )
        response_query = response_query.filter(ResponseItem.id.in_(team_response_ids))
    responses = response_query.order_by(ResponseItem.created_at.desc()).all()

    assignment_query = db.query(Assignment).options(
        joinedload(Assignment.response),
        joinedload(Assignment.assigned_team),
    )
    if from_date:
        assignment_query = assignment_query.filter(
            func.date(Assignment.created_at) >= from_date.isoformat()
        )
    if to_date:
        assignment_query = assignment_query.filter(
            func.date(Assignment.created_at) <= to_date.isoformat()
        )
    if team_id is not None:
        assignment_query = assignment_query.filter(Assignment.team_id == team_id)
    assignments = assignment_query.order_by(Assignment.created_at.desc()).all()

    response_ids = [item.id for item in responses]
    assigned_response_ids: set[int] = set()
    source_by_response: dict[int, str] = {}
    if response_ids:
        assigned_response_ids = {
            row[0]
            for row in db.query(Assignment.response_id)
            .filter(Assignment.response_id.in_(response_ids))
            .distinct()
            .all()
        }
        source_by_response = {
            response_id: source_channel
            for response_id, source_channel in db.query(
                IntakeSubmission.response_id, IntakeSubmission.source_channel
            )
            .filter(IntakeSubmission.response_id.in_(response_ids))
            .all()
        }

    priority_breakdown = Counter(
        (item.priority or "Unspecified").title() for item in responses
    )
    category_breakdown = Counter(
        (item.category or "Uncategorized").strip() or "Uncategorized"
        for item in responses
    )
    source_breakdown = Counter(
        source_by_response.get(item.id, "coordinator").replace("_", " ").title()
        for item in responses
    )
    location_breakdown = Counter(
        (item.location or "").strip() or "Location not recorded"
        for item in responses
    )
    trend_start = from_date or (report_end - timedelta(days=55))
    first_week = trend_start - timedelta(days=trend_start.weekday())
    last_week = report_end - timedelta(days=report_end.weekday())
    max_weeks = 26 if from_date else 8
    week_count = ((last_week - first_week).days // 7) + 1
    if week_count > max_weeks:
        first_week = last_week - timedelta(weeks=max_weeks - 1)
        trend_start = max(trend_start, first_week)
    weekly_activity = []
    week_start = first_week
    while week_start <= report_end:
        week_end = min(week_start + timedelta(days=6), report_end)
        bucket_start = max(week_start, trend_start)
        weekly_activity.append(
            ReportWeek(
                week_start=week_start,
                responses_created=sum(
                    1
                    for item in responses
                    if bucket_start <= item.created_at.date() <= week_end
                ),
                assignments_created=sum(
                    1
                    for item in assignments
                    if bucket_start <= item.created_at.date() <= week_end
                ),
            )
        )
        week_start += timedelta(days=7)

    summary = ReportSummary(
        total_responses=len(responses),
        active_responses=sum(1 for item in responses if item.status == "Active"),
        resolved_responses=sum(1 for item in responses if item.status == "Resolved"),
        total_assignments=len(assignments),
        active_assignments=sum(
            1 for item in assignments if item.status not in {"Completed", "Cancelled"}
        ),
        completed_assignments=sum(
            1 for item in assignments if item.status == "Completed"
        ),
        unassigned_active_responses=sum(
            1
            for item in responses
            if item.status == "Active" and item.id not in assigned_response_ids
        ),
        priority_breakdown=dict(sorted(priority_breakdown.items())),
        category_breakdown=dict(sorted(category_breakdown.items())),
        source_breakdown=dict(sorted(source_breakdown.items())),
        location_breakdown=dict(
            sorted(location_breakdown.items(), key=lambda item: (-item[1], item[0]))
        ),
        missing_location_responses=sum(
            1 for item in responses if not (item.location or "").strip()
        ),
        weekly_activity_from=trend_start,
        weekly_activity_to=report_end,
        weekly_activity=weekly_activity,
    )

    filters = ReportFilters(
        from_date=from_date,
        to_date=to_date,
        team_id=team_id,
        team_name=team.name if team else None,
    )
    return summary, responses, assignments, source_by_response, filters


def build_summary(
    db: Session,
    from_date: date | None = None,
    to_date: date | None = None,
    team_id: int | None = None,
) -> ReportSummary:
    summary, _, _, _, _ = _collect_report_data(db, from_date, to_date, team_id)
    return summary


def _breakdown_table(document: Document, title: str, values: dict[str, int]) -> None:
    document.add_heading(title, level=2)
    if not values:
        document.add_paragraph("No records in this category.")
        return
    table = document.add_table(rows=1, cols=2)
    table.style = "Light Shading Accent 1"
    table.rows[0].cells[0].text = "Category"
    table.rows[0].cells[1].text = "Count"
    for label, count in values.items():
        cells = table.add_row().cells
        cells[0].text = label
        cells[1].text = str(count)


def _weekly_activity_table(document: Document, summary: ReportSummary) -> None:
    document.add_heading("Weekly activity", level=2)
    document.add_paragraph(
        f"Trend window: {summary.weekly_activity_from.isoformat()} to "
        f"{summary.weekly_activity_to.isoformat()} (up to 26 weeks)."
    )
    if not summary.weekly_activity:
        document.add_paragraph("No activity in the selected trend window.")
        return
    table = document.add_table(rows=1, cols=3)
    table.style = "Light Shading Accent 1"
    for cell, label in zip(
        table.rows[0].cells, ["Week starting", "Responses created", "Assignments created"]
    ):
        cell.text = label
    for week in summary.weekly_activity:
        cells = table.add_row().cells
        cells[0].text = week.week_start.isoformat()
        cells[1].text = str(week.responses_created)
        cells[2].text = str(week.assignments_created)


def _response_table(
    document: Document,
    title: str,
    responses: list[ResponseItem],
    source_by_response: dict[int, str],
) -> None:
    document.add_heading(title, level=1)
    table = document.add_table(rows=1, cols=6)
    table.style = "Light Shading Accent 1"
    for cell, label in zip(
        table.rows[0].cells,
        ["Reference", "Title", "Category", "Priority", "Source", "Location"],
    ):
        cell.text = label
    for item in responses:
        cells = table.add_row().cells
        for cell, value in zip(
            cells,
            [
                item.reference_code,
                item.title,
                item.category or "",
                item.priority or "",
                source_by_response.get(item.id, "coordinator"),
                item.location or "",
            ],
        ):
            cell.text = value


def _assignment_table(
    document: Document,
    title: str,
    assignments: list[Assignment],
) -> None:
    document.add_heading(title, level=1)
    table = document.add_table(rows=1, cols=5)
    table.style = "Light Shading Accent 1"
    for cell, label in zip(
        table.rows[0].cells,
        ["Reference", "Response", "Team", "Status", "Task details"],
    ):
        cell.text = label
    for item in assignments:
        cells = table.add_row().cells
        for cell, value in zip(
            cells,
            [
                item.reference_code or "",
                item.response.reference_code,
                item.assigned_team.name,
                item.status,
                item.description or "",
            ],
        ):
            cell.text = value


def _filter_label(filters: ReportFilters) -> str:
    date_range = "All dates"
    if filters.from_date or filters.to_date:
        date_range = (
            f"{filters.from_date.isoformat() if filters.from_date else 'Beginning'}"
            f" to {filters.to_date.isoformat() if filters.to_date else 'Present'}"
        )
    team = filters.team_name or "All teams"
    return f"Date range: {date_range} · Team: {team}"


@router.get("/summary", response_model=ReportSummary)
def get_report_summary(
    from_date: date | None = None,
    to_date: date | None = None,
    team_id: int | None = Query(default=None, gt=0),
    db: Session = Depends(get_db),
):
    return build_summary(db, from_date, to_date, team_id)


@router.get("/preview", response_model=ReportPreview)
def get_report_preview(
    from_date: date | None = None,
    to_date: date | None = None,
    team_id: int | None = Query(default=None, gt=0),
    template: Literal["operational", "situation", "field"] = Query(
        default="operational"
    ),
    db: Session = Depends(get_db),
):
    summary, responses, assignments, source_by_response, filters = _collect_report_data(
        db, from_date, to_date, team_id
    )
    return ReportPreview(
        generated_at=datetime.utcnow(),
        template=template,
        filters=filters,
        summary=summary,
        responses=[
            ReportPreviewResponse(
                id=item.id,
                reference_code=item.reference_code,
                title=item.title,
                category=item.category,
                priority=item.priority,
                source_channel=source_by_response.get(item.id, "coordinator"),
                status=item.status,
                location=item.location,
                created_at=item.created_at,
            )
            for item in responses
        ],
        assignments=[
            ReportPreviewAssignment(
                id=item.id,
                reference_code=item.reference_code,
                response_reference=item.response.reference_code,
                response_title=item.response.title,
                team_name=item.assigned_team.name,
                status=item.status,
                description=item.description,
                created_at=item.created_at,
            )
            for item in assignments
        ],
    )


@router.get("/word")
def download_word_report(
    from_date: date | None = None,
    to_date: date | None = None,
    team_id: int | None = Query(default=None, gt=0),
    template: Literal["operational", "situation", "field"] = Query(
        default="operational"
    ),
    db: Session = Depends(get_db),
):
    summary, responses, assignments, source_by_response, filters = _collect_report_data(
        db, from_date, to_date, team_id
    )
    titles = {
        "operational": "CaseLoop Operational Report",
        "situation": "CaseLoop Situation Report",
        "field": "CaseLoop Field Action Brief",
    }
    document = Document()
    document.add_heading(titles[template], 0)
    document.add_paragraph(
        f"Generated {datetime.utcnow():%Y-%m-%d %H:%M} UTC. "
        f"{_filter_label(filters)}."
    )
    document.add_paragraph(
        "Figures are deterministic counts from approved response and assignment records."
    )

    document.add_heading("Operational summary", level=1)
    for label, value in (
        ("Total responses", summary.total_responses),
        ("Active responses", summary.active_responses),
        ("Resolved responses", summary.resolved_responses),
        ("Active responses without an assignment", summary.unassigned_active_responses),
        ("Total assignments", summary.total_assignments),
        ("Active assignments", summary.active_assignments),
        ("Completed assignments", summary.completed_assignments),
    ):
        document.add_paragraph(f"{label}: {value}")

    open_assignments = [
        item for item in assignments if item.status not in {"Completed", "Cancelled"}
    ]
    _weekly_activity_table(document, summary)
    if template == "operational":
        _breakdown_table(document, "Responses by priority", summary.priority_breakdown)
        _breakdown_table(document, "Responses by category", summary.category_breakdown)
        _breakdown_table(document, "Responses by source", summary.source_breakdown)
        _breakdown_table(document, "Responses by location", summary.location_breakdown)
        _response_table(document, "Approved response records", responses, source_by_response)
        _assignment_table(document, "Team assignments", assignments)
    elif template == "situation":
        _breakdown_table(document, "Responses by priority", summary.priority_breakdown)
        _breakdown_table(document, "Coverage by location", summary.location_breakdown)
        _response_table(document, "Situation overview", responses, source_by_response)
        _assignment_table(document, "Open team assignments", open_assignments)
    else:
        active_responses = [item for item in responses if item.status == "Active"]
        _breakdown_table(document, "Active responses by location", Counter(
            (item.location or "").strip() or "Location not recorded"
            for item in active_responses
        ))
        _response_table(
            document, "Active field responses", active_responses, source_by_response
        )
        _assignment_table(document, "Open field assignments", open_assignments)

    buffer = BytesIO()
    document.save(buffer)
    buffer.seek(0)
    return StreamingResponse(
        buffer,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        headers={"Content-Disposition": 'attachment; filename="caseloop-report.docx"'},
    )
