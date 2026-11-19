# To run : \scripts\audit_tree.ps1
Write-Host "🔍 Auditing CaseLoop Project Directory Tree..." -ForegroundColor Cyan

$excluded = 'node_modules|venv|\.git|__pycache__|dist|build|\.pytest_cache'
$files = Get-ChildItem -Recurse -File | Where-Object { $_.FullName -notmatch "\\($excluded)\\" }

$count = 0
foreach ($file in $files) {
    $relPath = $file.FullName.Replace((Get-Location).Path, "").TrimStart("\")
    Write-Host "  ├── $relPath" -ForegroundColor Green
    $count++
}

Write-Host "✅ Audit complete. Total files found: $count" -ForegroundColor Cyan
