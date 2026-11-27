# .\scripts\auditing\phase1\run_audit.ps1

$ErrorActionPreference = "Stop"

$rawDirectory = ".\docs\auditing\data\rawshell"
$rawFile = Join-Path $rawDirectory "phase1data.txt"

New-Item -ItemType Directory -Force -Path $rawDirectory | Out-Null

Write-Host "🔍 Starting Checkpoint 14 audit..." -ForegroundColor Cyan
Write-Host "📝 Recording session to $rawFile" -ForegroundColor Yellow

try {
    Start-Transcript -Path $rawFile -Force

    Write-Host ""
    Write-Host "📁 Auditing project directory tree..." -ForegroundColor Cyan
    & ".\scripts\auditing\phase1\audit_tree.ps1"

    Write-Host ""
    Write-Host "🌐 Add approved health-check commands here if needed." `
        -ForegroundColor Yellow

    Write-Host ""
    Write-Host "✅ Audit commands completed." -ForegroundColor Green
}
catch {
    Write-Host "❌ Audit stopped: $($_.Exception.Message)" -ForegroundColor Red
}
finally {
    Stop-Transcript | Out-Null
    Write-Host "📝 Session saved to $rawFile" -ForegroundColor Cyan
    Write-Host "✅ Audit finished." -ForegroundColor Green
}
