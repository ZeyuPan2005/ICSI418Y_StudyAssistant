# Frontend owner — read here

**Network boundary:** React talks to Express `/api/*`, not Python AI or model providers. Never put `AI_INTERNAL_BASE_URL` or the internal service key in browser/Vite environment. Express owns model calls and validation.

**Owner:** one React developer. **Selected stories:** US-01/02/03/05/06. Current `client/` is a functioning Demo; the Express backend does not yet exist.

## Read in order
1. [Team responsibilities](../team/TEAM_ASSIGNMENTS.md) and [acceptance criteria](../requirements/ACCEPTANCE_MATRIX.md).
2. [Short HTTP API contract](../contracts/HTTP_API.md) — **all common conventions**, then relevant Material, Quiz/Attempt/Result and Deadline routes.
3. [AD-04 Section 2 migration analysis](../design/IMPLEMENTATION_PLAN.md#2-inspected-implementation-realities-and-frontend-migration) — separate Demo and real async context, no fixture fallback.
4. Existing `client/src/App.jsx`, `client/src/screens/`, `client/src/services/demo.js`, `client/src/state/Demo.jsx`, `client/tests/`.

## Your delivery
- Make a separate **real API client** and route/session lifecycle; preserve Demo, existing routes and tests.
- Authenticated Student/Teacher Course navigation, real upload/material status, conversion state, Quiz preview/Start, drafts/errors/results, Teacher deadline edits, Student alerts.
- Do **not** call AI model, Atlas or private file paths directly. Express calls AI and persists its validated results.
- Handle request pending/failure/timeouts, session expiration, stale course/user data, incomplete answers, refresh/retry; never display secret correct keys during preview.
- Write a UI→DTO mapping and browser smoke tests for every claimed Complete Story. Pair with API owner; do not own everybody's E2E debugging.

**First artifact:** API client method table and screen-to-route mapping reviewed with Backend A/B/C. Tests: `cd client && npm ci && npm test && npm run build && npm run test:browser` (these are existing **Demo** tests, not proof of real backend).
