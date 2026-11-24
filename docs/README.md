# Team documentation — start here

**Current delivery target:** US-01 (upload), US-02 (quiz generation), US-03 (answer/grade), US-05 (teacher deadlines), US-06 (upcoming alerts). These are **five of seven** Milestone 2 MVP stories; 5/7 = 71.4% **only after each selected story meets its original acceptance criteria**. US-04 practice and US-07 teacher review remain in the overall plan, but are not current implementation targets.

**Reading rule:** Everyone reads the short shared materials, then their own role folder. The full AD documents below are references, not required cover-to-cover reading. All new interface documents are **proposed for team sign-off**, not evidence that the backend/AI/Atlas exists.

## Everyone — mandatory, in this order

1. [Team responsibilities and handoffs](TEAM_ASSIGNMENTS.md): who builds each API, AI module, persistence boundary and integration test.
2. [Selected-story acceptance matrix](ACCEPTANCE_MATRIX.md): what the demo and report must prove; explicitly identify the AI-vs-bank decision for US-02.
3. [HTTP API contract](contracts/HTTP_API.md): shared `/api` routes, session, success/error shapes, safe quiz previews, and module ownership.
4. [AI model ↔ Express internal contract](backend/ai/AI_MODEL_CONTRACT.md): read **Overview, Responsibility boundary, and end-to-end flow**; the AI owner, Backend C, and DB owner read all sections.

Before coding against a shared interface, **all five agree** the DTO/status fields and decisions marked OPEN. Do not treat proposed AD-03 routes or AI transport choices as already approved.

## Read by assigned role

| Role | Start with | Additional required parts |
| --- | --- | --- |
| **Frontend (1)** | [Frontend guide](frontend/README.md) | HTTP contract; AD-04 `2 async migration; existing `client/src/` screens |
| **Database (1)** | [Database guide](database/README.md) | [Persistence handoff](database/PERSISTENCE_CONTRACT.md); AD-02 `3, `5, `8 |
| **Backend A — Express/Auth/Deadlines** | [Backend A guide](backend/express/README.md) | AD-03 `4, `5 identity/deadlines, `10; AD-04 IMP-01/06A |
| **Backend B — AI + Material processing** | [Backend B guide](backend/ai/README.md) | [AI internal contract](backend/ai/AI_MODEL_CONTRACT.md); AD-03 material routes; AD-04 IMP-02/03 |
| **Backend C — Quiz/Attempts/Results** | [Backend C guide](backend/learning/README.md) | AI internal contract; AD-03 `5 quiz/attempt/result and `6; AD-04 IMP-04 |

[Backend coordination map](backend/README.md) describes the call chain and API ownership.

## Source documents retained at their existing paths

- [Requirements baseline](REQUIREMENTS_BASELINE.md) — full Phase 1 requirements and proposed ACs; consult original submitted M2 for exact wording.
- [Requirements traceability](REQUIREMENTS_TRACEABILITY.md) — all FR/UC/US/NFR mappings, including deferred work.
- [AD-01 Component architecture](COMPONENT_ARCHITECTURE.md) — logical boundaries C01–C10.
- [AD-02 Data model](DATA_MODEL.md) — logical entities, proposed Atlas persistence, snapshot constraints.
- [AD-03 Full Phase 1 API contract](API_CONTRACT.md) — extended scope including US-04/07; **pre-existing proposal assumes a predefined Question Bank**.
- [AD-04 Full Phase 1 implementation plan](IMPLEMENTATION_PLAN.md) — extended work packages, gates, tests and dependencies.
- [Preliminary architecture plan](ARCHITECTURE_PLAN.md) — older design history, optional reading.
- [AutoNote import review](AUTONOTE_IMPORT_REVIEW.md) — historical Python/security audit, **not part of current runtime**.

**Decision conflict to resolve:** The original M2 US-02 expects questions based on uploaded content. Earlier AD-03/04 deliberately used a predefined topic Question Bank without understanding file contents. The team now plans an **Express → AI model adapter → Express validation/persistence** flow for conversion, quiz and feedback. The new AI contract records this as a proposed change to be signed off and reconciled with AD-03/04 before implementation; do not silently present it as an already-approved Phase 1 requirement.

Current `server/` is a placeholder. `client/` is a working Demo, not real API/Atlas evidence. Keep the Demo functional during migration.
