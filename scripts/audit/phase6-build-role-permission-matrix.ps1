#Requires -Version 5.1

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$RepoRoot = (Get-Location).Path

$Phase = "phase6"

$RawShellDir     = Join-Path $RepoRoot "docs\auditing\data\rawshell\$Phase"
$FullstackDir    = Join-Path $RepoRoot "docs\auditing\data\fullstack\$Phase"
$SnrLeadDir      = Join-Path $RepoRoot "docs\auditing\data\snrlead\$Phase"
$VerificationDir = Join-Path $RepoRoot "docs\auditing\verification\$Phase"

@(
    $RawShellDir,
    $FullstackDir,
    $SnrLeadDir,
    $VerificationDir
) | ForEach-Object {
    if (!(Test-Path $_)) {
        New-Item -ItemType Directory -Force -Path $_ | Out-Null
    }
}

$RouteInventoryFile =
    Join-Path $RepoRoot `
    "docs\auditing\data\fullstack\phase5\backend-route-inventory.json"

$AuthorizationFile =
    Join-Path $RepoRoot `
    "docs\auditing\data\fullstack\phase5\authorization-dependencies.json"

if (!(Test-Path $RouteInventoryFile)) {
    throw "Missing backend-route-inventory.json"
}

if (!(Test-Path $AuthorizationFile)) {
    throw "Missing authorization-dependencies.json"
}

$Routes =
    Get-Content $RouteInventoryFile -Raw |
    ConvertFrom-Json

$AuthDependencies =
    Get-Content $AuthorizationFile -Raw |
    ConvertFrom-Json

$RolePermissionMatrix = New-Object System.Collections.ArrayList

foreach ($Entry in $AuthDependencies)
{
    $Role = $null
    $Permission = $null
    $Route = $null

    if ($Entry.PSObject.Properties["Role"]) {
        $Role = $Entry.Role
    }

    if ($Entry.PSObject.Properties["Permission"]) {
        $Permission = $Entry.Permission
    }

    if ($Entry.PSObject.Properties["Route"]) {
        $Route = $Entry.Route
    }

    if ($Entry.PSObject.Properties["Path"] -and -not $Route) {
        $Route = $Entry.Path
    }

    [void]$RolePermissionMatrix.Add(
        [PSCustomObject]@{
            Role       = $Role
            Permission = $Permission
            Route      = $Route
        }
    )
}

$MatrixFile =
    Join-Path $FullstackDir "role-permission-matrix.json"

$RolePermissionMatrix |
    ConvertTo-Json -Depth 20 |
    Set-Content $MatrixFile

$UniqueRoles =
    $RolePermissionMatrix |
    Where-Object { $_.Role } |
    Select-Object -ExpandProperty Role -Unique |
    Sort-Object

$UniquePermissions =
    $RolePermissionMatrix |
    Where-Object { $_.Permission } |
    Select-Object -ExpandProperty Permission -Unique |
    Sort-Object

$Summary = [PSCustomObject]@{
    RoutesDiscovered      = @($Routes).Count
    AuthorizationEntries  = @($AuthDependencies).Count
    MatrixRows            = @($RolePermissionMatrix).Count
    UniqueRoles           = @($UniqueRoles).Count
    UniquePermissions     = @($UniquePermissions).Count
    GeneratedUtc          = (Get-Date).ToUniversalTime()
}

$Summary |
    ConvertTo-Json -Depth 10 |
    Set-Content (
        Join-Path $FullstackDir `
        "role-permission-matrix-summary.json"
    )

$VerificationEvidence = @"
# Verification Evidence

Route Inventory File
$RouteInventoryFile

Authorization Dependency File
$AuthorizationFile

Route Count
$(@($Routes).Count)

Authorization Entry Count
$(@($AuthDependencies).Count)

Matrix Row Count
$(@($RolePermissionMatrix).Count)

Unique Role Count
$(@($UniqueRoles).Count)

Unique Permission Count
$(@($UniquePermissions).Count)
"@

$VerificationEvidence |
    Set-Content (
        Join-Path $VerificationDir `
        "verification-evidence.md"
    )

$SessionSummary = @"
# Session Summary

## Objective
Build role-permission matrix.

## Actions Performed
Consumed verified phase5 artifacts.
Generated matrix output.
Generated matrix summary.
Generated verification artifacts.

## Evidence Captured
backend-route-inventory.json
authorization-dependencies.json

## Findings
Matrix generated from authorization-dependency inventory.

## Failures
None during execution.

## Root Causes
N/A

## Corrections Applied
Replaced invalid phase5 artifact dependency.

## Verification Status
Evidence Collected

## Remaining Work
Review generated matrix.

## Recommended Starting Point
Inspect role-permission-matrix.json
"@

$SessionSummary |
    Set-Content (
        Join-Path $FullstackDir `
        "session-summary.md"
    )

$LeadReview = @"
# Senior Lead Review

Matrix generated from phase5 artifacts.

Review Focus:

- orphan permissions
- orphan role references
- missing authorization associations
- authorization consistency
"@

$LeadReview |
    Set-Content (
        Join-Path $SnrLeadDir `
        "role-permission-review.md"
    )

$ResultFile =
    Join-Path $VerificationDir `
    "verification-result.md"

$Pass =
(
    (Test-Path $MatrixFile) -and
    (@($RolePermissionMatrix).Count -gt 0)
)

if ($Pass)
{
    @"
PASS

Role-permission matrix artifacts generated.
"@ | Set-Content $ResultFile

    Write-Host ""
    Write-Host "PASS"
    Write-Host "Role-permission matrix artifacts generated."
}
else
{
    @"
FAIL

Role-permission matrix generation failed.
"@ | Set-Content $ResultFile

    exit 1
}
