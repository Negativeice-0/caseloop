#Requires -Version 5.1

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$Files = @(
    "docs\auditing\data\fullstack\phase5\backend-route-inventory.json",
    "docs\auditing\data\fullstack\phase5\authorization-dependencies.json"
)

foreach($File in $Files)
{
    if(!(Test-Path $File))
    {
        Write-Host "MISSING: $File"
        continue
    }

    Write-Host ""
    Write-Host "======================================="
    Write-Host $File
    Write-Host "======================================="

    $Json = Get-Content $File -Raw | ConvertFrom-Json

    if($Json -is [array])
    {
        Write-Host "Array Count:" $Json.Count

        if($Json.Count -gt 0)
        {
            $Json[0] |
                Get-Member -MemberType NoteProperty |
                Select-Object Name
        }
    }
    else
    {
        $Json |
            Get-Member -MemberType NoteProperty |
            Select-Object Name
    }
}