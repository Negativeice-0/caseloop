# CaseLoop Checkpoint 7 — Weekly Trends and Report Formats

**Date:** November 13, 2026  
**Status:** Implemented and locally verified.

## What changed

- Added weekly response and assignment creation counts to report summaries, with an exact eight-week default and a cap of 26 calendar-week buckets for explicitly longer ranges. The summary includes the exact trend-window dates.
- Added location coverage based on recorded location text and a count of approved responses with no recorded location. This is not geocoded or map-based analysis.
- Added Operational, Situation, and Field Action Brief report formats. The frontend preview and Word export pass the same date, team, and template selections.
- Operational reports include full breakdowns and records; situation reports emphasize priority, location coverage, and open assignments; field briefs focus on active responses by location and open assignments.
- Added test coverage for date/team-filtered weekly buckets, location/missing-location counts, and each preview/DOCX format. No database migration was needed.

## Verification

- Backend suite: **27 passed** with 7 existing dependency deprecation warnings using `backend\venv\Scripts\python.exe -m pytest -q`.
- Frontend TypeScript check and production build: **passed** using `frontend\npm.cmd run build`.
- Docker API image rebuilt successfully. The API health check reports PostgreSQL, the PostgreSQL 16 container is healthy, and the report routes expose the new template and summary fields.
- The updated Vite UI is responding at `http://127.0.0.1:5173`.

## Files and references

- [Implementation notes](../caseloop/IMPLEMENTATION.md)
- [Project overview](../caseloop/OVERVIEW.md)

The reports use deterministic structured data. Location strings are not coordinates; unreviewed intake remains excluded. Public hosting and a live Meta WhatsApp test remain blocked on provider configuration, public HTTPS, and organizational approval.
