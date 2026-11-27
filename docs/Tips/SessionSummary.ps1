# .\docs\Tips\SessionSummary.ps1
#Requires -Version 5.1

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

# ============================================================
# Configuration
# ============================================================

$KeywordLimit = 25
$ExcerptLength = 300

$StopWords = @(
    "and","the","for","with","from","that","this",
    "into","there","their","have","has","had",
    "been","were","was","will","would","could",
    "should","phase","docs","data","file","files",
    "summary","verification","audit","auditing"
)

# ============================================================
# Helper Functions
# ============================================================

function Write-MarkdownFile {
    param(
        [string]$Path,
        [string[]]$Content
    )

    $Text = $Content -join "`n"
    $Text = $Text.Replace("`r`n", "`n").Replace("`r", "`n")
    $Text = [regex]::Replace($Text, "[ \t]+(?=`n)", "")
    $Text = $Text.TrimEnd([char[]]"`r`n") + "`n"
    [System.IO.File]::WriteAllText(
        $Path,
        $Text,
        (New-Object System.Text.UTF8Encoding($false))
    )
}

function Get-KeywordFrequency {
    param(
        [string]$Text
    )

    $Frequency = @{}

    $RegexHits =
        [regex]::Matches(
            $Text.ToLower(),
            '\b[a-z][a-z0-9_-]{3,}\b'
        )

    foreach($Hit in $RegexHits)
    {
        $Word = $Hit.Value

        if($StopWords -contains $Word)
        {
            continue
        }

        if(-not $Frequency.ContainsKey($Word))
        {
            $Frequency[$Word] = 0
        }

        $Frequency[$Word]++
    }

    return $Frequency.GetEnumerator() |
        Sort-Object Value -Descending |
        Select-Object -First $KeywordLimit
}

# ============================================================
# Load Phase Metadata
# ============================================================

$CurrentPhaseFile =
"docs\Auditing\control\current-phase.json"

if(-not (Test-Path $CurrentPhaseFile))
{
    throw "Missing: $CurrentPhaseFile"
}

$CurrentPhase =
    Get-Content `
        $CurrentPhaseFile `
        -Raw |
    ConvertFrom-Json

$Phase = $CurrentPhase.phase

if([string]::IsNullOrWhiteSpace($Phase))
{
    throw "The active phase control file does not define a phase."
}

# ============================================================
# Paths
# ============================================================

$RawDir =
"docs\Auditing\data\rawshell\$Phase"

$FullDir =
"docs\Auditing\data\fullstack\$Phase"

$LeadDir =
"docs\Auditing\data\snrlead\$Phase"

New-Item `
    -ItemType Directory `
    -Force `
    -Path $FullDir | Out-Null

New-Item `
    -ItemType Directory `
    -Force `
    -Path $LeadDir | Out-Null

if(-not (Test-Path $RawDir))
{
    throw "Missing rawshell directory: $RawDir"
}

# ============================================================
# Load Manifest
# ============================================================

$ManifestFile =
Join-Path `
    $RawDir `
    "rawshell-manifest.json"

$Manifest = $null

if(Test-Path $ManifestFile)
{
    $Manifest =
        Get-Content `
            $ManifestFile `
            -Raw |
        ConvertFrom-Json
}

# ============================================================
# Evidence Discovery
# ============================================================

$EvidenceFiles = @(
    Get-ChildItem `
        -Path $RawDir `
        -Recurse `
        -File |
    Where-Object {
        $_.Name -ne "rawshell-manifest.json"
    }
)

if($EvidenceFiles.Count -eq 0)
{
    throw "No evidence files found."
}

# ============================================================
# Evidence Parsing
# ============================================================

$AllText = @()

$ExcerptEntries = @()

$TotalLines = 0
$TotalBytes = 0

foreach($EvidenceFile in $EvidenceFiles)
{
    $Text =
        Get-Content `
            $EvidenceFile.FullName `
            -Raw `
            -ErrorAction SilentlyContinue

    if([string]::IsNullOrWhiteSpace($Text))
    {
        continue
    }

    $AllText += $Text

    $TotalBytes += $EvidenceFile.Length

    $TotalLines +=
        ($Text -split "`n").Count

    $Length =
        [Math]::Min(
            $ExcerptLength,
            $Text.Length
        )

    $ExcerptEntries +=
        [pscustomobject]@{
            File    = $EvidenceFile.Name
            Excerpt = $Text.Substring(0,$Length)
        }
}

$CombinedText =
$AllText -join "`n"

# ============================================================
# Fact Extractors
# ============================================================

$VerifiedFacts = @(
    "Evidence files discovered: $($EvidenceFiles.Count)"
    "Evidence successfully parsed"
    "Keyword extraction completed"
)

foreach($Extractor in @($CurrentPhase.factExtractors))
{
    if(
        [string]::IsNullOrWhiteSpace($Extractor.file) -or
        [string]::IsNullOrWhiteSpace($Extractor.type) -or
        [string]::IsNullOrWhiteSpace($Extractor.label)
    )
    {
        throw "Each fact extractor must define file, type, and label."
    }

    $ExtractorPath = Join-Path $RawDir $Extractor.file
    $ExtractorType = [string]$Extractor.type

    if($ExtractorType -eq "exists")
    {
        $Value = Test-Path -LiteralPath $ExtractorPath
    }
    else
    {
        if(-not (Test-Path -LiteralPath $ExtractorPath -PathType Leaf))
        {
            throw "Fact extractor evidence file is missing: $ExtractorPath"
        }

        $ExtractorText = Get-Content -LiteralPath $ExtractorPath -Raw

        switch($ExtractorType)
        {
            "count-lines" {
                $Value = @(Get-Content -LiteralPath $ExtractorPath).Count
            }
            "count-matches" {
                if([string]::IsNullOrWhiteSpace($Extractor.search))
                {
                    throw "count-matches requires a search pattern: $($Extractor.label)"
                }

                $Value = [regex]::Matches(
                    $ExtractorText,
                    [string]$Extractor.search
                ).Count
            }
            "contains" {
                if($null -eq $Extractor.search)
                {
                    throw "contains requires a search value: $($Extractor.label)"
                }

                $Value = $ExtractorText.Contains([string]$Extractor.search)
            }
            "first-match" {
                if([string]::IsNullOrWhiteSpace($Extractor.search))
                {
                    throw "first-match requires a search pattern: $($Extractor.label)"
                }

                $Match = [regex]::Match(
                    $ExtractorText,
                    [string]$Extractor.search
                )
                $Value = if($Match.Success) { $Match.Value } else { "not found" }
            }
            default {
                throw "Unsupported fact extractor type: $ExtractorType"
            }
        }
    }

    $VerifiedFacts +=
        "$($Extractor.label): $Value (evidence: $($Extractor.file))"
}

if($Manifest)
{
    $VerifiedFacts += "Manifest detected"
}

# ============================================================
# Indicators
# ============================================================

$RegexOptions =
[System.Text.RegularExpressions.RegexOptions]::IgnoreCase

$PassCount =
([regex]::Matches(
    $CombinedText,
    '\bpass\b',
    $RegexOptions
)).Count

$FailCount =
([regex]::Matches(
    $CombinedText,
    '\bfail\b',
    $RegexOptions
)).Count

$WarningCount =
([regex]::Matches(
    $CombinedText,
    '\bwarning\b',
    $RegexOptions
)).Count

$ErrorCount =
([regex]::Matches(
    $CombinedText,
    '\berror\b',
    $RegexOptions
)).Count

$TodoCount =
([regex]::Matches(
    $CombinedText,
    '\btodo\b',
    $RegexOptions
)).Count

# ============================================================
# Keywords
# ============================================================

$Keywords =
Get-KeywordFrequency `
    -Text $CombinedText

# ============================================================
# Status
# ============================================================

$Status = "REVIEW REQUIRED"

# ============================================================
# Normalized JSON
# ============================================================

$Normalized = [ordered]@{
    phase         = $Phase
    objective     = $CurrentPhase.objective
    generated     = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    evidenceCount = $EvidenceFiles.Count
    totalLines    = $TotalLines
    totalBytes    = $TotalBytes

    textMentions = [ordered]@{
        PASS_MENTIONS    = $PassCount
        FAIL_MENTIONS    = $FailCount
        WARNING_MENTIONS = $WarningCount
        ERROR_MENTIONS   = $ErrorCount
        TODO_MENTIONS    = $TodoCount
    }

    verifiedFacts = @($VerifiedFacts)

    topKeywords = @(
        foreach($Keyword in $Keywords)
        {
            [ordered]@{
                keyword = $Keyword.Key
                count   = $Keyword.Value
            }
        }
    )
}

$Normalized |
ConvertTo-Json -Depth 20 |
Set-Content `
    (Join-Path $FullDir "normalized.json") `
    -Encoding UTF8

# ============================================================
# keyword-frequency.json
# ============================================================

@(
    foreach($Keyword in $Keywords)
    {
        [pscustomobject]@{
            keyword = $Keyword.Key
            count   = $Keyword.Value
        }
    }
) |
ConvertTo-Json -Depth 10 |
Set-Content `
    (Join-Path $FullDir "keyword-frequency.json") `
    -Encoding UTF8

# ============================================================
# evidence-excerpts.md
# ============================================================

$Output = @(
    "# Evidence Excerpts",
    ""
)

foreach($Entry in $ExcerptEntries)
{
    $Output += "## $($Entry.File)"
    $Output += ""
    $Output += $Entry.Excerpt
    $Output += ""
}

Write-MarkdownFile `
    -Path (Join-Path $FullDir "evidence-excerpts.md") `
    -Content $Output

# ============================================================
# findings.md
# ============================================================

$Output = @(
    "# Findings",
    "",
    "- Files Parsed: $($EvidenceFiles.Count)",
    "- Lines Parsed: $TotalLines",
    "- Text mentions (not test outcomes): PASS $PassCount; FAIL $FailCount; WARNING $WarningCount; ERROR $ErrorCount; TODO $TodoCount"
)

Write-MarkdownFile `
    -Path (Join-Path $FullDir "findings.md") `
    -Content $Output

# ============================================================
# summary.md
# ============================================================

$Output = @(
    "# Summary",
    "",
    "Phase: $Phase",
    "Objective: $($CurrentPhase.objective)",
    "Status: $Status",
    "",
    "## Verified Facts",
    ""
)

foreach($Fact in $VerifiedFacts)
{
    $Output += "- $Fact"
}

$Output += ""
$Output += "## Next Action"
$Output += ""
$Output += $CurrentPhase.nextAction

Write-MarkdownFile `
    -Path (Join-Path $FullDir "summary.md") `
    -Content $Output

# ============================================================
# verification.md
# ============================================================

$Output = @(
    "# Verification",
    "",
    "Status: $Status",
    "Evidence Files: $($EvidenceFiles.Count)",
    "Evidence Lines: $TotalLines",
    "This generator reports evidence-derived facts; manual review is still required.",
    ""
)

foreach($Fact in $VerifiedFacts)
{
    $Output += "- $Fact"
}

Write-MarkdownFile `
    -Path (Join-Path $LeadDir "verification.md") `
    -Content $Output

# ============================================================
# logbook.md
# ============================================================

$Rating = 8

if($FailCount -gt 0)
{
    $Rating = 6
}
elseif($WarningCount -gt 0)
{
    $Rating = 7
}

$Output = @(
    "Work Done:",
    "Processed $($EvidenceFiles.Count) evidence files and generated audit artifacts.",
    "",
    "Effective Rating:",
    "$Rating/10",
    "",
    "Knowledge Gained:",
    "",
    "People Interacted With:",
    "Copilot"
)

Write-MarkdownFile `
    -Path (Join-Path $FullDir "logbook.md") `
    -Content $Output

# ============================================================
# Console Output
# ============================================================

Write-Host ""
Write-Host "PASS SessionSummary Complete"
Write-Host ""

Write-Host (Join-Path $FullDir "normalized.json")
Write-Host (Join-Path $FullDir "keyword-frequency.json")
Write-Host (Join-Path $FullDir "evidence-excerpts.md")
Write-Host (Join-Path $FullDir "findings.md")
Write-Host (Join-Path $FullDir "summary.md")
Write-Host (Join-Path $LeadDir "verification.md")
Write-Host (Join-Path $FullDir "logbook.md")