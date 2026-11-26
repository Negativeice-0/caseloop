#Requires -Version 5.1

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

# =====================================================
# Inputs
# =====================================================

$SessionSummary =
"docs\projects\overview\session-summary.md"

$LearningDir =
"docs\knowledge\master\learning"

$OutputFile =
Join-Path `
$LearningDir `
"latest-learning-extract.md"

# =====================================================
# Directory Setup
# =====================================================

if(!(Test-Path $LearningDir))
{
    New-Item `
        -ItemType Directory `
        -Force `
        -Path $LearningDir | Out-Null
}

# =====================================================
# Read Summary
# =====================================================

$SummaryContent = ""

if(Test-Path $SessionSummary)
{
    $SummaryContent =
        Get-Content `
        $SessionSummary `
        -Raw
}

# =====================================================
# Extract Verification Results
# =====================================================

$VerificationFiles =
Get-ChildItem `
    "docs\Auditing\data\snrlead" `
    -Recurse `
    -Filter *.md `
    -ErrorAction SilentlyContinue |
Sort-Object LastWriteTime -Descending

$LatestReview = ""

if($VerificationFiles.Count -gt 0)
{
    $LatestReview =
        Get-Content `
        $VerificationFiles[0].FullName `
        -Raw
}

# =====================================================
# Extract Lessons
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
    "Route inventories should come from authoritative registration sources."
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

$Lessons =
$Lessons |
Sort-Object -Unique

# =====================================================
# Extract Useful Files
# =====================================================

$UsefulFiles = @()

$SummaryContent `
-split "`r?`n" |
ForEach-Object {

    if($_ -match '\.py$')
    {
        $UsefulFiles += $_.Trim()
    }

    if($_ -match '\.tsx$')
    {
        $UsefulFiles += $_.Trim()
    }

    if($_ -match '\.ts$')
    {
        $UsefulFiles += $_.Trim()
    }
}

$UsefulFiles =
$UsefulFiles |
Sort-Object -Unique

# =====================================================
# Extract Useful Scripts
# =====================================================

$Scripts =
Get-ChildItem `
scripts `
-Recurse `
-Filter *.ps1 `
-ErrorAction SilentlyContinue |
Select-Object -ExpandProperty FullName

# =====================================================
# Build Knowledge Output
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
    ($Scripts |
        Select-Object -First 20 |
        ForEach-Object {
            "- $_"
        }) -join "`r`n"
}
else
{
    "- No scripts found"
}

$Content = @"
# Learning Extraction

Generated:
$(Get-Date)

---

## Engineering Lessons

$LessonText

---

## Future Rules

- Evidence is more important than assumptions.
- Verification is more important than PASS messages.
- Discover once and consume normalized artifacts.
- Use authoritative sources before repository-wide scans.

---

## Useful Files

$FileText

---

## Useful Scripts

$ScriptText

---

## Latest Review Reference

$(
if($VerificationFiles.Count -gt 0)
{
    $VerificationFiles[0].FullName
}
else
{
    "No review found"
}
)

---

## Recommended Next Learning Goal

Continue the active engineering step before running another learning extraction.

Only run learning extraction after:

- checkpoint completion
- audit completion
- deployment completion
- major refactoring
- major bug resolution
"@

# =====================================================
# Save
# =====================================================

$Content |
Set-Content `
-Path $OutputFile `
-Encoding UTF8

Write-Host ""
Write-Host "PASS"
Write-Host "Learning extraction created:"
Write-Host $OutputFile