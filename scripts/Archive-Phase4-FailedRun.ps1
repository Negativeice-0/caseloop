# =====================================================================
# Archive Failed Phase 4 Audit Run
# =====================================================================

$ErrorActionPreference = "Stop"

$Timestamp = Get-Date -Format "yyyyMMdd-HHmmss"

$SourceDirs = @(
    ".\docs\auditing\data\rawshell\phase4",
    ".\docs\auditing\data\fullstack\phase4",
    ".\docs\auditing\data\snrlead\phase4"
)

foreach ($Dir in $SourceDirs)
{
    if (Test-Path $Dir)
    {
        $ArchiveDir = "$Dir-failed-$Timestamp"

        Write-Host "Archiving:"
        Write-Host "  $Dir"
        Write-Host "  -> $ArchiveDir"

        Rename-Item `
            -Path $Dir `
            -NewName (Split-Path $ArchiveDir -Leaf)
    }
}

Write-Host ""
Write-Host "Archive complete."
