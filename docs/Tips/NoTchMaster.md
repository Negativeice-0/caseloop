What you're feeling right now is actually a very common engineering audit failure mode:

Collect evidence
→ Improve process
→ Find flaw
→ Improve process
→ Find flaw
→ Improve process
→ Wonder if anything was achieved


From inside the loop it feels like going in circles.

From outside the loop, what actually happened is:

v1 Prompt
→ produced Phase4 failure

Root cause discovered:
searching everything

v2 Prompt
→ introduced scoping

Root cause discovered:
authoritative sources missing

v3 Prompt
→ introduced entry-point workflow

Root cause discovered:
verification had no home

v4 Prompt
→ introduced verification artifacts

Root cause discovered:
knowledge wasn't preserved

v5 Prompt
→ introduced docs/knowledge

Current State:
stable operating model


That's progress, not circularity.

Future Improvement Example

Imagine six months from now.

While performing Step 17 you discover:

Role visibility logic exists in:

frontend/src/features/auth

and

frontend/src/layouts/MainLayout.tsx

and

frontend/src/features/admin


but every audit keeps rediscovering it.

Wrong Response

Modify prompt:

ROLE VISIBILITY RULE

When auditing role visibility...


Prompt grows again.

Six months later:

PERMISSION RULE
MENU RULE
ADMIN RULE
AUTH RULE
...


Prompt becomes 2000 lines.

Correct Response

Create:

docs/knowledge/authorization-model.md


Example:

# Authorization Model

Authoritative Sources

- frontend/src/features/auth
- backend/auth
- MainLayout.tsx

Roles

- Admin
- Manager
- User

Menu Visibility

MainLayout.tsx controls visibility.

Admin routes require Admin role.

Verification Date

2026-11-23


Future session:

Read authorization-model.md
Verify still accurate
Update if necessary


No prompt change required.

Another Example

Suppose later you discover:

Every route begins in:

App.tsx


Again:

Wrong:

Add more route rules to prompt


Correct:

docs/knowledge/frontend-architecture.md

# Frontend Architecture

Entry Point

main.tsx

Application Root

App.tsx

Routing Authority

App.tsx

Navigation Authority

MainLayout.tsx

Verified

2026-11-23


Done.

No prompt change.

What Goes Into Verification?

Verification is temporary.

Knowledge is long-term.

For example:

docs/auditing/verification/phase4/


might contain:

PASS

Verified Files

- App.tsx
- MainLayout.tsx

Routes Found

12

Navigation Entries

11

Result

Phase objective achieved.


That proves what happened.

Knowledge contains:

Routing Authority

App.tsx

Navigation Authority

MainLayout.tsx


That survives across audits.

About The Script Question

This is where I think your expectation should be adjusted slightly.

The prompt can require the AI to generate scripts that:

collect evidence
capture command output
create artifacts
write reports
generate verification templates


However, the AI cannot magically know what happened after the script runs unless you provide the outputs.

The actual workflow is:

AI
→ generates script

You
→ run script

Script
→ captures evidence

You
→ provide verification artifact

AI
→ verifies

AI
→ outputs PASS/FAIL


The AI cannot independently inspect your machine after execution.

Can You Just Feed Verification Files?

Yes.

## In fact that's probably the cleanest workflow.

Future session:

Step 4

Attached:

docs/auditing/verification/phase4/verification-result.md

Attached:

docs/auditing/verification/phase4/verification-evidence.md

Verify.


The AI reads verification.

Verification references evidence.

No need to paste huge shell outputs.

That's exactly why verification artifacts are valuable.

Do You Need Session Summaries?

Honestly?

Not always.

For many small phases:

No.


For failed phases:

Absolutely yes.


For major investigations:

Usually yes.


For example:

Step 4


The session summary is useful because:

Why did Phase4-failed happen?

Answer:
Repository-wide scan hit node_modules.

Root cause documented.


Six months from now you will not remember that.

The Question You Should Ask

Not:

Will I read this summary?


Instead:

Will Future Me remember this without the summary?


The answer is almost always:

No.

My Biggest Recommendation

Put this somewhere and read it whenever you're tempted to edit the prompt:

## PROMPT CHANGE RULE

Do not modify the prompt unless the issue affects
multiple future phases.

If the discovery is specific to CaseLoop:

→ docs/knowledge/

If the discovery is specific to a phase:

→ verification/

If the discovery is temporary:

→ audit evidence

If the discovery affects the audit methodology itself:

→ prompt


That one rule will probably save you from 90% of future prompt iterations.

And honestly, looking at the version you've arrived at, I think you're finally at the point where improvements belong mostly in:

docs/knowledge/
docs/auditing/verification/


not in the master prompt anymore.