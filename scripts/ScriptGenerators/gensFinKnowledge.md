# =====================================================================
# Create Knowledge Generator Script
# =====================================================================

$TargetDir = ".\scripts\audit\knowledge"

if (!(Test-Path $TargetDir)) {
    New-Item -ItemType Directory -Force -Path $TargetDir | Out-Null
}

$ScriptContent = @'
[CmdletBinding()]
param()

$ErrorActionPreference = "Continue"

Write-Host ""
Write-Host "===============================" -ForegroundColor Cyan
Write-Host " CaseLoop Knowledge Builder"
Write-Host "===============================" -ForegroundColor Cyan
Write-Host ""

# ---------------------------------------------------------
# Create Folder Structure
# ---------------------------------------------------------

$MasterRoot = "docs\knowledge\master"

$Folders = @(
    $MasterRoot,
    "$MasterRoot\reports",
    "$MasterRoot\maps",
    "$MasterRoot\learning",
    "$MasterRoot\history",
    "$MasterRoot\portfolio"
)

foreach ($Folder in $Folders) {

    if (!(Test-Path $Folder)) {
        New-Item -ItemType Directory -Force -Path $Folder | Out-Null
    }
}

# ---------------------------------------------------------
# Gather Sources
# ---------------------------------------------------------

$SourceDirs = @(
    "README.md",
    "backend",
    "frontend",
    "docs"
)

$AllFiles = @()

foreach ($Source in $SourceDirs) {

    if (Test-Path $Source) {

        if ((Get-Item $Source).PSIsContainer) {

            $AllFiles += Get-ChildItem `
                -Path $Source `
                -Recurse `
                -File `
                -ErrorAction SilentlyContinue

        }
        else {

            $AllFiles += Get-Item $Source
        }
    }
}

# ---------------------------------------------------------
# Build File Inventory
# ---------------------------------------------------------

$InventoryFile = "$MasterRoot\system-map.md"

"# CaseLoop System Map" | Set-Content $InventoryFile
"" | Add-Content $InventoryFile

foreach ($File in $AllFiles) {

    $Relative =
        $File.FullName.Replace(
            (Get-Location).Path + "\",
            ""
        )

    "- $Relative" | Add-Content $InventoryFile
}

# ---------------------------------------------------------
# Build Concept Extraction
# ---------------------------------------------------------

$Concepts = @{}

foreach ($File in $AllFiles) {

    $Name =
        [System.IO.Path]::GetFileNameWithoutExtension(
            $File.Name
        )

    if ($Name.Length -gt 3) {

        if (!$Concepts.ContainsKey($Name)) {

            $Concepts[$Name] = 1
        }
        else {

            $Concepts[$Name]++
        }
    }
}

$ConceptFile = "$MasterRoot\glossary.md"

"# CaseLoop Glossary" | Set-Content $ConceptFile
"" | Add-Content $ConceptFile

$Concepts.Keys |
Sort-Object |
ForEach-Object {

    "- CaseLoop/$($_)" |
        Add-Content $ConceptFile
}

# ---------------------------------------------------------
# Executive Summary
# ---------------------------------------------------------

$Summary = "$MasterRoot\executive-summary.md"

@"
# CaseLoop Executive Summary

Generated: $(Get-Date)

## Overview

CaseLoop is a full-stack application containing:

- Frontend
- Backend
- Deployment
- Design
- Training
- Troubleshooting
- Audit Data
- Knowledge Assets

## Statistics

Files Discovered: $($AllFiles.Count)

## Major Areas

- Authentication
- Authorization
- Assignments
- Responses
- Teams
- Reporting
- Workflow
- Administration

## Purpose

Provide a searchable knowledge base
for future maintenance and onboarding.
"@ | Set-Content $Summary

# ---------------------------------------------------------
# Maintenance Guide
# ---------------------------------------------------------

@"
# Maintenance Guide

## Backend

backend/app

## Frontend

frontend/src

## Important Documents

docs/deployment
docs/design
docs/training

## Audit Data

docs/auditing

## Knowledge Base

docs/knowledge
"@ | Set-Content "$MasterRoot\maintenance-guide.md"

# ---------------------------------------------------------
# Brag Sheet
# ---------------------------------------------------------

@"
# CaseLoop Brag Sheet

## Stack

Frontend:
React
TypeScript

Backend:
Python

Database:
SQLite

Documentation:
Design
Training
Deployment
Troubleshooting
Auditing

## Features

Authentication
Authorization
Assignments
Responses
Reports
Administration
Teams

## Engineering Effort

Knowledge System
Audit System
Training Material
Deployment Documentation

## Portfolio Statement

CaseLoop demonstrates full-stack engineering,
documentation discipline,
audit automation,
knowledge management,
and long-term maintainability practices.
"@ | Set-Content "$MasterRoot\portfolio\brag-sheet.md"

# ---------------------------------------------------------
# Engineering Journal
# ---------------------------------------------------------

@"
# Engineering Journal

Generated: $(Get-Date)

## Findings

Review generated reports.

## Next Steps

Continue audit phases.

## Questions

Record discoveries here.

## Refactor Ideas

Record opportunities here.
"@ | Set-Content "$MasterRoot\history\engineering-journal.md"

# ---------------------------------------------------------
# Concise Log
# ---------------------------------------------------------

$LogFile = "$MasterRoot\extract-concise-log.txt"

"CASELOOP KNOWLEDGE INDEX" |
    Set-Content $LogFile

"" | Add-Content $LogFile

$AllFiles |
Sort-Object FullName |
ForEach-Object {

    $Relative =
        $_.FullName.Replace(
            (Get-Location).Path + "\",
            ""
        )

    Add-Content $LogFile $Relative
}

# ---------------------------------------------------------
# Knowledgebook
# ---------------------------------------------------------

@"
# CaseLoop Knowledgebook

This document serves as the central
encyclopedia for the repository.

See:

- executive-summary.md
- maintenance-guide.md
- system-map.md
- glossary.md
- brag-sheet.md
- engineering-journal.md

The goal is codebase mastery,
not merely evidence collection.
"@ | Set-Content "$MasterRoot\knowledgebook.md"

Write-Host ""
Write-Host "SUCCESS" -ForegroundColor Green
Write-Host ""
Write-Host "Output:"
Write-Host "docs\knowledge\master"
Write-Host ""
'@

$ScriptPath = ".\scripts\audit\knowledge\finalize-knowledge.ps1"

Set-Content `
    -Path $ScriptPath `
    -Value $ScriptContent `
    -Encoding UTF8

Write-Host ""
Write-Host "Created:" -ForegroundColor Green
Write-Host $ScriptPath
Write-Host ""

Write-Host "Run using:"
Write-Host ""
Write-Host ".\scripts\audit\knowledge\finalize-knowledge.ps1"
Write-Host ""