# CORRECTED STEP 6 COLLECTOR

Use this instead of building a matrix from `authorization-dependencies.json`.

The current evidence proves that file contains search hits:

```text
Line
LineNumber
Path
```

not actual role/permission relationships.

This collector discovers authorization sources from the repository and generates evidence for the role-permission matrix.

---

## Script Creation

```text
scripts\audit\phase6-collect-authorization-evidence.ps1
```

```powershell
#Requires -Version 5.1

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$RepoRoot = (Get-Location).Path

$Phase = "phase6"

$RawShellDir = Join-Path $RepoRoot "docs\auditing\data\rawshell\$Phase"
$FullstackDir = Join-Path $RepoRoot "docs\auditing\data\fullstack\$Phase"
$SnrLeadDir = Join-Path $RepoRoot "docs\auditing\data\snrlead\$Phase"
$VerificationDir = Join-Path $RepoRoot "docs\auditing\verification\$Phase"

@(
    $RawShellDir,
    $FullstackDir,
    $SnrLeadDir,
    $VerificationDir
) | ForEach-Object {
    if (!(Test-Path $_))
    {
        New-Item -ItemType Directory -Force -Path $_ | Out-Null
    }
}

$IncludedRoots = @(
    "src",
    "app",
    "api",
    "routes",
    "controllers",
    "middleware",
    "auth",
    "authorization",
    "permissions",
    "services"
)

$ExcludedPatterns = @(
    "\node_modules\",
    "\dist\",
    "\build\",
    "\.git\",
    "\vendor\",
    "\third_party\",
    "\.venv\",
    "\venv\"
)

$Files = New-Object System.Collections.ArrayList

foreach ($Root in $IncludedRoots)
{
    $Path = Join-Path $RepoRoot $Root

    if (Test-Path $Path)
    {
        Get-ChildItem $Path -Recurse -File -ErrorAction SilentlyContinue |
        ForEach-Object {

            $Skip = $false

            foreach ($Pattern in $ExcludedPatterns)
            {
                if ($_.FullName -match [regex]::Escape($Pattern))
                {
                    $Skip = $true
                    break
                }
            }

            if (-not $Skip)
            {
                [void]$Files.Add($_)
            }
        }
    }
}

$AuthorizationTerms = @(
    "role",
    "roles",
    "permission",
    "permissions",
    "authorize",
    "authorization",
    "policy",
    "claim",
    "claims",
    "guard",
    "RequireRole",
    "RequirePermission",
    "AllowedRoles",
    "CurrentUser",
    "IsAdmin",
    "hasPermission"
)

$Evidence = New-Object System.Collections.ArrayList

foreach ($Term in $AuthorizationTerms)
{
    $Results =
        $Files |
        Select-String -Pattern $Term -SimpleMatch -CaseSensitive:$false -ErrorAction SilentlyContinue

    foreach ($Result in $Results)
    {
        [void]$Evidence.Add(
            [PSCustomObject]@{
                Term       = $Term
                File       = $Result.Path
                LineNumber = $Result.LineNumber
                Line       = $Result.Line.Trim()
            }
        )
    }
}

$Evidence |
    Sort-Object File,LineNumber |
    ConvertTo-Json -Depth 10 |
    Set-Content (
        Join-Path $FullstackDir `
        "authorization-evidence.json"
    )

$RoleHits =
    $Evidence |
    Where-Object {
        $_.Term -match "role"
    }

$PermissionHits =
    $Evidence |
    Where-Object {
        $_.Term -match "permission"
    }

$Summary = [PSCustomObject]@{
    EvidenceRows    = @($Evidence).Count
    RoleHits        = @($RoleHits).Count
    PermissionHits  = @($PermissionHits).Count
    FilesScanned    = @($Files).Count
    GeneratedUtc    = (Get-Date).ToUniversalTime()
}

$Summary |
    ConvertTo-Json -Depth 10 |
    Set-Content (
        Join-Path $FullstackDir `
        "authorization-evidence-summary.json"
    )

$Verification = @()
$Verification += "# Verification Evidence"
$Verification += ""
$Verification += "Files Scanned: $(@($Files).Count)"
$Verification += "Evidence Rows: $(@($Evidence).Count)"
$Verification += "Role Hits: $(@($RoleHits).Count)"
$Verification += "Permission Hits: $(@($PermissionHits).Count)"

$Verification |
Set-Content (
    Join-Path $VerificationDir `
    "verification-evidence.md"
)

if (
    (@($RoleHits).Count -gt 0) -or
    (@($PermissionHits).Count -gt 0)
)
{
    @"
PASS

Authorization evidence discovered.
Role/permission extraction can proceed.
"@ | Set-Content (
        Join-Path $VerificationDir `
        "verification-result.md"
    )
}
else
{
    @"
FAIL

No authorization evidence discovered.
"@ | Set-Content (
        Join-Path $VerificationDir `
        "verification-result.md"
    )

    exit 1
}

@"
# Session Summary

## Objective
Discover authoritative authorization sources.

## Actions Performed
Collected authorization evidence.

## Findings
Authorization references identified.

## Verification Status
PASS
"@ | Set-Content (
    Join-Path $FullstackDir `
    "session-summary.md"
)

@"
# Senior Lead Review

Review authorization-evidence.json.

Identify:

- roles
- permissions
- policies
- decorators
- guards
- middleware
"@ | Set-Content (
    Join-Path $SnrLeadDir `
    "authorization-review.md"
)

Write-Host ""
Write-Host "PASS"
Write-Host "Authorization evidence discovered."
```

---

## Script Execution

```powershell
powershell -ExecutionPolicy Bypass `
    -File scripts\audit\phase6-collect-authorization-evidence.ps1
```

---

## Verification Commands

```powershell
Get-Content `
docs\auditing\verification\phase6\verification-result.md
```

```powershell
Get-Content `
docs\auditing\verification\phase6\verification-evidence.md
```

```powershell
Get-Content `
docs\auditing\data\fullstack\phase6\authorization-evidence-summary.json
```

---

## PASS Criteria

```text
Role Hits > 0

OR

Permission Hits > 0
```

This does not complete Step 6 yet. It provides the missing evidence needed to build a real role-permission 