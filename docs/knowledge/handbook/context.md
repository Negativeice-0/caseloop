# =====================================================================
# CASELOOP WILDCARD KNOWLEDGE COMMENT BLOCK
# =====================================================================

PURPOSE

This prompt is part of the CaseLoop Engineering System.

Before generating output:

Identify:

1. Source Material
2. Target Outcome
3. Output Location
4. Artifact Type
5. Verification Method

Always classify generated content.

------------------------------------------------

POSSIBLE INPUT LOCATIONS

Repository

backend/**
frontend/**
README.md

Auditing

docs/auditing/data/**
docs/auditing/verification/**

Knowledge

docs/knowledge/**

Design

docs/design/**
docs/design/mockups/**
docs/design/*.mmd

Deployment

docs/deployment/**

Training

docs/training/**

Projects

docs/projects/**
docs/projects/progress/**

Troubleshooting

docs/trouble/**

Tips

docs/tips/**

Scripts

scripts/**
scripts/auditing/**
scripts/audit/**

------------------------------------------------

CLASSIFICATION RULES

Architecture

Authorization
Authentication
Routing
Dependency Graph
System Design

Store:

docs/knowledge/master/architecture/

------------------------------------------------

Backend

API
Services
Models
Database
Migrations

Store:

docs/knowledge/master/backend/

------------------------------------------------

Frontend

Pages
Routes
Layouts
Navigation
Components

Store:

docs/knowledge/master/frontend/

------------------------------------------------

Database

Entities
Schemas
Relationships
Migrations

Store:

docs/knowledge/master/database/

------------------------------------------------

Operations

Docker
Deployment
Infrastructure

Store:

docs/knowledge/master/operations/

------------------------------------------------

Learning

Tutorials
Exercises
Roadmaps

Store:

docs/knowledge/master/learning/

------------------------------------------------

History

Checkpoints
Sessions
Lessons
Milestones

Store:

docs/knowledge/master/history/

------------------------------------------------

Portfolio

Brag Sheets
Presentations
Interview Prep

Store:

docs/knowledge/master/portfolio/

------------------------------------------------

Possible Maps

backend-route-map.md
frontend-route-map.md
permission-map.md
service-map.md
database-map.md
dependency-map.md
deployment-map.md

Store:

docs/knowledge/master/maps/

------------------------------------------------

Possible Reports

architecture-report.md
technical-debt-report.md
checkpoint-history.md
audit-findings.md
maintenance-report.md

Store:

docs/knowledge/master/reports/

------------------------------------------------

Possible Learning Artifacts

learning-guide.md
confidence-checklist.md
leetcode-exercises.md
interview-prep.md

Store:

docs/knowledge/master/learning/

------------------------------------------------

Possible Portfolio Artifacts

brag-sheet.md
project-story.md
engineering-growth.md

Store:

docs/knowledge/master/portfolio/

------------------------------------------------

Verification

Every generated artifact must include:

Purpose
Source Material
Generated Date
Verification Status

Never generate files without traceability.

# =====================================================================