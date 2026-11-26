#Requires -Version 5.1

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

# ============================================================
# Paths
# ============================================================

$SummaryFile =
"docs\projects\overview\session-summary.md"

$Phase6Summary =
"docs\Auditing\data\fullstack\phase6\role-permission-matrix-summary.json"

$Phase6Verify =
"docs\Auditing\verification\phase6\verification-result.md"

# ============================================================
# Defaults
# ============================================================

$RouteCount = "Unknown"
$AuthEvidenceCount = "Unknown"
$MatrixRows = "Unknown"
$Roles = @()
$VerificationStatus = "Unknown"

# ============================================================
# Phase 6 Summary
# ============================================================

if(Test-Path $Phase6Summary)
{
    try
    {
        $Data =
            Get-Content $Phase6Summary -Raw |
            ConvertFrom-Json

        if($Data.PSObject.Properties["RouteCount"])
        {
            $RouteCount = $Data.RouteCount
        }

        if($Data.PSObject.Properties["AuthorizationEvidenceCount"])
        {
            $AuthEvidenceCount =
                $Data.AuthorizationEvidenceCount
        }

        if($Data.PSObject.Properties["MatrixRows"])
        {
            $MatrixRows = $Data.MatrixRows
        }

        if($Data.PSObject.Properties["Roles"])
        {
            $Roles = @($Data.Roles)
        }
    }
    catch
    {
        Write-Warning "Unable to parse phase6 summary"
    }
}

# ============================================================
# Verification Status
# ============================================================

if(Test-Path $Phase6Verify)
{
    $VerificationStatus =
        Get-Content $Phase6Verify -Raw |
        Select-Object -First 1
}

# ============================================================
# Role Text
# ============================================================

if($Roles.Count -gt 0)
{
    $RoleText =
        ($Roles | ForEach-Object {
            "- $_"
        }) -join "`r`n"
}
else
{
    $RoleText = "- none discovered"
}

# ============================================================
# Generate Session Summary
# ============================================================

$Content = @"
# Session Summary

## Metadata

Date: $(Get-Date -Format "yyyy-MM-dd HH:mm")

Verification Status:
$VerificationStatus

---

## Current Objective

Step 7

Frontend → Backend → Database Connection Map

---

## Last Verified State

Routes:
$RouteCount

Authorization Evidence:
$AuthEvidenceCount

Matrix Rows:
$MatrixRows

Roles:

$RoleText

---

## Verified Facts

Architecture:

Frontend
→ API Service Layer
→ FastAPI Backend
→ Services
→ Models
→ Database

Deployment:

Frontend:
npm / vite

Backend:
uvicorn

Container:
docker

Cloud:
Oracle pending

---

## Important Files

frontend/src/services/api.ts

backend/app/api/*.py

backend/app/services/*.py

backend/app/models/models.py

---

## Current Blocker

None recorded.

---

## Next Action

Complete Step 7 connection map.

Trace:

Frontend Feature
→ api.ts
→ Backend Route
→ Backend Service
→ Database Model

---

## Restart Instructions

1. Read control.md

2. Read this file

3. Read latest review

4. Continue Step 7

Do not rerun completed inventories.
"@

# ============================================================
# Output
# ============================================================

$Dir =
    Split-Path $SummaryFile -Parent

if(!(Test-Path $Dir))
{
    New-Item `
        -ItemType Directory `
        -Force `
        -Path $Dir | Out-Null
}

$Content |
    Set-Content `
    -Path $SummaryFile `
    -Encoding UTF8

Write-Host ""
Write-Host "PASS"
Write-Host "Updated:"
Write-Host $SummaryFile