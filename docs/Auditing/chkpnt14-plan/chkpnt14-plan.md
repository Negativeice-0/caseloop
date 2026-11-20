# Baby steps

Don't rush, today it took you few hours to figure all this out, tomorrow it might take seconds. Plus later you can upload checkpoints for final readme darft. 

FYI: ensure docker engine is up first -> docker compose up -d db ->
backend server launch -> start frontend

I already feel like i am truly building for redcross throughout the globe.

It feels great -- i can definately add important notes here instead of stuffing up the main readme and keep less short so this page doesn't go past 400 lines -- i can even use ai to summarize my free thoughts.

## The complete one-step-at-a-time mega prompt
Text

----
Before pasting prompt below -- type the below below it
Or type it esnure numbering and naming e.g 1 done then paste rest above.

 Continue with Step [number]: [exact checklist title]. Step [previous number] is complete. Do not advance beyond this step.
----

Copy

---

Before pasting this prompt, prepend:

Continue with Step [number]: [exact checklist title]. Step [previous number] is complete. Do not advance beyond this step.

================================================================

Act as my senior CaseLoop engineering guide.

I will work in separate sessions. In each session, guide me through exactly ONE checklist step from preparation through completion. Never advance to the next step until I provide results and explicitly state the current step is complete.

STEP EXECUTION FORMAT

For every step:

1. State the objective.
2. Explain why it matters.
3. State what must not be changed.
4. Provide exact PowerShell 5.1 commands and/or exact file edits.
5. State expected output.
6. Explain success, failure, and ambiguity conditions.
7. Request results.
8. Help verify results.
9. Provide concise completion summary.
10. Stop and wait.

================================================================

ARTIFACT AUTOMATION REQUIREMENT

The goal is not only to complete the checklist item, but to create reusable engineering processes wherever practical.

If a phase requires more than five commands to execute correctly, prefer generating a single PowerShell 5.1 script that performs the entire phase and produces all required artifacts automatically.

When sufficient information exists, generate production-style PowerShell 5.1 audit scripts instead of long manual command sequences.

Scripts should:

- Be heavily commented.
- Preserve reproducibility.
- Avoid modifying application code unless explicitly required.
- Be rerunnable where practical.
- Generate reports automatically.
- Create required directories automatically.
- Capture evidence before analysis.

================================================================

ARTIFACT COMPOSITION REQUIREMENT

Generated audit scripts should automatically collect, transform, summarize, and distribute evidence into:

1. RawShell
2. FullStack
3. SeniorLead

Do not merely recommend these artifacts.

Generate scripts that create them automatically whenever sufficient information exists.

================================================================

PHASE FOLDER STRUCTURE

For every phase N:

.\docs\auditing\data\fullstack\phaseN\
.\docs\auditing\data\rawshell\phaseN\
.\docs\auditing\data\snrlead\phaseN\

Never delete prior phase artifacts.

================================================================

REQUIRED OUTPUTS

FULLSTACK REPORT

Location:
.\docs\auditing\data\fullstack\phaseN\

Contents:
- Technical findings
- Route inventories
- Permission inventories
- Architecture observations
- Dependency findings
- Environment metadata
- Build findings
- Test findings
- Branch
- Commit SHA
- Timestamp

----------------------------------------------------------------

RAWSHELL EVIDENCE

Location:
.\docs\auditing\data\rawshell\phaseN\

Contents:
- Unmodified terminal output
- Build logs
- Test logs
- Git evidence
- Environment inspection output

----------------------------------------------------------------

SENIORLEAD REVIEW

Location:
.\docs\auditing\data\snrlead\phaseN\

Contents:
- Risks
- Recommendations
- Architecture observations
- Technical debt
- Maintainability impact
- Business impact
- Leadership observations
- Future actions

================================================================

AUDIT PHASE BASELINE CAPTURE

When applicable, automatically capture:

- Timestamp
- Current branch
- Safety branch
- Commit SHA
- Git status
- Tracked files
- File hashes
- Package-lock hash
- Build status
- Test status
- Environment versions
- Running processes
- Listening ports
- Relevant inventories for the active phase

Optimize RawShell for evidence preservation.

Optimize FullStack for technical analysis.

Optimize SeniorLead for decision-making.

================================================================

CHECKLIST ORDER

1. Confirm backend and frontend health.
2. Capture Git status and create a safety branch.
3. Record baseline backend state of all files and frontend build; confirm whether both should be running.
4. Inventory all frontend routes and navigation entries.
5. Inventory backend routes and authorization dependencies.
6. Build the role-permission matrix.
7. Build the frontend-to-backend-to-database connection map.
8. Audit README and every linked documentation file.
9. Remove redundant navigation entries only.
10. Test desktop, mobile, direct URLs, and role visibility.
11. Decide whether old routes should remain, redirect, or be deleted.
12. Remove unused imports and dead route wiring.
13. Refactor components only where responsibility is clearly mixed.
14. Audit Python, Docker, frontend, and configuration references.
15. Produce deletion candidates; never delete automatically.
16. Add or improve backend authorization tests.
17. Add or improve frontend navigation and role tests.
18. Run final tests, build, and manual smoke checks.
19. Update README with verified current behavior.
20. Create final session summary and logbook entry.

================================================================

RULES

- Never invent filenames, routes, permissions, or components.
- Search first, then conclude.
- Backend authorization is authoritative.
- Hidden UI is never security.
- Never delete code without evidence, reversible Git history, and passing tests.
- Use synthetic data only.
- Keep each session focused.
- Begin with the requested step only.

---

## What The above Prompt Actually Does (Concise Summary)

### For You

- Forces one-step-at-a-time execution.
- Prevents accidental checklist skipping.
- Makes every phase auditable and reproducible.
- Produces evidence, not opinions.

### For Future AI Sessions

- Encourages generation of a single automation script when work becomes repetitive.
- Produces three audiences automatically:
   - RawShell → evidence
   - FullStack → engineers
   - SeniorLead → leadership/decision makers

### For CaseLoop

Creates a trail of:
- branch
- commit
- build status
- test status
- architecture findings
- route findings
- permission findings
- risks and recommendations

### For Learning

Lets you focus on:
- why the system exists
- how pieces connect
- how to verify changes

instead of memorizing thousands of generated lines.

----

## For Your Future CEO Goal

This prompt quietly enforces:


```Markdown
Evidence
→ Understanding
 
Understanding
→ Confidence
 
Confidence
→ Better Decisions
 
Better Decisions
→ Less Risk
 
Less Risk
→ More Reliable Delivery
 
Reliable Delivery
→ Customer Trust
 
Customer Trust
→ Business Success
```




## Why would do i need a checklist you wonder?
That checklist is not an everyday task list or just for interns. It is a structured process for auditing, securing, refactoring, and preparing a full-stack application for release.

Use the full checklist when:

- Taking over an unfamiliar codebase

- Preparing a major refactor or release

- Reviewing authentication, permissions, or routes

- Cleaning up a risky or poorly documented project

For normal daily work, use only the relevant parts: check Git status, run tests, make a focused change, review the diff, and verify the result.

Main message: the checklist is useful, but it should be applied proportionally—not followed mechanically for every small change.

## What “check Git, test, change, review, verify” means
For a developer, the normal loop is:

- Check Git status — know which branch you are on and whether existing changes might be affected.

- Understand the task — identify the user problem and the expected result.

- Make a focused change — avoid mixing unrelated cleanup with the requested work.

- Run relevant tests — use fast targeted tests first, then broader tests when the change is risky.

- Review the diff — look for accidental edits, missing tests, security problems, and unclear code.

- Verify the result — test the actual user path, including error cases and permissions where relevant.

Record the outcome — explain what changed, what was tested, and any remaining risk.

---

GitHub pull requests are appropriate for preserving discussion, checks, diffs, and review history; small changes are easier to review and reverse. 
GitHub Docs
GitHub Docs
+1
---

## Final session summary
A user comment usually moves through a filtered, collaborative process:

Text

Copy
User comment
   ↓
Support team / feedback system
   ↓
Product team groups similar comments
   ↓
Product manager identifies the underlying problem
   ↓
User researchers + data scientists investigate
   ↓
Data engineers prepare reliable data and measurement tools
   ↓
Designers create possible solutions
   ↓
Security, legal, accessibility, and infrastructure teams review risks
   ↓
Developers build the feature or fix
   ↓
Testers, engineers, and automated systems test it
   ↓
Small release or experiment with selected users
   ↓
Data team measures results
   ↓
Product leaders decide: improve, expand, pause, or remove
   ↓
Support and users provide new feedback
   ↺
The cycle continues
How one large building stays busy
A large company does not have every employee working on the same user comment. Different teams work on different products, problems, and company responsibilities:

---

Copy
Many user comments
   ├── Search problems → Search teams
   ├── Video problems → YouTube teams
   ├── Cloud requests → Cloud teams
   ├── Security reports → Security teams
   ├── App issues → Android or application teams
   ├── Data questions → Analysts and data scientists
   ├── Infrastructure needs → Reliability and platform teams
   ├── Business needs → Sales, finance, legal, and operations
   └── Employee needs → Recruiting, facilities, and internal IT
The data team does not simply read comments and hand finished data to developers. It may analyze comments, user behavior, experiments, surveys, and system performance. Developers, product managers, designers, researchers, and data specialists usually work together from the beginning.

Main idea: users provide feedback, product teams prioritize it, research and data teams investigate it, designers plan solutions, engineers build them, testing teams verify them, and the company measures whether the result actually helps. Not every request becomes a feature, and not every employee is involved in every request.
---