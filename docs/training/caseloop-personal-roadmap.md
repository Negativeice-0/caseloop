# Eight-Week Personal Roadmap: Placement, CaseLoop, Business, and Life

**Period:** October 26–December 20, 2026  
**Planning status:** Draft for the remaining weeks. It does not claim that future tasks have happened.

## Ground rules

- Your stated placement schedule is weekdays, 8:00 a.m.–4:00 p.m. That is committed time, not free project time.
- Protect sleep, meals, travel, recovery, and relationships. Do not try to turn every evening into a second workday.
- This is a proposal, not a claim about your available hours. Start small and reduce it if energy, travel, or school requires it.
- Keep the attachment assessment and near-term income needs ahead of optional projects.
- Do not combine private investing decisions with a software-project plan. This document offers learning boundaries, not investment or trading advice.

## The priority stack

1. **University and attachment:** keep the logbook current, clarify assessment and signatures, and complete required work.
2. **Sales/client work:** protect the activity most likely to bring near-term income; use a weekly client/outreach target you can realistically maintain.
3. **CaseLoop:** use it as the primary technical learning project until local PostgreSQL, tests, independent change, and a safe demo are understood.
4. **One startup experiment at a time:** alternate Matchmaker customer discovery and D/arsd exploration rather than building both at once.
5. **YouTube:** optionally repurpose a learning note into a short video; do not create a separate content workload until the weekly rhythm is stable.
6. **Finance learning:** learn product risks and local rules; avoid using tuition, rent, emergency funds, or borrowed money for speculation.
7. **Social life and rest:** schedule these on purpose. Rest is part of keeping the placement and business sustainable.

## A deliberately modest weekly template

Start with this as an experiment for two weeks and adjust. The placement is already 8–4 on weekdays; this template assumes only a few optional blocks outside it.

| Block | Example time | Focus |
|---|---:|---|
| Two short weekday blocks | 2 × 30–45 min | University admin/logbook, review notes, or a single small coding concept. Stop at the planned end. |
| One business block | 1–2 hours | Follow up with shop clients, prepare an offer, or do customer conversations. Track outcomes rather than hours alone. |
| One CaseLoop lab | 75–90 min | One session from the two-week lab: predict, inspect, attempt, test, and explain. |
| One rotating exploration | 45–60 min | Alternate Matchmaker discovery with D/arsd learning. Do not start a second large build. |
| One social/rest block | Protected | Friends, family, exercise, faith/community, or unstructured recovery. |
| Optional finance-learning note | 20–30 min | Compare concepts, fees, regulation, and risk; no live trade required. |

If this is too much, remove optional work in this order: finance content, YouTube, rotating exploration, then extra CaseLoop work. Do not reduce sleep or skip placement requirements to preserve side projects.

## Eight-week sequence

| Week | Dates | Main focus | Small evidence of progress |
|---|---|---|---|
| 1 | Oct 26–Nov 1 | Past period—reconstruct only from dated notes and ask the supervisor to clarify the logbook format. | Actual dated notes or explicit gaps; no invented entries. |
| 2 | Nov 2–Nov 8 | Past period—verify work and assessment expectations. | Weekly summary based on the real logbook. |
| 3 | Nov 9–Nov 15 | Past period—confirm what the Nov 13 checkpoint says about your own contribution. | One accurate evidence-backed entry; supervisor confirmation if required. |
| 4 | Nov 16–Nov 22 | Visit/contact the university this weekend; ask about December assessment backup. Request a meeting with the manager before December. | Written answers, dates, and a named contact/process. |
| 5 | Nov 23–Nov 29 | Complete current attachment duties; ask for a short demo/review only if the manager agrees. Continue one CaseLoop learning session. | Current logbook and one recorded technical learning result. |
| 6 | Nov 30–Dec 6 | Prepare for the manager's absence; confirm signatures, assessor, due dates, and work handover. Prioritize client follow-ups over extra features. | Assessment readiness checklist and supervisor feedback or documented follow-up. |
| 7 | Dec 7–Dec 13 | Follow the university-approved assessment process. Keep CaseLoop to a small practice block; no rushed public deployment. | Verified assessment evidence, a small independent code/test explanation, and current log. |
| 8 | Dec 14–Dec 20 | Close the period: complete factual weekly review, ask for feedback, and choose the next project based on evidence. | Finished logbook/report draft and a next-quarter decision list. |

For weeks 1–3, this table is a planning aid, not a retrospective work record. Use actual notes, messages, test history, or supervisor confirmation to reconstruct them.

## CaseLoop: turn a finished-looking app into skill

The app already has substantial code, but code existing is not the same as your being able to maintain it. Avoid adding arbitrary features. Use observable mastery checkpoints:

1. Run the application and identify which process serves the UI, API, and database.
2. Explain the `DATABASE_URL` → SQLAlchemy engine → `get_db()` → route path.
3. Run focused tests and explain which fixture/database each uses.
4. Reproduce one small behavior and make one useful change yourself.
5. Trace the official webhook from signature validation to pending review and approval.
6. Build a production frontend/proxy only after the local Docker/Compose path is understood.
7. Deploy synthetic data only after secrets, TLS, ports, backups, and cost gates are checked.

Use the [Two-Week Learning Lab](./caseloop-two-week-learning-lab.md) and [Completion Roadmap](./caseloop-completion-roadmap.md); ask for a hint rather than generated code when you are practising.

## Matchmaker and D/arsd: validate before expanding

### Matchmaker

Before a large build, identify a specific audience, a repeated pain, how people solve it now, willingness to try/pay, and privacy/safety implications. Conduct a small number of consent-based interviews. Do not collect sensitive personal data just to validate the idea. Decide whether the next step is a mockup, a waitlist, or no build.

### D and arsd

Treat “make D mainstream” as a long-term ambition, not an eight-week success metric. First build one small tool or library component that solves a demonstrated problem, has tests and documentation, and can be compared honestly with alternatives. Keep language/ecosystem study bounded until a real user or business need justifies more time.

Alternate one weekly discovery block: Matchmaker one week, D/arsd the next. If sales or university deadlines intensify, pause both without treating that as failure.

## Sales, YouTube, and investing

### Sales backup

Keep sales concrete: choose a customer segment, one clear offer, a weekly outreach/follow-up target, and a simple record of conversations, proposals, and outcomes. Do not promise features, timelines, or organizational adoption that are not confirmed. This is likely a more immediate income path than a speculative software product.

### YouTube

If useful, make a short learning log from one thing you actually did: “I expected X, observed Y, tested Z.” Avoid posting customer details, credentials, internal screenshots, or claims of Red Cross endorsement. Publishing is optional; the learning evidence matters more than a channel-growth target.

### Forex and HISA

If by HISA you mean a high-interest savings account, compare regulated providers, access terms, fees, taxes, inflation, deposit protection, and withdrawal restrictions using current local information. Forex is high risk; start with education and paper practice only if you choose to study it. Do not treat projected returns as income, borrow to trade, or use money needed for essentials. This is a general safety framework, not personalized financial advice; consult qualified local professionals for decisions.

## Getting university and Red Cross attention responsibly

Attention is earned through a small, credible request—not by sending a 60-page document to everyone.

1. Prepare a one-page brief: the operational problem (in general terms), intended users, workflow, what is already implemented, what is only a demo, current limitations, data/privacy safeguards, and one specific request.
2. Use synthetic records in a short demo: pending intake → coordinator review → approved response → optional assignment → timeline/report.
3. Ask the university for the right assessor, report requirements, and permission to present the project as attachment work.
4. Ask the manager for feedback on whether the workflow reflects real needs, what terminology/approval steps are wrong, and who should review it.
5. Ask the appropriate Red Cross contact for permission and guidance before using its name, logo, data, policies, or presenting the project as an organizational pilot.
6. Request one concrete next step: a 20-minute review, a named user to interview, or written feedback—not “make this globally renowned.”
7. Track feedback and decisions. A “not now,” security concern, or request to stop is a valid outcome that should shape the project.

Do not represent a local demo as an adopted product. Avoid protected emblems and marks unless authorized. The best proof is a documented user problem, a safe demo, clear constraints, and constructive feedback.

## Stay sustainable

- Keep a visible “now / next / later” list with no more than three active priorities.
- Do a 15-minute Sunday review: placement requirements, client follow-ups, next CaseLoop lesson, calendar, and rest.
- When a deadline changes, re-plan openly; do not secretly add night work.
- Keep a decision journal for project choices: evidence, assumptions, cost/risk, and revisit date.
- Measure progress by independent explanations, verified tests, customer conversations, and completed assessments—not by the number of features or tools installed.
