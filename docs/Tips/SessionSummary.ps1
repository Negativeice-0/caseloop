#Requires -Version 5.1

<#
========================================================================

SESSION SUMMARY GENERATOR

Purpose
-------
Generate:

docs\Auditing\data\fullstack\<phase>\summary.md

docs\Auditing\data\snrlead\<phase>\verification.md

from rawshell evidence.

Usage
-----

.\docs\Tips\SessionSummary.ps1 -Phase phase7

========================================================================
#>

param(
    [Parameter(Mandatory)]
    [string]$Phase
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

# ============================================================
# Phase Definitions
# ============================================================

$PhaseInfo = @{

    phase7 = @{
        Objective =
        "Frontend Backend Database Connection Map"

        NextAction =
        "Verify frontend feature to backend route mappings"

        ImportantFiles = @(
            "frontend/src/services/api.ts"
            "frontend/src/features"
            "backend/app/api"
            "backend/app/services"
            "backend/app/models/models.py"
        )
    }

    phase8 = @{
        Objective =
        "README and Documentation Audit"

        NextAction =
        "Compare documentation claims against verified artifacts"

        ImportantFiles = @(
            "README.md"
            "docs/deployment"
            "docs/design"
        )
    }

    phase9 = @{
        Objective =
        "Navigation Audit"

        NextAction =
        "Identify redundant navigation entries"

        ImportantFiles = @(
            "frontend/src/App.tsx"
            "frontend/src/features"
        )
    }

    phase10 = @{
        Objective =
        "Visibility and Route Testing"

        NextAction =
        "Verify access by role"

        ImportantFiles = @(
            "frontend/src"
            "backend/app/api"
        )
    }

    phase11 = @{
        Objective =
        "Route Disposition Review"

        NextAction =
        "Classify routes as retain, refactor, or candidate"

        ImportantFiles = @(
            "backend/app/api"
        )
    }

    phase12 = @{
        Objective =
        "Dead Route Wiring Analysis"

        NextAction =
        "Trace route references"

        ImportantFiles = @(
            "frontend/src"
            "backend/app/api"
        )
    }

    phase13 = @{
        Objective =
        "Mixed Responsibility Refactor Review"

        NextAction =
        "Identify components containing multiple responsibilities"

        ImportantFiles = @(
            "frontend/src/features"
            "backend/app/services"
        )
    }

    phase14 = @{
        Objective =
        "Reference Audit"

        NextAction =
        "Trace all references before deletion review"

        ImportantFiles = @(
            "frontend/src"
            "backend/app"
        )
    }

    phase15 = @{
        Objective =
        "Deletion Candidates"

        NextAction =
        "Produce candidate list only"

        ImportantFiles = @(
            "frontend/src"
            "backend/app"
        )
    }

    phase16 = @{
        Objective =
        "Backend Authorization Tests"

        NextAction =
        "Review authorization coverage"

        ImportantFiles = @(
            "backend/tests"
            "backend/app/core"
        )
    }

    phase17 = @{
        Objective =
        "Frontend Navigation Tests"

        NextAction =
        "Validate navigation coverage"

        ImportantFiles = @(
            "frontend/src"
        )
    }

    phase18 = @{
        Objective =
        "Smoke Tests and Build Verification"

        NextAction =
        "Run build and test validation"

        ImportantFiles = @(
            "frontend"
            "backend"
        )
    }

    phase19 = @{
        Objective =
        "Documentation Update"

        NextAction =
        "Bring documentation in line with verified system behavior"

        ImportantFiles = @(
            "README.md"
            "docs"
        )
    }

    phase20 = @{
        Objective =
        "Final Summary and Handover"

        NextAction =
        "Generate final review and handover package"

        ImportantFiles = @(
            "docs"
        )
    }
}

if(-not $PhaseInfo.ContainsKey($Phase))
{
    throw "Unknown phase: $Phase"
}

$Current = $PhaseInfo[$Phase]

# ============================================================
# Paths
# ============================================================

$RawShellDir =
"docs\Auditing\data\rawshell\$Phase"

$FullstackDir =
"docs\Auditing\data\fullstack\$Phase"

$SnrLeadDir =
"docs\Auditing\data\snrlead\$Phase"

if(!(Test-Path $RawShellDir))
{
    throw "Missing evidence directory: $RawShellDir"
}

New-Item -ItemType Directory -Force -Path $FullstackDir | Out-Null
New-Item -ItemType Directory -Force -Path $SnrLeadDir | Out-Null

$SummaryFile =
Join-Path $FullstackDir "summary.md"

$VerificationFile =
Join-Path $SnrLeadDir "verification.md"

# ============================================================
# Discover Evidence
# ============================================================

$RawFiles =
Get-ChildItem `
    $RawShellDir `
    -Recurse `
    -File `
    -ErrorAction SilentlyContinue

$EvidenceCount =
@($RawFiles).Count

$EvidenceList =
if($EvidenceCount -gt 0)
{
    ($RawFiles |
        Select-Object -ExpandProperty Name |
        Sort-Object |
        ForEach-Object {
            "- $_"
        }) -join "`r`n"
}
else
{
    "- none"
}

# ============================================================
# Verification Status
# ============================================================

if($EvidenceCount -gt 0)
{
    $Status = "PASS"
}
else
{
    $Status = "PARTIAL"
}

# ============================================================
# Summary
# ============================================================

$ImportantFiles =
($Current.ImportantFiles | ForEach-Object {
    "- $_"
}) -join "`r`n"

$Summary = @"
# Summary

## Metadata

Date:
$(Get-Date -Format "yyyy-MM-dd HH:mm")

Phase:
$Phase

Status:
$Status

---

## Objective

$($Current.Objective)

---

## Evidence Source

$RawShellDir

---

## Evidence Files

$EvidenceList

---

## Important Files

$ImportantFiles

---

## Next Action

$($Current.NextAction)

---

## Restart Instructions

1. Read control.md

2. Read verification.md

3. Continue current phase

4. Do not rerun completed inventories
"@

$Summary |
Set-Content `
    -Path $SummaryFile `
    -Encoding UTF8

# ============================================================
# Verification
# ============================================================

$Verification = @"
# Verification

## Status

$Status

---

## Evidence Count

$EvidenceCount

---

## Evidence Files

$EvidenceList

---

## Findings

Evidence exists for review.

---

## Risks

Artifact contents have not been manually reviewed.

PASS does not imply correctness.

---

## Verification Commands

Get-ChildItem "$RawShellDir" -Recurse

Get-Content "$SummaryFile"

Get-Content "$VerificationFile"

---

## Recommended Next Action

$($Current.NextAction)

---

## Stop Conditions

Do not close the phase until:

- evidence reviewed
- outputs reviewed
- findings validated
"@

$Verification |
Set-Content `
    -Path $VerificationFile `
    -Encoding UTF8

# ============================================================
# Console
# ============================================================

Write-Host ""
Write-Host "PASS"

Write-Host ""
Write-Host "Summary:"
Write-Host $SummaryFile

Write-Host ""
Write-Host "Verification:"
Write-Host $VerificationFile