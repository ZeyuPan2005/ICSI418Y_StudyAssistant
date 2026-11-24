# Backend B — Materials + AI model integration

**Selected direction:** Build a **separate Python HTTP service** for Conversion, Quiz Generation and AI Feedback, called by Express over private HTTP. Python never handles browser sessions, course permissions or Atlas.

You own **three model-facing capabilities**: **Conversion, Quiz Generation, AI Feedback**. You also own Material/Topic upload-readiness endpoints and protected file handling, but **not** Quiz/Attempt/Result persistence or grading.

**Read in order:**
1. [Backend coordination](../README.md) + [Team responsibilities](../../TEAM_ASSIGNMENTS.md).
2. **[AI ↔ Express internal contract](AI_MODEL_CONTRACT.md)** and **[private Python HTTP protocol](PYTHON_HTTP_PROTOCOL.md)** — agree the wire format with Backend A and C.
3. [HTTP API](../../contracts/HTTP_API.md) Material/Topic endpoints; [Persistence contract](../../database/PERSISTENCE_CONTRACT.md).
4. [AD-01 C03/C04/C05/C10](../../COMPONENT_ARCHITECTURE.md#4-component-architecture); [AD-03 upload/generation design](../../API_CONTRACT.md#7-upload-and-generation-operation-contracts); [AD-04 IMP-02/03](../../IMPLEMENTATION_PLAN.md#4-small-future-codex-tasks).

**First delivery:** Python HTTP stub for three `/internal/v1/*` routes with deterministic fixtures, schema/secret validation and safe errors; then test Express → Python HTTP → Express validation/persistence with no secret/answer leak. Develop Material upload/status alongside this; no live model key needed for stub tests.

**Important:** Original AD-03 selected predefined topic Question Bank for Phase 1. AI-grounded quiz generation is a **proposed scope change** to resolve the original Milestone 2 US-02 content requirement; record approval and external-model data/cost policy before live model calls.
