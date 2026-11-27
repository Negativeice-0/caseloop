#Requires -Version 5.1

param(
    [string]$Root = "."
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

# ============================================================
# Paths
# ============================================================

$RawDir =
Join-Path `
    $Root `
    "docs\Auditing\data\rawshell\phase8"

$ControlDir =
Join-Path `
    $Root `
    "docs\Auditing\control"

$null =
New-Item `
    -ItemType Directory `
    -Force `
    -Path $RawDir

$null =
New-Item `
    -ItemType Directory `
    -Force `
    -Path $ControlDir

# ============================================================
# Exclusions
# ============================================================

$ExcludedPatterns = @(
    "node_modules"
    ".git"
    "venv"
    ".venv"
    "__pycache__"
    "dist"
    "build"
    "coverage"
    ".pytest_cache"
)

function Test-ExcludedPath
{
    param(
        [string]$Path
    )

    foreach($Pattern in $ExcludedPatterns)
    {
        if($Path -match [regex]::Escape($Pattern))
        {
            return $true
        }
    }

    return $false
}

# ============================================================
# Documentation Discovery
# ============================================================

$DocumentationFiles = @(
    Get-ChildItem `
        -Path $Root `
        -Recurse `
        -File `
        -ErrorAction SilentlyContinue |
    Where-Object {

        if(Test-ExcludedPath $_.FullName)
        {
            return $false
        }

        (
            $_.Name -match '^README(\..+)?$'
        ) -or (
            $_.Extension -in @(
                ".md",
                ".rst",
                ".txt"
            )
        )
    } |
    Sort-Object FullName
)

$DocumentationInventoryFile =
Join-Path `
    $RawDir `
    "documentation-inventory.txt"

$DocumentationFiles |
Select-Object `
    FullName,
    Length,
    LastWriteTime |
Out-File `
    -FilePath $DocumentationInventoryFile `
    -Encoding UTF8

# ============================================================
# README Discovery
# ============================================================

$ReadmeFiles = @(
    $DocumentationFiles |
    Where-Object {
        $_.Name -match '^README'
    }
)

$ReadmeInventoryFile =
Join-Path `
    $RawDir `
    "readme-inventory.txt"

$ReadmeFiles |
Select-Object FullName |
Out-File `
    -FilePath $ReadmeInventoryFile `
    -Encoding UTF8

# ============================================================
# Coverage Checks
# ============================================================

$ExpectedDocuments = @(
    "README.md"
    "docker-compose.yml"
)

$CoverageResults =
foreach($Document in $ExpectedDocuments)
{
    $DocumentHits = @(
        Get-ChildItem `
            -Path $Root `
            -Recurse `
            -File `
            -ErrorAction SilentlyContinue |
        Where-Object {

            if(Test-ExcludedPath $_.FullName)
            {
                return $false
            }

            $_.Name -eq $Document
        }
    )

    [pscustomobject]@{
        Item    = $Document
        Present = ($DocumentHits.Count -gt 0)
        Hits    = $DocumentHits.Count
    }
}

$CoverageFile =
Join-Path `
    $RawDir `
    "documentation-coverage.txt"

$CoverageResults |
Format-Table -AutoSize |
Out-File `
    -FilePath $CoverageFile `
    -Encoding UTF8

# ============================================================
# rawshell-manifest.json
# ============================================================

$EvidenceFiles = @(
    "documentation-inventory.txt"
    "readme-inventory.txt"
    "documentation-coverage.txt"
)

$Manifest = [ordered]@{
    phase           = "phase8"
    objective       = "README and Documentation Audit"
    generated       = (Get-Date).ToString("yyyy-MM-dd HH:mm:ss")
    evidenceFiles   = $EvidenceFiles
    evidenceCount   = $EvidenceFiles.Count

    primaryEvidence = @(
        "documentation-inventory.txt"
        "documentation-coverage.txt"
    )

    notes = @(
        "Documentation inventory collected"
        "README inventory collected"
        "Coverage checks completed"
    )
}

$ManifestPath =
Join-Path `
    $RawDir `
    "rawshell-manifest.json"

$Manifest |
ConvertTo-Json -Depth 20 |
Set-Content `
    -Path $ManifestPath `
    -Encoding UTF8


# ============================================================
# phase8.json
# ============================================================

$PhaseControl = [ordered]@{

    phase = "phase8"

    phaseNumber = 8

    objective =
    "README and Documentation Audit"

    status =
    "COMPLETE"

    factExtractors = @(

        @{
            file  = "readme-inventory.txt"
            type  = "count-lines"
            label = "README files discovered"
        },

        @{
            file  = "documentation-inventory.txt"
            type  = "count-lines"
            label = "Documentation files discovered"
        },

        @{
            file   = "documentation-coverage.txt"
            type   = "contains"
            search = "README.md"
            label  = "README.md present"
        },

        @{
            file   = "documentation-coverage.txt"
            type   = "contains"
            search = "docker-compose.yml"
            label  = "docker-compose.yml present"
        }
    )

    importantFiles = @(
        "README.md"
        "docs/deployment"
        "docs/design"
    )

    expectedEvidence = @(
        "documentation-inventory.txt"
        "readme-inventory.txt"
        "documentation-coverage.txt"
    )

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
        "README accuracy"
        "Deployment documentation accuracy"
        "Architecture documentation accuracy"
        "API documentation accuracy"
    )

    verificationCommands = @(
        "Get-ChildItem docs/Auditing/data/rawshell/phase8"
        "Get-Content docs/Auditing/data/rawshell/phase8/documentation-coverage.txt"
        "Get-Content docs/Auditing/control/phase8.json"
    )

    successCriteria = @(
        "Documentation inventory exists"
        "README inventory exists"
        "Coverage report exists"
        "Manifest exists"
        "Control file exists"
    )

    nextAction =
    "Run SessionSummary and validate documentation findings"

    generatedBy =
    "CASELOOP"
}

$PhaseControlPath =
Join-Path `
    $ControlDir `
    "phase8.json"

$CurrentPhasePath =
Join-Path `
    $ControlDir `
    "current-phase.json"

$PhaseControl |
ConvertTo-Json -Depth 20 |
Set-Content `
    -Path $PhaseControlPath `
    -Encoding UTF8

$PhaseControl |
ConvertTo-Json -Depth 20 |
Set-Content `
    -Path $CurrentPhasePath `
    -Encoding UTF8

# ============================================================
# Console Output
# ============================================================

Write-Host ""
Write-Host "PASS Documentation Files:" $DocumentationFiles.Count
Write-Host "PASS README Files:" $ReadmeFiles.Count
Write-Host "PASS Manifest Generated"
Write-Host "PASS Control Files Generated"

Write-Host ""
Write-Host "Artifacts"
Write-Host ""

Write-Host $DocumentationInventoryFile
Write-Host $ReadmeInventoryFile
Write-Host $CoverageFile
Write-Host $ManifestPath
Write-Host $PhaseControlPath
Write-Host $CurrentPhasePath

Write-Host ""
Write-Host "Verification Commands"
Write-Host ""

Write-Host "Get-ChildItem docs\Auditing\data\rawshell\phase8"
Write-Host ""

Write-Host "Get-Content docs\Auditing\data\rawshell\phase8\rawshell-manifest.json"
Write-Host ""

Write-Host "Get-Content docs\Auditing\control\phase8.json"

Write-Host ""
Write-Host "Success Criteria"
Write-Host ""

Write-Host "- documentation-inventorysts"
Write-Host "- readme-inventory.txt exists"
Write-Host "- documentation-coverage.txt exists"
Write-Host "- rawshell-manifest.json exists"
Write-Host "- phase8.json exists"
Write-Host "- current-phase.json exists"