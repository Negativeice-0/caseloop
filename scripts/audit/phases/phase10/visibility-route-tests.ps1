#Requires -Version 5.1

param(
    [string]$Root = "."
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$Root = (Resolve-Path $Root).Path
$RawDir = Join-Path $Root "docs\Auditing\data\rawshell\phase10"
$ControlDir = Join-Path $Root "docs\Auditing\control"
$AppPath = Join-Path $Root "frontend\src\App.tsx"
$LayoutPath = Join-Path $Root "frontend\src\layouts\MainLayout.tsx"
$PackagePath = Join-Path $Root "frontend\package.json"
$SourceDir = Join-Path $Root "frontend\src"

New-Item -ItemType Directory -Force -Path $RawDir | Out-Null
New-Item -ItemType Directory -Force -Path $ControlDir | Out-Null

foreach($Path in @($AppPath, $LayoutPath, $PackagePath))
{
    if(-not (Test-Path -LiteralPath $Path -PathType Leaf))
    {
        throw "Required visibility-test source is missing: $Path"
    }
}

$Patterns = @(
    [pscustomobject]@{
        Path = $AppPath
        Pattern = "isAdminEntry|canCoordinate|currentUser\.role|activeTab ==="
        Label = "app"
    },
    [pscustomobject]@{
        Path = $LayoutPath
        Pattern = "currentUser\.role|setActiveTab|selectTab|aria-label"
        Label = "layout"
    }
)

$VisibilityEvidence = @("Role visibility and entry-point source matches:")
foreach($Entry in $Patterns)
{
    foreach($Hit in @(Select-String -LiteralPath $Entry.Path -Pattern $Entry.Pattern))
    {
        $RelativePath = $Hit.Path.Substring($Root.Length).TrimStart("\")
        $VisibilityEvidence +=
            "[$($Entry.Label)] $RelativePath`:$($Hit.LineNumber): $($Hit.Line.Trim())"
    }
}

$VisibilityEvidencePath = Join-Path $RawDir "visibility-source-evidence.txt"
$VisibilityEvidence |
    Set-Content -LiteralPath $VisibilityEvidencePath -Encoding UTF8

$Package = Get-Content -LiteralPath $PackagePath -Raw | ConvertFrom-Json
$TestScripts = @()
if($Package.scripts)
{
    foreach($Property in $Package.scripts.PSObject.Properties)
    {
        if($Property.Name -match "test")
        {
            $TestScripts += "$($Property.Name): $($Property.Value)"
        }
    }
}

$TestFiles = @(
    Get-ChildItem -LiteralPath $SourceDir -Recurse -File |
    Where-Object { $_.Name -match "\.(test|spec)\." }
)

$TestCapabilityPath = Join-Path $RawDir "frontend-test-capability.txt"
$TestCapabilityEvidence = @(
    "Frontend test scripts:"
    if($TestScripts.Count -gt 0) { $TestScripts } else { "None declared in frontend/package.json." }
    ""
    "Frontend source test files:"
    if($TestFiles.Count -gt 0)
    {
        $TestFiles | ForEach-Object { $_.FullName.Substring($Root.Length).TrimStart("\") }
    }
    else
    {
        "No .test. or .spec. files found under frontend/src."
    }
)
$TestCapabilityEvidence |
    Set-Content -LiteralPath $TestCapabilityPath -Encoding UTF8

$EntryEvidencePath = Join-Path $RawDir "entry-point-evidence.txt"
@(
    Select-String -LiteralPath $AppPath -Pattern "window\.location\.pathname|setActiveTab"
    Select-String -LiteralPath (Join-Path $Root "frontend\src\features\auth\AuthGateway.tsx") -Pattern "window\.location\.assign"
) |
    ForEach-Object {
        $RelativePath = $_.Path.Substring($Root.Length).TrimStart("\")
        "$RelativePath`:$($_.LineNumber): $($_.Line.Trim())"
    } |
    Set-Content -LiteralPath $EntryEvidencePath -Encoding UTF8

$EvidenceFiles = @(
    "visibility-source-evidence.txt"
    "frontend-test-capability.txt"
    "entry-point-evidence.txt"
)

$Manifest = [ordered]@{
    phase = "phase10"
    objective = "Visibility and Route Testing"
    generated = (Get-Date).ToString("yyyy-MM-dd HH:mm:ss")
    evidenceFiles = $EvidenceFiles
    evidenceCount = $EvidenceFiles.Count
    primaryEvidence = @("visibility-source-evidence.txt", "entry-point-evidence.txt")
    notes = @("Static role gates and test capabilities recorded; runtime assertions are separate evidence.")
}
$Manifest |
    ConvertTo-Json -Depth 20 |
    Set-Content -LiteralPath (Join-Path $RawDir "rawshell-manifest.json") -Encoding UTF8

$PhaseControl = [ordered]@{
    phase = "phase10"
    phaseNumber = 10
    objective = "Visibility and Route Testing"
    status = "REVIEW REQUIRED"
    factExtractors = @(
        @{
            file = "visibility-source-evidence.txt"
            type = "contains"
            search = "currentUser.role === 'admin'"
            label = "Admin-only visibility gate present"
        },
        @{
            file = "frontend-test-capability.txt"
            type = "contains"
            search = "No .test. or .spec. files found"
            label = "No frontend source test files detected"
        },
        @{
            file = "entry-point-evidence.txt"
            type = "contains"
            search = "'/admin'"
            label = "Admin entry-point evidence present"
        }
    )
    importantFiles = @(
        "frontend/src/App.tsx"
        "frontend/src/layouts/MainLayout.tsx"
        "frontend/src/features/auth/AuthGateway.tsx"
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
        "Responder cannot open coordinator/admin views"
        "Coordinator sees intake and reports but not admin controls"
        "Admin sees all views"
        "Authentication entry paths load expected screens"
    )
    nextAction = "Review route disposition in Phase 11."
    generatedBy = "CASELOOP"
}

foreach($ControlPath in @(
    (Join-Path $ControlDir "phase10.json"),
    (Join-Path $ControlDir "current-phase.json")
))
{
    $PhaseControl |
        ConvertTo-Json -Depth 20 |
        Set-Content -LiteralPath $ControlPath -Encoding UTF8
}

Write-Host "PASS Phase 10 source evidence generated."
Write-Host "Evidence: $RawDir"
Write-Host "Control: $(Join-Path $ControlDir 'phase10.json')"
