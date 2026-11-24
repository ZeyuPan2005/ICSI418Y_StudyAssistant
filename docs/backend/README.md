# Backend coordination — 3 Express-side owners

**Decided boundary:** One browser-facing Node/Express server + one **private Python AI HTTP service**. The three Backend people own different modules, **not** three public servers. [Exact private protocol](ai/PYTHON_HTTP_PROTOCOL.md).

There is **one application backend** (planned Node.js/Express modular monolith). The three backend members own **different interfaces**, not three unrelated HTTP servers.

| Owner | Your folder | What you expose to others |
| --- | --- | --- |
| **A — Express foundation/auth/deadlines** | [express/](express/README.md) | Session/membership middleware, Course/Deadline HTTP, shared config/errors |
| **B — AI and material processing** | [ai/](ai/README.md) | Material/Topic HTTP; **private Python HTTP conversion / quiz / feedback endpoints** |
| **C — Learning workflow** | [learning/](learning/README.md) | Quiz/Attempt/Result HTTP; calls the B-owned Python HTTP service through a shared Express client and uses Database repositories |

## Non-negotiable invocation direction

`Frontend → Express router/controller → authenticated application service → private Python HTTP AI service (B) → structured AI response → Express validates and persists through Database repository → Express sends safe JSON → Frontend.`

- The browser does **not** call model providers or handle API keys.
- Backend B does **not** own submitted scores or create Attempt/Result records.
- Backend C does **not** implement model SDK/prompts; it calls a shared **Express-side Python HTTP client** maintained with Backend A/B.
- Backend A does **not** decide grading or AI output validity; it owns common security/request rules.
- Database team owns shared persistent invariants; every module uses the approved repository interfaces.

**Read:** [HTTP contract](../contracts/HTTP_API.md), [AI interface contract](ai/AI_MODEL_CONTRACT.md) and [Python HTTP protocol](ai/PYTHON_HTTP_PROTOCOL.md), [Persistence contract](../database/PERSISTENCE_CONTRACT.md), [Team assignments](../team/TEAM_ASSIGNMENTS.md). **Python-over-private-HTTP transport is selected**; exact endpoints, security and DTO fields require team sign-off.
