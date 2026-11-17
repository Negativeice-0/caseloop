# CaseLoop documentation plan

## Purpose and audience

Create one coherent explanation of the problem, intended users, system behavior, safeguards, and delivery plan. Write for both the academic attachment assessor and operational/admin stakeholders. Use simple language, label assumptions, and distinguish implemented behavior from proposals.

## Document set

| Priority | Document | Main contents | Audience | Status / next action |
|---|---|---|---|---|
| 1 | Project brief | Problem, goals, scope, non-goals, users, expected outcomes | Both | Existing overview is the starting point; review with stakeholders |
| 2 | Requirements and acceptance criteria | User stories, role permissions, validation rules, measurable acceptance tests | Product/operations | Draft from the current workflow; validate names and policy |
| 3 | Workflow and system context | Intake-to-report flow, actors, external systems, trust boundaries | Both | Initial diagrams in this design pack |
| 4 | Architecture and deployment | React 18, Python 3.11, Docker Compose/PostgreSQL, target OCI VM, HTTPS, backup/restore | Technical/IT | Current baseline documented; OCI runbook still needs a step-by-step |
| 5 | Data dictionary and ERD | Response, assignment, team, intake, user, event, source IDs, branch fields and relationships | Developers/admin | Confirm exact schema and branch representation before WhatsApp work |
| 6 | Security and privacy notes | Roles, authentication, webhook validation, secrets, consent, retention, incident handling | Admin/IT | Required before real data or group intake |
| 7 | Test and demo plan | Synthetic scenarios, expected UI/API/database outcomes, failure cases | Both | Checklist in this pack; expand to signed-off UAT |
| 8 | User and administrator guide | Registration, sign-in, intake review, assignment, reports, account management | Coordinators/responders/admins | Write after workflow is approved |
| 9 | Student attachment report | Organization context, objectives, weekly summary, skills learned, diagrams, challenges, recommendations | Academic assessor | Maintain the institute's daily logbook separately and follow its handling instructions |
| 10 | Decision/change log | Date, decision, reason, alternatives, owner, effect on scope | Project team | Keep entries short and update when design choices change |

## Suggested creation order

1. Review the project brief and identify stakeholders.
2. Confirm role permissions, workflow, branch/location vocabulary, and what must remain human-approved.
3. Validate the workflow and architecture diagrams with both audiences.
4. Finish requirements, data dictionary/ERD, and privacy/security review before adding WhatsApp group support.
5. Write the OCI deployment runbook and acceptance tests; deploy synthetic data only.
6. Conduct a controlled WhatsApp test after hosting and HTTPS are verified.
7. Prepare the user guide and attachment report from verified behavior, not planned features.

## Diagram set

- **Workflow:** Who submits, reviews, publishes, assigns, audits, and reports.
- **System context/deployment:** Browser, frontend, API, PostgreSQL, Meta webhook, and OCI host; mark current versus planned components.
- **ERD:** Add after confirming the database schema and branch/location design.
- **Sequence diagram:** Add for one inbound message, including retry/deduplication and approval.
- **Swimlane:** Optional for responder, coordinator, administrator, and system responsibilities.
