# To run:
# .\scripts\verify_baseline.ps1

$ErrorActionPreference = "Stop"

$Root = (Get-Location).Path
$Stamp = Get-Date -Format "yyyyMMdd-HHmmss"
$BaselineDir = Join-Path $env:TEMP "CaseLoop-Baseline-$Stamp"

New-Item -ItemType Directory -Path $BaselineDir -Force | Out-Null

Write-Host ""
Write-Host "🔍 Running CaseLoop baseline verification..." -ForegroundColor Cyan
Write-Host "Root: $Root"
Write-Host "Logs: $BaselineDir"

$Requirements = Join-Path $Root "backend\requirements.txt"
$BackendTests = Join-Path $Root "backend\tests"
$PackageJson = Join-Path $Root "frontend\package.json"

if (-not (Test-Path $Requirements)) {
    throw "Missing backend\requirements.txt"
}

if (-not (Test-Path $BackendTests)) {
    throw "Missing backend\tests directory"
}

if (-not (Test-Path $PackageJson)) {
    throw "Missing frontend\package.json"
}

$HasPytest = Get-Content $Requirements |
    Where-Object { $_ -match "^\s*pytest([<>=!~]|$)" }

$Package = Get-Content $PackageJson -Raw | ConvertFrom-Json

if (-not $HasPytest) {
    throw "pytest was not listed in backend\requirements.txt"
}

if ($null -eq $Package.scripts.build) {
    throw "No frontend build script was found in frontend\package.json"
}

Write-Host ""
Write-Host "## Backend test runner" -ForegroundColor Yellow

$PythonCandidates = @(
    (Join-Path $Root "backend\.venv\Scripts\python.exe"),
    (Join-Path $Root ".venv\Scripts\python.exe"),
    (Join-Path $Root "venv\Scripts\python.exe")
)

$PythonPath = $null
$PythonMode = $null

foreach ($Candidate in $PythonCandidates) {
    if (Test-Path $Candidate) {
        $PythonPath = $Candidate
        $PythonMode = "path"
        break
    }
}

if ($null -eq $PythonPath) {
    $PyCommand = Get-Command py -ErrorAction SilentlyContinue

    if ($null -ne $PyCommand) {
        $PythonPath = "py"
        $PythonMode = "launcher"
    }
}

if ($null -eq $PythonPath) {
    $PythonCommand = Get-Command python -ErrorAction SilentlyContinue

    if ($null -ne $PythonCommand) {
        $PythonPath = "python"
        $PythonMode = "launcher"
    }
}

$BackendLog = Join-Path $BaselineDir "backend-tests.log"

if ($null -eq $PythonPath) {
    "No existing Python interpreter was found. No packages were installed." |
        Tee-Object -FilePath $BackendLog

    $BackendExit = 127
    Write-Host "Backend test runner unavailable." -ForegroundColor Red
}
else {
    Push-Location (Join-Path $Root "backend")
    try {
        if ($PythonMode -eq "path") {
            & $PythonPath -m pytest -q 2>&1 |
                Tee-Object -FilePath $BackendLog
        }
        else {
            & $PythonPath -m pytest -q 2>&1 |
                Tee-Object -FilePath $BackendLog
        }

        $BackendExit = $LASTEXITCODE
    }
    finally {
        Pop-Location
    }

    Write-Host "Backend exit code: $BackendExit"
}

Write-Host ""
Write-Host "## Frontend build" -ForegroundColor Yellow

$FrontendLog = Join-Path $BaselineDir "frontend-build.log"

Push-Location (Join-Path $Root "frontend")
try {
    npm run build 2>&1 |
        Tee-Object -FilePath $FrontendLog

    $FrontendExit = $LASTEXITCODE
}
finally {
    Pop-Location
}

Write-Host "Frontend exit code: $FrontendExit"

Write-Host ""
Write-Host "## Repository status" -ForegroundColor Yellow
git -C $Root status --short

Write-Host ""

if ($BackendExit -eq 0 -and $FrontendExit -eq 0) {
    Write-Host "✅ Step 3 complete: backend tests and frontend build passed." -ForegroundColor Green
}
else {
    Write-Host "❌ Step 3 incomplete: one or more baseline commands failed or were unavailable." -ForegroundColor Red
}

Write-Host "Logs saved to: $BaselineDir" -ForegroundColor Cyan

if ($BackendExit -ne 0 -or $FrontendExit -ne 0) {
    exit 1
}

exit 0
