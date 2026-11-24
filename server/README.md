# Server (planned)

**Selected integration:** Future Express public app server calls a separate private Python HTTP AI service for Conversion, Quiz Generation and Feedback. Express validates output and persists through Atlas repositories. No Python/Express implementation exists yet. Read [AI contract](../docs/backend/ai/AI_MODEL_CONTRACT.md), [wire protocol](../docs/backend/ai/PYTHON_HTTP_PROTOCOL.md) and [team roles](../docs/team/TEAM_ASSIGNMENTS.md).

This directory is reserved for the Phase 1 Node.js/Express modular-monolith backend.

**No backend application has been implemented yet.** IMP-01A will establish the validated configuration and local foundation after the required technical gates are reviewed. Subsequent units will implement authentication, course access, materials, quizzes, attempts, results, practice and deadlines.

Do not add placeholder endpoints or claim Atlas/session integration is working before the relevant IMP has been implemented and tested.

See [AD-04 Implementation Plan](../docs/design/IMPLEMENTATION_PLAN.md) and [AD-03 API Contract](../docs/design/API_CONTRACT.md).
