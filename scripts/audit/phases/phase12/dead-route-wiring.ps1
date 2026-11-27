#Requires -Version 5.1

param(
    [string]$Root = "."
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$Root = (Resolve-Path $Root).Path
$RawDir = Join-Path $Root "docs\Auditing\data\rawshell\phase12"
$ControlDir = Join-Path $Root "docs\Auditing\control"
$FrontendDir = Join-Path $Root "frontend"
$SourceDir = Join-Path $FrontendDir "src"
$TabListPath = Join-Path $Root "docs\Auditing\data\rawshell\phase9\navigation-tabs.txt"
$PackagePath = Join-Path $FrontendDir "package.json"

New-Item -ItemType Directory -Force -Path $RawDir | Out-Null
New-Item -ItemType Directory -Force -Path $ControlDir | Out-Null

foreach($Path in @($SourceDir, $TabListPath, $PackagePath))
{
    if(-not (Test-Path -LiteralPath $Path))
    {
        throw "Required route-reference input is missing: $Path"
    }
}

$SourceFiles = @(
    Get-ChildItem -LiteralPath $FrontendDir -Recurse -File |
    Where-Object {
        $_.FullName -notmatch '[\\/]node_modules[\\/]' -and
        $_.FullName -notmatch '[\\/](dist|build|coverage)[\\/]' -and
        $_.Extension -in @(".ts", ".tsx", ".js", ".jsx", ".html")
    }
)

$Tabs = @(Get-Content -LiteralPath $TabListPath | Where-Object { -not [string]::IsNullOrWhiteSpace($_) })
$RouteReferenceLines = @("Frontend tab-token references (first-party source only):")
foreach($Tab in $Tabs)
{
    $Hits = @(
        Select-String -Path $SourceFiles.FullName -SimpleMatch -CaseSensitive -Pattern "'$Tab'"
    )

    $RouteReferenceLines += "TAB: $Tab | source match count: $($Hits.Count)"
    foreach($Hit in $Hits)
    {
        $RelativePath = $Hit.Path.Substring($Root.Length).TrimStart("\")
        $RouteReferenceLines += "  $RelativePath`:$($Hit.LineNumber): $($Hit.Line.Trim())"
    }
}
$RouteReferencePath = Join-Path $RawDir "tab-reference-matrix.txt"
$RouteReferenceLines | Set-Content -LiteralPath $RouteReferencePath -Encoding UTF8

$RouterHits = @(
    Select-String -Path $SourceFiles.FullName -SimpleMatch -Pattern "react-router-dom"
)
$RouterReferencePath = Join-Path $RawDir "router-source-references.txt"
if($RouterHits.Count -gt 0)
{
    $RouterHits |
        ForEach-Object {
            $RelativePath = $_.Path.Substring($Root.Length).TrimStart("\")
            "$RelativePath`:$($_.LineNumber): $($_.Line.Trim())"
        } |
        Set-Content -LiteralPath $RouterReferencePath -Encoding UTF8
}
else
{
    "No react-router-dom references found in first-party frontend source files." |
        Set-Content -LiteralPath $RouterReferencePath -Encoding UTF8
}

$PackageReferencePath = Join-Path $RawDir "router-package-reference.txt"
Select-String -LiteralPath $PackagePath -SimpleMatch -Pattern "react-router-dom" |
    ForEach-Object {
        "$($_.Path.Substring($Root.Length).TrimStart("\"))`:$($_.LineNumber): $($_.Line.Trim())"
    } |
    Set-Content -LiteralPath $PackageReferencePath -Encoding UTF8

$AuthPathEvidencePath = Join-Path $RawDir "auth-path-references.txt"
$AuthFiles = @(
    (Join-Path $SourceDir "App.tsx"),
    (Join-Path $SourceDir "features\auth\AuthGateway.tsx")
)
Select-String -Path $AuthFiles -Pattern "window\.location\.pathname|window\.location\.assign" |
    ForEach-Object {
        "$($_.Path.Substring($Root.Length).TrimStart("\"))`:$($_.LineNumber): $($_.Line.Trim())"
    } |
    Set-Content -LiteralPath $AuthPathEvidencePath -Encoding UTF8

$EvidenceFiles = @(
    "tab-reference-matrix.txt"
    "router-source-references.txt"
    "router-package-reference.txt"
    "auth-path-references.txt"
)
$Manifest = [ordered]@{
    phase = "phase12"
    objective = "Dead Route Wiring Analysis"
    generated = (Get-Date).ToString("yyyy-MM-dd HH:mm:ss")
    evidenceFiles = $EvidenceFiles
    evidenceCount = $EvidenceFiles.Count
    primaryEvidence = @("tab-reference-matrix.txt", "router-source-references.txt", "auth-path-references.txt")
    notes = @("References searched in first-party frontend source; generated dependencies and build output excluded.")
}
$Manifest |
    ConvertTo-Json -Depth 20 |
    Set-Content -LiteralPath (Join-Path $RawDir "rawshell-manifest.json") -Encoding UTF8

$PhaseControl = [ordered]@{
    phase = "phase12"
    phaseNumber = 12
    objective = "Dead Route Wiring Analysis"
    status = "REVIEW REQUIRED"
    factExtractors = @(
        @{
            file = "tab-reference-matrix.txt"
            type = "count-matches"
            search = "TAB:"
            label = "Navigation tab reference groups"
        },
        @{
            file = "router-source-references.txt"
            type = "contains"
            search = "No react-router-dom references found"
            label = "No router source references found"
        },
        @{
            file = "auth-path-references.txt"
            type = "contains"
            search = "'/admin'"
            label = "Admin auth path is referenced"
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
        "Confirm every tab has both navigation and render references"
        "Confirm auth entry paths are used"
        "Trace declared-but-unimported dependencies before recommending removal"
    )
    nextAction = "Review mixed responsibilities in Phase 13."
    generatedBy = "CASELOOP"
}
foreach($ControlPath in @(
    (Join-Path $ControlDir "phase12.json"),
    (Join-Path $ControlDir "current-phase.json")
))
{
    $PhaseControl |
        ConvertTo-Json -Depth 20 |
        Set-Content -LiteralPath $ControlPath -Encoding UTF8
}

Write-Host "PASS Phase 12 route-reference evidence generated."
Write-Host "Evidence: $RawDir"
