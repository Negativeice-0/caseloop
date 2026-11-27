#Requires -Version 5.1

param(
    [string]$Root = "."
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$Root = (Resolve-Path $Root).Path
$RawDir = Join-Path $Root "docs\Auditing\data\rawshell\phase19"
$ControlDir = Join-Path $Root "docs\Auditing\control"
$Phase18Evidence = Join-Path $Root "docs\Auditing\data\rawshell\phase18\backend-pytest.txt"
$Docs = @(
    [pscustomobject]@{
        Path = Join-Path $Root "README.md"
        Required = @(
            "The current seeder creates built-in default accounts"
            "Use the UI or isolated test fixtures for synthetic data"
        )
    },
    [pscustomobject]@{
        Path = Join-Path $Root "docs\deployment\DEPLOYMENT.md"
        Required = @(
            "The current seeder creates built-in default accounts"
            "Use the application UI or isolated test fixtures for synthetic data"
        )
    },
    [pscustomobject]@{
        Path = Join-Path $Root "docs\deployment\oracle-whatsapp-learning-runbook.md"
        Required = @(
            "short-lived pull-request branches"
            "Promote the same reviewed commit"
        )
    }
)

New-Item -ItemType Directory -Force -Path $RawDir | Out-Null
New-Item -ItemType Directory -Force -Path $ControlDir | Out-Null

$EvidenceLines = @("Phase 19 documentation checks:")
foreach($Doc in $Docs)
{
    if(-not (Test-Path -LiteralPath $Doc.Path -PathType Leaf))
    {
        throw "Documentation file is missing: $($Doc.Path)"
    }
    $Content = Get-Content -LiteralPath $Doc.Path -Raw
    foreach($Phrase in $Doc.Required)
    {
        if(-not $Content.Contains($Phrase))
        {
            throw "Expected verified documentation text is missing from $($Doc.Path): $Phrase"
        }
    }
    $RelativePath = $Doc.Path.Substring($Root.Length).TrimStart("\")
    $EvidenceLines += "${RelativePath}: required safety/deployment guidance present."
}

$Readme = Get-Content -LiteralPath (Join-Path $Root "README.md") -Raw
if($Readme.Contains("The seeder refuses to create any placeholder/default account"))
{
    throw "README still contains the contradicted seeder claim."
}
if(-not (Test-Path -LiteralPath $Phase18Evidence -PathType Leaf))
{
    throw "Phase 18 backend test evidence is missing: $Phase18Evidence"
}
$TestEvidence = Get-Content -LiteralPath $Phase18Evidence -Raw
if(-not $TestEvidence.Contains("1 failed, 28 passed"))
{
    throw "Phase 18 test evidence no longer contains the reviewed outcome."
}
$EvidenceLines += "README no longer claims the seeder refuses default-account creation."
$EvidenceLines += "Oracle runbook recommends: Promote the same reviewed commit from test/staging to production."
$EvidenceLines += "Phase 18 backend evidence cross-check: 28 passed, 1 failed (seed-guard expectation)."

$EvidencePath = Join-Path $RawDir "documentation-review.txt"
$EvidenceLines | Set-Content -LiteralPath $EvidencePath -Encoding UTF8

$EvidenceFiles = @("documentation-review.txt")
$Manifest = [ordered]@{
    phase = "phase19"
    objective = "Documentation Update"
    generated = (Get-Date).ToString("yyyy-MM-dd HH:mm:ss")
    evidenceFiles = $EvidenceFiles
    evidenceCount = $EvidenceFiles.Count
    primaryEvidence = $EvidenceFiles
    notes = @("Documentation statements were checked against Phase 18 test evidence and current deployment guidance.")
}
$Manifest |
    ConvertTo-Json -Depth 20 |
    Set-Content -LiteralPath (Join-Path $RawDir "rawshell-manifest.json") -Encoding UTF8

$PhaseControl = [ordered]@{
    phase = "phase19"
    phaseNumber = 19
    objective = "Documentation Update"
    status = "REVIEW REQUIRED"
    factExtractors = @(
        @{
            file = "documentation-review.txt"
            type = "contains"
            search = "README no longer claims"
            label = "Contradicted seeder documentation corrected"
        },
        @{
            file = "documentation-review.txt"
            type = "contains"
            search = "Promote the same reviewed commit"
            label = "Recommended branch/deployment flow documented"
        }
    )
    importantFiles = @(
        "README.md"
        "docs/deployment/DEPLOYMENT.md"
        "docs/deployment/oracle-whatsapp-learning-runbook.md"
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
        "Seeder safety warning matches Phase 18 test evidence"
        "Oracle and WhatsApp branch/promotion guidance is present"
    )
    nextAction = "Prepare the final evidence-backed handover and learning extraction in Phase 20."
    generatedBy = "CASELOOP"
}
foreach($ControlPath in @(
    (Join-Path $ControlDir "phase19.json"),
    (Join-Path $ControlDir "current-phase.json")
))
{
    $PhaseControl |
        ConvertTo-Json -Depth 20 |
        Set-Content -LiteralPath $ControlPath -Encoding UTF8
}

Write-Host "PASS Phase 19 documentation cross-checks."
Write-Host "Evidence: $EvidencePath"
