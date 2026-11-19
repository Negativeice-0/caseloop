# copy the below as is and create extract_audit

New-Item -ItemType Directory -Force `
    -Path "scripts",
          "docs\auditing\data\fullstack\phase1",
          "docs\projects\progress" | Out-Null

$phase1Content = @'
# Full-Stack Audit — Phase 1

## Verified

- Backend root returned `200 OK`.
- Frontend root returned `200 OK`.
- Backend and frontend were reachable during the health check.
- No files were changed during the health check.

## Not verified

- Login success.
- Authentication behavior.
- Authorization behavior.
- Protected API requests.
- Database workflows.
- Frontend route correctness.

## Status

Phase 1 health verification is complete.

## Next step

Proceed to the next approved Checkpoint 14 checklist item.
'@

Set-Content `
    -Path "docs\auditing\data\fullstack\phase1\README.md" `
    -Value $phase1Content `
    -Encoding UTF8


$progressContent = @'
# Checkpoint 14 Progress

## Current status

Checkpoint 14 planning is complete. Phase 1 service health verification is complete.

## Completed

- Backend checked at `http://127.0.0.1:8000`.
- Frontend checked at `http://localhost:5173/`.
- Backend returned `200 OK`.
- Frontend returned `200 OK`.
- No files were changed during the check.

## Limitations

The health check confirms service availability only. It does not prove that login, authorization, protected API requests, database workflows, or frontend routes work correctly.

## Documentation

- Canonical plan: `docs/auditing/chkpnt14-plan/chkpnt14-plan`
- Phase 1 findings: `docs/auditing/data/fullstack/phase1/`
- This file: progress summary only.

## Recommendation

Keep the canonical plan unchanged. Keep only verified findings in the Phase 1 directory. Do not duplicate the full plan or store large raw terminal output in the progress document.

## Next step

Confirm the working tree is safe, then proceed to the next approved Checkpoint 14 checklist item.
'@

Set-Content `
    -Path "docs\projects\progress\chpnt14.md" `
    -Value $progressContent `
    -Encoding UTF8


$summaryContent = @'
# Final Session Summary

## Work completed

Organized the Checkpoint 14 progress summary and Phase 1 audit findings. Confirmed that the backend and frontend health checks returned HTTP `200 OK`.

## Effectiveness

9/10. The session established clear documentation boundaries and preserved the distinction between service availability and untested application behavior.

## Skills applied

PowerShell inspection, HTTP health verification, evidence classification, and documentation organization.

## Problems encountered

Documentation duplication and uncertainty about retaining raw terminal output.

## Resolution

Raw terminal data should be reviewed before deletion. Only verified conclusions need to remain in the project documentation.

## Remaining limitations

Authentication, authorization, protected API behavior, database workflows, and frontend route behavior remain untested.

## Status

Phase 1 health verification is complete.
'@

Set-Content `
    -Path "docs\projects\progress\chpnt14-session-summary.md" `
    -Value $summaryContent `
    -Encoding UTF8


$extractContent = @'
# scripts/extract_audit.ps1

param(
    [Parameter(Mandatory = $true)]
    [string]$InputFile
)

$ErrorActionPreference = "Stop"

if (-not (Test-Path $InputFile)) {
    Write-Host "❌ Input file not found: $InputFile" -ForegroundColor Red
    exit 1
}

$lines = Get-Content $InputFile

$patterns = [ordered]@{
    "Commands"  = "Invoke-WebRequest|Get-|Set-|git |docker |npm |python |pytest|curl"
    "Results"   = "200|201|204|401|403|404|500|passed|failed|success|OK|error"
    "Files"     = "\.(py|js|jsx|ts|tsx|md|json|yml|yaml|ps1)\b"
    "Problems"  = "error|failed|failure|issue|problem|blocked|warning|unresolved"
    "Decisions" = "decision|decided|deferred|keep|delete|avoid|recommend"
}

Write-Host ""
Write-Host "🔍 Extracting useful audit information..." -ForegroundColor Cyan
Write-Host ""

foreach ($section in $patterns.Keys) {
    Write-Host "## $section" -ForegroundColor Yellow

    $matches = $lines |
        Where-Object { $_ -match $patterns[$section] } |
        Select-Object -Unique -First 12

    if ($matches) {
        foreach ($match in $matches) {
            Write-Host "  - $match" -ForegroundColor Green
        }
    }
    else {
        Write-Host "  - Not recorded" -ForegroundColor DarkGray
    }

    Write-Host ""
}

Write-Host "✅ Extraction complete. Raw data was not changed." -ForegroundColor Cyan
'@

Set-Content `
    -Path "scripts\extract_audit.ps1" `
    -Value $extractContent `
    -Encoding UTF8

Write-Host ""
Write-Host "✅ Documentation and audit scripts created or updated." `
    -ForegroundColor Cyan