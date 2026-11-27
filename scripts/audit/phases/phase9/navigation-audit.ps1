#Requires -Version 5.1

param(
    [string]$Root = "."
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$Root = (Resolve-Path $Root).Path
$RawDir = Join-Path $Root "docs\Auditing\data\rawshell\phase9"
$ControlDir = Join-Path $Root "docs\Auditing\control"
$SourceDir = Join-Path $Root "frontend\src"
$LayoutPath = Join-Path $SourceDir "layouts\MainLayout.tsx"
$AppPath = Join-Path $SourceDir "App.tsx"
$AuthPath = Join-Path $SourceDir "features\auth\AuthGateway.tsx"
$PackagePath = Join-Path $Root "frontend\package.json"

foreach($Path in @($RawDir, $ControlDir))
{
    New-Item -ItemType Directory -Force -Path $Path | Out-Null
}

foreach($Path in @($LayoutPath, $AppPath, $AuthPath, $PackagePath))
{
    if(-not (Test-Path -LiteralPath $Path -PathType Leaf))
    {
        throw "Required navigation source is missing: $Path"
    }
}

$LayoutText = Get-Content -LiteralPath $LayoutPath -Raw
if($LayoutText -notmatch "export type TabType = (?<tabs>[^;]+);")
{
    throw "Could not identify the navigation tab type in MainLayout.tsx."
}

$Tabs = @(
    [regex]::Matches($Matches.tabs, "'(?<tab>[^']+)'") |
    ForEach-Object { $_.Groups["tab"].Value }
)

if($Tabs.Count -eq 0)
{
    throw "No navigation tabs were discovered."
}

$TabInventoryPath = Join-Path $RawDir "navigation-tabs.txt"
$Tabs | Set-Content -LiteralPath $TabInventoryPath -Encoding UTF8

$EvidencePatterns = @(
    [pscustomobject]@{
        Path = $LayoutPath
        Pattern = "export type TabType|onClick=.*(setActiveTab|selectTab)|currentUser\.role"
        Label = "layout"
    },
    [pscustomobject]@{
        Path = $AppPath
        Pattern = "window\.location\.pathname|setActiveTab|activeTab ===|canCoordinate"
        Label = "app"
    },
    [pscustomobject]@{
        Path = $AuthPath
        Pattern = "window\.location\.assign"
        Label = "auth-gateway"
    },
    [pscustomobject]@{
        Path = $PackagePath
        Pattern = "react-router-dom"
        Label = "package"
    }
)

$SourceEvidence = @(
    "Navigation source matches (relative path and line number):"
    foreach($Entry in $EvidencePatterns)
    {
        $Hits = @(
            Select-String `
                -LiteralPath $Entry.Path `
                -Pattern $Entry.Pattern
        )

        if($Hits.Count -eq 0)
        {
            "[$($Entry.Label)] no matches"
            continue
        }

        foreach($Hit in $Hits)
        {
            $RelativePath = $Hit.Path.Substring($Root.Length).TrimStart("\")
            "[$($Entry.Label)] $RelativePath`:$($Hit.LineNumber): $($Hit.Line.Trim())"
        }
    }
)

$SourceEvidencePath = Join-Path $RawDir "navigation-source-evidence.txt"
$SourceEvidence | Set-Content -LiteralPath $SourceEvidencePath -Encoding UTF8

$SourceFiles = @(
    Get-ChildItem -LiteralPath $SourceDir -Recurse -File |
    Where-Object { $_.Extension -in @(".ts", ".tsx") }
)
$RouterReferences = @(
    Select-String `
        -Path $SourceFiles.FullName `
        -Pattern "react-router-dom"
)

$RouterReferencePath = Join-Path $RawDir "router-source-references.txt"
if($RouterReferences.Count -gt 0)
{
    $RouterReferences |
        ForEach-Object {
            $RelativePath = $_.Path.Substring($Root.Length).TrimStart("\")
            "$RelativePath`:$($_.LineNumber): $($_.Line.Trim())"
        } |
        Set-Content -LiteralPath $RouterReferencePath -Encoding UTF8
}
else
{
    "No react-router-dom references found under frontend/src." |
        Set-Content -LiteralPath $RouterReferencePath -Encoding UTF8
}

$EvidenceFiles = @(
    "navigation-tabs.txt"
    "navigation-source-evidence.txt"
    "router-source-references.txt"
)

$Manifest = [ordered]@{
    phase = "phase9"
    objective = "Navigation Audit and Cleanup Candidates"
    generated = (Get-Date).ToString("yyyy-MM-dd HH:mm:ss")
    evidenceFiles = $EvidenceFiles
    evidenceCount = $EvidenceFiles.Count
    primaryEvidence = @("navigation-tabs.txt", "navigation-source-evidence.txt")
    notes = @("Static navigation and route-wiring evidence collected; no deletion decisions made.")
}

$Manifest |
    ConvertTo-Json -Depth 20 |
    Set-Content -LiteralPath (Join-Path $RawDir "rawshell-manifest.json") -Encoding UTF8

$PhaseControl = [ordered]@{
    phase = "phase9"
    phaseNumber = 9
    objective = "Navigation Audit and Cleanup Candidates"
    status = "REVIEW REQUIRED"
    factExtractors = @(
        @{
            file = "navigation-tabs.txt"
            type = "count-lines"
            label = "Navigation tabs defined"
        },
        @{
            file = "navigation-source-evidence.txt"
            type = "contains"
            search = "currentUser.role !== 'responder'"
            label = "Role-gated navigation evidence present"
        },
        @{
            file = "router-source-references.txt"
            type = "contains"
            search = "No react-router-dom references found"
            label = "No frontend source imports of react-router-dom"
        }
    )
    importantFiles = @(
        "frontend/src/App.tsx"
        "frontend/src/layouts/MainLayout.tsx"
        "frontend/src/features/auth/AuthGateway.tsx"
        "frontend/package.json"
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
        "Desktop and mobile navigation parity"
        "Role-specific navigation visibility"
        "Tab rendering and entry-point wiring"
        "Unused router dependency reference audit"
    )
    nextAction = "Run role visibility and route tests in Phase 10."
    generatedBy = "CASELOOP"
}

foreach($ControlPath in @(
    (Join-Path $ControlDir "phase9.json"),
    (Join-Path $ControlDir "current-phase.json")
))
{
    $PhaseControl |
        ConvertTo-Json -Depth 20 |
        Set-Content -LiteralPath $ControlPath -Encoding UTF8
}

Write-Host "PASS Phase 9 navigation evidence generated."
Write-Host "Evidence: $RawDir"
Write-Host "Control: $(Join-Path $ControlDir 'phase9.json')"
