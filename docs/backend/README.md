# Backend coordination — 3 Express-side owners

There is **one application backend** (planned Node.js/Express modular monolith). The three backend members own **different interfaces**, not three unrelated HTTP servers.

| Owner | Your folder | What you expose to others |
| --- | --- | --- |
| **A — Express foundation/auth/deadlines** | [express/](express/README.md) | Session/membership middleware, Course/Deadline HTTP, shared config/errors |
| **B — AI and material processing** | [ai/](ai/README.md) | Material/Topic HTTP; **internal conversion / quiz / feedback AI functions** |
| **C — Learning workflow** | [learning/](learning/README.md) | Quiz/Attempt/Result HTTP; calls B's AI functions and Database repositories |

## Non-negotiable invocation direction

`Frontend → Express router/controller → authenticated application service → internal AI gateway (B) → structured AI response → Express validates and persists through Database repository → Express sends safe JSON → Frontend.`

- The browser does **not** call model providers or handle API keys.
- Backend B does **not** own submitted scores or create Attempt/Result records.
- Backend C does **not** implement model SDK/prompts; it calls `AiGateway`.
- Backend A does **not** decide grading or AI output validity; it owns common security/request rules.
- Database team owns shared persistent invariants; every module uses the approved repository interfaces.

**Read:** [HTTP contract](../contracts/HTTP_API.md), [AI interface contract](ai/AI_MODEL_CONTRACT.md), [Persistence contract](../database/PERSISTENCE_CONTRACT.md), [Team assignments](../TEAM_ASSIGNMENTS.md). Endpoints and transport are proposed pending team sign-off.
