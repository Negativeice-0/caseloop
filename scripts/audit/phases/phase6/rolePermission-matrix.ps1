#Requires -Version 5.1

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

# --------------------------------------------------
# Paths
# --------------------------------------------------

$RouteFile = "docs\Auditing\data\fullstack\phase5\backend-route-inventory.json"
$AuthFile  = "docs\Auditing\data\fullstack\phase5\authorization-normalized.json"

$PhaseDir  = "docs\Auditing\data\fullstack\phase6"
$VerifyDir = "docs\Auditing\verification\phase6"

New-Item -ItemType Directory -Force -Path $PhaseDir | Out-Null
New-Item -ItemType Directory -Force -Path $VerifyDir | Out-Null

# --------------------------------------------------
# Validate Inputs
# --------------------------------------------------

if (!(Test-Path $RouteFile))
{
    throw "Missing $RouteFile"
}

if (!(Test-Path $AuthFile))
{
    throw "Missing $AuthFile"
}

# --------------------------------------------------
# Load Data
# --------------------------------------------------

$Routes = Get-Content $RouteFile -Raw | ConvertFrom-Json
$Auth   = Get-Content $AuthFile -Raw | ConvertFrom-Json

# --------------------------------------------------
# Build Matrix
# --------------------------------------------------

$Matrix = @()

foreach ($Item in $Auth)
{
    $Evidence = ""

    if ($Item.PSObject.Properties["Evidence"])
    {
        $Evidence = [string]$Item.Evidence
    }

    $Role = $null

    if ($Evidence -match 'admin')
    {
        $Role = 'admin'
    }
    elseif ($Evidence -match 'coordinator')
    {
        $Role = 'coordinator'
    }
    elseif ($Evidence -match 'responder')
    {
        $Role = 'responder'
    }

    if ($Role)
    {
        $Matrix += [PSCustomObject]@{
            Role       = $Role
            File       = $Item.File
            LineNumber = $Item.LineNumber
            Evidence   = $Evidence
        }
    }
}

# --------------------------------------------------
# Save Matrix
# --------------------------------------------------

$MatrixFile =
Join-Path $PhaseDir "role-permission-matrix.json"

$Matrix |
ConvertTo-Json -Depth 10 |
Set-Content $MatrixFile

# --------------------------------------------------
# Stats
# --------------------------------------------------

$UniqueRoles =
$Matrix |
Select-Object -ExpandProperty Role -Unique |
Sort-Object

$Summary = [PSCustomObject]@{
    RouteCount                 = @($Routes).Count
    AuthorizationEvidenceCount = @($Auth).Count
    MatrixRows                 = @($Matrix).Count
    UniqueRoleCount            = @($UniqueRoles).Count
    Roles                      = @($UniqueRoles)
}

$Summary |
ConvertTo-Json -Depth 10 |
Set-Content (
    Join-Path $PhaseDir "role-permission-matrix-summary.json"
)

# --------------------------------------------------
# Verification Evidence
# --------------------------------------------------

@"
Route Count: $(@($Routes).Count)
Authorization Evidence: $(@($Auth).Count)
Matrix Rows: $(@($Matrix).Count)
Unique Roles: $(@($UniqueRoles).Count)
"@ |
Set-Content (
    Join-Path $VerifyDir "verification-evidence.md"
)

# --------------------------------------------------
# PASS / FAIL
# --------------------------------------------------

$Pass =
(
    (@($Routes).Count -gt 0) -and
    (@($Auth).Count -gt 0) -and
    (@($Matrix).Count -gt 0) -and
    (@($UniqueRoles).Count -gt 0)
)

if ($Pass)
{
    "PASS" |
    Set-Content (
        Join-Path $VerifyDir "verification-result.md"
    )
}
else
{
    "FAIL" |
    Set-Content (
        Join-Path $VerifyDir "verification-result.md"
    )

    exit 1
}

# --------------------------------------------------
# Console
# --------------------------------------------------

Write-Host ""
Write-Host "PASS"
Write-Host "Routes:" @($Routes).Count
Write-Host "Authorization Evidence:" @($Auth).Count
Write-Host "Matrix Rows:" @($Matrix).Count
Write-Host "Unique Roles:" @($UniqueRoles).Count
Write-Host ""

Write-Host "Roles Found:"

$UniqueRoles | ForEach-Object {
    Write-Host " - $_"
}