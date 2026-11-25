#Requires -Version 5.1

$ErrorActionPreference = "Stop"

$RequiredFiles = @(
    "docs\auditing\data\fullstack\phase6\role-permission-matrix.json",
    "docs\auditing\data\fullstack\phase6\role-permission-matrix-summary.json",
    "docs\auditing\data\fullstack\phase6\session-summary.md",
    "docs\auditing\data\snrlead\phase6\role-permission-review.md",
    "docs\auditing\verification\phase6\verification-evidence.md",
    "docs\auditing\verification\phase6\verification-result.md"
)

$Missing = @()

foreach ($File in $RequiredFiles)
{
    if (!(Test-Path $File))
    {
        $Missing += $File
    }
}

if ($Missing.Count -gt 0)
{
    Write-Host ""
    Write-Host "FAIL - Missing Artifacts"
    $Missing | ForEach-Object { Write-Host $_ }
    exit 1
}

$SummaryFile = "docs\auditing\data\fullstack\phase6\role-permission-matrix-summary.json"

$Summary = Get-Content $SummaryFile -Raw | ConvertFrom-Json

Write-Host ""
Write-Host "RoutesDiscovered     :" $Summary.RoutesDiscovered
Write-Host "AuthorizationEntries :" $Summary.AuthorizationEntries
Write-Host "MatrixRows           :" $Summary.MatrixRows
Write-Host "UniqueRoles          :" $Summary.UniqueRoles
Write-Host "UniquePermissions    :" $Summary.UniquePermissions

if ($Summary.MatrixRows -gt 0)
{
    Write-Host ""
    Write-Host "PASS"
}
else
{
    Write-Host ""
    Write-Host "FAIL - MatrixRows = 0"
    exit 1
}