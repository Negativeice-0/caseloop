#Requires -Version 5.1

$ErrorActionPreference = "Stop"

$EvidenceFile = "docs\Auditing\data\rawshell\phase5\backend-route-auth-evidence.txt"
$OutputFile = "docs\Auditing\data\fullstack\phase5\authorization-normalized.json"

if (!(Test-Path $EvidenceFile))
{
    throw "Missing $EvidenceFile"
}

$Results = @()

Get-Content $EvidenceFile | ForEach-Object {

    $Line = $_

    if (
        $Line -match "role" -or
        $Line -match "permission" -or
        $Line -match "auth" -or
        $Line -match "admin" -or
        $Line -match "Depends\(" -or
        $Line -match "current_user" -or
        $Line -match "authorize"
    )
    {
        $Results += [PSCustomObject]@{
            Evidence = $Line.Trim()
        }
    }
}

$Results |
    ConvertTo-Json -Depth 5 |
    Set-Content $OutputFile

Write-Host "PASS"
Write-Host "authorization-normalized.json created"