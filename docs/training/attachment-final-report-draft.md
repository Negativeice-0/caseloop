# Industrial Attachment Report — Dedicated Draft

**Status:** Editable draft based on the “Written Report Format” on the final page of the Africa International University School of Business and Economics Student Attachment Guide. Replace every bracketed instruction, verify every first-person statement, and obtain supervisor/university approval before submission. This is not a final assessed report.

## How to use this draft

- The guide's final page specifies preliminary pages, three chapters, and appendices. The headings below follow that structure.
- You identified **60 pages as a personal target**, not as a confirmed university minimum. The guide's final page does not state a page count. Confirm the required length, formatting, and whether the daily logbook is separate with your university coordinator.
- Checkpoint documents are **project context only**, not evidence that you personally completed work. This draft uses the current repository documentation for the application's technical description and leaves personal activities/evidence for you to verify.
- Do not claim CaseLoop was deployed or adopted by Red Cross, the university, or a branch. No such approval or live operation is documented here.
- Use only approved organization details. Do not include beneficiary/personnel information, operational data, credentials, or private supervisor contact details.

## Preliminary Pages

Arrange these pages according to the university's latest instructions. Use Word heading styles and automatic tables of contents/lists after final pagination; do not type page numbers manually.

### Cover page

**AFRICA INTERNATIONAL UNIVERSITY**  
**[SCHOOL / DEPARTMENT — confirm the current official name]**

**INDUSTRIAL ATTACHMENT REPORT**

**HOST ORGANIZATION:** `[Official organization name, approved for this report]`  
**DEPARTMENT / UNIT:** `[Official department or unit]`

**STUDENT:** `[Full name]`  
**REGISTRATION NUMBER:** `[Registration number]`  
**COURSE / PROGRAMME:** `[Official course/programme]`

**ATTACHMENT PERIOD:** `[Confirmed start date]` to `[Confirmed end date]`

**WORKPLACE SUPERVISOR:** `[Name and title, with permission]`  
**UNIVERSITY SUPERVISOR:** `[Name and title]`

**SUBMISSION DATE:** `[Date]`

### Declaration

Use the declaration wording supplied by the university. Do not sign a statement until it is accurate. If the institution requires an originality statement, complete it yourself and follow its policy on AI assistance and other contributions.

`[Insert the university's approved declaration and signature/date fields.]`

### Dedication

`[Optional. Add a brief personal dedication only if required or desired.]`

### Acknowledgement

`[Thank only people and organizations who may be acknowledged. Obtain permission before naming a workplace supervisor or disclosing internal support.]`

### Table of Contents

`[Generate automatically from heading styles after the report is formatted.]`

### List of Tables

`[Generate automatically if the final report contains tables.]`

### List of Figures

`[Generate automatically if the final report contains figures or diagrams.]`

### Abbreviations and Acronyms

Include only terms used in the final report. Draft list:

| Term | Meaning |
|---|---|
| API | Application Programming Interface |
| CORS | Cross-Origin Resource Sharing |
| CRUD | Create, Read, Update, Delete |
| CSRF | Cross-Site Request Forgery |
| DB | Database |
| HTTP / HTTPS | Hypertext Transfer Protocol / its encrypted form |
| ORM | Object-Relational Mapper |
| UI | User Interface |
| VMS | Volunteer Management System |
| WSGI / ASGI | Web Server Gateway Interface / Asynchronous Server Gateway Interface |

### Abstract

This report describes an industrial attachment with the Kenya Red Cross Society (KRCS), at `[official branch/unit name as shown on placement documents]`, from `[verified start date]` to `[verified end date]`. It presents the organization's background and structure, the purpose and objectives of the attachment, the work actually undertaken, learning opportunities, challenges, and recommendations. CaseLoop, a software project documented during the period, is described as a local coordination-workflow prototype using a React/TypeScript frontend and a Python/FastAPI backend. Its documented workflow keeps supported incoming text as a pending intake for human review before publication. The report distinguishes repository capabilities from the student's verified activities and from production deployment or organizational adoption. `[Add two or three sentences summarizing actual placement outcomes after the logbook and supervisor review are complete.]`

**Keywords:** industrial attachment, software engineering, FastAPI, React, database, testing, `[add only relevant terms]`

## Chapter One: Introduction

### 1.1 Background of the Organization

The host organization is the **Kenya Red Cross Society (KRCS)**. The Society's official website describes it as Kenya's National Red Cross Society and states that it was founded in 1965 under the Kenya Red Cross Society Act (Chapter 256). KRCS works in the humanitarian sector. Its published programme areas include disaster management, health, youth development, national society development, and special programmes. These are national-level facts; confirm the local unit's official name, remit, and any branch-specific details with the placement letter or supervisor. ([KRCS About Us](https://redcross.or.ke/about-us/); [KRCS programmes](https://redcross.or.ke/programmes/))

#### Description of the organization

The Kenya Red Cross Society is the national Red Cross Society in Kenya. Its published mission is: “We facilitate communities to respond to humanitarian emergencies to alleviate human suffering and work with partners to implement innovative community driven programmes that transform lives and enhance community resilience.” Its official website lists work in disaster management, health, youth development, national society development, and special programmes. The attachment was associated with `[official branch/unit name and approved location]`; verify this designation and describe the actual unit's work using placement records or information approved by the supervisor. ([KRCS About Us](https://redcross.or.ke/about-us/); [KRCS programmes](https://redcross.or.ke/programmes/))

#### Vision, mission, and values

The Society's published vision is “To be a leading humanitarian organization sustainably promoting the well-being, health and resilience of communities.” Its published core values are **Service to Humanity, Accountability, Community Centered, Inclusivity, and Innovation**. Confirm these against the official website at submission time in case the wording changes. ([KRCS About Us](https://redcross.or.ke/about-us/))

#### Industry

KRCS operates in the humanitarian sector. Its published national programme areas include disaster management, health, youth development, national society development, and special programmes. Describe only the services relevant to the actual placement unit, and verify those details with an approved source. ([KRCS programmes](https://redcross.or.ke/programmes/))

#### Reasons for choosing the organization

**Draft for personal review:**  
I chose `[organization]` because `[state your genuine reason]`. I expected the placement to expose me to `[specific work area]` and help me connect my studies in `[course/programme]` with practical responsibilities. `[Verify this against your placement application and actual experience.]`

#### Other relevant information

The Society's public website reports **47 county branches** and **8+ regional offices**. This national-level information does not verify whether “Karen Langata branch” is the formal name of the placement unit or establish its local reporting structure. Use the exact name on the placement letter or confirm it with the university/host supervisor; do not infer a local chart from the national structure. ([KRCS About Us](https://redcross.or.ke/about-us/); [KRCS contact page](https://redcross.or.ke/contact-us/))

### 1.2 Organization Structure

#### Departments and their roles

KRCS publicly describes national programme areas including disaster management, health, youth development, national society development, and special programmes. These are programme areas, not necessarily the departments or reporting lines of the student's local placement. `[Add the actual local unit/team and its roles from approved placement information.]` ([KRCS programmes](https://redcross.or.ke/programmes/))

#### Roles of personnel

`[Describe roles rather than naming staff unless naming is approved. Explain the position you reported to and the scope of your assigned work.]`

#### Organization chart

The official website reports a nationwide network of 47 county branches and 8+ regional offices, but this draft does not have a verified organization chart for the local unit. `[Insert a chart only if the host organization provides or approves one. Use role titles where possible; omit private contact details.]`

#### Other relevant information

`[Explain how work is assigned, reviewed, and escalated if this is relevant and approved.]`

### 1.3 Objectives of the Attachment

The guide asks what the student hoped to achieve and how. Replace or reconcile the draft objectives below with the **official objectives from your placement letter or university form**. Do not claim an objective was achieved until you attach evidence and assess it.

| Draft objective for confirmation | How it could be achieved | Evidence to add |
|---|---|---|
| Apply concepts from `[course/programme]` to supervised technical work. | Complete assigned tasks, discuss design choices with a supervisor, and record lessons. | Dated logbook, reviewed work, supervisor feedback. |
| Understand how a web application connects its user interface, API, and database. | Trace one CaseLoop workflow from browser request to persisted record and back. | Diagram, test or browser evidence, personal explanation. |
| Practise software quality and maintenance. | Read existing tests, make a small approved change, run the relevant checks, and review the result. | Test output, reviewed change, explanation. |
| Improve professional communication and documentation. | Record daily work, summarize weekly learning, and present limitations accurately. | Logbook, weekly self-analysis, supervisor review. |
| `[Insert an objective from the official attachment plan.]` | `[State the actual method.]` | `[Attach evidence.]` |

## Chapter Two: Observations and Accomplishments

### 2.1 In-depth discussion of activities/work done during the entire period

Write this section from the completed daily logbook and weekly self-analysis reports. The material below is a project description and a set of prompts; it is **not a claim that you personally performed every task**.

#### Placement and onboarding

`[Describe the actual induction, workplace rules, assigned duties, tools, team interactions, and expectations. State dates only where supported by your logbook or supervisor records.]`

#### CaseLoop project context

CaseLoop is documented as an offline-first coordination-notebook concept. Its intended workflow is:

1. Capture a report from a supported input channel.
2. Keep the original text as a pending intake draft.
3. Have an authorized coordinator review and correct the draft.
4. Publish an approved response record and optionally create an assignment.
5. Record attributed timeline events and generate structured report previews/Word exports.

The repository describes a React 18/TypeScript browser interface, a Python 3.11/FastAPI API, SQLAlchemy data access, Alembic migration support, SQLite local mode, and a Docker Compose PostgreSQL/API setup. A documented Meta webhook validates provider requests and stores supported text as pending intake. The current record does not show a public HTTPS deployment or live Meta message test. Confirm the current code and product documentation before describing these capabilities in the final version.

#### Work package A — application and data-flow learning

`[Describe what you personally read, tested, changed, or explained about the frontend → API → database flow. Identify the exact files and dates from your records.]`

Technical context to explain if it matches your actual learning:

```text
Browser React UI
  -> HTTP request through the frontend API client
  -> FastAPI route and authorization
  -> SQLAlchemy session and model
  -> SQLite locally or PostgreSQL in the Compose setup
  -> JSON response back to the browser
```

The browser does not connect directly to PostgreSQL. The backend's `DATABASE_URL` selects its database; the frontend API URL selects which HTTP API it calls. These settings solve different problems.

#### Work package B — database, migrations, and testing

`[Describe the database-related activity you personally undertook, what environment it used, the error or question, your investigation, and the verified result. Do not say a schema mismatch was fixed unless the intended database and migration state were checked.]`

Learning points that may be included after personal verification:

- SQLAlchemy models, Pydantic API schemas, frontend TypeScript types, and actual database tables are separate representations that must agree.
- Alembic revisions describe schema changes; `alembic current`, `alembic heads`, and `alembic history` help inspect migration state.
- A seed script is not a migration. `create_all()` does not safely upgrade every existing table.
- Tests may use in-memory SQLite or dependency overrides and therefore may not test the running Docker PostgreSQL service.
- A passing unit or integration test does not prove a public deployment, TLS configuration, or provider integration.

Attach only test output you personally retained or can reproduce. The historical checkpoint counts are deliberately not used here as evidence.

#### Work package C — authentication, roles, and administrative workflow

`[Describe the access-control work you personally observed or performed, including the user role, allowed action, server-side check, and how the behavior was tested.]`

The current project documentation describes named email/password accounts, server-side roles, revocable sessions, CSRF protections, and role-limited administrative operations. Older project notes refer to prototype access methods that are no longer the current design. Do not present an early hidden-click or keyword experiment as the final security model.

#### Work package D — intake review, assignments, timeline, and reports

`[For each feature you personally handled, write the requirement, your role, steps, result, and evidence. Identify unimplemented or untested work as future work.]`

The current documented workflow keeps inbound text pending until a coordinator approves it. Approval may create a response and a linked assignment; timeline events preserve attribution. Report summaries are deterministic and based on structured records. These capabilities are project context, not evidence of your individual contribution or of organizational use.

#### Work package E — Docker, hosting, and WhatsApp learning

`[Record only what you actually ran or observed. Separate a Docker version check, local Compose run, Oracle deployment, and official Meta test as different milestones.]`

The local Compose configuration is a development setup, not a cloud deployment. The documented production path still requires a production frontend/static-server image, HTTPS reverse proxy, domain/DNS, secure secrets, private database networking, backup/restore, and cost review. Oracle does not require Docker; containers are a packaging choice. No live WhatsApp test should be claimed without provider-side evidence.

### 2.2 Objectives achieved

After confirming the official objectives in Chapter One, complete the table from your actual records.

| Objective | Status | Example from the attachment | Evidence | Supervisor comment |
|---|---|---|---|---|
| Apply course concepts to supervised work | `[Achieved / partly / not achieved]` | `[Actual task and your role]` | `[Logbook, reviewed output]` | `[Leave for supervisor]` |
| Explain frontend/API/database flow | `[Status]` | `[What you can now explain or demonstrate]` | `[Diagram/test/demo]` | `[Leave for supervisor]` |
| Practise testing and maintenance | `[Status]` | `[Test or change you personally performed]` | `[Command/result/diff]` | `[Leave for supervisor]` |
| Improve communication/documentation | `[Status]` | `[Actual logbook, handover, or presentation]` | `[Approved artifact]` | `[Leave for supervisor]` |

### 2.3 Value of the attachment to your course

**Draft for review:**  
The attachment can connect academic concepts to a working software repository. CaseLoop provides a context for discussing HTTP requests, component-based interfaces, data validation, relational storage, migrations, role-based access, automated tests, and deployment boundaries. The value to `[course/programme]` should be described using the topics actually taught and the work personally completed. `[Insert specific course modules and examples; do not assume these align without checking your syllabus.]`

### 2.4 Learning opportunities, experience gained, and skills acquired

For each skill, describe the starting point, the learning activity, what you can now do, and the evidence. Use accurate levels: “observed,” “can explain with notes,” “performed with guidance,” or “performed independently.”

| Skill area | Starting point | Learning activity | Current demonstrated level | Evidence |
|---|---|---|---|---|
| Git and version control | `[Describe honestly]` | `[Commands or review performed]` | `[Level]` | `[Reviewed diff/log]` |
| Python/FastAPI | `[Describe honestly]` | `[Route, schema, or test work]` | `[Level]` | `[Test or explanation]` |
| React/TypeScript | `[Describe honestly]` | `[Component/API work]` | `[Level]` | `[Build or UI evidence]` |
| Databases/Alembic | `[Describe honestly]` | `[Configuration/migration exercise]` | `[Level]` | `[Safe DB/test output]` |
| Docker/operations | `[Describe honestly]` | `[Compose/services/network exercise]` | `[Level]` | `[Commands and observations]` |
| Professional practice | `[Describe honestly]` | `[Communication, planning, review]` | `[Level]` | `[Supervisor feedback]` |

### 2.5 Main challenges/difficulties faced and how they were overcome

The following are candidate challenges from your own earlier descriptions. Keep only those that accurately reflect your experience; describe the steps you personally took and whether the issue is resolved.

| Challenge to verify | Investigation or response to describe | Evidence/status |
|---|---|---|
| Confusion about which database a process used (SQLite vs. PostgreSQL). | Trace `DATABASE_URL` into the backend engine; identify which API process answers; check the health endpoint. | `[Add your actual command/result; do not claim you performed it unless you did.]` |
| Uncertainty about which database the tests use. | Read `conftest.py` and test overrides; run tests with a safe SQLite URL. | `[Add actual test output and explanation.]` |
| Alembic/model/database schema disagreement. | Compare models, migration heads/current revision, actual selected database, and seed expectations before changing schema. | `[Add the actual error, root cause, and verified fix—or say unresolved.]` |
| Installing/using Git on Windows and understanding Docker Desktop/WSL differences. | Choose one shell, verify the executable/engine, and record each tool's role. | `[Add what you personally tried and learned.]` |
| Uncertainty about the future of AI-assisted coding and independent skill. | Use a hint-first practice loop, attempt a test/change first, then verify any assistance. | `[Describe one real exercise and what you can now explain.]` |
| `[Another actual challenge]` | `[Steps taken]` | `[Evidence/result]` |

Do not state “overcame” unless the issue is genuinely resolved. A remaining uncertainty can be a valid lesson and recommendation.

### 2.6 Contributions the attachment made to the department/organization

**Careful draft:**  
CaseLoop is documented as a student project intended to explore a reviewed intake-to-response workflow. No organizational adoption, operational use, formal endorsement, or measurable time savings are established in the material available for this draft. Any contribution should therefore be stated as a prototype or learning outcome unless a supervisor confirms a specific benefit. `[Ask the workplace supervisor what contribution, if any, may be reported and what evidence supports it.]`

Potential contributions to discuss only if confirmed:

- a synthetic demonstration that helped stakeholders review the proposed workflow;
- a documented requirements question or design recommendation accepted by the department;
- a tested local prototype shown to an authorized reviewer;
- a report or handover that the department requested and accepted.

Do not use the Red Cross emblem or imply official endorsement without authorization. Do not put real operational or beneficiary data in a learning demo.

### 2.7 Influence of the attachment on future career choices and expectations

**Draft for review:**  
The attachment experience has strengthened my interest in becoming a capable software engineer who can understand and maintain a complete application, not only produce code. It has shown me that software work includes requirement clarification, data integrity, testing, deployment, documentation, and communication. I intend to continue practising independently and use AI as an optional aid whose suggestions I verify. `[Adjust this reflection so it describes your actual view and what changed during the attachment.]`

You may mention broader interests in software entrepreneurship or sales if relevant to the course and report. Keep private financial plans and unrelated personal goals out of the assessed report unless specifically requested by the university.

### 2.8 Areas of improvement for another attachment

**Draft for review:**  
For a future attachment, I would begin by confirming the objectives, assessment dates, daily log format, and supervisor availability. I would maintain contemporaneous daily records, collect permitted evidence as work occurs, and schedule regular feedback. Technically, I would practise database selection, migrations, tests, and deployment in small reversible steps before relying on a complete feature. `[Add your own examples and supervisor advice.]`

## Chapter Three: Summary, Conclusion and Recommendations

### Summary

`[Summarize the confirmed placement period, assigned work, objectives addressed, main skills, and main challenges. Refer only to verified entries and supervisor feedback.]`

### Conclusion

**Draft for review:**  
The attachment provided an opportunity to connect `[course/programme]` with `[verified duties]`. Work involving CaseLoop can illustrate how a web application combines a browser interface, API, database, tests, and operational configuration, provided the final report distinguishes the repository's capabilities from the student's personal contribution. The learning deployment and webhook are not evidence of production readiness or organizational adoption. `[Conclude with your actual outcomes and assessment.]`

### Recommendations

#### Recommendations to the student

- Keep the daily logbook current and record evidence as work happens.
- Practise one technical layer at a time; write a test or make a small change before requesting a full solution.
- Verify database, migration, seed, and UI expectations against the same environment.
- Distinguish local tests, local Docker, public hosting, and live provider tests.
- Disclose AI assistance according to university rules and claim only work you understand and can explain.

#### Recommendations to the university

- Confirm the current report template, acceptable page count, required formatting, assessment dates, and AI-use policy before the attachment period ends.
- Provide an alternate assessment contact when the workplace supervisor will be unavailable.
- Schedule clear feedback/sign-off points for the logbook and report.

#### Recommendations to the host organization

`[Add only recommendations discussed with or approved by the organization. Possible topics include clearer learning objectives, scheduled student feedback, and an identified alternate supervisor.]`

#### Technical recommendations for CaseLoop (only if appropriate to the placement)

- Keep human review between external intake and publication.
- Use synthetic data until privacy/security and organizational approval are completed.
- Test Alembic migrations and database restore on disposable/staging databases.
- Build and locally test a production frontend/reverse proxy before any public deployment.
- Keep PostgreSQL private, store secrets outside source control, and test backup/restore.
- Validate workflow assumptions with authorized users before claiming operational value.

## Appendices

The guide's final page specifically asks for completed weekly self-analysis reports and supporting documentation. Include only completed, approved, relevant items:

1. Completed weekly self-analysis reports, signed/reviewed where required.
2. Daily logbook for the verified placement dates.
3. Attachment objectives or placement plan.
4. Approved organization chart or public organization information.
5. Synthetic architecture/workflow diagrams.
6. Test/build evidence personally retained or reproduced, with secrets removed.
7. Supervisor or university assessment forms and permitted feedback.
8. Glossary or references required by the department.

Do not append raw checkpoints as proof, secret-bearing files, `.env`, credentials, real user/beneficiary data, private chats, or unapproved screenshots.

## Provisional 60-page layout

This is a planning target only; the guide's final page does not prescribe page count. Confirm the page rule and formatting with the coordinator. A possible 60-page allocation is:

| Part | Target pages |
|---|---:|
| Preliminary pages | 8 |
| Chapter One: Introduction | 8 |
| Chapter Two: Observations and Accomplishments | 32 |
| Chapter Three: Summary, Conclusion and Recommendations | 5 |
| Appendices | 7 |
| **Total** | **60** |

Do not reach the target by padding or fabricating activities. If verified content does not support 60 pages, ask the coordinator whether the personal target is appropriate before expanding.

## Finalization checklist

- [ ] Confirm the current university report format and page requirement.
- [ ] Fill organization background, mission/vision/values, structure, and chart from approved sources.
- [ ] Replace draft objectives with the official objectives.
- [ ] Replace all bracketed text with verified details or delete it.
- [ ] Complete daily entries from actual records; do not treat project notes as proof.
- [ ] Ensure every activity is accurately attributed and disclose AI assistance where required.
- [ ] Obtain supervisor review of organizational contribution and recommendations.
- [ ] Add completed weekly self-analysis reports and approved appendices.
- [ ] Generate the contents and lists automatically after pagination.
- [ ] Remove personal, operational, and credential data from any public version.
