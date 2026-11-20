# Purpose
Checkpoint 14 organized the audit workflow, documented Phase 1 findings, preserved raw PowerShell output, and created scripts for running and extracting audit results.

The final arrangement uses scripts\run_audit.ps1 as the main audit entry point. It prints audit commands and results, records the complete PowerShell session, checks the project structure, reports required files, records limitations, and saves the raw transcript.

## Directory structure
The audit workflow uses these directories:

Text

Copy
scripts\
docs\
├── auditing\
│   └── data\
│       ├── fullstack\
│       │   └── phase1\
│       └── rawshell\
└── projects\
    └── progress\
The raw PowerShell transcript is stored at:

Text

## Copy
docs\auditing\data\rawshell\phasendata.txt
The filename phasendata.txt is used by the audit workflow and should remain consistent unless the input path is intentionally changed.

Files and responsibilities
scripts\audit_tree.ps1 — Lists project files while excluding dependency, generated, cache, build, and version-control directories.

scripts\extract_audit.ps1 — Reads the completed PowerShell transcript and extracts useful audit information.

scripts\run_audit.ps1 — Main audit wrapper that contains the audit commands, prints commands and results, starts the transcript, checks files, reports limitations, and stops the transcript.

docs\auditing\data\fullstack\phase1\README.md — Phase 1 audit documentation and findings.

docs\auditing\data\rawshell\phasendata.txt — Raw PowerShell transcript produced by the audit session.

docs\projects\progress\chpnt14.md — Checkpoint 14 progress notes, verified findings, and recommendations.

docs\projects\progress\chpnt14-session-summary.md — This complete session summary.

PowerShell commands
Create the required directories
Powershell

## Copy
New-Item -ItemType Directory -Force `
  -Path "scripts",
        "docs\auditing\data\fullstack\phase1",
        "docs\auditing\data\rawshell",
        "docs\projects\progress"
This creates the script directory, Phase 1 documentation directory, raw transcript directory, and progress documentation directory if they do not already exist.

Confirm the current project location
Powershell

Copy
Get-Location
Run the audit from the project root so that relative paths such as .\scripts and .\docs resolve correctly.

Display the PowerShell environment
Powershell

Copy
$PSVersionTable
This records the PowerShell version and environment information used during the audit.

Display the project root contents
Powershell

Copy
Get-ChildItem -Force
This displays visible and hidden files and directories at the project root.

Run the directory audit script
Powershell

Copy
powershell -ExecutionPolicy Bypass `
  -File ".\scripts\audit_tree.ps1"
The directory audit should list relevant project files while excluding:

node_modules

venv

.git

__pycache__

dist

build

.pytest_cache

Start a manual transcript
Powershell

Copy
Start-Transcript `
  -Path ".\docs\auditing\data\rawshell\phasendata.txt"
After starting the transcript, run the approved audit and verification commands.

Stop a manual transcript
Powershell

Copy
Stop-Transcript
The transcript must be stopped after the commands finish so that the raw file is finalized and can be analyzed.

Run the complete audit wrapper
Powershell

Copy
powershell -ExecutionPolicy Bypass `
  -File ".\scripts\run_audit.ps1"
This is the recommended main command. It runs the audit workflow, prints commands and results, checks project files, records limitations and recommendations, and creates or overwrites:

Text

Copy
docs\auditing\data\rawshell\phasendata.txt
The raw transcript may be overwritten on each run because the audit uses the -Force option.

Confirm that the raw transcript exists
Powershell

Copy
Test-Path ".\docs\auditing\data\rawshell\phasendata.txt"
A result of True means the raw transcript exists at the expected path. A result of False means it has not yet been created at that location.

Inspect the raw transcript
Powershell

Copy
Get-Content `
  ".\docs\auditing\data\rawshell\phasendata.txt"
This displays the recorded PowerShell session.

Extract useful information from the completed transcript
Powershell

Copy
powershell -ExecutionPolicy Bypass `
  -File ".\scripts\extract_audit.ps1" `
  -InputFile ".\docs\auditing\data\rawshell\phasendata.txt"
Run this after run_audit.ps1 has finished and the transcript is no longer open.

Check the required files
Powershell

Copy
$requiredFiles = @(
    "scripts\audit_tree.ps1",
    "scripts\extract_audit.ps1",
    "scripts\run_audit.ps1",
    "docs\auditing\data\fullstack\phase1\README.md",
    "docs\projects\progress\chpnt14.md",
    "docs\projects\progress\chpnt14-session-summary.md"
)

foreach ($file in $requiredFiles) {
    if (Test-Path ".\$file") {
        Write-Output "PRESENT: $file"
    }
    else {
        Write-Output "MISSING: $file"
    }
}
This confirms whether the expected scripts and documentation files are present.

Review the project file list
Powershell

Copy
Get-ChildItem `
  -Path "." `
  -Recurse `
  -File `
  -Force
For a cleaner audit, generated and dependency directories should be excluded as configured by audit_tree.ps1 and run_audit.ps1.

## Recommended workflow
Open PowerShell at the project root.

Confirm the project location with Get-Location.

Confirm that the required directories exist.

Run scripts\run_audit.ps1.

Confirm that docs\auditing\data\rawshell\phasendata.txt exists.

Review the raw transcript.

Run scripts\extract_audit.ps1 against the completed transcript.

Review the extracted findings.

Update docs\projects\progress\chpnt14.md only with verified results.

Keep the raw transcript as evidence until the audit is complete.

Responsibilities of each script
audit_tree.ps1
This script inspects the project directory and lists relevant files. It should avoid reporting large dependency, cache, build, generated, and version-control directories.

run_audit.ps1
## This script is responsible for running the audit session. It should:

Resolve the project root.

Create the raw transcript directory.

Define the raw transcript path.

Start the PowerShell transcript.

Print the project location.

Print PowerShell environment information.

Print the project root contents.

List project files.

Check required audit files.

Report whether the raw transcript exists.

Print audit limitations.

Print recommended next commands.

Record start and finish times.

Stop the transcript.

run_audit.ps1 is the main execution script and should not be changed merely to update this summary.

extract_audit.ps1
This script analyzes the completed transcript. It should be run after the transcript has been closed with Stop-Transcript.

## Audit evidence
The raw evidence is stored at:

docs\auditing\data\rawshell\phasendata.txt
The raw file records what PowerShell printed during the audit. The progress files should contain conclusions only after the corresponding evidence has been reviewed.

Audit limitations
The audit workflow records and organizes evidence, but it does not automatically prove that the application is fully functional.

## It does not by itself prove that:

- Authentication works.

- Authorization works.

- Protected API requests work.

- Database workflows work.

- Every frontend route works.

- Every backend route works.

- External services are configured correctly.

- Production deployment matches the local project.

- Security controls are complete.

All Phase 1 findings have been resolved.

A file being present does not prove that the file is correct, complete, executed, or connected to the rest of the application.

## Important transcript considerations
- Run the commands from the project root.

- Use the exact raw transcript path consistently.

- Do not run extract_audit.ps1 until the transcript has been stopped.

- The raw transcript can be overwritten by a later audit run.

Preserve a copy of important evidence before starting a new run if historical comparison is needed.

Record only verified findings in chpnt14.md.

Treat printed commands and file listings as evidence of inspection, not proof of application behavior.

Final recommendations
Use scripts\run_audit.ps1 as the single main entry point for the audit session.

## Keep raw output in:

docs\auditing\data\rawshell\phasendata.txt
Use scripts\extract_audit.ps1 only after the session has finished and the transcript has been closed.

## Keep conclusions and verified findings in:

docs\auditing\data\fullstack\phase1\README.md
docs\projects\progress\chpnt14.md
Use this session summary as the complete record of the directories, files, commands, workflow, evidence location, responsibilities, limitations, and recommendations associated with Checkpoint 14.

## Final status
The documentation and audit workflow are organized. The audit is considered evidence-producing only after run_audit.ps1 has been executed, phasendata.txt has been created, the transcript has been reviewed, and the extracted findings have been checked against the actual project contents.