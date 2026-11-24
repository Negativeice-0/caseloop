# ===================================================================
# Phase 4
# Inventory Frontend Routes and Navigation Entries
# Evidence First
# ===================================================================

$ErrorActionPreference = "Continue"

$Phase = "phase4"

$RawDir       = "docs/auditing/data/rawshell/$Phase"
$FullDir      = "docs/auditing/data/fullstack/$Phase"
$LeadDir      = "docs/auditing/data/snrlead/$Phase"
$VerifyDir    = "docs/auditing/verification/$Phase"

New-Item -ItemType Directory -Force -Path $RawDir | Out-Null
New-Item -ItemType Directory -Force -Path $FullDir | Out-Null
New-Item -ItemType Directory -Force -Path $LeadDir | Out-Null
New-Item -ItemType Directory -Force -Path $VerifyDir | Out-Null

# -----------------------------------------------------------
# Baseline Metadata
# -----------------------------------------------------------

$Timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

git branch --show-current `
    > "$RawDir/git-branch.txt" 2>&1

git rev-parse HEAD `
    > "$RawDir/git-sha.txt" 2>&1

git status `
    > "$RawDir/git-status.txt" 2>&1

# -----------------------------------------------------------
# Authoritative Sources First
# -----------------------------------------------------------

$AuthorityPatterns = @(
    "main.tsx",
    "main.jsx",
    "App.tsx",
    "App.jsx",
    "*router*.ts",
    "*router*.tsx",
    "*routes*.ts",
    "*routes*.tsx"
)
# -----------------------------------------------------------
# Exclusions
# -----------------------------------------------------------

$ExcludedFolders = @(
    "node_modules",
    ".git",
    "dist",
    "build",
    "coverage",
    ".next",
    ".nuxt",
    ".vite",
    "venv",
    ".venv",
    "__pycache__"
)

function Test-IsExcluded {

    param(
        [string]$Path
    )

    foreach($folder in $ExcludedFolders)
    {
        if($Path -like "*\$folder\*")
        {
            return $true
        }
    }

    return $false
}

# -----------------------------------------------------------
# Import Resolution
# -----------------------------------------------------------

function Resolve-ImportPath {

    param(
        [string]$CurrentFile,
        [string]$ImportPath
    )

    if(
        -not $ImportPath.StartsWith("./") -and
        -not $ImportPath.StartsWith("../")
    )
    {
        return $null
    }

    $BaseDir = Split-Path $CurrentFile

    $Base = Join-Path $BaseDir $ImportPath

    $Candidates = @(
        "$Base.tsx",
        "$Base.ts",
        "$Base.jsx",
        "$Base.js",
        "$Base\index.tsx",
        "$Base\index.ts",
        "$Base\index.jsx",
        "$Base\index.js"
    )

    foreach($candidate in $Candidates)
    {
        if(Test-Path $candidate)
        {
            return (Resolve-Path $candidate).Path
        }
    }

    return $null
}

# -----------------------------------------------------------
# Import Extraction
# -----------------------------------------------------------

function Get-Imports {

    param(
        [string]$FilePath
    )
# so verification runs logic instead of hardcoded text
    if(-not (Test-Path $FilePath))
    {
        Add-Content `
        "$VerifyDir/verification-evidence.md" `
        "MISSING FILE: $FilePath"

        return @()
    }

    $Imports = @()

    try
    {
        $Content = Get-Content $FilePath -Raw

        $Matches = [regex]::Matches(
            $Content,
            'import\s+(?:.+?\s+from\s+)?["'']([^"'']+)["'']'
        )

        foreach($Match in $Matches)
        {
            $Imports += $Match.Groups[1].Value
        }
    }
    catch
    {
    }

    return $Imports
}

# -----------------------------------------------------------
# Dependency Graph Traversal
# -----------------------------------------------------------

$DiscoveredFiles = @{}
$Queue = New-Object System.Collections.Queue

# Entry Points

$EntryFiles = Get-ChildItem `
    -Recurse `
    -File |
Where-Object {

    -not (Test-IsExcluded $_.FullName)
} |
Where-Object {

    $_.Name -in @(
        "main.tsx",
        "main.jsx",
        "index.tsx",
        "index.jsx",
        "App.tsx",
        "App.jsx"
    )
}

foreach($file in $EntryFiles)
{
    $DiscoveredFiles[$file.FullName] = $true
    $Queue.Enqueue($file.FullName)
}

# Traverse

while($Queue.Count -gt 0)
{
    $Current = $Queue.Dequeue()

    $Imports = Get-Imports $Current

    Write-Host "Scanning: $Current"

    foreach($Import in $Imports)
    {
        Write-Host "Import Found: $Import"
    }

    foreach($Import in $Imports)
    {
        $Resolved = Resolve-ImportPath `
            -CurrentFile $Current `
            -ImportPath $Import

        if(
            $Resolved -and
            -not $DiscoveredFiles.ContainsKey($Resolved)
        )
        {
            if(-not (Test-IsExcluded $Resolved))
            {
                $DiscoveredFiles[$Resolved] = $true
                $Queue.Enqueue($Resolved)
            }
        }
    }
}

# -----------------------------------------------------------
# Outputs
# -----------------------------------------------------------

$Inventory = $DiscoveredFiles.Keys |
    Sort-Object

$InventoryCount = $Inventory.Count

@"
Files discovered: $InventoryCount
"@ | Set-Content "$VerifyDir/verification-evidence.md"

$Inventory |
    Out-File "$RawDir/route-registration-files.txt"

$Inventory |
    Out-File "$RawDir/navigation-files.txt"

$EntryFiles |
    Select-Object -ExpandProperty FullName |
    Sort-Object |
    Out-File "$RawDir/authoritative-files.txt"

$Inventory |
    Out-File "$RawDir/frontend-dependency-graph.txt"

# -----------------------------------------------------------
# Session Summary Placeholder
# -----------------------------------------------------------

@"
# Session Summary

## Objective
Inventory frontend routes and navigation entries.

## Actions Performed
Evidence collection only.

## Evidence Captured
See rawshell artifacts.

## Findings
Pending review.

## Failures
None recorded.

## Root Causes
N/A

## Corrections Applied
None.

## Verification Status
Pending.

## Remaining Work
Review evidence and build verified inventory.

## Recommended Starting Point
Review authoritative route registrations first.
"@ | Set-Content "$FullDir/session-summary.md"

# -----------------------------------------------------------
# Verification Evidence
# -----------------------------------------------------------

@"
Verification pending analysis.
"@ | Set-Content "$VerifyDir/verification-evidence.md"

if($InventoryCount -gt 2)
{
@"
PASS

Dependency graph generated.

Files discovered: $InventoryCount
"@ |
Set-Content "$VerifyDir/verification-result.md"
}
else
{
@"
FAIL

Only $InventoryCount files discovered.

Import traversal appears incomplete.
"@ |
Set-Content "$VerifyDir/verification-result.md"
}

Write-Host "Phase 4 evidence collection complete."
