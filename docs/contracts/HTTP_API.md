# Shared HTTP API agreement — current selected stories

**Two separate HTTP boundaries:** This file documents **React → Express** only. Express calls a **private Python AI HTTP service** using the [internal wire protocol](../backend/ai/PYTHON_HTTP_PROTOCOL.md); Python is not a browser API. All Python outputs return to Express for validation and persistence.

**Status:** PROPOSED v0.2 for all-five team freeze; routes are **not implemented**. **Scope:** US-01/02/03/05/06. This is the short **implementation-facing** subset of [AD-03 full Phase 1 API](../design/API_CONTRACT.md); it is not an automatic override of AD-03. Confirm any differences in a reviewed decision record before coding.

## Common conventions to approve

- Same-origin `/api` with Vite proxy. JSON success `{"data":...}` and lists `{"data":{"items":[...]},"page":{"nextCursor":null}}`. Dates `YYYY-MM-DD` in offering timezone; event timestamps UTC ISO 8601.
- Anonymous/authenticated session + HttpOnly cookie; `credentials:"include"`. Backend A approves cookie/session/CSRF/Origin policy; never accept browser-supplied role, ownership, score, correct answer or private storage path.
- Safe JSON error `{"error":{"code":"INVALID_REQUEST","message":"...","retry":{"action":"correctRequest","outcome":"notApplied","reuseOperationIdentity":false}},"requestId":"..."}`; stable 400/401/403/404/409/413/415/422/503 choices need a team freeze.
- Never fall back to Demo on API failure. Real mode cannot use LocalStorage fixtures for authentication or grading.
- Upload and Quiz-generation operation identity and uncertainty recovery follow full AD-03 proposal (`Upload-Operation-Id` and `Generation-Operation-Id` pending approval).
- Public API returns no correct answers or model secrets in Quiz preview. Result may show correct answers **after submission** to authorized owner.

## Owner and endpoint inventory

| Owner | Method | Endpoint | Permission / purpose |
| --- | --- | --- | --- |
| A | GET | `/api/auth/csrf` | CSRF token bootstrap |
| A | POST | `/api/auth/register`, `/api/auth/login`, `/api/auth/logout` | Student register, login/logout |
| A | GET | `/api/auth/me`, `/api/courses`, `/api/courses/:courseId` | Session restore, assigned Course list/detail |
| A | GET/POST | `/api/courses/:courseId/deadlines` | Student/Teacher reads; only assigned Teacher writes |
| A | PATCH/DELETE | `/api/courses/:courseId/deadlines/:deadlineId` | Assigned Teacher only |
| B | GET | `/api/courses/:courseId/topics` | Valid Course topics |
| B | GET/POST | `/api/courses/:courseId/materials` | Authorized list / real multipart upload |
| B | GET | `/api/courses/:courseId/materials/:materialId` | Status, conversion, eligibility detail |
| B | GET | `/api/courses/:courseId/materials/:materialId/file` | Protected byte download |
| B | GET | `/api/courses/:courseId/material-upload-operations/:operationId` | Recover unknown upload result |
| B (NEW proposal) | POST | `/api/courses/:courseId/materials/:materialId/process` | Authenticated explicit conversion/transcription; agree whether needed vs upload-triggered processing |
| C | POST | `/api/courses/:courseId/materials/:materialId/quizzes` | Material-based AI quiz request; C calls B's internal AI provider |
| C | GET | `/api/quizzes/:quizId`, `/api/me/quizzes` | Safe preview, authorized Quiz list |
| C | POST | `/api/quizzes/:quizId/attempts` | Create or recover one Draft at Start |
| C | GET/PUT | `/api/attempts/:attemptId` (GET), `/api/attempts/:attemptId/draft` (PUT) | Draft + revision |
| C | POST | `/api/attempts/:attemptId/submit` | Validate complete answers, grade **deterministically**, persist Result |
| C | GET | `/api/attempts/:attemptId/result`, `/api/results/:resultId`, `/api/me/results` | Recover/read private results |
| C (NEW optional) | GET | `/api/results/:resultId/ai-feedback` | Authorized explanation status/data; depends on agreed feedback lifecycle |

There is **no browser → AI model** endpoint. Express authenticates/authorizes, then calls the private Python service through the server-side AI client, validates its structured response, persists and returns the safe result.

## Mandatory boundary DTOs (example only)

`Course`: `{courseId, code, name, term, academicYear, calendarTimezone, today}`.
`Material`: `{materialId, courseId, filename, format, byteSize, topicIds, storageState, conversionStatus, quizEligibility, fileUrl}`.
`Quiz`: `{quizId, courseId, materialId, kind:"regular", questionCount:10, items:[{snapshotQuestionId,prompt,options:[{optionId,text}],topics}], attemptId:null, contentSource:"ai-material"}`.
`Attempt`: `{attemptId,quizId,state:"draft",revision:0,answers:{},resultId:null}`.
`Result`: `{resultId,quizId,attemptId,score,total,feedback:[{snapshotQuestionId,chosenOptionId,correctOptionId,correct}]}`.
`Deadline`: `{deadlineId,courseId,title,type,dueDate,upcoming}` (server derives `upcoming`).

- Upload: multipart `file` actual bytes + JSON-encoded `topicIds`. A successful material upload stores **real bytes and metadata**, but **does not automatically mean its AI conversion succeeded**. Expose status honestly (e.g. `stored`, `processing`, `ready`, `failed` after team freeze). Invalid supported file, zero bytes, foreign Topics, disk/DB failure return safe error.
- Processing: the **recommended development path** is explicit `POST .../process` with bounded synchronous conversion for small files, clear status on timeout, and no assumed queue. Team must approve limits/timeouts and status before implementation. AI on large audio can take longer than HTTP timeout; do not claim a background queue exists yet.
- Generate: requires authorized material and converted content; request body `{}` plus reviewed operation ID. Returns ten distinct validated **Quiz snapshots** with safe preview. **No Attempt until Start.** If conversion/model/validation fails, no partial Quiz. Actual questions must be grounded in source content; a predefined-bank fallback must never be mislabeled AI.
- Start: `POST /api/quizzes/:quizId/attempts` body `{}` → one Draft, repeated Start returns same Draft.
- Draft: `PUT .../draft` body `{"expectedRevision":0,"answers":{"item-1":"opt-a"}}`. Stale revisions reject; client retains pending answers.
- Submit: `POST .../submit` includes expectedRevision + all question answers; Backend C compares with stored snapshot keys, persists **one** immutable Result, returns score and missed-item feedback. AI explanation is separate, optional, **cannot change score**, and must not silently imply a background worker exists.
- Deadlines: Teacher writes `{"title":"Homework 2","type":"Homework","dueDate":"2026-11-28"}`; Student sees future list in course timezone, day 0–7 Upcoming, day 8+ visible/unmarked; edited/deleted reminders disappear.

## Explicit unresolved choices and contradictions

1. **US-02 content grounding:** Original M2 requires questions based on the uploaded lecture; old AD-03 assumes predefined bank (not semantic content analysis). The selected path is Express → private Python conversion/quiz HTTP → Express validation/persistence; provider/privacy/source-grounding and output review still need sign-off. Modify AD-03/04 explicitly once accepted.
2. **Processing trigger & latency:** explicit bounded synchronous `process` is **recommended for this implementation increment**; formalize size/duration/timeout and `stored/processing/ready/failed` status before building. The endpoint is proposed, not implemented.
3. **AI feedback lifecycle:** Result grade must survive AI timeout; choose separate versioned `ResultFeedback` or associated record rather than editing immutable Result. `ai-feedback` GET remains optional.
4. **Contracts to freeze:** Session/CSRF/cookies, exact error codes, DTO fields, file limits/MIME, generation/upload idempotency, course zone, persistent unique IDs and indexes. Use [AI contract](../backend/ai/AI_MODEL_CONTRACT.md) and [Persistence contract](../database/PERSISTENCE_CONTRACT.md).
