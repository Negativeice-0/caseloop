#Requires -Version 5.1

param(
    [string]$Root = "."
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$Root = (Resolve-Path $Root).Path
$RawDir = Join-Path $Root "docs\Auditing\data\rawshell\phase17"
$ControlDir = Join-Path $Root "docs\Auditing\control"
$PackagePath = Join-Path $Root "frontend\package.json"
$SourceDir = Join-Path $Root "frontend\src"
$NavigationResultsPath = Join-Path $RawDir "frontend-navigation-results.txt"

foreach($Path in @($PackagePath, $SourceDir, $NavigationResultsPath))
{
    if(-not (Test-Path -LiteralPath $Path))
    {
        throw "Required frontend navigation audit input is missing: $Path"
    }
}

New-Item -ItemType Directory -Force -Path $RawDir | Out-Null
New-Item -ItemType Directory -Force -Path $ControlDir | Out-Null

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

$CapabilityLines = @(
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
$CapabilityPath = Join-Path $RawDir "frontend-test-capability.txt"
$CapabilityLines | Set-Content -LiteralPath $CapabilityPath -Encoding UTF8

$EvidenceFiles = @(
    "frontend-navigation-results.txt"
    "frontend-test-capability.txt"
)
$Manifest = [ordered]@{
    phase = "phase17"
    objective = "Frontend Navigation Testing"
    generated = (Get-Date).ToString("yyyy-MM-dd HH:mm:ss")
    evidenceFiles = $EvidenceFiles
    evidenceCount = $EvidenceFiles.Count
    primaryEvidence = @("frontend-navigation-results.txt")
    notes = @("Navigation interactions were manually checked in the integrated browser; test capability was inventoried.")
}
$Manifest |
    ConvertTo-Json -Depth 20 |
    Set-Content -LiteralPath (Join-Path $RawDir "rawshell-manifest.json") -Encoding UTF8

$PhaseControl = [ordered]@{
    phase = "phase17"
    phaseNumber = 17
    objective = "Frontend Navigation Testing"
    status = "REVIEW REQUIRED"
    factExtractors = @(
        @{
            file = "frontend-navigation-results.txt"
            type = "contains"
            search = "Officer Profile selected the Account & Security view. PASS"
            label = "Responder navigation interaction results recorded"
        },
        @{
            file = "frontend-test-capability.txt"
            type = "contains"
            search = "No .test. or .spec. files found"
            label = "No frontend source test files detected"
        }
    )
    importantFiles = @(
        "frontend/package.json"
        "frontend/src/App.tsx"
        "frontend/src/layouts/MainLayout.tsx"
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
        "Register tab selection"
        "Teams tab selection"
        "Timeline tab selection"
        "Responder mobile More menu and profile navigation"
    )
    nextAction = "Run backend smoke tests and frontend production build in Phase 18."
    generatedBy = "CASELOOP"
}
foreach($ControlPath in @(
    (Join-Path $ControlDir "phase17.json"),
    (Join-Path $ControlDir "current-phase.json")
))
{
    $PhaseControl |
        ConvertTo-Json -Depth 20 |
        Set-Content -LiteralPath $ControlPath -Encoding UTF8
}

Write-Host "PASS Phase 17 evidence and frontend test capability generated."
Write-Host "Evidence: $RawDir"
