$InputFile  = ".\docs\knowledge\master\extract-concise-log.txt"
$OutputFile = ".\docs\knowledge\master\extract-concise-log-filtered.txt"

$backend = Get-Content $InputFile |
    Where-Object { $_ -match '^backend\\app(\\|$)' }

$frontend = Get-Content $InputFile |
    Where-Object { $_ -match '^frontend\\src(\\|$)' }

@(
    "## Backend"
    ""
    $backend
    ""
    "## Frontend"
    ""
    $frontend
) | Set-Content $OutputFile

Write-Host "Saved to $OutputFile"