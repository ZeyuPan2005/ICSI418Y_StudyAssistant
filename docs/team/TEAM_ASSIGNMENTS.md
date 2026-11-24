# Team responsibilities and integration handoffs

**Chosen cross-service boundary:** Express calls an independently running **private Python AI HTTP service**. The Python process does not serve the browser and never writes Atlas. Review the [AI contract](../backend/ai/AI_MODEL_CONTRACT.md) and [wire protocol](../backend/ai/PYTHON_HTTP_PROTOCOL.md); wire details remain proposed.

**Status:** Role-level working proposal; reading navigation and documentation restructure are now in `main`, but the **API DTOs and wire details still require team sign-off**. **Organization:** 1 Frontend, 1 Database, 3 Backend. **Current selected stories:** US-01, US-02, US-03, US-05, US-06; do not count them Complete until verified against original M2 criteria.

| Owner role | Owns | API / internal boundary | First independently reviewable delivery |
| --- | --- | --- | --- |
| Frontend | `client/` React, real-mode API client/session, upload/conversion/generation/quiz/deadlines UI; retain Demo | Consumes `contracts/HTTP_API.md` | Real-mode shell, API error/loading states and UI→DTO mapping |
| Database | Atlas dev/test, schemas, indexes, seed/provisioning support and persistence adapters; no business authorization | Provides `database/PERSISTENCE_CONTRACT.md` to Backend A/B/C | Proposed collections/indexes, seed, repository method shapes and DB smoke evidence |
| Backend A — Express | Server bootstrap, config, sessions/CSRF, role/course access, deadline CRUD + Upcoming calculation, shared middleware/errors | Provides Auth/Course/Deadline HTTP routes and shared authentication middleware | Startup/health/proxy, authenticated Course list, verified role/course guards |
| Backend B — AI & Materials | Protected material bytes intake/read/status, content conversion/transcription/notes, model adapter for quiz generation **and AI feedback** | Provides Material/Topic routes, typed Express AI client wrappers **and** Python HTTP service ([wire protocol](../backend/ai/PYTHON_HTTP_PROTOCOL.md)) to Backend C | Validated storage + conversion smoke, fixture AI responses and schema validation |
| Backend C — Learning workflow | Quiz request orchestration, safe preview, Start/Attempt/draft, deterministic grading, immutable Results; invoke Backend B's AI methods | Provides Quiz/Attempt/Result HTTP routes; consumes AI methods | Pure grading/validation tests and Quiz/Attempt/Result DTO integration |

## API owner — no overlapping route ownership

- **Backend A:** `/api/auth/*`; `GET /api/courses`; `GET /api/courses/:courseId`; `/api/courses/:courseId/deadlines*`.
- **Backend B:** `GET /api/courses/:courseId/topics`; `/api/courses/:courseId/materials` list/upload/detail/file; proposed process/conversion route. **No public browser→model route.**
- **Backend C:** `POST /api/courses/:courseId/materials/:materialId/quizzes`; `/api/quizzes/:quizId` and Start; `/api/attempts/:attemptId*`; `/api/results/:resultId`; own Quiz/Result indices.
- **Database** defines shared repository methods and protects indexes; API owners choose business rules, validate permissions and call persistence. Database owner does **not** write all HTTP routes.
- **Python AI service B** returns untrusted **candidates** only. C validates, assigns stable identifiers, persists snapshots, grades using stored keys, and returns sanitized responses. AI never acts as the authenticated authority, never grants membership, and never overwrites a persisted score.
- **Frontend** does not send role/grade/answer key as trusted inputs; cannot directly call AI provider or MongoDB.

## End-to-end handoffs

`Browser → Express (A shared middleware) → B Material upload/protected storage → B AI convert → Express persists converted content/status → C calls B AI quiz → C validates/persists Quiz snapshot → Browser safe preview → C Start/Draft/Submit → C deterministic grading/persist Result → C calls B AI feedback for explanations → Express serves authorized Result and optional AI feedback.`

### What can progress in parallel

1. **All five:** freeze shared headers/DTOs/errors, status lifecycle, Python HTTP wire schema, timeouts, ports, authentication and model privacy, secret/data policy and persistence keys. Record owner/reviewer.
2. **A + DB:** bootstrap Express/auth, Atlas and trusted fixture Course membership. **Frontend:** create real API boundary while Demo tests remain working.
3. **B:** implement private Python HTTP endpoints using deterministic stubs before calling live models (no live model required initially). **C:** implement deterministic grading, lifecycle and tests using fixtures matching the AI contract.
4. After auth/course base, **A + Frontend** finish deadlines independently of quiz. **B + Frontend** integrate materials; **B + C + Frontend** integrate generated Quiz.
5. **All:** E2E tests + demo evidence for all five selected stories, including error/restart/authorization cases. Each owner provides a recorded contribution for the PDF.

## Working agreement

Each workstream uses its own feature branch and small PR, with one non-author reviewer. Agree one integration coordinator; this person coordinates merges, not all debugging. Do not push secrets, student recordings, raw lecture files, production credentials, model outputs, or private answer keys. Documentation can be merged after review. Code changes to shared API boundaries should be agreed in a task PR and reviewed before merging into `main`.
