#Requires -Version 5.1

<#
========================================================================
LEARN EXTRACT

Purpose
-------
Generate long-term engineering knowledge from the current phase.

Input
-----
docs\Auditing\data\snrlead\<phase>\verification.md

Output
------
docs\knowledge\master\learning\latest-learning-extract.md

Usage
-----

.\learn-extract.ps1 -Phase phase7

When To Run
-----------

✅ Phase complete

✅ Major checkpoint complete

✅ Major debugging session complete

✅ Deployment complete

✅ Refactor complete

❌ Every work session

❌ Every script execution

Notes
-----

This script extracts:

- engineering lessons
- future rules
- useful files
- useful scripts

This script does NOT:

- update session state
- generate verification
- generate inventories

Those belong elsewhere.

========================================================================
#>

param(
    [Parameter(Mandatory)]
    [string]$Phase
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

# =====================================================
# Paths
# =====================================================

$SessionSummary =
"docs\Auditing\data\snrlead\$Phase\verification.md"

$LearningDir =
"docs\knowledge\master\learning"

$OutputFile =
Join-Path `
$LearningDir `
"latest-learning-extract.md"

# =====================================================
# Setup
# =====================================================

if(!(Test-Path $LearningDir))
{
    New-Item `
        -ItemType Directory `
        -Force `
        -Path $LearningDir | Out-Null
}

# =====================================================
# Read Source
# =====================================================

$SummaryContent = ""

if(Test-Path $SessionSummary)
{
    $SummaryContent =
        Get-Content `
        $SessionSummary `
        -Raw
}
else
{
    throw "Missing: $SessionSummary"
}

# =====================================================
# Lessons
# =====================================================

$Lessons = @()

if($SummaryContent -match "authorization")
{
    $Lessons +=
    "Authorization inventories must be normalized before matrix generation."
}

if($SummaryContent -match "verification")
{
    $Lessons +=
    "PASS messages do not replace artifact verification."
}

if($SummaryContent -match "route")
{
    $Lessons +=
    "Route inventories should come from authoritative sources."
}

if($SummaryContent -match "dependency")
{
    $Lessons +=
    "Dependency tracing should happen before refactoring."
}

if($SummaryContent -match "matrix")
{
    $Lessons +=
    "Normalized evidence is more useful than raw search results."
}

$Lessons = @(
    $Lessons |
    Sort-Object -Unique
)

# =====================================================
# Useful Files
# =====================================================

$UsefulFiles = @()

$SummaryContent `
-split "`r?`n" |
ForEach-Object {

    if(
        $_ -match '^[a-zA-Z0-9_\/\\\.\-\*]+\.(py|ts|tsx|js|jsx)$'
    )
    {
        $UsefulFiles += $_.Trim()
    }
}

$UsefulFiles = @(
    $UsefulFiles |
    Sort-Object -Unique
)

# =====================================================
# Current Phase Scripts
# =====================================================

$Scripts = @()

$PhaseScriptDir =
"scripts\audit\phases\$Phase"

if(Test-Path $PhaseScriptDir)
{
    $Scripts = @(
        Get-ChildItem `
            $PhaseScriptDir `
            -Filter *.ps1 `
            -File `
            -ErrorAction SilentlyContinue |
        Select-Object -ExpandProperty FullName
    )
}

# =====================================================
# Formatting
# =====================================================

$LessonText =
if($Lessons.Count -gt 0)
{
    ($Lessons | ForEach-Object {
        "- $_"
    }) -join "`r`n"
}
else
{
    "- No lessons extracted"
}

$FileText =
if($UsefulFiles.Count -gt 0)
{
    ($UsefulFiles | ForEach-Object {
        "- $_"
    }) -join "`r`n"
}
else
{
    "- No important files extracted"
}

$ScriptText =
if($Scripts.Count -gt 0)
{
    ($Scripts | ForEach-Object {
        "- $_"
    }) -join "`r`n"
}
else
{
    "- No phase scripts found"
}

# =====================================================
# Output
# =====================================================

$Content = @"
# Learning Extraction

Generated:
$(Get-Date)

Phase:
$Phase

---

## Engineering Lessons

$LessonText

---

## Future Rules

- Evidence is more important than assumptions.
- Verification is more important than PASS messages.
- Discover once and reuse normalized artifacts.
- Prefer authoritative sources over repository scans.

---

## Useful Files

$FileText

---

## Useful Scripts

$ScriptText

---

## Source

$SessionSummary
"@

$Content |
Set-Content `
-Path $OutputFile `
-Encoding UTF8

Write-Host ""
Write-Host "PASS"
Write-Host "Learning extraction created:"
Write-Host $OutputFile