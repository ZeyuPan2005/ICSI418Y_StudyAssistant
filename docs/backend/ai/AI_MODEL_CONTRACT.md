# AI ↔ Express contract — Python HTTP sidecar

**Architecture decision:** Express calls an **independently running private Python AI service over HTTP**, receives structured data, then Express validates, applies business rules, persists and answers React. This **transport choice is selected** for the team handoff; the actual endpoints and schemas below are **proposed v0.2** until A/B/C/Database/Frontend review. No server or Python service is currently implemented.

**Owners:** Backend A provides Express bootstrap, auth/session, course authorization and shared error handling; Backend B owns Express Material APIs, file processing and the private Python AI service; Backend C owns Express Quiz/Attempt/Result APIs, answer validation and deterministic grading; Database owns persistence and unique constraints. The Python process never connects directly to MongoDB and never accepts requests from the browser.

**Read the exact HTTP request/response contract in [PYTHON_HTTP_PROTOCOL.md](PYTHON_HTTP_PROTOCOL.md).** [Public browser ↔ Express routes](../../contracts/HTTP_API.md) are separate. [Shared persistence contract](../../database/PERSISTENCE_CONTRACT.md) covers storing model outputs. Use the [role map](../README.md) to assign reviewers.

## 1. Boundary and sequence

```text
React (public)
  |
  |  /api/** + session cookie / CSRF as appropriate
  v
Express (one public application server)
  |-- authenticate / authorize Course & resource
  |-- accept & store bounded material bytes (protected storage + Atlas)
  |-- call private Python service on 127.0.0.1 via HTTP:
  |     POST /internal/v1/convert          (multipart, server-owned source bytes)
  |     POST /internal/v1/generate-quiz    (JSON, converted content)
  |     POST /internal/v1/generate-feedback (JSON, graded Result context)
  |  <-- structured JSON OR safe internal error
  |-- verify DTO, resource ownership, question count, answer keys, source references
  |-- persist material conversion, immutable Quiz/Attempt/Result (via DB repositories)
  |-- strip correct answers from preview and secrets from all HTTP responses
  v
React (safe application response)
```

- One **Node/Express** application server, one **Python AI sidecar** (recommended FastAPI/Uvicorn, subject to dependency review). Python is a private model adapter, **not a second public application backend**.
- Python is bound to `127.0.0.1` only for local development; Express also authenticates its private requests with an injected internal service key (header specified in protocol). Neither model credentials nor internal shared key is sent to React. Cross-host production deployment requires private networking, TLS/service authentication, and a separate deployment review — localhost-only is not a production network model.
- Express generates the `requestId` for correlation, enforces deadlines and size ceilings, and **never** trusts AI data as authorization, grading result, snapshot ID or database path.
- Do not import `legacy/AutoNote/` into production code until a separate technical and credential security review. No direct Python-to-Atlas writes.

## 2. Internal operations and outputs

### A. Conversion — source file → usable content

**Caller:** Backend B Express Material Service **after** accepting real bytes and Atlas metadata. **Callee:** Backend B Python `POST /internal/v1/convert`; multipart part `file` plus metadata. Python may extract PDF/PPTX text or transcribe MP3/WAV and optionally structure notes. It returns a `ConvertedContent`, not a Material/Quiz ID.

```json
{
  "language": "en",
  "plainText": "Functional requirements describe observable behaviors...",
  "sections": [
    {"sectionId": "s1", "title": "Requirements", "text": "Functional requirements ..."}
  ],
  "warnings": []
}
```

Express validates nonempty usable content, section boundaries and safe lengths, saves converted content linked to the original Material, then updates conversion status. **Real upload succeeded** and **conversion ready** are separate facts. Convert can fail while uploaded bytes remain valid. Trigger (explicit `process` endpoint vs after-upload) and bounded synchronous behavior must be frozen before implementation. The initial proposal uses explicit processing with bounded file size/duration, **no unimplemented queue or background job claim**.

### B. Quiz generation — converted content → question candidates

**Caller:** Backend C Express Quiz Service obtains authorized Material/`ConvertedContent`; calls Backend B Python `POST /internal/v1/generate-quiz` using a JSON body (never browser-supplied answer keys). Python returns **draft candidates**.

```json
{
  "questions": [
    {
      "prompt": "Which action is a functional requirement?",
      "options": [
        {"optionId": "a", "text": "Allow uploading a lecture file"},
        {"optionId": "b", "text": "Load a page within two seconds"}
      ],
      "correctOptionId": "a",
      "explanation": "File upload is a required behavior.",
      "topicIds": ["topic-1"],
      "sourceRefs": [
        {"sectionId": "s1", "quote": "Allow uploading a lecture file"}
      ]
    }
  ]
}
```

This illustrates **one** candidate. The accepted regular Quiz must have **exactly ten validated distinct questions**. Express must reject invalid count, duplicate prompts/options, unknown topic IDs, bad answer keys, empty/irrelevant sources, malformed JSON or unsafe content. `sourceRefs` are supporting citations, **not automatic proof** that a model faithfully used the lecture. Validate traceability with fictional test lectures. On success Backend C assigns immutable snapshot IDs and persists private answer keys, and returns a preview with question text + option IDs/text **but no correct answer or explanation that reveals it**. **Generate creates Quiz only; Start creates Attempt.** No partial Quiz is stored on model failure.

Original Phase 1 AD-03/AD-04 used a manually matched predefined Question Bank without semantic content extraction. The AI content-grounded mode here is a **new selected implementation direction**, not an unacknowledged equivalence. The old bank can remain a **test stub only**, with visibly distinct provenance and never masquerading as content AI.

### C. Feedback — saved graded Result → explanation

**Caller:** Backend C Express Result Service calculates score by comparing submitted answer option IDs against **stored correct snapshot keys**, persists one immutable Result, **then** calls Backend B Python `POST /internal/v1/generate-feedback`. Python receives minimal question content, wrong choices and correct choice text, with no student name/email/session.

```json
{
  "summary": "Review functional versus non-functional requirements.",
  "perQuestion": [
    {"snapshotQuestionId": "q3", "explanation": "Latency is a performance constraint."}
  ],
  "suggestions": ["Compare the two types in lecture section s1."]
}
```

AI **never assigns or changes score, correctness, attempts or the immutable Result**. If model feedback times out, the score/answer feedback required by Milestone 2 US-03 remains available. Proposed `ResultFeedback` record stores status `pending/available/failed` separately, with privacy and version controls. Browser retrieval of AI explanation is optional pending review of an explicit GET endpoint or safe projection. Avoid holding the original submit request open for a long model call; choose an explicit request/response lifecycle before shipping. **No asynchronous worker exists yet.**

## 3. Security and data handling

- Model text and uploaded file bytes are untrusted. Ignore instructions embedded inside lecture content; constrain model capabilities to transformation, question and explanation outputs only. Schema checks are mandatory but **do not guarantee educational correctness**.
- Express authenticates and checks User/Teacher/Course ownership; Python trusts only the authorized internal caller via a service credential and never accepts user-chosen resource IDs as proof of rights.
- **Credentials:** provider API key only in Python environment; service-to-service key in both process environments (not source). Never log raw prompts, recordings, question keys, response bodies, tokens or local file paths. Do not commit real lecture media or private student submissions.
- Review the model provider's privacy/data retention terms and obtain any required consent or instructor approval before transmitting real recordings, student answers or coursework. Use fictional demo fixtures for the first tests.
- Internal HTTP errors map to stable, safe Express API errors. A Python `200` response does **not** authorize Express to commit without validation. Include explicit timeout, payload and content-type ceilings, safe redacted logs, health/readiness and shutdown behavior.

## 4. Testing and ownership

| Proof | Owner | Reviewer |
| --- | --- | --- |
| Python /internal routes validate service key, schema, size/type, and error responses | B | A |
| Express calls stub Python over HTTP, receives and validates Conversion | B | Database |
| Express calls stub Python over HTTP and persists **only ten valid** source-grounded Quiz candidates | C + B | Database + Frontend |
| Safe public Quiz preview has no answer key / internal endpoint URL | C | Frontend |
| Submit uses persisted snapshot to deterministically grade exactly once; AI outage does not change grade | C | Database |
| Auth / course / cross-user guard on all public routes | A + affected API owner | Frontend |
| Missing Python process, timeout, invalid JSON, invalid option key, 9/10/11 question counts, upload failure | A/B/C respective paths | Other Backend |

Existing `client/tests` are Demo regression only, **not** proof of this integration.

## 5. Decision register — confirmed vs open

**Chosen:** Node/Express public app server → **private Python HTTP AI sidecar** → Express output validation/persistence → React response. **Not chosen:** browser-direct model calls, separate public Python backend or Python-to-Atlas persistence.

**Review before affected code:** Python framework/dependencies (FastAPI recommended), private port and internal service key rotation; exact wire DTOs in [protocol](PYTHON_HTTP_PROTOCOL.md); file size/processing timeout/trigger; bounded synchronous versus explicit queued architecture; model provider/cost/data privacy; when and how optional AI feedback is retrieved. All remain proposal details, not claims of running code. Record approved deltas to older [AD-03](../../API_CONTRACT.md) and [AD-04](../../IMPLEMENTATION_PLAN.md) without removing their historical baseline.
