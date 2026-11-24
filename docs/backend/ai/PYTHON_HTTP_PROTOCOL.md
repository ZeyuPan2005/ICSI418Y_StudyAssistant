# Private HTTP protocol — Express ↔ Python AI service

**Status:** implementation handoff **proposal v0.2**. **Architecture fixed:** private HTTP call from Express to a separate Python process; wire fields, framework, limits and operational parameters require A/B/C sign-off. This is **not** a browser-facing API. Backend B implements this protocol; Backend A supplies shared secure configuration; Backend C calls the Express-side AI client functions.

## Local processes and network

| Process | Role | Suggested local binding |
| --- | --- | --- |
| React/Vite | public UI dev server / proxy | existing `localhost:5173` |
| Node/Express | only browser-facing authenticated application API | proposed `localhost:9000`; route prefix `/api` |
| Python AI service | **private** conversion, quiz and feedback compute | proposed `127.0.0.1:8001`, no public port exposure |
| Atlas | shared persistent data | Database team controlled nonproduction project |

`9000` and `8001` are provisional development ports, **not** deployed endpoints or implemented services. Vite proxies `/api` → Express, and Express calls Python via `AI_INTERNAL_BASE_URL` such as `http://127.0.0.1:8001`. Python must not be exposed via Vite proxy, CORS wildcard, browser JS or a public tunnel. Cross-host deployment requires private TLS/network and service-to-service authentication review.

**Recommended transport:** FastAPI + Uvicorn in a dedicated Python environment (version/packages frozen before code), with `httpx` or equivalent server-side HTTP client in Express; libraries not yet installed/committed. Express owns `AI_INTERNAL_BASE_URL`, `AI_INTERNAL_SHARED_KEY` and outbound request timeout config. Python owns the matching service key and model provider keys. Missing keys fail startup, never silently disable internal auth.

## Shared headers and failure envelope

All `POST /internal/v1/*` require:
- `X-Internal-Service-Key: <injected-secret>` (server-to-server only; verify securely; rotate through protected deployment config)
- `X-Request-Id: <opaque-server-generated-correlation-id>` (non-auth identity; never use as operation id)
- `Content-Type: application/json` for quiz/feedback; `multipart/form-data` for conversion (boundary set by HTTP client)

No user session cookies, student ID, Mongo credentials, file system path, API model key or arbitrary Authorization header forwarded to Python. Validate method/content type, input/output sizes, request schema and headers on **both ends**. Restrict Python binding to loopback even with key authentication.

**Successful JSON response convention (proposed):** `{"data":{...},"requestId":"..."}` with stable structures below. **Internal error convention:** `{"error":{"code":"AI_INVALID_INPUT","message":"Short safe diagnostic"},"requestId":"..."}`. Error messages must never expose prompt, model raw output, secrets or filesystem paths.

| Status | Internal code | Meaning | Express handling |
| --- | --- | --- | --- |
| 401 | INTERNAL_UNAUTHORIZED | Missing/invalid service-to-service key | Fail closed; report safe internal integration error |
| 400/422 | AI_INVALID_INPUT | Request malformed, unsupported type, oversized text or invalid metadata | No write of generated resource; safe 422/400 mapping |
| 413/415 | FILE_TOO_LARGE / UNSUPPORTED_FILE_TYPE | Python rejects bounded uploaded bytes | No conversion success; valid stored upload may remain |
| 422 | AI_INVALID_OUTPUT | Model responded but normalized DTO fails validation | Do not persist partial Quiz or mark conversion ready |
| 502 | AI_PROVIDER_ERROR | Provider or model computation failed | Public API returns safe transient failure |
| 503 | AI_PROVIDER_UNAVAILABLE | Model/config unavailable | Public API signals unavailable, without credentials |
| 504 | AI_PROVIDER_TIMEOUT | Bounded model operation exceeded deadline | Express reconciles current resource/operation; never assume a write succeeded |

**GET `/internal/health`** may report service readiness without model secrets, bound to loopback and appropriately limited; it must not exercise paid model calls on every probe. No public docs/OpenAPI UI or auto-generated endpoint should be exposed outside loopback.

## POST /internal/v1/convert

**Request: multipart/form-data**

- `file`: raw PDF/PPTX/MP3/WAV bytes, with bounded safe filename and MIME hint. Express reads authorized server-owned bytes, not the browser path.
- `metadata`: JSON string form field, e.g. `{"materialId":"material-1","filename":"lecture.pdf","mimeType":"application/pdf","languageHint":"en"}`. `materialId` is **correlation only**, not a storage target or authorization proof.

**Response 200:**
```json
{
  "data": {
    "language": "en",
    "plainText": "Lecture content...",
    "sections": [{"sectionId":"s1","title":"Topic","text":"Content in source"}],
    "warnings": []
  },
  "requestId": "req-1"
}
```

Python reads no Atlas record and writes no Material state. Express validates, stores ConvertedContent, and records conversion success/failed status. Processing trigger, max bytes/seconds and async design are **still open**; do not claim all lecture audio lengths are supported.

## POST /internal/v1/generate-quiz

**Request: application/json**

```json
{
  "materialId": "material-1",
  "courseId": "offering-1",
  "topicIds": ["topic-1"],
  "questionCount": 10,
  "content": {
    "language": "en",
    "plainText": "Functional requirements describe observable behaviors...",
    "sections": [{"sectionId":"s1","title":"Requirements","text":"Functional requirements..."}],
    "warnings": []
  }
}
```

These IDs are informational; **Express has already authorized Course and Material**. Python must not fetch course data from DB or select new resources. Output has **ten** candidates; example shows **one** for readability:

```json
{
  "data": {
    "questions": [
      {
        "prompt": "What is a functional requirement?",
        "options": [
          {"optionId":"a","text":"A behavior a system provides"},
          {"optionId":"b","text":"A latency target"}
        ],
        "correctOptionId": "a",
        "explanation": "It describes what the system does.",
        "topicIds": ["topic-1"],
        "sourceRefs": [{"sectionId":"s1","quote":"Functional requirements describe observable behaviors"}]
      }
    ]
  },
  "requestId": "req-2"
}
```

Express independently checks `questionCount=10`, distinctness, selected Topics, valid options and correct answer keys. `sourceRefs` must identify actual source sections; model-origin quote matching is an **aid**, not verified factual grounding. Assign protected snapshot IDs, persist one Quiz, return **only** safe preview fields to React. Do **not** return `correctOptionId` or full private rationale in public preview.

## POST /internal/v1/generate-feedback

**Request: application/json** from an **already persisted and graded Result**, with only minimum needed content:

```json
{
  "resultId": "result-1",
  "score": 8,
  "total": 10,
  "missed": [
    {"snapshotQuestionId":"q3","prompt":"...","chosenOptionText":"...","correctOptionText":"...","topicIds":["topic-1"]}
  ]
}
```

**Response 200:**
```json
{
  "data": {
    "summary": "Review topic terminology.",
    "perQuestion": [
      {"snapshotQuestionId":"q3","explanation":"The correct option refers to system behavior."}
    ],
    "suggestions": ["Revisit lecture section s1."]
  },
  "requestId": "req-3"
}
```

Python cannot grade, change stored Answer/Result/score or write directly to MongoDB. Express validates returned text lengths and question IDs, then persists an independent versioned explanation/status record **if** feedback storage is approved. Provider failure leaves original Result unchanged and accessible with deterministic correctness feedback. The HTTP request/retrieval lifecycle for optional AI explanation remains to be chosen; don't silently add unsupported background processing.

## Contract tests to complete before real model calls

1. Python returns valid JSON and rejects missing/invalid service key, malformed multipart, oversize, unknown input fields, invalid formats, and bad content type.
2. Express with **stub Python HTTP server** can exercise all three routes, safely maps 4xx/5xx/timeout/invalid JSON, and never leaks private key/raw AI response in public errors.
3. Generated Quiz count 9/10/11, duplicate question, correctOptionId not in options, foreign Topics, unrelated source quote ⇒ invalid output blocks database writes.
4. Submit grades from **frozen stored answer keys** even if Python is down; duplicate submit cannot create two Results; bad or late AI explanation cannot mutate Result.
5. Restart/refresh: accepted Material bytes and metadata persist; converted content/Quiz snapshots/Results remain authorized and consistent.

**Pending team freeze:** payload byte limits, maximum audio duration, timeout thresholds, sync vs queue, provider selection, cost/privacy, model responses to unknown source content, auth key management, exact status mappings and versioning.
