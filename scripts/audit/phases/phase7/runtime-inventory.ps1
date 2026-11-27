#Requires -Version 5.1

$Files = @()

$Roots = @(
    "frontend\src\features",
    "frontend\src\services",
    "backend\app\api",
    "backend\app\services",
    "backend\app\models"
)

foreach($Root in $Roots)
{
    if(Test-Path $Root)
    {
        Get-ChildItem `
            $Root `
            -Recurse `
            -File |
        ForEach-Object {
            $Files += $_.FullName
        }
    }
}

$Output =
"docs\Auditing\data\fullstack\phase7\runtime-inventory.txt"

New-Item `
    -ItemType Directory `
    -Force `
    "docs\Auditing\data\fullstack\phase7" |
Out-Null

$Files |
Sort-Object |
Set-Content $Output

Write-Host ""
Write-Host "PASS"
Write-Host "Runtime Files:" $Files.Count