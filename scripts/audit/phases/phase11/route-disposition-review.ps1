#Requires -Version 5.1

param(
    [string]$Root = "."
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$Root = (Resolve-Path $Root).Path
$RawDir = Join-Path $Root "docs\Auditing\data\rawshell\phase11"
$ControlDir = Join-Path $Root "docs\Auditing\control"
$LayoutPath = Join-Path $Root "frontend\src\layouts\MainLayout.tsx"
$AppPath = Join-Path $Root "frontend\src\App.tsx"
$AuthPath = Join-Path $Root "frontend\src\features\auth\AuthGateway.tsx"
$ApiMainPath = Join-Path $Root "backend\app\main.py"
$RuntimeEvidencePath = Join-Path $Root "docs\Auditing\data\rawshell\phase10\ui-role-test-results.txt"

New-Item -ItemType Directory -Force -Path $RawDir | Out-Null
New-Item -ItemType Directory -Force -Path $ControlDir | Out-Null

foreach($Path in @($LayoutPath, $AppPath, $AuthPath, $ApiMainPath, $RuntimeEvidencePath))
{
    if(-not (Test-Path -LiteralPath $Path -PathType Leaf))
    {
        throw "Required route disposition evidence is missing: $Path"
    }
}

$TabEvidencePath = Join-Path $RawDir "tab-disposition-source.txt"
$TabEvidence = @()
foreach($Entry in @(
    [pscustomobject]@{ Path = $LayoutPath; Pattern = "export type TabType|onClick=.*(setActiveTab|selectTab)" },
    [pscustomobject]@{ Path = $AppPath; Pattern = "activeTab ===" }
))
{
    foreach($Hit in @(Select-String -LiteralPath $Entry.Path -Pattern $Entry.Pattern))
    {
        $RelativePath = $Hit.Path.Substring($Root.Length).TrimStart("\")
        $TabEvidence += "$RelativePath`:$($Hit.LineNumber): $($Hit.Line.Trim())"
    }
}
$TabEvidence | Set-Content -LiteralPath $TabEvidencePath -Encoding UTF8

$EntryEvidencePath = Join-Path $RawDir "entry-path-source.txt"
$EntryEvidence = @()
foreach($Entry in @(
    [pscustomobject]@{ Path = $AppPath; Pattern = "window\.location\.pathname|isAdminEntry" },
    [pscustomobject]@{ Path = $AuthPath; Pattern = "window\.location\.assign" }
))
{
    foreach($Hit in @(Select-String -LiteralPath $Entry.Path -Pattern $Entry.Pattern))
    {
        $RelativePath = $Hit.Path.Substring($Root.Length).TrimStart("\")
        $EntryEvidence += "$RelativePath`:$($Hit.LineNumber): $($Hit.Line.Trim())"
    }
}
$EntryEvidence | Set-Content -LiteralPath $EntryEvidencePath -Encoding UTF8

$ApiRouterEvidencePath = Join-Path $RawDir "api-router-registration.txt"
Select-String -LiteralPath $ApiMainPath -Pattern "include_router" |
    ForEach-Object {
        $RelativePath = $_.Path.Substring($Root.Length).TrimStart("\")
        "$RelativePath`:$($_.LineNumber): $($_.Line.Trim())"
    } |
    Set-Content -LiteralPath $ApiRouterEvidencePath -Encoding UTF8

$RuntimeEvidence = Join-Path $RawDir "runtime-entry-tests.txt"
Copy-Item -LiteralPath $RuntimeEvidencePath -Destination $RuntimeEvidence -Force

$EvidenceFiles = @(
    "tab-disposition-source.txt"
    "entry-path-source.txt"
    "api-router-registration.txt"
    "runtime-entry-tests.txt"
)

$Manifest = [ordered]@{
    phase = "phase11"
    objective = "Route Disposition Review"
    generated = (Get-Date).ToString("yyyy-MM-dd HH:mm:ss")
    evidenceFiles = $EvidenceFiles
    evidenceCount = $EvidenceFiles.Count
    primaryEvidence = @("tab-disposition-source.txt", "entry-path-source.txt", "runtime-entry-tests.txt")
    notes = @("Route dispositions are recommendations based on source and Phase 10 runtime evidence.")
}
$Manifest |
    ConvertTo-Json -Depth 20 |
    Set-Content -LiteralPath (Join-Path $RawDir "rawshell-manifest.json") -Encoding UTF8

$PhaseControl = [ordered]@{
    phase = "phase11"
    phaseNumber = 11
    objective = "Route Disposition Review"
    status = "REVIEW REQUIRED"
    factExtractors = @(
        @{
            file = "tab-disposition-source.txt"
            type = "count-lines"
            label = "Tab and renderer source matches"
        },
        @{
            file = "entry-path-source.txt"
            type = "contains"
            search = "'/admin'"
            label = "Admin entry path referenced"
        },
        @{
            file = "runtime-entry-tests.txt"
            type = "contains"
            search = "Coordinator direct /admin entry: Administrator access required."
            label = "Coordinator admin entry denial evidenced"
        }
    )
    importantFiles = @(
        "frontend/src/App.tsx"
        "frontend/src/layouts/MainLayout.tsx"
        "frontend/src/features/auth/AuthGateway.tsx"
        "backend/app/main.py"
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
        "Retain or refactor each workspace tab"
        "Retain authentication entry paths"
        "Determine whether any route is a deletion candidate"
    )
    nextAction = "Trace route references in Phase 12."
    generatedBy = "CASELOOP"
}

foreach($ControlPath in @(
    (Join-Path $ControlDir "phase11.json"),
    (Join-Path $ControlDir "current-phase.json")
))
{
    $PhaseControl |
        ConvertTo-Json -Depth 20 |
        Set-Content -LiteralPath $ControlPath -Encoding UTF8
}

Write-Host "PASS Phase 11 route disposition evidence generated."
Write-Host "Evidence: $RawDir"
