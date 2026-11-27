# CASELOOP PHASE 8

Objective

README and Documentation Audit

=====================================================================
OUTPUT REQUIREMENTS
=====================================================================

Generate a PowerShell script:

scripts/audit/phases/phase8/doc-audit.ps1

The script must:

1. Generate rawshell evidence

2. Generate rawshell-manifest.json

3. Generate phase8.json

4. Update current-phase.json

5. Support SessionSummary automation

Do not generate summary.md.

Do not generate verification.md.

SessionSummary is responsible for those artifacts.

=====================================================================
RAWSHELL OUTPUTS
=====================================================================

Write:

docs/Auditing/data/rawshell/phase8/

documentation-inventory.txt

readme-inventory.txt

documentation-coverage.txt

rawshell-manifest.json

=====================================================================
CONTROL OUTPUTS
=====================================================================

Write:

docs/Auditing/control/phase8.json

docs/Auditing/control/current-phase.json

=====================================================================
DOCUMENTATION INVENTORY
=====================================================================

Discover:

README*

*.md

*.rst

*.txt

Exclude:

node_modules

.git

venv

.venv

__pycache__

dist

build

coverage

.pytest_cache

Sort results.

Write:

documentation-inventory.txt

=====================================================================
README INVENTORY
=====================================================================

Find:

README*

Write:

readme-inventory.txt

=====================================================================
DOCUMENTATION COVERAGE
=====================================================================

Verify presence of:

README.md

docker-compose.yml

Write:

documentation-coverage.txt

=====================================================================
RAWSHELL MANIFEST
=====================================================================

Generate:

rawshell-manifest.json

Schema:

{
  "phase": "phase8",
  "objective": "README and Documentation Audit",
  "generated": "<timestamp>",
  "evidenceFiles": [
    "documentation-inventory.txt",
    "readme-inventory.txt",
    "documentation-coverage.txt"
  ],
  "evidenceCount": 3,
  "primaryEvidence": [
    "documentation-inventory.txt",
    "documentation-coverage.txt"
  ],
  "notes": [
    "Documentation inventory collected",
    "README inventory collected",
    "Coverage checks completed"
  ]
}

=====================================================================
PHASE CONTROL FILE
=====================================================================

Generate:

phase8.json

Schema:

{
  "phase": "phase8",

  "phaseNumber": 8,

  "objective":
    "README and Documentation Audit",

  "status": "COMPLETE",

  "importantFiles": [

    "README.md",

    "docs/deployment",

    "docs/design"
  ],

  "expectedEvidence": [

    "documentation-inventory.txt",

    "readme-inventory.txt",

    "documentation-coverage.txt"
  ],

  "expectedArtifacts": [

    "normalized.json",

    "summary.md",

    "verification.md",

    "logbook.md"
  ],

  "validationCandidates": [

    "README accuracy",

    "Deployment documentation accuracy",

    "Architecture documentation accuracy",

    "API documentation accuracy"
  ],

  "verificationCommands": [

    "Get-ChildItem docs/Auditing/data/rawshell/phase8",

    "Get-Content docs/Auditing/data/rawshell/phase8/documentation-coverage.txt"
  ],

  "successCriteria": [

    "Documentation inventory exists",

    "README inventory exists",

    "Coverage report exists"
  ],

  "nextAction":
    "Compare documentation claims against implementation",

  "generatedBy":
    "CASELOOP"
}

=====================================================================
CURRENT PHASE
=====================================================================

Write:

current-phase.json

Contents:

Same as phase8.json

Purpose:

SessionSummary reads:

docs/Auditing/control/current-phase.json

without requiring:

- hardcoded phase logic
- uploaded evidence
- manual phase selection

=====================================================================
CONSOLE OUTPUT
=====================================================================

Output:

PASS Documentation Files: <count>

PASS Manifest Generated

PASS Control Files Generated

Provide:

Run Command

Verification Commands

Artifact Locations

Success Criteria