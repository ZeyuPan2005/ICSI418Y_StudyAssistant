# Architecture decision register

A short change log for team choices that affect multiple owned modules. Old AD-01/02/03/04 documents remain historical design sources; this file records **new implementation direction**, not proof code exists.

| ID | Date | Status | Decision / effect | Follow-up |
| --- | --- | --- | --- | --- |
| D-M4-01 | 2026-11-24 | Selected by project maintainer; team review pending on wire details | **Express makes authenticated/internal HTTP calls to an independent Python AI service; Python returns structured results to Express; Express validates, persists and returns safe HTTP to React.** No browser → AI, no Python → Atlas, no AI authority for scores. | Sign off [AI contract](../backend/ai/AI_MODEL_CONTRACT.md) and [private protocol](../backend/ai/PYTHON_HTTP_PROTOCOL.md), choose FastAPI/dependencies and internal secret configuration |
| D-M4-02 | 2026-11-24 | Selected delivery target | Milestone 4 work targets US-01, US-02, US-03, US-05, US-06 (5 of 7 original M2 MVP Stories). | Verify each criterion, including content-grounded US-02, before marking Complete |
| D-M4-03 | 2026-11-24 | Proposed scope revision, cross-team agreement needed | Enable actual material conversion and content-grounded AI generation **instead of claiming** that predefined topic-bank questions read a lecture. AI feedback is explanatory enhancement; backend deterministic grade/feedback remains valid if AI fails. | Update AD-03/04 after approved, confirm provider privacy/cost and test source relevance |
| D-M4-04 | 2026-11-24 | Proposed, not chosen | Python FastAPI/Uvicorn bound to `127.0.0.1` on local development; private HTTP `/internal/v1/convert`, `/generate-quiz`, `/generate-feedback`; shared service key plus strict limits | Backend A/B/C freeze exact wire behavior and deploy/security review |

**Rules:** The more narrowly scoped implementation handoff files in `docs/contracts/` and `docs/backend/ai/` are **review proposals** until signed off; they do not silently override the existing AD-03 confirmed decisions. When approved, record a dated change to AD-03/04 and update the compatibility section of the new contracts. If unresolved, developers can build against mocks/stubs but must not claim integration is complete.

**Roles:** Frontend and Database each have one owner; Backend A (Express/Auth/Deadlines), Backend B (Materials/AI/Python), Backend C (Quiz/Attempts/Results). See [Assignments](TEAM_ASSIGNMENTS.md).
