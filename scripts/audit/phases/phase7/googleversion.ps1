
#Requires -Version 5.1

$ErrorActionPreference = "Stop"

$ProjectRoot = (Get-Location).Path

$OutputDirectory = Join-Path `
    $ProjectRoot `
    "docs\Auditing\data\rawshell\phase7"

$InventoryFile = Join-Path `
    $OutputDirectory `
    "runtime-inventory.txt"

$ManifestFile = Join-Path `
    $OutputDirectory `
    "runtime-inventory.csv"

$Roots = @(
    # Frontend
    @{ Path = "frontend\src\features"; Layer = "Frontend Features" }
    @{ Path = "frontend\src\components"; Layer = "Frontend Components" }
    @{ Path = "frontend\src\hooks"; Layer = "Frontend Hooks" }
    @{ Path = "frontend\src\services"; Layer = "Frontend Services" }
    @{ Path = "frontend\src\api"; Layer = "Frontend API" }
    @{ Path = "frontend\src\store"; Layer = "Frontend State" }

    # Backend
    @{ Path = "backend\app\api"; Layer = "Backend API" }
    @{ Path = "backend\app\services"; Layer = "Backend Services" }
    @{ Path = "backend\app\repositories"; Layer = "Backend Repositories" }
    @{ Path = "backend\app\models"; Layer = "Backend Models" }
    @{ Path = "backend\app\schemas"; Layer = "Backend Schemas" }
    @{ Path = "backend\app\db"; Layer = "Database Infrastructure" }
    @{ Path = "backend\app\core"; Layer = "Backend Core" }
    @{ Path = "backend\app\tasks"; Layer = "Background Tasks" }
    @{ Path = "backend\app\events"; Layer = "Event Processing" }
    @{ Path = "backend\app\integrations"; Layer = "External Integrations" }

    # Database
    @{ Path = "backend\migrations"; Layer = "Database Migrations" }
    @{ Path = "migrations"; Layer = "Database Migrations" }

    # Infrastructure
    @{ Path = "infrastructure"; Layer = "Infrastructure" }
    @{ Path = "deploy"; Layer = "Deployment" }
    @{ Path = "k8s"; Layer = "Kubernetes" }
)

New-Item `
    -ItemType Directory `
    -Force `
    -Path $OutputDirectory |
Out-Null

$Inventory = @()

foreach ($Root in $Roots) {

    $FullPath = Join-Path `
        $ProjectRoot `
        $Root.Path

    if (-not (Test-Path $FullPath -PathType Container)) {
        continue
    }

    Get-ChildItem `
        -LiteralPath $FullPath `
        -Recurse `
        -File |
    ForEach-Object {

        $Inventory += [PSCustomObject]@{
            Layer = $Root.Layer
            Root = $Root.Path
            File = $_.FullName
            Extension = $_.Extension
            Name = $_.Name
            RelativePath = $_.FullName.Substring(
                $ProjectRoot.Length
            ).TrimStart('\')
        }
    }
}

$Inventory = @(
    $Inventory |
    Sort-Object File -Unique
)

$Inventory |
Select-Object -ExpandProperty File |
Set-Content -LiteralPath $InventoryFile

$Inventory |
Export-Csv `
    -LiteralPath $ManifestFile `
    -NoTypeInformation `
    -Encoding UTF8

Write-Host ""
Write-Host "PASS"
Write-Host "Runtime Files:" $Inventory.Count
Write-Host "Inventory:" $InventoryFile
Write-Host "Manifest:" $ManifestFile
Write-Host ""

$Inventory |
Group-Object Layer |
Sort-Object Name |
ForEach-Object {
    Write-Host ("{0}: {1}" -f $_.Name, $_.Count)
}
