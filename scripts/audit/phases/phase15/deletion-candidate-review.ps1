#Requires -Version 5.1

param(
    [string]$Root = "."
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$Root = (Resolve-Path $Root).Path
$RawDir = Join-Path $Root "docs\Auditing\data\rawshell\phase15"
$ControlDir = Join-Path $Root "docs\Auditing\control"
New-Item -ItemType Directory -Force -Path $RawDir | Out-Null
New-Item -ItemType Directory -Force -Path $ControlDir | Out-Null

$TrackedPaths = @(& git -C $Root ls-files)
if($LASTEXITCODE -ne 0)
{
    throw "git ls-files failed; cannot establish repository reference scope."
}

$TextExtensions = @(
    ".py", ".ts", ".tsx", ".js", ".jsx", ".json", ".md", ".mdx",
    ".txt", ".ps1", ".html", ".yml", ".yaml", ".ini", ".toml"
)
$TrackedFiles = @(
    foreach($RelativePath in $TrackedPaths)
    {
        $Path = Join-Path $Root $RelativePath
        if(
            (Test-Path -LiteralPath $Path -PathType Leaf) -and
            [IO.Path]::GetExtension($Path) -in $TextExtensions
        )
        {
            Get-Item -LiteralPath $Path
        }
    }
)

if($TrackedFiles.Count -eq 0)
{
    throw "No tracked text files found for candidate review."
}

$Candidate = "react-router-dom"
$Hits = @(
    Select-String `
        -Path $TrackedFiles.FullName `
        -SimpleMatch `
        -Pattern $Candidate
)

$MetadataHits = @(
    $Hits | Where-Object {
        $_.Path -match '[\\/]frontend[\\/](package\.json|package-lock\.json)$'
    }
)
$NonMetadataHits = @($Hits | Where-Object { $MetadataHits -notcontains $_ })
$SourceHits = @(
    $NonMetadataHits | Where-Object {
        $_.Path -match '[\\/](src|app)[\\/]' -or $_.Path -match '\.(py|ts|tsx|js|jsx)$'
    }
)
$TestHits = @(
    $NonMetadataHits | Where-Object { $_.Path -match '[\\/]tests?[\\/]|(\.test\.|\.spec\.)' }
)
$DocumentationHits = @(
    $NonMetadataHits | Where-Object { $_.Path -match '\.(md|mdx)$' }
)

$Output = @(
    "Targeted deletion-candidate reference scan."
    "Tracked text files searched: $($TrackedFiles.Count)"
    "Candidate: $Candidate"
    "Total literal matches: $($Hits.Count)"
    "Package metadata/lockfile matches: $($MetadataHits.Count)"
    "First-party source matches: $($SourceHits.Count)"
    "Test matches: $($TestHits.Count)"
    "Documentation matches: $($DocumentationHits.Count)"
    "Non-metadata tracked references: $($NonMetadataHits.Count)"
    ""
    "Matches:"
)
foreach($Hit in $Hits)
{
    $RelativePath = $Hit.Path.Substring($Root.Length).TrimStart("\")
    $Output += "$RelativePath`:$($Hit.LineNumber): $($Hit.Line.Trim())"
}
if($NonMetadataHits.Count -eq 0)
{
    $Output += ""
    $Output += "No non-metadata tracked references found."
}
else
{
    $Output += ""
    $Output += "Non-metadata tracked references:"
    foreach($Hit in $NonMetadataHits)
    {
        $RelativePath = $Hit.Path.Substring($Root.Length).TrimStart("\")
        $Output += "$RelativePath`:$($Hit.LineNumber): $($Hit.Line.Trim())"
    }
}
$Output += ""
if($DocumentationHits.Count -gt 0)
{
    $Output += "Disposition: no deletion approved; documentation references require review."
}
else
{
    $Output += "Disposition: recommendation only; no files or dependencies were removed."
}
$EvidencePath = Join-Path $RawDir "deletion-candidate-evidence.txt"
$Output | Set-Content -LiteralPath $EvidencePath -Encoding UTF8

$RuntimePath = Join-Path $Root "docs\Auditing\data\rawshell\phase10\ui-role-test-results.txt"
if(Test-Path -LiteralPath $RuntimePath -PathType Leaf)
{
    Copy-Item -LiteralPath $RuntimePath -Destination (Join-Path $RawDir "runtime-navigation-reference.txt") -Force
}
else
{
    throw "Phase 10 runtime navigation evidence is required."
}

$EvidenceFiles = @("deletion-candidate-evidence.txt", "runtime-navigation-reference.txt")
$Manifest = [ordered]@{
    phase = "phase15"
    objective = "Deletion Candidates"
    generated = (Get-Date).ToString("yyyy-MM-dd HH:mm:ss")
    evidenceFiles = $EvidenceFiles
    evidenceCount = $EvidenceFiles.Count
    primaryEvidence = $EvidenceFiles
    notes = @("Deletion decisions remain recommendations; no source or dependency was removed.")
}
$Manifest |
    ConvertTo-Json -Depth 20 |
    Set-Content -LiteralPath (Join-Path $RawDir "rawshell-manifest.json") -Encoding UTF8

$PhaseControl = [ordered]@{
    phase = "phase15"
    phaseNumber = 15
    objective = "Deletion Candidates"
    status = "REVIEW REQUIRED"
    factExtractors = @(
        @{
            file = "deletion-candidate-evidence.txt"
            type = "contains"
            search = "First-party source matches: 0"
            label = "No first-party source references to router dependency"
        },
        @{
            file = "deletion-candidate-evidence.txt"
            type = "contains"
            search = "Disposition: no deletion approved"
            label = "Dependency deletion is not approved"
        },
        @{
            file = "deletion-candidate-evidence.txt"
            type = "contains"
            search = "Documentation matches:"
            label = "Documentation references assessed"
        },
        @{
            file = "runtime-navigation-reference.txt"
            type = "contains"
            search = "Administrator desktop: all seven tabs visible."
            label = "Navigation runtime evidence present"
        }
    )
    importantFiles = @(
        "frontend/package.json"
        "frontend/package-lock.json"
        "frontend/src"
        "backend/tests"
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
        "Recommend removal only where all required references are absent"
        "Never delete automatically"
    )
    nextAction = "Run backend authorization tests in Phase 16."
    generatedBy = "CASELOOP"
}
foreach($ControlPath in @(
    (Join-Path $ControlDir "phase15.json"),
    (Join-Path $ControlDir "current-phase.json")
))
{
    $PhaseControl |
        ConvertTo-Json -Depth 20 |
        Set-Content -LiteralPath $ControlPath -Encoding UTF8
}

Write-Host "PASS Phase 15 deletion-candidate evidence generated."
Write-Host "Tracked text files searched: $($TrackedFiles.Count)"
Write-Host "Evidence: $RawDir"
