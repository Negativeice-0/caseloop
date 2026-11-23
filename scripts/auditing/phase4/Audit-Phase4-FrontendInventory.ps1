# =====================================================================
# Phase 4
# Frontend Route + Navigation Inventory
# =====================================================================

$ErrorActionPreference = "Continue"

$Phase = "phase4"

$RawDir  = ".\docs\auditing\data\rawshell\$Phase"
$FullDir = ".\docs\auditing\data\fullstack\$Phase"
$LeadDir = ".\docs\auditing\data\snrlead\$Phase"

New-Item -ItemType Directory -Force -Path $RawDir,$FullDir,$LeadDir | Out-Null

$Timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

$Branch = git branch --show-current
$Commit = git rev-parse HEAD

git status > "$RawDir\git-status.txt" 2>&1

$FrontendRoot = ".\frontend"

$SourceFiles =
Get-ChildItem `
    $FrontendRoot `
    -Recurse `
    -File `
    -Include *.js,*.jsx,*.ts,*.tsx

$routePatterns = @(
    'createBrowserRouter',
    'createHashRouter',
    'useRoutes',
    '<Route',
    'path=',
    'navigate\(',
    'router\.'
)

$routeResults = foreach ($File in $SourceFiles)
{
    Select-String `
        -Path $File.FullName `
        -Pattern $routePatterns `
        -ErrorAction SilentlyContinue
}

$routeResults |
ForEach-Object {
    "{0}:{1}:{2}" -f $_.Path,$_.LineNumber,$_.Line.Trim()
} |
Out-File "$RawDir\route-candidates.txt"

$navPatterns = @(
    'NavLink',
    'Link',
    'sidebar',
    'navigation',
    'menu',
    'href',
    'to='
)

$navResults = foreach ($File in $SourceFiles)
{
    Select-String `
        -Path $File.FullName `
        -Pattern $navPatterns `
        -ErrorAction SilentlyContinue
}

$navResults |
ForEach-Object {
    "{0}:{1}:{2}" -f $_.Path,$_.LineNumber,$_.Line.Trim()
} |
Out-File "$RawDir\navigation-candidates.txt"

$authPatterns = @(
    'role',
    'roles',
    'permission',
    'permissions',
    'auth',
    'ProtectedRoute',
    'PrivateRoute'
)

$authResults = foreach ($File in $SourceFiles)
{
    Select-String `
        -Path $File.FullName `
        -Pattern $authPatterns `
        -ErrorAction SilentlyContinue
}

$authResults |
ForEach-Object {
    "{0}:{1}:{2}" -f $_.Path,$_.LineNumber,$_.Line.Trim()
} |
Out-File "$RawDir\permission-candidates.txt"

node --version > "$RawDir\node-version.txt"
npm --version > "$RawDir\npm-version.txt"

@"
PHASE 4 FRONTEND INVENTORY

Timestamp: $Timestamp
Branch: $Branch
Commit: $Commit

Route Matches: $($routeResults.Count)
Navigation Matches: $($navResults.Count)
Auth Matches: $($authResults.Count)

Status:
Inventory Captured
"@ | Out-File "$FullDir\frontend-route-audit.txt"

@"
PHASE 4 SENIOR REVIEW

Risks:
- Hidden routes
- Duplicate navigation
- Dead route references

Route Matches: $($routeResults.Count)
Navigation Matches: $($navResults.Count)
Authorization Matches: $($authResults.Count)
"@ | Out-File "$LeadDir\senior-review.txt"

Write-Host ""
Write-Host "Phase 4 inventory complete."
Write-Host "Route Matches: $($routeResults.Count)"
Write-Host "Navigation Matches: $($navResults.Count)"
Write-Host "Authorization Matches: $($authResults.Count)"
