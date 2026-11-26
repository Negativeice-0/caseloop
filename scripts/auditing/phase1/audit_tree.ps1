# To run:
# .\scripts\auditing\phase1\audit_tree.ps1

$ErrorActionPreference = "Stop"

$Root = (Get-Location).Path
$Excluded = 'node_modules|venv|\.venv|\.git|__pycache__|dist|build|coverage|\.pytest_cache'

Write-Host ""
Write-Host "🔍 Auditing CaseLoop project tree..." -ForegroundColor Cyan
Write-Host "Root: $Root" -ForegroundColor DarkGray
Write-Host ""

$Files = Get-ChildItem -Path $Root -Recurse -File -Force |
    Where-Object {
        $_.FullName -notmatch "\\($Excluded)(\\|$)"
    } |
    Sort-Object FullName

$Count = 0

foreach ($File in $Files) {
    $RelativePath = $File.FullName.Substring($Root.Length).TrimStart("\")
    Write-Host "  ├── $RelativePath" -ForegroundColor Green
    $Count++
}

Write-Host ""
Write-Host "✅ Audit complete. Total files found: $Count" -ForegroundColor Cyan
Write-Host "Excluded: $Excluded" -ForegroundColor DarkGray
