# Documentation hub — Study Assistant

This is the **single entry point** for team onboarding. Read **shared handoff**, then **your role folder**. Full design documents are preserved under `design/` for targeted consultation, not mandatory end-to-end reading.

**Current goal:** US-01 Material Upload · US-02 material-grounded Quiz Generation · US-03 Quiz Submission/Grading · US-05 Teacher Deadlines · US-06 Upcoming Alerts. All five must meet their original acceptance criteria before claiming **5/7 (71.4%)**. US-04/07 are out of the current target, not deleted from MVP.

**Selected architecture:** **React → Express → private Python AI service (HTTP) → Express validation/persistence → React**. Python handles Conversion, AI Quiz and explanatory AI Feedback; Express is the only browser-facing API and the only application service writing Atlas. Source-grounded AI is a new implementation direction that differs from the historical predefined-bank Phase 1 design. The actual backend and AI service are **not implemented**; many wire fields and operational settings still need team sign-off.

## Everyone reads first

1. [Team assignments and module/route ownership](team/TEAM_ASSIGNMENTS.md).
2. [Acceptance matrix for selected stories](requirements/ACCEPTANCE_MATRIX.md).
3. [Shared public HTTP contract (React ↔ Express)](contracts/HTTP_API.md): common headers/JSON/errors, plus your endpoints.
4. [Architecture decisions](team/DECISIONS.md): what is selected vs proposed.
5. [Backend coordination overview](backend/README.md), at least the service-boundary diagram and ownership table. Backend A/B/C and Database additionally read the [private Python wire protocol](backend/ai/PYTHON_HTTP_PROTOCOL.md); Frontend does **not** call Python.

## Read by role

| Role | Mandatory starting point | Detailed reference sections |
| --- | --- | --- |
| **Frontend (1)** | [frontend/README](frontend/README.md) | [HTTP contract](contracts/HTTP_API.md); [AD-04 §2 migration](design/IMPLEMENTATION_PLAN.md#2-inspected-implementation-realities-and-frontend-migration) |
| **Database (1)** | [database/README](database/README.md) and [persistence interface](database/PERSISTENCE_CONTRACT.md) | [AD-02 §3/5/8](design/DATA_MODEL.md#3-logical-entities-and-proposed-fields); [private Python wire](backend/ai/PYTHON_HTTP_PROTOCOL.md) |
| **Backend A — Express/Auth/Deadlines** | [backend/express/README](backend/express/README.md) | [AD-03 Auth/Deadline](design/API_CONTRACT.md#4-authentication-and-authorization-contract); [AD-04 IMP-01/06](design/IMPLEMENTATION_PLAN.md#4-small-future-codex-tasks) |
| **Backend B — Materials/Python AI** | [backend/ai/README](backend/ai/README.md), [AI contract](backend/ai/AI_MODEL_CONTRACT.md) and [Python wire](backend/ai/PYTHON_HTTP_PROTOCOL.md) | [AD-01 component map](design/COMPONENT_ARCHITECTURE.md#4-component-architecture); [AD-03 upload](design/API_CONTRACT.md#7-upload-and-generation-operation-contracts) |
| **Backend C — Quiz/Attempts/Results** | [backend/learning/README](backend/learning/README.md) and [AI contract](backend/ai/AI_MODEL_CONTRACT.md) | [AD-02 entities](design/DATA_MODEL.md#3-logical-entities-and-proposed-fields); [AD-03 Quiz/Result](design/API_CONTRACT.md#5-proposed-request-and-response-dto-examples) |

## Reference library

| Folder | Use |
| --- | --- |
| [team/](team/README.md) | Shared ownership and architecture decisions |
| [requirements/](requirements/README.md) | Original scope, selected-story acceptance and FR/US/NFR traceability |
| [design/](design/README.md) | Original full AD-01 Component, AD-02 Data, AD-03 API and AD-04 Plan |
| [contracts/](contracts/HTTP_API.md) | Browser ↔ Express endpoint contract |
| [backend/](backend/README.md) | Backend coordination, separate Python AI wire and learning logic |
| [frontend/](frontend/README.md) | React read/implement guide |
| [database/](database/README.md) | MongoDB/Atlas design and persistence contract |
| [archive/](archive/README.md) | Preliminary architecture and historical AutoNote review; **optional** |

**Source of truth and conflicts:** Original submitted M2 acceptance wording governs story completion; selected implementation and interface changes are recorded in [team/DECISIONS](team/DECISIONS.md) and current focused contracts. The older AD-03/04 retain their predefined-bank assumptions. **Open contract choices must be agreed and recorded**, not guessed by different contributors.
