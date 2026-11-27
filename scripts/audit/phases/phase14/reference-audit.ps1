#Requires -Version 5.1

param(
    [string]$Root = "."
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$Root = (Resolve-Path $Root).Path
$RawDir = Join-Path $Root "docs\Auditing\data\rawshell\phase14"
$ControlDir = Join-Path $Root "docs\Auditing\control"
New-Item -ItemType Directory -Force -Path $RawDir | Out-Null
New-Item -ItemType Directory -Force -Path $ControlDir | Out-Null

$SearchRoots = @(
    "frontend\src"
    "frontend\package.json"
    "frontend\package-lock.json"
    "backend\app"
    "backend\tests"
    "README.md"
    "docs\deployment"
    "docs\design"
)
$Extensions = @(".py", ".ts", ".tsx", ".js", ".jsx", ".json", ".md", ".mmd", ".ps1")
$Excluded = @(
    '[\\/]\.git[\\/]'
    '[\\/]node_modules[\\/]'
    '[\\/](venv|\.venv|__pycache__)[\\/]'
    '[\\/](dist|build|coverage|\.pytest_cache)[\\/]'
)

$Files = @()
foreach($RelativeRoot in $SearchRoots)
{
    $Path = Join-Path $Root $RelativeRoot
    if(-not (Test-Path -LiteralPath $Path))
    {
        continue
    }

    if((Get-Item -LiteralPath $Path).PSIsContainer)
    {
        $Files += Get-ChildItem -LiteralPath $Path -Recurse -File |
            Where-Object { $_.Extension -in $Extensions }
    }
    else
    {
        $Files += Get-Item -LiteralPath $Path
    }
}
$Files = @(
    $Files |
    Sort-Object -Property FullName -Unique |
    Where-Object {
        $CurrentPath = $_.FullName
        $CurrentPath -notlike "*\docs\deployment\FinaSteps.md" -and
        -not ($Excluded | Where-Object { $CurrentPath -match $_ })
    }
)

if($Files.Count -eq 0)
{
    throw "No first-party files were found in the reference audit scope."
}

$Candidates = [ordered]@{
    "react-router-dom" = "react-router-dom"
    "IntakeReview" = "\bIntakeReview\b"
    "TimelineView" = "\bTimelineView\b"
    "ReportsView" = "\bReportsView\b"
    "ResponseRegister" = "\bResponseRegister\b"
    "AssignmentsManager" = "\bAssignmentsManager\b"
    "AdminControl" = "\bAdminControl\b"
    "UserProfile" = "\bUserProfile\b"
    "MainLayout" = "\bMainLayout\b"
    "getIntakes" = "\bgetIntakes\b"
    "getTimelineFeed" = "\bgetTimelineFeed\b"
    "getReportPreview" = "\bgetReportPreview\b"
}

$ReferenceLines = @()
foreach($Candidate in $Candidates.Keys)
{
    $MatchesFound = @(
        Select-String `
            -Path $Files.FullName `
            -Pattern $Candidates[$Candidate]
    )
    $ReferenceLines += "CANDIDATE: $Candidate | matching lines: $($MatchesFound.Count)"
    foreach($Hit in $MatchesFound)
    {
        $RelativePath = $Hit.Path.Substring($Root.Length).TrimStart("\")
        $ReferenceLines += "  $RelativePath`:$($Hit.LineNumber): $($Hit.Line.Trim())"
    }
}
$ReferencePath = Join-Path $RawDir "target-reference-map.txt"
$ReferenceLines | Set-Content -LiteralPath $ReferencePath -Encoding UTF8

$FrontendSourceFiles = @(
    Get-ChildItem -LiteralPath (Join-Path $Root "frontend\src") -Recurse -File |
    Where-Object { $_.Extension -in @(".ts", ".tsx", ".js", ".jsx") }
)
$RouterSourceHits = @(
    Select-String -Path $FrontendSourceFiles.FullName -SimpleMatch -Pattern "react-router-dom"
)
$RouterEvidencePath = Join-Path $RawDir "router-reference-audit.txt"
$RouterEvidence = @(
    "First-party frontend source imports:"
    if($RouterSourceHits.Count -gt 0)
    {
        $RouterSourceHits |
            ForEach-Object {
                "$($_.Path.Substring($Root.Length).TrimStart("\"))`:$($_.LineNumber): $($_.Line.Trim())"
            }
    }
    else
    {
        "None found in frontend/src."
    }
    ""
    "Dependency metadata references:"
    Select-String `
        -Path (Join-Path $Root "frontend\package.json"), (Join-Path $Root "frontend\package-lock.json") `
        -SimpleMatch `
        -Pattern "react-router-dom" |
        ForEach-Object {
            "$($_.Path.Substring($Root.Length).TrimStart("\"))`:$($_.LineNumber): $($_.Line.Trim())"
        }
)
$RouterEvidence | Set-Content -LiteralPath $RouterEvidencePath -Encoding UTF8

$EvidenceFiles = @("target-reference-map.txt", "router-reference-audit.txt")
$Manifest = [ordered]@{
    phase = "phase14"
    objective = "Reference Audit"
    generated = (Get-Date).ToString("yyyy-MM-dd HH:mm:ss")
    evidenceFiles = $EvidenceFiles
    evidenceCount = $EvidenceFiles.Count
    primaryEvidence = $EvidenceFiles
    notes = @("Targeted first-party code, tests, scripts, and selected deployment/design docs searched; generated dependencies excluded.")
}
$Manifest |
    ConvertTo-Json -Depth 20 |
    Set-Content -LiteralPath (Join-Path $RawDir "rawshell-manifest.json") -Encoding UTF8

$PhaseControl = [ordered]@{
    phase = "phase14"
    phaseNumber = 14
    objective = "Reference Audit"
    status = "REVIEW REQUIRED"
    factExtractors = @(
        @{
            file = "target-reference-map.txt"
            type = "count-matches"
            search = "CANDIDATE:"
            label = "Candidate reference groups"
        },
        @{
            file = "router-reference-audit.txt"
            type = "contains"
            search = "None found in frontend/src."
            label = "No router source imports found"
        },
        @{
            file = "router-reference-audit.txt"
            type = "contains"
            search = "frontend\package.json"
            label = "Router dependency is declared in package metadata"
        }
    )
    importantFiles = @(
        "frontend/src"
        "frontend/package.json"
        "frontend/package-lock.json"
        "backend/app"
        "backend/tests"
    )
    expectedEvidence = $EvidenceFiles
    expectedArtifacts = @(
        "normalized.json"
        "keyword-frequency.json"
        "evidence-excerpts.md"
        "findings.md"
        "summary.md"
        "verification.md"
        "logbook.md"
    )
    validationCandidates = @(
        "Trace all references before marking any candidate unused"
        "Include runtime, tests, configuration, and deployment documentation"
        "Carry only evidence-supported deletion candidates into Phase 15"
    )
    nextAction = "Review deletion candidates in Phase 15."
    generatedBy = "CASELOOP"
}
foreach($ControlPath in @(
    (Join-Path $ControlDir "phase14.json"),
    (Join-Path $ControlDir "current-phase.json")
))
{
    $PhaseControl |
        ConvertTo-Json -Depth 20 |
        Set-Content -LiteralPath $ControlPath -Encoding UTF8
}

Write-Host "PASS Phase 14 reference evidence generated."
Write-Host "Files searched: $($Files.Count)"
Write-Host "Evidence: $RawDir"
