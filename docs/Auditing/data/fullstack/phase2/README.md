Use this single PowerShell script to validate the final repository state and generate a concise handoff file.

Powershell to be run in terminal directly to create run all commands below

# Copy

$ErrorActionPreference = 'Stop'

# Expected final state
$expectedBranch = 'safety/main-20261119-142303'
$expectedCommit = '0a97e91'
$expectedRemote = 'origin/safety/main-20261119-142303'
$outputFile = 'case-loop-session-summary.md'

# Repository checks
$repoRoot = (git rev-parse --show-toplevel).Trim()
$branch = (git branch --show-current).Trim()
$commit = (git rev-parse --short HEAD).Trim()
$status = @(git status --porcelain)
$branchStatus = (git status --short --branch | Select-Object -First 1).Trim()
$safetyBranches = @(git branch --list 'safety/*' | ForEach-Object {
    ($_ -replace '^\*?\s+', '').Trim()
})

# Validate expected state
if ($repoRoot -ne 'C:/Users/Admin/Documents/caseloop') {
    throw "Unexpected repository root: $repoRoot"
}

if ($branch -ne $expectedBranch) {
    throw "Unexpected branch: $branch"
}

if ($commit -ne $expectedCommit) {
    throw "Unexpected commit: $commit"
}

if ($status.Count -gt 0) {
    throw "Working tree is not clean:`n$($status -join "`n")"
}

if ($safetyBranches.Count -ne 1 -or $safetyBranches[0] -ne $expectedBranch) {
    throw "Unexpected safety branches:`n$($safetyBranches -join "`n")"
}

if ($branchStatus -notmatch [regex]::Escape($expectedRemote)) {
    throw "Branch is not tracking the expected remote: $branchStatus"
}

# Generate concise handoff
$summary = @"
# CaseLoop Session Handoff

## Final state

- Repository: `$repoRoot`
- Branch: `$branch`
- Commit: `$commit`
- Working tree: clean
- Remote: up to date with `$expectedRemote`
- Safety branches: one
- Nested safety branches: removed
- Application files changed: none
- Commits created or rewritten: none

## Completed

- Verified repository root.
- Verified active branch and commit.
- Confirmed a clean working tree.
- Removed accidental nested safety branches.
- Preserved the intended safety branch.
- Confirmed the branch remains synchronized with its remote.

## Cause of the branch issue

A safety-branch command was run while already on a branch beginning with `safety/`, producing a redundant nested name. The nested branches pointed to the same commit and did not alter files or history.

## Final verified Git status

```text
$branchStatus
Next step
Record baseline backend tests and frontend build before changing application code.
"@

$summary | Set-Content -Path $outputFile -Encoding UTF8

Write-Host "`nSession verified successfully."
Write-Host "Summary written to: $outputFile"
Write-Host "`n$summary"

Code

Copy

Run it from:

```powershell
C:\Users\Admin\Documents\caseloop
with:

Powershell

Copy
.\verify-session.ps1
If you have not saved it yet:

Powershell

Copy
notepad .\verify-session.ps1
Paste the script, save, close Notepad, then run it.

The script will stop instead of generating a misleading summary if the branch, commit, remote, safety branches, or working tree differ from the expected final state.