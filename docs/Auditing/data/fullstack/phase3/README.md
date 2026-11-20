Below is a single PowerShell 5.1 generator script. Paste it into PowerShell from your repository root.

It creates:

.\Create-Phase3Audit.ps1


When executed, that script will:

Create baseline artifacts
Capture Git state
Capture current branch
Capture safety branches
Capture commit SHA
Capture package-lock hash
Capture environment versions
Capture frontend build
Capture frontend/backend tests (where possible)
Capture running processes
Capture listening ports
Capture raw terminal output
Generate a trimmed audit report
Generate recommendations
Generate a logbook entry
Include brief explanatory comments


---

$script = @'

param()

$ErrorActionPreference = "Continue"

# ============================================================
# CASELOOP PHASE 3 AUDIT CAPTURE
#
# Purpose:
# Capture a reproducible baseline before analysis,
# refactoring, route cleanup, or authorization work.
#
# Philosophy:
# Evidence first.
# Analysis second.
# Modification third.
#
# This script does not intentionally modify application code.
# ============================================================

$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"

$baselinePath = ".\baseline"
$auditPath    = ".\docs\auditing\data\rawshell\phase3data"

New-Item -ItemType Directory -Force -Path $baselinePath | Out-Null
New-Item -ItemType Directory -Force -Path $auditPath | Out-Null

$rawOutputFile =
    Join-Path $auditPath "raw-terminal-$timestamp.txt"

$summaryFile =
    Join-Path $auditPath "phase3-summary-$timestamp.txt"

# ------------------------------------------------------------
# Utility Logging
# ------------------------------------------------------------

function Add-Section {

    param([string]$Title)

    Add-Content $rawOutputFile ""
    Add-Content $rawOutputFile "==========================================================="
    Add-Content $rawOutputFile $Title
    Add-Content $rawOutputFile "==========================================================="
}

function Invoke-Capture {

    param(
        [string]$Title,
        [scriptblock]$Command
    )

    Add-Section $Title

    try {

        $out = & $Command 2>&1

        if ($out) {
            $out |
                Out-String |
                Add-Content $rawOutputFile
        }

    }
    catch {

        $_ |
            Out-String |
            Add-Content $rawOutputFile

    }

}

# ------------------------------------------------------------
# Session Metadata
# ------------------------------------------------------------

Invoke-Capture "TIMESTAMP" {
    Get-Date
}

Invoke-Capture "CURRENT USER" {
    whoami
}

Invoke-Capture "MACHINE NAME" {
    $env:COMPUTERNAME
}

# ------------------------------------------------------------
# Git Baseline
# ------------------------------------------------------------

# Establish exact repository state.

Invoke-Capture "GIT STATUS" {
    git status --short
}

git status --short |
    Out-File "$baselinePath\git-status.txt"

Invoke-Capture "CURRENT BRANCH" {
    git branch --show-current
}

git branch --show-current |
    Out-File "$baselinePath\branch.txt"

Invoke-Capture "ALL BRANCHES" {
    git branch -a
}

git branch -a |
    Out-File "$baselinePath\all-branches.txt"

# Attempt to identify rollback/safety branches.
Invoke-Capture "SAFETY BRANCH SEARCH" {

    git branch -a |
    Select-String `
        -Pattern "safety|backup|audit|rollback|baseline"
}

git branch -a |
Select-String `
    -Pattern "safety|backup|audit|rollback|baseline" |
Out-File "$baselinePath\safety-branch.txt"

Invoke-Capture "COMMIT SHA" {
    git rev-parse HEAD
}

git rev-parse HEAD |
    Out-File "$baselinePath\commit-sha.txt"

# ------------------------------------------------------------
# File Inventory
# ------------------------------------------------------------

Invoke-Capture "TRACKED FILES" {
    git ls-files
}

git ls-files |
    Out-File "$baselinePath\git-tracked-files.txt"

Invoke-Capture "TRACKED FILE HASHES" {

    git ls-files |
    ForEach-Object {

        if(Test-Path $_){

            Get-FileHash `
                $_ `
                -Algorithm SHA256

        }

    }

}

git ls-files |
ForEach-Object {

    if(Test-Path $_){

        Get-FileHash `
            $_ `
            -Algorithm SHA256

    }

} |
Format-Table Path,Hash -AutoSize |
Out-File "$baselinePath\tracked-file-hashes.txt"

# ------------------------------------------------------------
# Dependency Integrity
# ------------------------------------------------------------

# Detect dependency drift.

if(Test-Path ".\package-lock.json"){

    Invoke-Capture "PACKAGE LOCK HASH" {

        Get-FileHash `
            ".\package-lock.json" `
            -Algorithm SHA256

    }

    Get-FileHash `
        ".\package-lock.json" `
        -Algorithm SHA256 |
    Out-File "$baselinePath\package-lock.hash.txt"

}

# ------------------------------------------------------------
# Environment Inventory
# ------------------------------------------------------------

# Enables reproducible local environment recreation.

Invoke-Capture "NODE VERSION" {
    node -v
}

Invoke-Capture "NPM VERSION" {
    npm -v
}

Invoke-Capture "NPX VERSION" {
    npx -v
}

Invoke-Capture "PYTHON VERSION" {
    python --version
}

Invoke-Capture "DOCKER VERSION" {
    docker --version
}

Invoke-Capture "GIT VERSION" {
    git --version
}

@"
NODE
-----
$(node -v 2>&1)

NPM
----
$(npm -v 2>&1)

NPX
----
$(npx -v 2>&1)

PYTHON
-------
$(python --version 2>&1)

DOCKER
-------
$(docker --version 2>&1)

GIT
----
$(git --version 2>&1)
"@ |
Out-File "$baselinePath\environment.txt"

# ------------------------------------------------------------
# Runtime Inspection
# ------------------------------------------------------------

# Determine whether frontend/backend processes
# are currently running.

Invoke-Capture "NODE PROCESSES" {
    Get-Process node -ErrorAction SilentlyContinue
}

Invoke-Capture "PYTHON PROCESSES" {
    Get-Process python -ErrorAction SilentlyContinue
}

Invoke-Capture "DOTNET PROCESSES" {
    Get-Process dotnet -ErrorAction SilentlyContinue
}

Invoke-Capture "LISTENING PORTS" {

    Get-NetTCPConnection `
        -State Listen |
    Sort-Object LocalPort

}

# ------------------------------------------------------------
# package.json
# ------------------------------------------------------------

Invoke-Capture "PACKAGE JSON" {

    if(Test-Path ".\package.json"){

        Get-Content ".\package.json"

    }

}

# ------------------------------------------------------------
# Build
# ------------------------------------------------------------

# Baseline build verification.

$buildSucceeded = $false
$buildCommand   = ""

if(Test-Path ".\package.json"){

    try {

        $pkg =
            Get-Content ".\package.json" -Raw |
            ConvertFrom-Json

        $buildCommand =
            $pkg.scripts.build

    }
    catch {}

}

Add-Section "BUILD SCRIPT"

$buildCommand |
    Add-Content $rawOutputFile

if($buildCommand){

    try {

        npm run build *>&1 |
            Tee-Object "$baselinePath\frontend-build.txt" |
            Out-String |
            Add-Content $rawOutputFile

        $buildSucceeded = $true

    }
    catch {

        $_ |
        Out-String |
        Add-Content $rawOutputFile

    }

}

# ------------------------------------------------------------
# Tests
# ------------------------------------------------------------

# Attempt common test entrypoints.
# Failures are informational only.

$testOutput =
    "$baselinePath\test-result.txt"

"TEST EXECUTION" |
    Out-File $testOutput

if(Test-Path ".\package.json"){

    try {

        "npm run test" |
            Add-Content $testOutput

        npm run test *>&1 |
            Tee-Object -Append $testOutput |
            Out-Null

    }
    catch {

        $_ |
        Out-String |
        Add-Content $testOutput

    }

}

try {

    "pytest" |
        Add-Content $testOutput

    pytest *>&1 |
        Tee-Object -Append $testOutput |
        Out-Null

}
catch {}

Get-Content $testOutput |
    Add-Content $rawOutputFile

# ------------------------------------------------------------
# Signal Extraction
# ------------------------------------------------------------

# Produce readable audit summary.

$raw =
    Get-Content $rawOutputFile

$signals =
    $raw |
    Where-Object {

        $_ -match "error" `
        -or $_ -match "warning" `
        -or $_ -match "failed" `
        -or $_ -match "success" `
        -or $_ -match "compiled" `
        -or $_ -match "branch" `
        -or $_ -match "SHA" `
        -or $_ -match "version" `
        -or $_ -match "listen" `
        -or $_ -match "PASS" `
        -or $_ -match "FAIL"

    }

# ------------------------------------------------------------
# Summary Report
# ------------------------------------------------------------

@"
PHASE 3 BASELINE AUDIT REPORT

Generated:
$(Get-Date)

===========================================================
OBJECTIVE
===========================================================

Capture a verifiable baseline before route audits,
permission reviews, navigation cleanup, architectural
changes, refactoring, or deletion analysis.

===========================================================
ARTIFACTS COLLECTED
===========================================================

- Git Status
- Current Branch
- Branch Inventory
- Safety Branch Search
- Commit SHA
- Tracked File Inventory
- Tracked File Hashes
- Package Lock Hash
- Environment Versions
- Runtime Process Inventory
- Listening Ports
- package.json Snapshot
- Build Results
- Test Results

===========================================================
TRIMMED SIGNALS
===========================================================

$($signals -join :NewLine)

===========================================================
WHY THIS MATTERS
===========================================================

Professional engineering organizations separate:

1. Evidence Collection
2. Analysis
3. Decision Making
4. Modification
5. Verification

This ensures future investigators can answer:

"What changed?"

before asking:

"How do we fix it?"

===========================================================
RECOMMENDATIONS
===========================================================

Security:
- Hidden UI is never authorization.
- Backend authorization is authoritative.

Engineering:
- Every change should be reversible.
- Every deletion should have evidence.

Operations:
- Builds should remain reproducible.
- Dependency drift should be monitored.

Data:
- Reliable systems produce reliable metrics.

Management:
- Predictable engineering improves planning.

Sales:
- Reliable software improves customer trust.

Leadership:
- Sustainable engineering supports revenue,
  retention, and organizational confidence.

===========================================================
LOGBOOK ENTRY
===========================================================

Work Done:
Captured baseline repository state, branch inventory,
commit identity, dependency integrity, environment
versions, test outcomes, build outcomes, runtime
inspection, and audit evidence.

Effective Rating:
8/10

Self-Rating Reason:
Strong traceability established before any
architectural or behavioral changes.

Knowledge/Skills Learned/Applied:
Git auditing, baseline management, dependency
verification, reproducible build practices,
environment analysis, change-control techniques.

Problems Encountered/Solved:
Reduced uncertainty through structured evidence
collection and repeatable baseline creation.

"@ |
Set-Content $summaryFile

Write-Host ""
Write-Host "==============================================="
Write-Host "PHASE 3 AUDIT COMPLETE"
Write-Host "==============================================="
Write-Host ""
Write-Host "RAW DATA:"
Write-Host $rawOutputFile
Write-Host ""
Write-Host "SUMMARY:"
Write-Host $summaryFile
Write-Host ""
Write-Host "BASELINE:"
Write-Host $baselinePath
Write-Host ""

'@

Set-Content `
    ".\Create-Phase3Audit.ps1" `
    $script

Write-Host ""
Write-Host "Created:"
Write-Host ".\Create-Phase3Audit.ps1"
Write-Host ""
Write-Host "Execute:"
Write-Host ".\Create-Phase3Audit.ps1"
Write-Host ""

---


One senior-engineering enhancement I'd add later (not in Step 3 itself) is recording frontend dependency tree (npm ls), Docker image inventory (docker images), and git diff against the safety branch, because those become extremely useful during later route-cleanup and authorization-audit phases.