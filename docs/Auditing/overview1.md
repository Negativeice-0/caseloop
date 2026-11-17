# Create file

$scriptContent = @'
# scripts/audit_tree.ps1
Write-Host "🔍 Auditing CaseLoop Project Directory Tree..." -ForegroundColor Cyan

$excluded = 'node_modules|venv|\.git|__pycache__|dist|build|\.pytest_cache'
$files = Get-ChildItem -Recurse -File | Where-Object { $_.FullName -notmatch "\\($excluded)\\" }

$count = 0
foreach ($file in $files) {
    $relPath = $file.FullName.Replace((Get-Location).Path, "").TrimStart("\")
    Write-Host "  ├── $relPath" -ForegroundColor Green
    $count++
}

Write-Host "✅ Audit complete. Total files found: $count" -ForegroundColor Cyan
'@

Set-Content -Path "scripts\audit_tree.ps1" -Value $scriptContent -Encoding UTF8


# Actual Overview

PS C:\Users\Admin\Documents\caseloop> .\scripts\audit_tree.ps1

🔍 Auditing CaseLoop Project Directory Tree...
  ├── README.md
  ├── setup.ps1
  ├── backend\alembic.ini
  ├── backend\caseloop.db
  ├── backend\requirements.txt
  ├── backend\alembic\env.py
  ├── backend\alembic\README
  ├── backend\alembic\script.py.mako
  ├── backend\alembic\versions\1b86f570ca4e_add_response_reference_code_category_.py
  ├── backend\alembic\versions\63fb95653be7_add_full_name_and_user_updates.py
  ├── backend\alembic\versions\cda7af70145b_add_is_active_to_users.py
  ├── backend\app\main.py
  ├── backend\app\seed.py
  ├── backend\app\api\__init__.py
  ├── backend\app\core\config.py
  ├── backend\app\core\database.py
  ├── backend\app\models\models.py
  ├── backend\app\models\__init__.py
  ├── backend\app\modules\__init__.py
  ├── backend\app\schemas\__init__.py
  ├── backend\app\services\__init__.py
  ├── backend\tests\test_main.py
  ├── docs\Auditing\week1.md
  ├── docs\Auditing\data\backend\week1api.md
  ├── docs\Auditing\data\database\week1alchmy.md
  ├── docs\Auditing\data\frontend\week1react18.md
  ├── docs\deployment\DEPLOYMENT.md
  ├── docs\projects\caseloop\.vsconfig
  ├── docs\projects\caseloop\CASE-LOOP_RED-CROSS_CONSIDERATION.txt
  ├── docs\projects\caseloop\caseloop_master_handover_attachment_blueprint.md
  ├── docs\projects\caseloop\IMPLEMENTATION.md
  ├── docs\projects\caseloop\OVERVIEW.md
  ├── docs\Tips\TIP1.md
  ├── docs\trouble\1-setup.md
  ├── docs\trouble\2-dbIssues.md
  ├── frontend\index.html
  ├── frontend\package-lock.json
  ├── frontend\package.json
  ├── frontend\src\App.tsx
  ├── frontend\src\main.tsx
  ├── frontend\src\postcss.config.js
  ├── frontend\src\tailwind.config.js
  ├── frontend\src\features\dashboard\Dashboard.tsx
  ├── frontend\src\services\api.ts
  ├── scripts\audit_tree.ps1
✅ Audit complete. Total files found: 45