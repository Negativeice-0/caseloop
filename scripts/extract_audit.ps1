# To run : .\scripts\extract_audit.ps1

param(
    [Parameter(Mandatory = $true)]
    [string]$InputFile
)

$ErrorActionPreference = "Stop"

if (-not (Test-Path $InputFile)) {
    Write-Host "❌ Input file not found: $InputFile" -ForegroundColor Red
    exit 1
}

$lines = Get-Content $InputFile

$patterns = [ordered]@{
    "Commands"  = "Invoke-WebRequest|Get-|Set-|git |docker |npm |python |pytest|curl"
    "Results"   = "200|201|204|401|403|404|500|passed|failed|success|OK|error"
    "Files"     = "\.(py|js|jsx|ts|tsx|md|json|yml|yaml|ps1)\b"
    "Problems"  = "error|failed|failure|issue|problem|blocked|warning|unresolved"
    "Decisions" = "decision|decided|deferred|keep|delete|avoid|recommend"
}

Write-Host ""
Write-Host "🔍 Extracting useful audit information..." -ForegroundColor Cyan
Write-Host ""

foreach ($section in $patterns.Keys) {
    Write-Host "## $section" -ForegroundColor Yellow

    $matches = $lines |
        Where-Object { $_ -match $patterns[$section] } |
        Select-Object -Unique -First 12

    if ($matches) {
        foreach ($match in $matches) {
            Write-Host "  - $match" -ForegroundColor Green
        }
    }
    else {
        Write-Host "  - Not recorded" -ForegroundColor DarkGray
    }

    Write-Host ""
}

Write-Host "✅ Extraction complete. Raw data was not changed." -ForegroundColor Cyan
