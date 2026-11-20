Step 3 — Record baseline backend tests and frontend build
Objective: Identify the repository’s actual backend test command and frontend build command, then run each without changing application code and capture their results as the pre-change baseline.

Why it matters: Later refactors need an objective comparison point. A passing baseline confirms that failures introduced later are attributable to subsequent changes rather than pre-existing problems.

Must not be changed:

Do not edit source code, configuration, dependencies, routes, tests, or documentation.

Do not install, upgrade, remove, or regenerate packages.

Do not run formatting, migrations, database writes, or destructive commands.

Do not guess a backend or frontend command before inspecting the repository.

Use only synthetic or local test data already supported by the project.

Run these commands from the repository root in PowerShell 5.1:

Powershell

Copy
$RepoRoot = (Get-Location).Path
$Stamp = Get-Date -Format "yyyyMMdd-HHmmss"
$BaselineDir = Join-Path $env:TEMP ("CaseLoop-Baseline-" + $Stamp)
New-Item -ItemType Directory -Path $BaselineDir -Force | Out-Null

Write-Host "Repository root:"
Write-Host $RepoRoot
Write-Host ""
Write-Host "Baseline capture directory:"
Write-Host $BaselineDir
Write-Host ""

Write-Host "Candidate project and test/build files:"
Get-ChildItem -Path $RepoRoot -Recurse -File -Force |
    Where-Object {
        $_.FullName -notmatch '\\(node_modules|\.git|\.venv|venv|__pycache__|dist|build|coverage|\.next|\.pytest_cache)\\' -and
        $_.Name -in @(
            'package.json',
            'package-lock.json',
            'npm-shrinkwrap.json',
            'yarn.lock',
            'pnpm-lock.yaml',
            'pyproject.toml',
            'pytest.ini',
            'tox.ini',
            'setup.cfg',
            'requirements.txt',
            'manage.py',
            'Dockerfile',
            'docker-compose.yml',
            'docker-compose.yaml'
        )
    } |
    Select-Object -ExpandProperty FullName |
    Tee-Object -FilePath (Join-Path $BaselineDir 'discovered-project-files.txt')

Write-Host ""
Write-Host "Frontend package scripts, if package.json exists:"
$PackageFiles = Get-ChildItem -Path $RepoRoot -Recurse -File -Filter 'package.json' -Force |
    Where-Object {
        $_.FullName -notmatch '\\(node_modules|\.git)\\'
    }

foreach ($PackageFile in $PackageFiles) {
    Write-Host ""
    Write-Host ("--- " + $PackageFile.FullName + " ---")
    try {
        $PackageJson = Get-Content -LiteralPath $PackageFile.FullName -Raw | ConvertFrom-Json
        if ($null -ne $PackageJson.scripts) {
            $PackageJson.scripts | Format-List | Out-String | Write-Host
        }
        else {
            Write-Host "No scripts object found."
        }
    }
    catch {
        Write-Host ("Could not parse package.json: " + $_.Exception.Message)
    }
}

Write-Host ""
Write-Host "Python test configuration indicators:"
Get-ChildItem -Path $RepoRoot -Recurse -File -Force |
    Where-Object {
        $_.FullName -notmatch '\\(node_modules|\.git|\.venv|venv|__pycache__)\\' -and
        $_.Name -in @('pyproject.toml','pytest.ini','tox.ini','setup.cfg','requirements.txt','manage.py')
    } |
    ForEach-Object {
        Write-Host $_.FullName
    } |
    Tee-Object -FilePath (Join-Path $BaselineDir 'python-test-indicators.txt')

Write-Host ""
Write-Host "The discovery phase is complete."
Write-Host "No application files were changed."
Expected output
You should see:

The repository root.

A temporary baseline-capture directory.

One or more discovered files such as package.json, pyproject.toml, pytest.ini, manage.py, or equivalent files.

The frontend scripts entries from each discovered package.json.

Python test-configuration indicators, if present.

The final message: The discovery phase is complete.

The command also writes discovery information outside the repository under $BaselineDir, so it should not create repository changes.

How to interpret the result
Success: At least one real frontend package.json is identified, and its scripts reveal a test and/or build command; backend test configuration or a recognizable backend test layout is also identified.

Failure: The command itself reports a PowerShell error, cannot parse a manifest, or finds no project files. Do not run guessed commands; paste the error and discovery output.

Ambiguity: Multiple package.json files, multiple backend services, or no obvious test/build scripts. Paste the complete output so we can select the correct commands based on evidence.

Important: A missing test script does not prove that frontend tests do not exist. It means we must inspect the actual project structure before choosing a baseline command.

Paste the complete PowerShell output, including the repository root, discovered files, package scripts, Python indicators, and any errors. The baseline step remains in progress until the correct commands are identified and their results are recorded.