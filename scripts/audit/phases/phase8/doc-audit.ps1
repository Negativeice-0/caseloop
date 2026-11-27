# .\scripts\audit\phases\phase8\doc-audit.ps1
param(
    [string]$Root = "."
)

$ErrorActionPreference = "Stop"

# --------------------------------------------------
# Paths
# --------------------------------------------------

$RawDir = Join-Path $Root "docs\Auditing\data\rawshell\phase8"
$FullDir = Join-Path $Root "docs\Auditing\data\fullstack\phase8"
$LeadDir = Join-Path $Root "docs\Auditing\data\snrlead\phase8"

$null = New-Item -ItemType Directory -Force -Path $RawDir
$null = New-Item -ItemType Directory -Force -Path $FullDir
$null = New-Item -ItemType Directory -Force -Path $LeadDir

# --------------------------------------------------
# Exclusions
# --------------------------------------------------

$Excluded =
@(
    '\node_modules\'
    '\.git\'
    '\venv\'
    '\.venv\'
    '\__pycache__\'
    '\dist\'
    '\build\'
    '\coverage\'
    '\.pytest_cache\'
)

function Test-Excluded {
    param([string]$Path)

    foreach ($e in $Excluded) {
        if ($Path -match [regex]::Escape($e)) {
            return $true
        }
    }

    return $false
}

# --------------------------------------------------
# Documentation Discovery
# --------------------------------------------------

$Docs =
Get-ChildItem $Root -Recurse -File |
Where-Object {

    $p = $_.FullName

    if (Test-Excluded $p) {
        return $false
    }

    $_.Name -match '^README(\..+)?$' `
    -or $_.Extension -in '.md','.rst','.txt'
} |
Sort-Object FullName

$Docs |
Select-Object FullName,Length,LastWriteTime |
Out-File "$RawDir\documentation-inventory.txt"

# --------------------------------------------------
# README Inventory
# --------------------------------------------------

$Readmes =
$Docs |
Where-Object {
    $_.Name -match '^README'
}

$Readmes |
Select-Object FullName |
Out-File "$RawDir\readme-inventory.txt"

# --------------------------------------------------
# Targeted Documentation Checks
# --------------------------------------------------

$ExpectedDocs =
@(
    'README.md',
    'docker-compose.yml'
)

$Report = @()

foreach ($e in $ExpectedDocs)
{
    $Found = Get-ChildItem $Root -Recurse -File |
        Where-Object { $_.Name -eq $e }

    $Report += [pscustomobject]@{
        Item = $e
        Present = $Found.Count -gt 0
    }
}

$Report |
Format-Table -AutoSize |
Out-File "$RawDir\documentation-coverage.txt"

Write-Host "PASS Documentation Files:" $Docs.Count