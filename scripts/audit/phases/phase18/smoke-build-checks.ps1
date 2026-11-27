#Requires -Version 5.1

param(
    [string]$Root = "."
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$Root = (Resolve-Path $Root).Path
$RawDir = Join-Path $Root "docs\Auditing\data\rawshell\phase18"
$ControlDir = Join-Path $Root "docs\Auditing\control"
$BackendDir = Join-Path $Root "backend"
$FrontendDir = Join-Path $Root "frontend"
$Python = Join-Path $BackendDir "venv\Scripts\python.exe"
$PackagePath = Join-Path $FrontendDir "package.json"
$Npm = Get-Command "npm.cmd" -ErrorAction SilentlyContinue

foreach($Path in @($Python, $PackagePath))
{
    if(-not (Test-Path -LiteralPath $Path -PathType Leaf))
    {
        throw "Required smoke/build input is missing: $Path"
    }
}
if(-not $Npm)
{
    throw "npm.cmd is not available on PATH."
}

New-Item -ItemType Directory -Force -Path $RawDir | Out-Null
New-Item -ItemType Directory -Force -Path $ControlDir | Out-Null

$BackendResultPath = Join-Path $RawDir "backend-pytest.txt"
$FrontendResultPath = Join-Path $RawDir "frontend-production-build.txt"
$BackendOutput = @()
$FrontendOutput = @()

Push-Location $BackendDir
try
{
    $BackendOutput = @(& $Python -m pytest -q 2>&1)
    $BackendExitCode = $LASTEXITCODE
}
finally
{
    Pop-Location
}

Push-Location $FrontendDir
try
{
    $FrontendOutput = @(& $Npm.Source run build 2>&1)
    $FrontendExitCode = $LASTEXITCODE
}
finally
{
    Pop-Location
}

function Write-SanitizedResult
{
    param(
        [string]$Path,
        [string[]]$Header,
        [object[]]$Lines,
        [int]$ExitCode
    )

    $SanitizedLines = foreach($Line in $Lines)
    {
        [regex]::Replace(
            $Line.ToString(),
            "[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
            "[redacted email]"
        )
    }
    $Content = @($Header) + @($SanitizedLines) + @("Exit code: $ExitCode")
    [System.IO.File]::WriteAllLines($Path, [string[]]$Content, [System.Text.Encoding]::UTF8)
}

Write-SanitizedResult `
    -Path $BackendResultPath `
    -Header @("Command: backend/venv/Scripts/python.exe -m pytest -q", "Working directory: backend", "") `
    -Lines $BackendOutput `
    -ExitCode $BackendExitCode
Write-SanitizedResult `
    -Path $FrontendResultPath `
    -Header @("Command: npm run build", "Working directory: frontend", "") `
    -Lines $FrontendOutput `
    -ExitCode $FrontendExitCode

$EvidenceFiles = @("backend-pytest.txt", "frontend-production-build.txt")
$Manifest = [ordered]@{
    phase = "phase18"
    objective = "Smoke Tests and Build Verification"
    generated = (Get-Date).ToString("yyyy-MM-dd HH:mm:ss")
    evidenceFiles = $EvidenceFiles
    evidenceCount = $EvidenceFiles.Count
    primaryEvidence = $EvidenceFiles
    notes = @(
        "Backend pytest and frontend production build were run; each exit code is recorded."
        "Email addresses in captured output are redacted."
    )
}
$Manifest |
    ConvertTo-Json -Depth 20 |
    Set-Content -LiteralPath (Join-Path $RawDir "rawshell-manifest.json") -Encoding UTF8

$PhaseControl = [ordered]@{
    phase = "phase18"
    phaseNumber = 18
    objective = "Smoke Tests and Build Verification"
    status = "REVIEW REQUIRED"
    factExtractors = @(
        @{
            file = "backend-pytest.txt"
            type = "contains"
            search = "Exit code: 0"
            label = "Backend test suite exited successfully"
        },
        @{
            file = "frontend-production-build.txt"
            type = "contains"
            search = "Exit code: 0"
            label = "Frontend production build exited successfully"
        }
    )
    importantFiles = @(
        "backend/tests/test_assignments.py"
        "frontend/package.json"
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
        "Backend pytest suite"
        "Frontend TypeScript check and Vite production build"
    )
    nextAction = "Update verified documentation in Phase 19."
    generatedBy = "CASELOOP"
}
foreach($ControlPath in @(
    (Join-Path $ControlDir "phase18.json"),
    (Join-Path $ControlDir "current-phase.json")
))
{
    $PhaseControl |
        ConvertTo-Json -Depth 20 |
        Set-Content -LiteralPath $ControlPath -Encoding UTF8
}

Write-Host "Backend pytest exit code: $BackendExitCode"
Write-Host "Frontend build exit code: $FrontendExitCode"
Write-Host "Evidence: $RawDir"

if($BackendExitCode -ne 0 -or $FrontendExitCode -ne 0)
{
    throw "One or more Phase 18 checks failed. Review the recorded evidence."
}
