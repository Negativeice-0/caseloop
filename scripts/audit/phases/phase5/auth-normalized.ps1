$Files = @(
    "backend\app\core\auth.py",
    "backend\app\core\security.py"
)

Get-ChildItem "backend\app\api\*.py" |
ForEach-Object {
    $Files += $_.FullName
}

$Results = @()

foreach ($File in $Files)
{
    if (!(Test-Path $File)) { continue }

    $LineNumber = 0

    Get-Content $File | ForEach-Object {

        $LineNumber++

        if (
            $_ -match "Depends\(" -or
            $_ -match "admin" -or
            $_ -match "auth" -or
            $_ -match "permission" -or
            $_ -match "role"
        )
        {
            $Results += [PSCustomObject]@{
                File       = $File
                LineNumber = $LineNumber
                Evidence   = $_.Trim()
            }
        }
    }
}

$Results |
ConvertTo-Json -Depth 10 |
Set-Content `
"docs\Auditing\data\fullstack\phase5\authorization-normalized.json"

Write-Host "PASS"
Write-Host "Normalized authorization evidence:" $Results.Count