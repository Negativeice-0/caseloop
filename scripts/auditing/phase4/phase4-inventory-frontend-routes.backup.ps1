# ===================================================================
# Phase 4
# Inventory Frontend Routes and Navigation Entries
# Evidence First
# ===================================================================

$ErrorActionPreference = "Continue"

$Phase = "phase4"

$RawDir       = "docs/auditing/data/rawshell/$Phase"
$FullDir      = "docs/auditing/data/fullstack/$Phase"
$LeadDir      = "docs/auditing/data/snrlead/$Phase"
$VerifyDir    = "docs/auditing/verification/$Phase"

New-Item -ItemType Directory -Force -Path $RawDir | Out-Null
New-Item -ItemType Directory -Force -Path $FullDir | Out-Null
New-Item -ItemType Directory -Force -Path $LeadDir | Out-Null
New-Item -ItemType Directory -Force -Path $VerifyDir | Out-Null

# -----------------------------------------------------------
# Baseline Metadata
# -----------------------------------------------------------

$Timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

git branch --show-current `
    > "$RawDir/git-branch.txt" 2>&1

git rev-parse HEAD `
    > "$RawDir/git-sha.txt" 2>&1

git status `
    > "$RawDir/git-status.txt" 2>&1

# -----------------------------------------------------------
# Authoritative Sources First
# -----------------------------------------------------------

$AuthorityPatterns = @(
    "main.tsx",
    "main.jsx",
    "App.tsx",
    "App.jsx",
    "*router*.ts",
    "*router*.tsx",
    "*routes*.ts",
    "*routes*.tsx"
)

Get-ChildItem -Recurse -File |
    Where-Object {
        $name = $_.Name.ToLower()

        ($AuthorityPatterns | Where-Object {
            $name -like $_.ToLower()
        }).Count -gt 0
    } |
    Select FullName |
    Out-File "$RawDir/authoritative-files.txt"

# -----------------------------------------------------------
# Route Registration Evidence
# -----------------------------------------------------------

$RouteEvidence = @()

Get-ChildItem src,app,pages,routes,features -Recurse -ErrorAction SilentlyContinue -File |
ForEach-Object {

    try {

        $content = Get-Content $_.FullName -Raw

        if(
            $content -match "createBrowserRouter" -or
            $content -match "createHashRouter" -or
            $content -match "<Route" -or
            $content -match "path:" -or
            $content -match "useRoutes"
        ) {
            $RouteEvidence += $_.FullName
        }

    } catch {}

}

$RouteEvidence |
Sort-Object -Unique |
Out-File "$RawDir/route-registration-files.txt"

# -----------------------------------------------------------
# Navigation Evidence
# -----------------------------------------------------------

$NavEvidence = @()

Get-ChildItem src,app,components,layouts,features `
    -Recurse `
    -ErrorAction SilentlyContinue `
    -File |
ForEach-Object {

    try {

        $content = Get-Content $_.FullName -Raw

        if(
            $content -match "Sidebar" -or
            $content -match "Navigation" -or
            $content -match "NavLink" -or
            $content -match "menuItems" -or
            $content -match "navigation"
        ) {
            $NavEvidence += $_.FullName
        }

    } catch {}

}

$NavEvidence |
Sort-Object -Unique |
Out-File "$RawDir/navigation-files.txt"

# -----------------------------------------------------------
# Session Summary Placeholder
# -----------------------------------------------------------

@"
# Session Summary

## Objective
Inventory frontend routes and navigation entries.

## Actions Performed
Evidence collection only.

## Evidence Captured
See rawshell artifacts.

## Findings
Pending review.

## Failures
None recorded.

## Root Causes
N/A

## Corrections Applied
None.

## Verification Status
Pending.

## Remaining Work
Review evidence and build verified inventory.

## Recommended Starting Point
Review authoritative route registrations first.
"@ | Set-Content "$FullDir/session-summary.md"

# -----------------------------------------------------------
# Verification Evidence
# -----------------------------------------------------------

@"
Verification pending analysis.
"@ | Set-Content "$VerifyDir/verification-evidence.md"

@"
FAIL

Reason:
Inventory not yet reviewed.

Root Cause:
Evidence collection complete but verification not performed.
"@ | Set-Content "$VerifyDir/verification-result.md"

Write-Host "Phase 4 evidence collection complete."
