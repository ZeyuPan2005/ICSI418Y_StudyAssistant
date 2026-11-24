# Backend C — Quiz / Attempt / Grading / Result

You own **learning-domain business state and HTTP routes**, not model integrations.

**Read in order:**
1. [Backend coordination](../README.md), [Team assignments](../../TEAM_ASSIGNMENTS.md).
2. [HTTP API](../../contracts/HTTP_API.md) Quiz/Attempt/Result section + **[AI internal contract](../ai/AI_MODEL_CONTRACT.md)** `generateQuiz` and `generateFeedback`.
3. [Persistence contract](../../database/PERSISTENCE_CONTRACT.md), [AD-02 Quiz/Attempt/Result](../../DATA_MODEL.md#3-logical-entities-and-proposed-fields), [AD-03 `5/6](../../API_CONTRACT.md#5-proposed-request-and-response-dto-examples), [AD-04 IMP-04](../../IMPLEMENTATION_PLAN.md#4-small-future-codex-tasks).

**Own:** request generation orchestration, invoke B's AI Quiz provider from within Express, validate **exactly 10 distinct** questions grounded in the converted material, create immutable snapshot and safe preview, Start the one Draft, revision checked saves, full submit validation, deterministic option grading, one Result per Attempt. For AI feedback: invoke B's model adapter **after** score persistence, without changing submitted answers/grade.

**First delivery:** pure scoring and question/answer schema validation tests, a DTO agreement with B/Database, then create-and-preview via a fake AI gateway. Do not wait for real model credentials to exercise the workflow.

**Do not:** let an AI model decide final score, expose correct option IDs in preview, overwrite a Result after late AI feedback, or silently switch to Demo if the model is unavailable.
