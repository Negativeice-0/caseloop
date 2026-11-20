# setup.ps1
# Script to create CaseLoop project directories

$dirs = @(
    "backend\app\api",
    "backend\app\core",
    "backend\app\models",
    "backend\app\schemas",
    "backend\app\services",
    "backend\app\modules",
    "backend\tests",
    "frontend\src\components",
    "frontend\src\layouts",
    "frontend\src\pages",
    "frontend\src\features\responses",
    "frontend\src\features\assignments",
    "frontend\src\features\timeline",
    "frontend\src\features\resources",
    "frontend\src\features\reports",
    "frontend\src\features\dashboard",
    "frontend\src\services",
    "frontend\src\hooks",
    "frontend\src\types",
    "frontend\src\utils",
    "docs\projects\caseloop",
    "scripts",
    "data\demo"
)

foreach ($d in $dirs) {
    New-Item -ItemType Directory -Path $d -Force | Out-Null
}

Write-Host "✅ Project directories created successfully."

# In windows no chmod, only gatekeeper policy -- so below
# allows file by file permission override since i did not
# wish to alter the policy of this pc as it is not mine
# powershell -ExecutionPolicy Bypass -File .\setup.ps1

## even activating venv is a bit of a hustle
## PS C:\Users\Admin\Documents\caseloop\backend> Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
## PS C:\Users\Admin\Documents\caseloop\backend> .\venv\Scripts\Activate.ps1    
## (venv) PS C:\Users\Admin\Documents\caseloop\backend> 
## Set-ExecutionPolicy stilll left untouched for security.