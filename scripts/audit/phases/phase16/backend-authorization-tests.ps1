#Requires -Version 5.1

param(
    [string]$Root = "."
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$Root = (Resolve-Path $Root).Path
$RawDir = Join-Path $Root "docs\Auditing\data\rawshell\phase16"
$ControlDir = Join-Path $Root "docs\Auditing\control"
$BackendDir = Join-Path $Root "backend"
$Python = Join-Path $BackendDir "venv\Scripts\python.exe"
$TestFile = Join-Path $BackendDir "tests\test_assignments.py"

New-Item -ItemType Directory -Force -Path $RawDir | Out-Null
New-Item -ItemType Directory -Force -Path $ControlDir | Out-Null

foreach($Path in @($Python, $TestFile))
{
    if(-not (Test-Path -LiteralPath $Path -PathType Leaf))
    {
        throw "Required authorization test input is missing: $Path"
    }
}

$ResultPath = Join-Path $RawDir "backend-authorization-pytest.txt"
$TestSelector = "api_requires_session or admin_sign_in or admin_provisioned or admin_password_reset or demo_seed_requires or responder_only or session_logout or public_registration"
$Header = @(
    "Command: backend/venv/Scripts/python.exe -m pytest -q tests/test_assignments.py -k `"$TestSelector`""
    "Working directory: backend"
    ""
)

Push-Location $BackendDir
try
{
    $TestOutput = @(& $Python -m pytest -q tests/test_assignments.py -k $TestSelector 2>&1)
    $TestExitCode = $LASTEXITCODE
}
finally
{
    Pop-Location
}

$SanitizedOutput = foreach($Line in $TestOutput)
{
    [regex]::Replace(
        $Line.ToString(),
        "[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
        "[redacted email]"
    )
}
$Output = @($Header) + @($SanitizedOutput) + @("Exit code: $TestExitCode")
[System.IO.File]::WriteAllLines($ResultPath, [string[]]$Output, [System.Text.Encoding]::UTF8)

$EvidenceFiles = @("backend-authorization-pytest.txt")
$Manifest = [ordered]@{
    phase = "phase16"
    objective = "Backend Authorization Testing"
    generated = (Get-Date).ToString("yyyy-MM-dd HH:mm:ss")
    evidenceFiles = $EvidenceFiles
    evidenceCount = $EvidenceFiles.Count
    primaryEvidence = $EvidenceFiles
    notes = @("Focused authorization and session tests executed; exit status recorded.")
}
$Manifest |
    ConvertTo-Json -Depth 20 |
    Set-Content -LiteralPath (Join-Path $RawDir "rawshell-manifest.json") -Encoding UTF8

$PhaseControl = [ordered]@{
    phase = "phase16"
    phaseNumber = 16
    objective = "Backend Authorization Testing"
    status = "REVIEW REQUIRED"
    factExtractors = @(
        @{
            file = "backend-authorization-pytest.txt"
            type = "contains"
            search = "passed"
            label = "Pytest pass summary present"
        },
        @{
            file = "backend-authorization-pytest.txt"
            type = "contains"
            search = "Exit code: 0"
            label = "Focused authorization test process exited successfully"
        }
    )
    importantFiles = @(
        "backend/app/core/auth.py"
        "backend/app/core/security.py"
        "backend/app/api/auth.py"
        "backend/tests/test_assignments.py"
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
        "Session and CSRF enforcement"
        "Admin audience restrictions"
        "Responder data and assignment restrictions"
        "Public registration role constraints"
    )
    nextAction = "Run frontend navigation tests in Phase 17."
    generatedBy = "CASELOOP"
}
foreach($ControlPath in @(
    (Join-Path $ControlDir "phase16.json"),
    (Join-Path $ControlDir "current-phase.json")
))
{
    $PhaseControl |
        ConvertTo-Json -Depth 20 |
        Set-Content -LiteralPath $ControlPath -Encoding UTF8
}

if($TestExitCode -ne 0)
{
    throw "Focused authorization tests failed with exit code $TestExitCode. Review $ResultPath."
}

Write-Host "PASS Phase 16 authorization tests."
Write-Host "Evidence: $ResultPath"
