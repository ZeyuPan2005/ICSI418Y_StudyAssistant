# AD-03 API Contract

| Document control | Value |
| --- | --- |
| Version | 1.0 |
| Date | 2026-11-18 |
| Status | **Prepared for Review** |
| Scope | Phase 1 HTTP contracts; documentation/design only, no API implementation |
| Foundation | [Requirements Baseline v1.2](REQUIREMENTS_BASELINE.md), [traceability](REQUIREMENTS_TRACEABILITY.md), [AD-01](COMPONENT_ARCHITECTURE.md), [AD-02](DATA_MODEL.md), [architecture plan](ARCHITECTURE_PLAN.md), [README](../README.md) |
| Repository reference | `main`, `8fbb43e` (AD-01/AD-02 documentation commit) |
| Authority | Task 6 explicitly confirms AD03-D01 through AD03-D10 below. Endpoint names, DTOs, headers and status/error selections are proposals for review. No formal team approval or implementation completion is asserted. |

## 1. Confirmed decisions and review boundary

**Confirmed** means explicitly supplied behavior. **Proposed** means a concrete contract
recommendation awaiting review. **Open** means a policy/mechanism still to resolve.
These subsequent decisions refine older documents' open/proposed statements; they do not
rewrite their historical decision registers. Original FR/UC/US/NFR meanings are preserved;
the existing [M3 evolution audit](DATA_MODEL.md#2-milestone-consistency-and-design-evolution)
remains the source for the Concept/Topic and retake changes. No new milestone audit is claimed.

| ID | Status | Confirmed decision and limits |
| --- | --- | --- |
| AD03-D01 | Confirmed | Server-side Session + HttpOnly Cookie: opaque cookie session identifier; backend resolves User identity. JWT Bearer Tokens are not the primary Phase 1 strategy. Store, lifetime and library remain open. |
| AD03-D02 | Confirmed | Trusted Seed / Provisioning Script: idempotent trusted provisioning of Courses, Topics, Teacher accounts, memberships and bank content; no production credentials in source. Public Students initially have no course access until assigned. No Teacher self-registration, role-escalation, self-enrollment endpoint or enrollment-management UI. |
| AD03-D03 | Confirmed | Synchronous Confirmed Upload: success only after actual protected local bytes and associated Atlas metadata persist. Require at least one valid predefined course Topic; storage and generation eligibility differ. Staging/recovery remain proposals; timeout/lost response does not prove failure. |
| AD03-D04 | Confirmed | Operation-based Idempotent Generation: new intentional operation uses a new identity; replay of the same operation returns the same created Quiz. Identity is scoped to authenticated Student, Course, inputs and request identity. Conflicting reuse never creates/overwrites a Quiz. Header, fingerprint, lifetime and persistence remain proposed. |
| AD03-D05 | Confirmed | Start-time Attempt Creation: Generate persists complete immutable Quiz snapshots; preview creates no Attempt; Start creates the sole Draft. Repeated Start returns existing Draft; submitted Attempt never reopens. Same rule for regular and practice. |
| AD03-D06 | Confirmed | Regular Result Only: practice source must be a submitted Regular Quiz Result, never a Practice Result. Independent practice Quiz, Attempt and submitted Result preserve all original records. Practice has 1-10 distinct missed-topic questions, excluding every source Quiz question by stable identity. Repeated-practice and cross-practice exclusions remain open. |
| AD03-D07 | Confirmed | Course-scoped Calendar Timezone: trusted configured IANA timezone per Course Offering; backend determines course-local today. YYYY-MM-DD dates; past hidden from Students; day 0 through +7 Upcoming, +8 onward visible/unmarked; Teachers manage past dates. Alerts/Upcoming are derived. America/New_York is only an example, not a global default. |
| AD03-D08 | Confirmed | Revision-based Draft Conflict Detection: conditional Draft saves require current expected revision; stale writes never overwrite newer answers. Recover acknowledged drafts while retaining unsynchronized client choices; no silent last-write-wins. Final Submit carries complete answers to avoid an autosave race. Autosave interval, recovery storage and conflict UI remain proposed. |
| AD03-D09 | Confirmed | Same-origin API + CSRF Token + Origin Validation: same-origin requests, optional development proxy, HttpOnly sessions, secure cookie configuration, session-bound CSRF and Origin checks on relevant writes including auth. Cookie/token lifecycle requires review; HttpOnly/SameSite alone does not prevent CSRF or XSS. |
| AD03-D10 | Confirmed | Unified Error Envelope + Operation-aware Retry: distinguish validation, authentication, authorization, state/business conflict, definite persistence failure and unknown outcome. Retry respects identity and persisted state, preventing duplicate materials/Quizzes/Attempts/Results. Timeout/database error is not proof of rollback; exact codes/statuses/intervals remain proposals. |

## 2. API conventions and DTO rules (Proposed)

Use REST-style HTTP/JSON with `/api` prefix, multipart upload and same-origin cookie
transport. All paths below are proposed. IDs are opaque strings for specific offerings,
never authorization credentials or course-code aliases. Reject malformed/unknown writable
fields; never accept client role, owner, grade or persistence state as trusted input.
Validate whole Topic sets against the offering, not just their individually valid IDs.

Propose JSON success as `{"data": ...}`; lists also carry `page: {nextCursor}`. All
errors use section 10. Dates use YYYY-MM-DD; event timestamps use UTC instants. JSON body
sizes, field lengths, pagination limits/cursors and filter allowlists require review.
Absent cursor means first page; null nextCursor means no next page. Pagination must apply
authorization before returning items or counts; filters can only narrow allowed data.
GET endpoints do not mutate domain resources: no generation, Attempt creation or grading.
CSRF bootstrap may initialize session-bound security context without creating or changing
Course, material, Quiz, Attempt, Result or Deadline data.

DTOs are explicit allowlists, independent of private Atlas documents. File delivery is
protected streaming with reviewed Content-Type/Content-Disposition, safe filename and
no public storage path. Propose private/no-store caching for session, drafts and answer
responses; reviewed cache policy must prevent cross-user reuse. No credentials or raw
errors enter responses/log correlation. Exactly ten distinct regular items, 1-10 practice
items, frozen snapshots, course isolation and history preservation remain invariants.
Phase 1 uses a predefined Question Bank with manual Topics; no semantic AI generation.

## 3. Complete API inventory (Proposed)

S = authenticated Student; T = authenticated Teacher; M = active trusted membership of
loaded resource's Course; O = Student owner. All writes require section 4 protections.
Public auth writes still need anonymous-session CSRF/Origin validation. Main DTO names
below are defined in section 5. Successful codes are proposals, not additional confirmations.

| Method | Proposed path | Actor / authorization | Purpose | Request -> response | FR / original UC |
| --- | --- | --- | --- | --- | --- |
| POST | `/api/auth/register` | Public | Register Student with no memberships | Registration -> 201 User; proposed no automatic login | FR-01; supports UC-01–05 |
| POST | `/api/auth/login` | Public | Establish server session | Login -> 200 User | FR-01; supports UC-01–05 |
| GET | `/api/auth/me` | Authenticated | Session recovery/identity | None -> 200 User | FR-01; supports UC-01–05 |
| POST | `/api/auth/logout` | Session/anonymous CSRF context | Revoke session and clear cookie | Empty -> 204 | FR-01; supports UC-01–05 |
| GET | `/api/auth/csrf` | Public/session context | Obtain session-bound CSRF token | None -> 200 Csrf | FR-01; supports UC-01–05 |
| GET | `/api/courses` | S/T | List assigned offerings only | Page -> 200 Course list | FR-01; UC-01–05 |
| GET | `/api/courses/:courseId` | S/T + M | Offering/calendar context | None -> 200 Course | FR-01/06; UC-01–05 |
| GET | `/api/courses/:courseId/topics` | S/T + M | Upload Topic catalog | Page -> 200 Topic list | FR-02/03; UC-01/02 |
| GET | `/api/courses/:courseId/materials` | S/T + M | Course material listing | Page -> 200 Material list | FR-02; UC-01 |
| POST | `/api/courses/:courseId/materials` | S/T + M | Synchronously store upload | Multipart + upload key -> 201 Material (200 replay) | FR-02; UC-01 |
| GET | `/api/courses/:courseId/materials/:materialId` | S/T + M; matching course | Storage/eligibility details | None -> 200 Material | FR-02/03; UC-01/02 |
| GET | `/api/courses/:courseId/materials/:materialId/file` | S/T + M; matching course | Authorized file retrieval | None -> 200 protected bytes | FR-02; UC-01 |
| GET | `/api/courses/:courseId/material-upload-operations/:operationId` | S/T + M + operation owner | Recover upload outcome | None -> 200 UploadOutcome | FR-02; UC-01 |
| POST | `/api/courses/:courseId/materials/:materialId/quizzes` | S + M; course match | New/replayed regular Quiz | Empty + generation key -> 201 Quiz (200 replay) | FR-03; UC-02 |
| GET | `/api/quizzes/:quizId` | S + M + O | Safe preview/current lifecycle | None -> 200 Quiz | FR-03/04/05; UC-02/03/04 |
| GET | `/api/me/quizzes` | S; each item's M + O | Own Quiz index | Page/course filter -> 200 QuizSummary list | FR-03/04/05; UC-02/03/04 |
| POST | `/api/quizzes/:quizId/attempts` | S + M + O | Start or recover sole Draft | Empty -> 201 Attempt (200 existing Draft) | FR-04/05; UC-03/04 |
| GET | `/api/attempts/:attemptId` | S + M + O | Recover own Draft/submitted state | None -> 200 Attempt | FR-04; UC-03 |
| PUT | `/api/attempts/:attemptId/draft` | S + M + O; Draft | Replace saved draft answers conditionally | DraftWrite -> 200 Attempt | FR-04; UC-03 |
| POST | `/api/attempts/:attemptId/submit` | S + M + O | Finalize once/recover result | Submit -> 200 Result | FR-04; UC-03 |
| GET | `/api/attempts/:attemptId/result` | S + M + O | Reconcile uncertain submission | None -> 200 Result or state error | FR-04; UC-03 |
| GET | `/api/results/:resultId` | S + M + O | Own historical feedback | None -> 200 Result | FR-04/05; UC-03/04 |
| GET | `/api/me/results` | S; each item's M + O | Own Result index | Page/course filter -> 200 ResultSummary list | FR-04/05; UC-03/04 |
| POST | `/api/results/:resultId/practice-quizzes` | S + M + O; Regular submitted source | Generate/replay practice | Empty + generation key -> 201 Quiz (200 replay) | FR-05; UC-04 |
| GET | `/api/courses/:courseId/deadlines` | S/T + M | Student visible dates or Teacher management | Page -> 200 Deadline list/calendar | FR-06; UC-05 |
| POST | `/api/courses/:courseId/deadlines` | T + M | Publish valid date | DeadlineWrite -> 201 Deadline | FR-06; UC-05 |
| PATCH | `/api/courses/:courseId/deadlines/:deadlineId` | T + M; course match | Edit current course entry | Partial DeadlineWrite -> 200 Deadline | FR-06; UC-05 |
| DELETE | `/api/courses/:courseId/deadlines/:deadlineId` | T + M; course match | Remove entry from views | None -> 204 | FR-06; UC-05 |
| GET | `/api/courses/:courseId/results` | T + M | Submitted results only | Page -> 200 TeacherResultSummary list | FR-07; US-07, no sixth UC |
| GET | `/api/courses/:courseId/results/:resultId` | T + M; course match | Read submitted answers/score | None -> 200 TeacherResult | FR-07; US-07, no sixth UC |

All 30 candidates are retained for required capabilities. The Attempt-result lookup resolves
unknown completion when no Result ID is known; Result-ID retrieval serves historical links.
Teacher course routes reuse Result serialization under a different policy, not a second
Result store. `/me` indexes serve dashboard navigation. Upload operation lookup is recovery
of a synchronous write, not a requirement for a background job service. No public Course,
Topic, Question, role or enrollment CRUD is introduced.

## 4. Authentication and authorization contract

AD03-D01/D02/D09 confirm identity/provisioning/transport direction; these protocol details
are proposed. Fetch `/api/auth/csrf` to establish an anonymous server-side CSRF context and
receive a token in JSON. Submit it in proposed `X-CSRF-Token` on register/login/logout and
all other POST/PUT/PATCH/DELETE operations, including multipart. Backend validates the
session-bound token and an exact allowed same-origin Origin. Define reviewed rejection
for absent/untrusted Origin; do not silently skip validation. Browser-origin configuration
and development proxy must preserve these checks, not enable wildcard credentialed CORS.

Login verifies securely hashed credentials, rotates the opaque session ID and invalidates
the anonymous context; refetch CSRF after login. `GET /auth/me` returns only safe identity;
expired sessions return 401, causing reauthentication and CSRF refresh before writes.
Logout invalidates the server session, clears the matching cookie and resets CSRF context;
a retried logout may return 204 after validating the current anonymous context. It does
not delete saved drafts or historical records. Login errors should not disclose account
existence. Registration proposes rejecting role/course/membership fields rather than
silently accepting them; trusted scripts alone assign courses/Teacher privileges.

The session ID travels only in an HttpOnly cookie, never a response JSON field, URL or
browser local-storage token. Propose Secure under HTTPS, SameSite=Lax, Path=/ and no Domain;
exact cookie name, expiry, deployment/dev exceptions, store and rotation rules need review.
CSRF tokens are intentionally browser-readable; they are not session IDs. A secure cookie
configuration, CSRF token and Origin check work together. HttpOnly/SameSite alone is not
CSRF or XSS prevention. No JWT Bearer primary flow is specified.

| Resource/action | Student | Teacher | Unauthenticated |
| --- | --- | --- | --- |
| Course/Topic/material/file reads; upload | Assigned offering only | Assigned offering only | Denied |
| Generate, preview, Start, draft, submit | Assigned offering + own Quiz/Attempt | Denied | Denied |
| Student Result/practice APIs | Assigned offering + own Result; practice only Regular source | Denied; use Teacher read routes | Denied |
| Course submitted results | No peer access | Assigned offering only; no draft access/result mutation | Denied |
| Deadline list | Assigned; today/future | Assigned; past/current/future | Denied |
| Deadline create/edit/delete | Denied | Assigned offering only | Denied |
| Trusted provisioning | No public access | No public access | No public access |

Resolve membership and role from the backend on every relevant request, including replay
and direct ID reads. Validate URL course against loaded resource course, even for identical
codes across years/terms. Proposed policy: 401 for missing/expired authentication; 403 for
known disallowed role/action; 404 for nonexistent or deliberately concealed foreign-owned/
unassigned resource. Avoid revealing whether another Student's Result/operation exists.
CSRF rejection may precede auth failure on writes. Lists filter before paging; a client
query cannot opt into Teacher visibility. Reauthentication/revocation never bypasses current
membership checks for history. Never disclose hashes, internal session IDs, credentials,
filesystem paths or raw database errors in DTOs.

## 5. Proposed request and response DTO examples

All IDs/dates/questions below are illustrative placeholders. Request/response pairs show
JSON bodies, not private documents. Empty-body endpoints accept no business fields. Page
examples omit additional pages, not required security checks. No passwords/tokens shown
below are actual credentials. `expectedRevision` is a nonnegative integer; answer maps use
snapshotQuestionId keys and stable option IDs. Unknown answer/option IDs are rejected.

### Identity and course context

Registration: POST `/api/auth/register` accepts only displayName, email and password;
propose 201 User without creating a logged-in session. Login is explicit afterward.

```json
{"displayName":"Example Student","email":"student@example.invalid","password":"<user-supplied-password>"}
```

Login: POST `/api/auth/login`, with current CSRF/Origin and cookie context:

```json
{"email":"student@example.invalid","password":"<user-supplied-password>"}
```

Login 200 (Set-Cookie is transport only); `/api/auth/me` has the same User shape:

```json
{"data":{"userId":"user-1","displayName":"Example Student","role":"Student"}}
```

CSRF acquisition 200; token is bound to the current anonymous/authenticated session:

```json
{"data":{"csrfToken":"<session-bound-csrf-token>"}}
```

Course list 200; a newly registered unassigned Student receives `items: []`:

```json
{"data":{"items":[{"courseId":"course-fall","code":"ICSI418Y","name":"Software Engineering","academicYear":"2026","term":"Fall","calendarTimezone":"America/New_York","today":"2026-11-18"}]},"page":{"nextCursor":null}}
```

The zone is an illustrative trusted UAlbany course configuration. Course detail returns
that item under data. Topic list 200:

```json
{"data":{"items":[{"topicId":"topic-1","courseId":"course-fall","name":"Requirements"}]},"page":{"nextCursor":null}}
```

### Material upload and details

POST `/api/courses/course-fall/materials` uses multipart, proposed `Upload-Operation-Id`
header, CSRF header, Origin and cookie. Proposed parts: `file` = actual nonempty supported
bytes; `topicIds` = JSON-encoded nonempty unique ID array, e.g. `["topic-1"]`. Browser sets
multipart boundary. Validate actual file policy, all Topics, size and type server-side.
No client storageState, owner or path field is accepted.

201 after both bytes and metadata commit; detail GET/200 uses the same Material DTO:

```json
{"data":{"materialId":"material-1","courseId":"course-fall","uploaderId":"user-1","filename":"lecture.pdf","format":"PDF","byteSize":1024,"topicIds":["topic-1"],"storageState":"stored","storedAt":"2026-11-18T15:00:00Z","quizEligibility":{"state":"insufficient","requiredCount":10,"eligibleDistinctCount":5,"checkedAt":"2026-11-18T15:00:00Z"},"fileUrl":"/api/courses/course-fall/materials/material-1/file"}}
```

Eligibility is an advisory current bank check, not semantic processing or an upload
success precondition. Propose states `eligible`, `insufficient`, `unknown`; when not checked,
use unknown and omit counts/check time. Never fail an otherwise completed upload merely
because this advisory check is unavailable. No public staging record is a stored material.
Material list uses `data.items` of summary fields without private storage keys.

Upload-operation GET/200 recovery example:

```json
{"data":{"operationId":"upload-op-1","state":"succeeded","materialId":"material-1"}}
```

Proposed other outcome states: inProgress, failed, unknown; failed has the same safe error
code/retry information defined in section 10, and unknown never asserts no material exists.
Lookup returning 404 does not alone authorize a fresh identity after an uncertain upload;
operation retention rules must first guarantee safe reconciliation.

### Regular generation, preview and Start

POST `/api/courses/course-fall/materials/material-1/quizzes` sends empty JSON `{}` with
proposed `Generation-Operation-Id: generation-op-1`. Backend resolves current material Topics;
clients cannot send item IDs, grading keys or a desired regular count.

**Abbreviated Quiz DTO (201 generation or 200 preview):** `items` below shows only one of
exactly ten persisted regular items. Omitted items are intentionally absent from this
illustration; this is not a complete valid ten-question payload.

```json
{"data":{"quizId":"quiz-1","courseId":"course-fall","materialId":"material-1","kind":"regular","sourceResultId":null,"questionCount":10,"items":[{"snapshotQuestionId":"item-1","prompt":"Which statement describes a requirement?","options":[{"optionId":"option-a","text":"An expected system behavior"},{"optionId":"option-b","text":"A random implementation detail"}],"topics":[{"topicId":"topic-1","name":"Requirements"}]}],"attemptId":null,"resultId":null,"contentSource":"predefined-question-bank"}}
```

Preview never creates Attempt. After Start/submit, preview can expose the authorized
Attempt/Result IDs but retains the same safe question projection. `/api/me/quizzes`
returns paged QuizSummary items (IDs, course, kind, questionCount, createdAt, attemptId,
state and resultId), not grading keys or another Student's data.

POST `/api/quizzes/quiz-1/attempts` body `{}`; first success 201, repeated Draft Start 200:

```json
{"data":{"attemptId":"attempt-1","quizId":"quiz-1","state":"draft","revision":0,"answers":{},"resultId":null}}
```

### Draft, submit and Result

PUT `/api/attempts/attempt-1/draft`: complete replacement of the saved draft map; omitted
answers are cleared only on a successful authorized current-revision write. Partial answer
sets are valid drafts, not valid final submissions. Empty map deliberately clears draft.

```json
{"expectedRevision":0,"answers":{"item-1":"option-a"}}
```

200 save acknowledgement; GET `/api/attempts/attempt-1` returns the same Attempt shape:

```json
{"data":{"attemptId":"attempt-1","quizId":"quiz-1","state":"draft","revision":1,"answers":{"item-1":"option-a"},"lastSavedAt":"2026-11-18T15:01:00Z","resultId":null}}
```

POST `/api/attempts/attempt-1/submit` carries expected revision and **complete** answer set.
The following example is complete for a separately generated one-item practice Quiz,
`practice-quiz-1` / `practice-attempt-1`, and is sent to
`/api/attempts/practice-attempt-1/submit`. A regular submission must include all ten items.

```json
{"expectedRevision":1,"answers":{"practice-item-1":"option-a"}}
```

200 submit Result example (also GET `/api/results/practice-result-1` or
`/api/attempts/practice-attempt-1/result`):

```json
{"data":{"resultId":"practice-result-1","quizId":"practice-quiz-1","attemptId":"practice-attempt-1","courseId":"course-fall","kind":"practice","sourceResultId":"regular-result-1","submittedAt":"2026-11-18T15:05:00Z","score":1,"total":1,"missedTopicIds":[],"feedback":[{"snapshotQuestionId":"practice-item-1","prompt":"What should validation check?","options":[{"optionId":"option-a","text":"The complete association"},{"optionId":"option-b","text":"Only a display label"}],"chosenOptionId":"option-a","correctOptionId":"option-a","correct":true,"topics":[{"topicId":"topic-1","name":"Requirements"}]}]}}
```

Regular Result uses the same shape with kind regular, sourceResultId null, total 10 and
all ten feedback items. ResultSummary list returns resultId, quizId, attemptId, courseId,
kind, sourceResultId, score, total and submittedAt; full answers belong in authorized detail.
Submitted Attempt GET returns final answers/revision, state submitted, submittedAt and
resultId; it never becomes editable. Missing Result for a Draft is a state error, not a
synthetic zero grade. Immutable feedback comes from preserved snapshots, not the live bank.

### Targeted practice

POST `/api/results/regular-result-1/practice-quizzes`, body `{}`, with a new generation
operation identity. Source must be owned, submitted, Regular and have missed Topics.
201 response with a complete one-item practice set:

```json
{"data":{"quizId":"practice-quiz-1","courseId":"course-fall","materialId":"material-1","kind":"practice","sourceResultId":"regular-result-1","questionCount":1,"items":[{"snapshotQuestionId":"practice-item-1","prompt":"What should validation check?","options":[{"optionId":"option-a","text":"The complete association"},{"optionId":"option-b","text":"Only a display label"}],"topics":[{"topicId":"topic-1","name":"Requirements"}]}],"attemptId":null,"resultId":null,"contentSource":"predefined-question-bank"}}
```

This one-item practice example is a full valid item set. Its draft/answering uses its own
Attempt, then its own Result shown above. A Practice Result source request is rejected.

### Deadlines and Teacher submitted results

POST `/api/courses/course-fall/deadlines`:

```json
{"title":"Requirements review","type":"Homework","dueDate":"2026-11-25"}
```

PATCH `/api/courses/course-fall/deadlines/deadline-1`, at least one allowed field:

```json
{"dueDate":"2026-11-26"}
```

Proposed 201 create / 200 update Deadline detail includes deadlineId, courseId, title, type,
dueDate and createdByUserId. Student list example **before** that update, on day +7:

```json
{"data":{"courseId":"course-fall","calendarTimezone":"America/New_York","today":"2026-11-18","items":[{"deadlineId":"deadline-1","courseId":"course-fall","title":"Requirements review","type":"Homework","dueDate":"2026-11-25","upcoming":true}]},"page":{"nextCursor":null}}
```

After the update the item is day +8, visible with upcoming false. Teacher list includes
past items as management data. Do not accept upcoming, author or course mutation in writes.
Partial PATCH validates the merged title/type/date before saving. Concurrent Teacher edit
preconditions and delete replay/retention policy remain review items.

Teacher GET `/api/courses/course-fall/results` (list example):

```json
{"data":{"items":[{"resultId":"regular-result-1","student":{"userId":"user-1","displayName":"Example Student"},"quizId":"quiz-1","kind":"regular","score":9,"total":10,"submittedAt":"2026-11-18T15:03:00Z"}]},"page":{"nextCursor":null}}
```

Teacher detail `/api/courses/course-fall/results/regular-result-1` reuses full Result DTO
plus that minimal student projection. Regular feedback includes all ten saved answer rows;
no draft answers or account email/hash/session data are exposed. Submitted practice Results
are also reviewable; practice-source restrictions do not hide submitted practice history.
Teachers can read, never edit/regrade Results through these routes.

## 6. Quiz snapshot security and lifecycle

Generate -> Preview -> Start -> Draft Save -> Submit -> Result applies equally to regular
and practice. Generate commits a complete immutable Quiz, **zero Attempts and zero Results**.
Preview is read-only and exposes no correctOptionId, grading key, unreleased explanation,
private bank metadata or other Students' answers/results. Keep private grading snapshots
out of generic serializers, list DTOs and error details. Backend alone scores from the
preserved Quiz snapshots. Editing/retiring bank content never changes historical meaning.

Start creates at most one Attempt. Concurrent Start resolves the same Draft; a submitted
Attempt returns proposed 409 ALREADY_SUBMITTED with its authorized result link, not a new
Draft. A Draft may have zero answers, must have zero final Results, and can accept incomplete
maps. Successful submission requires every required item answered and produces **exactly
one immutable Result**. Missing answers return field/item errors and preserve selections.
A new deliberate learning attempt needs another Quiz, preserving all earlier records.

AD03-D08 confirms revision checking; propose a conditional draft write matching ID, owner,
course, Draft state and expectedRevision, then increment revision. Stale requests return
409 ATTEMPT_REVISION_CONFLICT with currentRevision and recovery URL. Client retains unsynced
choices, fetches current draft and presents reviewed conflict resolution; no automatic
last-write-wins. A retried save with an old revision may conflict even when prior save
succeeded; recover before writing again. PUT alone does not make revision increments replay-safe.

Final Submit sends full answers plus expectedRevision. An autosave/submit race permits only
one matching revision transition; losing write reconciles current state. If already submitted,
identical final-answer replay returns the original Result even with old revision; different
answers return 409 ALREADY_SUBMITTED with original result link and never change the grade.
Do not reject a committed replay solely for stale revision before checking finalized state.

AD-02 proposes conditional updates, unique Attempt.quizId/Result.attemptId and an atomic
transaction for final Attempt+Result. Those mechanisms are still proposals, not selected or
tested implementations. Definite transaction abort retains Draft with no final Result;
concurrent submits yield one committed final outcome. Unknown commit/response requires
lookup by Attempt and Result reconciliation, not new IDs or a second grade. Do not expose
submitted state without its matching persisted Result. Driver/Atlas retry behavior and
membership-revocation races require implementation review. Client retains answers during
same-session disconnect, including unsent choices; server draft persistence alone cannot
satisfy NFR-06.

## 7. Upload and generation operation contracts

Operation headers/names, fingerprints and records below are **proposed**. AD03-D04 confirms
generation replay behavior; upload replay identity is a proposed means to satisfy AD03-D10
without duplicate materials. Keep upload and generation namespaces separate, including
regular versus practice context. Authenticate/authorize before exposing any operation outcome.
Propose client-created opaque upload/generation IDs, not session IDs or file names.

Bind upload identity to authenticated uploader, Course, canonical Topic set and verified file
identity; same file/name alone is insufficient. Verify content digest server-side rather
than trusting a supplied hash. Bind generation identity to authenticated Student, Course,
operation kind, material or source Regular Result, frozen canonical Topic/input context
and request fingerprint. Client cannot choose another actor's scope. Concurrent same-key
requests serialize/reconcile, never both create resources. An operation bound before a
material Topic edit must retain its original context on replay, not silently recompute it.

| Situation | Proposed upload behavior | Proposed generation behavior |
| --- | --- | --- |
| First successful write | 201 Material only after bytes plus metadata completion | 201 complete Quiz; no Attempt |
| Same identity, identical input | 200 same stored Material, no second file/material | 200 same created Quiz, no reselection or changed snapshots |
| Same identity, conflicting input | 409 IDEMPOTENCY_CONFLICT; no new write | 409 IDEMPOTENCY_CONFLICT; no overwrite/new Quiz |
| Same operation still executing | 409 OPERATION_IN_PROGRESS; recover status | 409 OPERATION_IN_PROGRESS; replay later with same identity |
| Completion unknown | 503 OUTCOME_UNKNOWN; query upload operation, retain identity | 503 OUTCOME_UNKNOWN; replay/reconcile same generation identity; once committed return same Quiz |
| Definite failure/no committed resource | Safe error with outcome notApplied only after verified reconciliation | Validation/bank failure creates no Quiz; definite persistence failure has no committed Quiz |
| Deliberate new operation | New identity denotes another upload, not automatic timeout recovery | New identity can create an independent Quiz under confirmed access/business rules |

Upload success is synchronous (AD03-D03), not 202 acceptance of background storage. The
status lookup recovers in-flight/unknown outcomes; it does not require a queue/worker/job
architecture. Pending/staged states and cleanup are private implementation proposals.
Atlas transactions cannot atomically include filesystem writes; both stores must be
associated before success. Never mark a stored material invalid merely for insufficient
questions. Missing/foreign Topics or invalid bytes cannot become valid ready material.

Do not automatically replace an identity after timeout, operation-record expiry or unknown
outcome. Lifetime/retention must preserve resource association or reject stale identities
without duplication. A missing operation record is not proof a write did not happen.
For generation, replay uses the original operation identity/header; no extra public status
endpoint is required. Definite rejected operations' retry eligibility, terminal-failure
caching, authentication interruptions and repeated-practice policy need review. Retry
interval/backoff is unspecified; no unbounded automatic retry is promised.

## 8. Targeted practice contract

Validate the source Result is owned, in an assigned offering, successfully submitted and
belongs to a **Regular** Quiz. Deny Practice Result sources with proposed 409
PRACTICE_SOURCE_NOT_REGULAR. Review of a Practice Result remains allowed. Derive missed
Topics from preserved source feedback, not mutable bank tags; the proposed multi-tag union
policy remains subject to review. Match course/missed Topics, deduplicate candidates and
exclude every originalQuestionId from the entire source Quiz, including correct answers.
Changing source bank revision or snapshot ID never bypasses exclusion.

A perfect source returns proposed 409 PRACTICE_NOT_NEEDED, no new records. Zero eligible
candidates after exclusions returns 409 NO_ELIGIBLE_PRACTICE, no new records. Positive pools
support successful 1-10 distinct items, never more than available; fewer than ten is not
itself a failure. Exact sizing and repeated new practice operations from one Regular Result,
including cross-practice exclusions, remain open: do not invent a confirmed repeat limit
or unlimited entitlement. Replaying an already successful practice operation must still
recover that same Quiz. Before implementation, resolve repeated new-operation policy.

The practice Quiz links to sourceResultId, previews without Attempt, starts its own sole
Draft, and on submission owns its own immutable Result. Neither creation nor completion
changes original Quiz/Attempt/answers/Result/score. Return-to-original navigation reads
preserved history. No partial Quiz on selection failure and no source mutation on errors.

## 9. Deadline and Teacher review contracts

Each offering has a trusted configured IANA calendarTimezone; backend supplies course-local
today in date-list DTOs. Missing/invalid course zone is a configuration failure, not a
silent browser/global timezone fallback. Validate actual YYYY-MM-DD calendar dates,
including leap years; compare calendar days in the course zone, not UTC midnight instants
or elapsed 24-hour durations. The exact configured zone is a provisioning input; the
per-offering policy is confirmed by AD03-D07. America/New_York in examples is not universal.

| Date relative to course-local today | Student visibility | Derived upcoming |
| --- | --- | --- |
| Past (day -1 or earlier) | Hidden | Not displayed |
| Today (day 0) | Visible | true |
| Day +1 through +7 inclusive | Visible | true |
| Day +8 onward | Visible | false |

Assigned Teachers can create/edit/delete valid Lecture/Homework dates, including past
entries. Students cannot write or reveal past entries by adding query filters. Both UI-01
and UI-08 use the same projection; recompute after edits/removal and local day rollover.
Upcoming/Alerts are derived values, never separate persistent entities. Paging/caches must
not preserve removed entries or obsolete badges. No external notifications are introduced.

Teacher result routes require global Teacher role and current membership of loaded Course.
List/detail return only submitted immutable scores and answer snapshots, including submitted
practice. Drafts are excluded; a forged course/result pair is denied/concealed. Do not
expose other offerings sharing the same code. C08 reads through C06 and cannot write or
regrade Results. Student private Result routes require their own ownership independently.

## 10. Unified error contract (Proposed)

One machine-readable error envelope for JSON routes and pre-stream file failures:

```json
{"error":{"code":"ATTEMPT_REVISION_CONFLICT","message":"Newer answers have been saved. Recover the current draft before saving again.","details":{"currentRevision":2,"recoveryUrl":"/api/attempts/attempt-1"},"retry":{"action":"reconcileDraft","outcome":"notApplied","reuseOperationIdentity":false}},"requestId":"request-example-1"}
```

Required proposed fields: error.code, safe message, retry.action, retry.outcome,
retry.reuseOperationIdentity and requestId. `details` is optional and allowlisted; it can
include safe field/item errors or authorized recovery links, never raw queries, stack
traces, paths, keys or foreign-owned data. requestId correlates logs, not permissions or
idempotency. Authentication failures omit account existence and credentials.

Proposed outcomes: notApplied = this rejected write made no changes, not a claim that all
previous retries failed; committed = original final resource exists; inProgress = known
ongoing operation; unknown = cannot determine completion; notApplicable = non-write error.
Actions: correctRequest, reauthenticate, stop, reconcileDraft, readResult, recoverUpload,
retrySameOperation, retrySameResource, waitThenRecover. Never interpret status alone as a
retry policy. CSRF context may need refresh before retry after session rotation/expiry.

| HTTP | Proposed code | Condition / outcome | Safe client action |
| --- | --- | --- | --- |
| 400 | INVALID_REQUEST | Malformed/invalid fields; notApplied | Correct request; preserve choices |
| 401 | UNAUTHENTICATED | Missing/expired identity; notApplied for denied write | Reauthenticate, refresh CSRF, recover previous outcome before resending |
| 403 | FORBIDDEN | Disallowed role/action; notApplied | Stop; do not retry privileges |
| 403 | CSRF_REJECTED | Invalid token or Origin; notApplied | Verify same-origin context; refresh token if legitimate; no bypass |
| 404 | NOT_FOUND | Missing or deliberately hidden resource | Stop; do not infer another user's object exists |
| 422 | INVALID_TOPIC_SELECTION | Empty/foreign/invalid complete Topic set; notApplied | Correct Topics within Course |
| 415 | UNSUPPORTED_FILE_TYPE | Byte/type policy rejection; notApplied as valid material | Select supported content |
| 413 | FILE_TOO_LARGE | Reviewed upload limit exceeded; notApplied as valid material | Reduce/select file; no numeric limit assumed |
| 409 | INSUFFICIENT_QUESTION_BANK | Fewer than ten distinct regular candidates; notApplied | Explain shortage; material remains stored; no blind retry |
| 409 | PRACTICE_NOT_NEEDED | Perfect source; notApplied | Show no weak Topics; no new records |
| 409 | NO_ELIGIBLE_PRACTICE | Zero candidates after exclusion; notApplied | Explain no available practice; preserve original |
| 409 | PRACTICE_SOURCE_NOT_REGULAR | Submitted Practice Result used as source; notApplied | Return to original Regular Result |
| 422 | INCOMPLETE_ANSWERS | Missing required snapshot answers; notApplied | Show safe missing item IDs; retain existing selections |
| 409 | ATTEMPT_REVISION_CONFLICT | Stale expected revision; notApplied | Fetch current Draft and reconcile unsynced choices |
| 409 | ALREADY_SUBMITTED | Start/save or conflicting final answers after finalization; committed | Read authorized existing Result; never reopen |
| 409 | RESULT_NOT_READY | Authorized Attempt still Draft; notApplied for lookup | Recover Draft; do not synthesize Result or resubmit blindly |
| 409 | IDEMPOTENCY_CONFLICT | Same operation identity/different inputs; notApplied for rejected replay | Recover existing context; new deliberate action requires new identity |
| 409 | OPERATION_IN_PROGRESS | Same identified operation executing; inProgress | Wait then recover same identity, no new operation |
| 429 | RATE_LIMITED | Rejected before write; notApplied only when guaranteed | Respect proposed Retry-After, recover prior requests first |
| 503 | STORAGE_UNAVAILABLE | Verified definite persistence failure; notApplied as valid committed resource | Reconcile/cleanup as required, retry same operation/resource only when allowed |
| 503 | OUTCOME_UNKNOWN | Write/commit may have succeeded; unknown | Upload lookup, generation same-key replay, or Attempt-result lookup; never use new identity |

Except confirmed business outcomes, every code/status and response field above is proposed.
File streaming interrupted after headers cannot switch to a JSON envelope; terminate the
stream, correlate safely, and let the authorized client retry the read. Unexpected server
faults use a safe generic error under the same envelope; if writes might have occurred,
classify unknown rather than assigning definite failure from an exception alone. A lost
network response has no readable envelope; client must conservatively recover the original
operation/resource. Error names do not prove database rollback or file compensation.

## 11. Requirements, components and data traceability

All acceptance/verifications below are proposed future checks, not executed backend tests.
Original [traceability](REQUIREMENTS_TRACEABILITY.md) retains all UC/US/UI IDs and conditions.

| FR / original use cases and stories | Contract coverage | AD-01 owners / AD-02 data | Acceptance |
| --- | --- | --- | --- |
| FR-01; all UC-01–05 / US-01–07 | Auth/session/CSRF, assigned courses, role+membership+ownership | C02, C09; User, Course, CourseMembership | AC-01, AC-11 |
| FR-02; UC-01 / US-01 | Multipart synchronous upload, status recovery, protected read | C03, C09, C10; LectureMaterial, Topic, Course, uploader User | AC-02, AC-03, AC-11 |
| FR-03; UC-02 / US-02 | Operation-scoped generation, safe preview, own Quiz index | C04/C05, C03, C09; Question, Topic, LectureMaterial, Quiz snapshots | AC-04, AC-05 |
| FR-04; UC-03 / US-03 | Start, Draft revision/recovery, complete Submit, Result recovery/detail | C06/C02/C09; Quiz, sole Attempt, exactly one submitted Result | AC-06, AC-11 |
| FR-05; UC-04 / US-04 | Regular-source practice, stable exclusions, independent lifecycle/history | C04/C05/C06/C09; source Result, new Quiz/Attempt/Result | AC-07, AC-08 |
| FR-06; UC-05 / US-05 and US-06 | Teacher Deadline writes, Student date list, derived badges | C07/C02/C09; Deadline, Course timezone and membership | AC-09, AC-11 |
| FR-07; US-07, no sixth critical UC | Teacher submitted list/detail and course filtering | C08 via C06, C02/C09; saved Result/Quiz/Attempt and membership | AC-10, AC-11 |
| All FRs / original workflows | C01 browser navigation, recoverable safe DTOs; API runs without AI | C01–C10 within AD-01 boundaries, all ten AD-02 entities above | AC-12 no AI; AC-13 UI continuity; AC-14 future automated success/failure/state checks |

C04 alone creates Quiz; C06 alone writes Attempt/Result; C03 coordinates files/metadata;
C05 supplies candidates; C07 writes Deadline; C08 only reads submitted Results. C09/C10
are adapters, not independent permission/business owners. C01 retains unsynchronized
answers and maps errors to existing screens. No extra public provisioning product is added.

| Original NFR | Contract connection / evidence limit |
| --- | --- |
| NFR-01 | Original processed lecture <=30 slides, 18/20 ten-question requests within 30 seconds, one active user and working AI service remain unchanged. Phase 1 bank-only generation does not prove this NFR or semantic content understanding. |
| NFR-02 | Result/list queries support later timing study: 100 saved results, one active user, 19/20 result-page requests within 3 seconds on standard desktop/stable campus Wi-Fi. No measurement is claimed. |
| NFR-03 | Deny Student Deadline writes and others' private answers; apply backend role/membership/ownership on lists and direct requests. Contract is not proof of enforcement. |
| NFR-04 | Clear upload/generation/submission errors support study; still requires five first-time Students, at least four unassisted completions within 10 minutes. |
| NFR-05 | Item/field errors support keyboard recovery; upload/answer/submit keyboard operation and visible focus, including native chooser, need UI verification. |
| NFR-06 | Preserve unsent selections and acknowledged Drafts on same-session network reconnect; recover ambiguous finalization without duplicates. Real disconnection test remains required. |

## 12. Open choices and implementation handoff

Confirmed direction does not select the following implementation mechanisms. Contract review
must finalize exact DTO validation and status/error choices before clients depend on them.
No new code, schema, database connection, seed, tests, dependencies or infrastructure is
created here, and no AutoNote module is executed.

| Open choice | Implementation gate / AD-04 planning |
| --- | --- |
| Session library/store, expiry, hashing configuration, login rotation/logout/recovery | Blocks auth implementation; AD-04 sequences credential/session work and integration checks |
| CSRF mechanism/token lifecycle, cookie attributes, Origin allowlist and proxy trust | Blocks browser write integration; review auth and anonymous CSRF bootstrap together |
| Trusted idempotent provisioning and safe credential injection | Blocks usable backend courses/accounts; AD-04 plans scripts without hardcoded production credentials |
| Upload limits, type validation, operation fingerprints/retention, cross-store recovery and backup | Blocks safe upload acceptance; AD-04 plans crash/orphan/restore checks without requiring background jobs |
| Exact Topic-balanced algorithm/ties, Question tags/usage/versioning | Blocks predictable generation acceptance; AD-04 prepares real bank capacity, including single-Topic ten-question coverage |
| Practice exact sizing, repeated new-operation policy and cross-practice exclusions | Resolve before enabling repeated-practice behavior; Regular-only source is already confirmed |
| Autosave interval, local recovery store and conflict UI | Blocks reliable draft UX; AD-04 plans concurrent-save/offline/real reconnect evidence |
| Atomic finalization mechanism, indexes, Atlas/driver transaction retries and unknown commits | Blocks submission correctness; AD-04 schedules concurrency and failure tests; no mechanism is claimed tested |
| Upload/generation identity lifetime, failure caching, expired/missing operation reconciliation | Blocks safe automatic replay; never silently treat expired identity as a fresh creation |
| Course timezone provisioning, supported date range, rollover/zone changes | Trusted IANA per offering is confirmed; concrete config and refresh behavior block date-boundary acceptance |
| Pagination/filtering, exact DTO schemas/status codes, delete/edit concurrency | Finalize required slices before implementation; AD-04 can sequence pagination/performance and stale-view checks |
| Real Question Bank/seed capacity, repeatable fictional datasets and NFR evidence | AD-04 planning; preserve original NFR applicability/open AI requirement review |

AD-04 should turn reviewed contracts into implementation increments and evidence gates.
This document does not begin AD-04, choose package versions, implement routes or grant
formal team approval to the proposed protocol details.

## 13. Revision history

| Version / date | Change | Review boundary |
| --- | --- | --- |
| 1.0 / 2026-11-18 | Task 6: ten confirmed AD-03 decisions; 30 proposed endpoints, safe DTOs, authorization, operation recovery, lifecycle, errors and traceability | Prepared for Review; implementation choices remain proposed/open; no implementation, staging, commit or push |
