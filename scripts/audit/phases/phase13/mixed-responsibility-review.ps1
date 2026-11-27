#Requires -Version 5.1

param(
    [string]$Root = "."
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$Root = (Resolve-Path $Root).Path
$RawDir = Join-Path $Root "docs\Auditing\data\rawshell\phase13"
$ControlDir = Join-Path $Root "docs\Auditing\control"
$Files = @(
    "frontend\src\App.tsx"
    "frontend\src\layouts\MainLayout.tsx"
    "frontend\src\features\workflow\WorkflowViews.tsx"
    "frontend\src\features\admin\AdminControl.tsx"
    "frontend\src\features\assignments\AssignmentsManager.tsx"
)

New-Item -ItemType Directory -Force -Path $RawDir | Out-Null
New-Item -ItemType Directory -Force -Path $ControlDir | Out-Null

$Metrics = @()
$Declarations = @("Exported component and local orchestration declarations:")
foreach($RelativePath in $Files)
{
    $Path = Join-Path $Root $RelativePath
    if(-not (Test-Path -LiteralPath $Path -PathType Leaf))
    {
        throw "Required responsibility review source is missing: $RelativePath"
    }

    $Lines = @(Get-Content -LiteralPath $Path)
    $Metrics += "$RelativePath | lines: $($Lines.Count) | bytes: $((Get-Item -LiteralPath $Path).Length)"

    foreach($Hit in @(Select-String -LiteralPath $Path -Pattern "^(export )?(default )?(function|const|interface|type) "))
    {
        $Declarations += "$RelativePath`:$($Hit.LineNumber): $($Hit.Line.Trim())"
    }
}

$WorkflowPath = Join-Path $Root "frontend\src\features\workflow\WorkflowViews.tsx"
foreach($Hit in @(Select-String -LiteralPath $WorkflowPath -Pattern "^export function (IntakeReview|TimelineView|ReportsView)"))
{
    $Declarations += "workflow boundary | $($Hit.LineNumber): $($Hit.Line.Trim())"
}

$MetricsPath = Join-Path $RawDir "component-metrics.txt"
$Metrics | Set-Content -LiteralPath $MetricsPath -Encoding UTF8

$DeclarationsPath = Join-Path $RawDir "component-boundaries.txt"
$Declarations | Set-Content -LiteralPath $DeclarationsPath -Encoding UTF8

$EvidenceFiles = @("component-metrics.txt", "component-boundaries.txt")
$Manifest = [ordered]@{
    phase = "phase13"
    objective = "Mixed Responsibility Refactor Review"
    generated = (Get-Date).ToString("yyyy-MM-dd HH:mm:ss")
    evidenceFiles = $EvidenceFiles
    evidenceCount = $EvidenceFiles.Count
    primaryEvidence = $EvidenceFiles
    notes = @("Component sizes and declaration boundaries recorded; no refactor performed.")
}
$Manifest |
    ConvertTo-Json -Depth 20 |
    Set-Content -LiteralPath (Join-Path $RawDir "rawshell-manifest.json") -Encoding UTF8

$PhaseControl = [ordered]@{
    phase = "phase13"
    phaseNumber = 13
    objective = "Mixed Responsibility Refactor Review"
    status = "REVIEW REQUIRED"
    factExtractors = @(
        @{
            file = "component-metrics.txt"
            type = "count-lines"
            label = "UI component files measured"
        },
        @{
            file = "component-boundaries.txt"
            type = "contains"
            search = "export function IntakeReview"
            label = "Workflow component boundary evidence present"
        },
        @{
            file = "component-boundaries.txt"
            type = "contains"
            search = "export function TimelineView"
            label = "Timeline component boundary evidence present"
        },
        @{
            file = "component-boundaries.txt"
            type = "contains"
            search = "export function ReportsView"
            label = "Reports component boundary evidence present"
        }
    )
    importantFiles = $Files
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
        "Review workflow view co-location"
        "Review admin control component boundaries"
        "Preserve role behavior and rendered output in any future refactor"
    )
    nextAction = "Trace references across the repository in Phase 14."
    generatedBy = "CASELOOP"
}
foreach($ControlPath in @(
    (Join-Path $ControlDir "phase13.json"),
    (Join-Path $ControlDir "current-phase.json")
))
{
    $PhaseControl |
        ConvertTo-Json -Depth 20 |
        Set-Content -LiteralPath $ControlPath -Encoding UTF8
}

Write-Host "PASS Phase 13 responsibility evidence generated."
Write-Host "Evidence: $RawDir"
