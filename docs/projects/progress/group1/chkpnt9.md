# Checkpoint 9: Brand Navigation and Hosting/WhatsApp Guidance

## Completed

- Replaced the animated shield mark with a static, generic CaseLoop HeartPulse mark. The Red Cross emblem was not recreated; use only an authorized organization-supplied asset if one is approved.
- Made the brand mark clickable. Signed-in administrators return to the Admin dashboard; other signed-in users return to Responses. On authentication screens, the mark returns to the regular auth home.
- Added a prominent README link to the Render + Neon hosting guide.
- Documented that administrator access is provisioned rather than publicly self-registered, and noted current gaps (SSO, MFA, email invitations).
- Clarified the official WhatsApp Groups API boundary: it requires an Official Business Account, supports invite-only API-created groups of up to 8 participants, and is not arbitrary existing-group scraping. CaseLoop does not yet implement Groups API payloads.

## Verification and remaining setup

- `npm.cmd run build` in `frontend` passed (TypeScript and Vite production build).
- No public deployment or live Meta webhook test was performed. Hosting/provider access and Meta credentials are not configured in this workspace.
- The current WhatsApp webhook remains the supported test-number/direct-message intake path. Messages enter coordinator review before publication or assignment.
