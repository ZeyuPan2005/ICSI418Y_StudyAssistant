# Requirements Baseline

| Document control | Value |
| --- | --- |
| Version | 1.0 |
| Status | Approved Working Baseline |
| Established | 2026-11-17 |
| Repository reference | `ZeyuPan2005/ICSI418Y_StudyAssistant`, inspected at `5833fc5` |
| Approval scope | The development phases and decisions explicitly supplied in Task 2; no additional formal team sign-off is asserted. |

## Purpose and scope

Define the requirements for converting the existing frontend prototype into a working
Study Assistant application before detailed architecture design. This baseline preserves
the five critical use cases and seven original user stories and introduces Phase 1
implementation requirements without renumbering the original requirements.

This document defines required outcomes. The [traceability matrix](REQUIREMENTS_TRACEABILITY.md)
connects them to existing screens and proposed tests; the [architecture plan](ARCHITECTURE_PLAN.md)
organizes subsequent design work. Neither document implements a backend or finalizes schemas,
API routes, authentication mechanisms or deployment details.

## Requirements authority and provenance

| Source | Authority and use |
| --- | --- |
| M2: submitted Milestone 2 report, local copy `Team01- Milestone 2- Report.pdf` | Original requirements authority. Section 1, p. 1: actors and open questions; section 2, pp. 1-2: US-01 through US-07; section 3, pp. 2-4: UC-01 through UC-05; section 4, p. 4: NFR-01 through NFR-06. Read and checked for this baseline. |
| Task 2: Establish Requirements Baseline v1.0 | Explicitly approved phased strategy, D-01 through D-03 and Phase 1 requirements. These are new development decisions, not quotations from M2. |
| [Design assumptions](design-assumptions.md) | Prototype conventions and design context; does not override original requirements or later explicit decisions. |
| [Phase A plan](archive/milestone-3/phase-a-plan.md), [UI mapping](archive/milestone-3/ui-mapping.md), [checklist](archive/milestone-3/demo-checklist.md) | Historical workflow and UI evidence; not proof of production compliance. |
| [README](../README.md), [frontend services](../src/services/demo.js), [fixtures](../src/data/fixtures.js), [service tests](../tests/services.test.js), [browser tests](../tests/browser.mjs) | Evidence of current prototype behavior only. |
| [AutoNote import review](AUTONOTE_IMPORT_REVIEW.md) | Legacy implementation findings and security limitations, not a functional specification or verified backend. |

The five-page M2 PDF is outside this repository, at `Project/Milestone/2/` in the local
course workspace. Its SHA-256 is
`7b86a241c5bb7f5b33a84973f82d9b4f438071e1c1eab73fbaba3516c12d0070`.
The report was read without adding or modifying it. Section and PDF page references above
identify the source without creating a nonportable repository link. A shared authoritative
report location remains to be agreed in Q-09.

Descriptions below summarize the verified report unless identified as Task 2 decisions.
The original report remains authoritative for exact wording. Do not reinterpret an open
question or prototype behavior as an approved design. Later changes must identify affected
IDs, source/decision, acceptance impact and baseline version in a reviewed change.

## Current system versus development phases

| State | Scope and limitations |
| --- | --- |
| Current implementation | React/Vite frontend, fictional profiles, local-storage state, metadata-only file selection, timer-based readiness, predefined quiz/practice banks and browser-side grading/access checks. No real registration, backend API, Atlas persistence, server file storage or AI integration exists. |
| Phase 1: Core MVP, approved | React/Vite + Node.js/Express + MongoDB Atlas + protected local server file storage + deterministic backend question bank/topic matching. Persist real materials, quizzes, attempts, results and deadlines. All core workflows must work without external AI services or Python/AutoNote. |
| Phase 2: AI enhancement, potential | Evaluate selected Whisper transcription, structured notes, AI quiz generation and other validated lecture processing behind a replaceable interface. Candidates are not commitments that every legacy module will be integrated. |

**Scope interpretation:** M2 US-02/UC-02 expect questions based on lecture content and
UC-01 ties readiness to usable content. Task 2 D-03 explicitly stages delivery through
predefined topic-matched content, with semantic extraction deferred. Phase 1 must disclose
this limitation and associate questions with the eligible material's supported topics;
it must not claim to have interpreted file contents. The topic source and readiness rule
remain Q-02/Q-04. Meeting this phased acceptance is not evidence that the original
content-understanding goal or AI-dependent NFR-01 has been fully satisfied.

## Actors and roles

| Actor | Required Phase 1 permissions |
| --- | --- |
| Student | Register/login; upload to assigned courses; preview, answer and submit their own quizzes; revisit their own results; request linked practice; view current/future course deadlines. No teacher privileges or access to another student's private answers. |
| Teacher | Authenticate with a server-controlled Teacher role; upload to assigned courses; manage those courses' deadlines; inspect submitted student scores and answers only in assigned courses. |

Both actors operate under backend-enforced course membership. Public registration must
not permit Teacher self-assignment or arbitrary course enrollment, including through forged
requests. Memberships are preassigned. Provisioning and account-to-membership association
are design questions, not a new administrator product role or enrollment-management feature.
Service components named in M2 use cases are supporting system responsibilities, not new
human actors. The prototype role switcher is not an authentication solution.

## Approved technical decisions

| ID | Approved requirement decision | Source |
| --- | --- | --- |
| D-01 | Real registration/login, securely hashed passwords, backend-controlled Student/Teacher roles, preassigned memberships and backend authentication/authorization. Public registration cannot grant Teacher privileges or choose arbitrary courses. | Task 2 |
| D-02 | Store accepted file bytes in protected local server storage. Store metadata, uploader/ownership, course association, processing status and file references in MongoDB Atlas. Client metadata alone is not an upload. | Task 2 |
| D-03 | Use a backend-managed predefined topic-tagged bank, persist real quizzes and question snapshots, disclose predefined content, and keep the generation interface replaceable. AutoNote is not a Phase 1 dependency. | Task 2 |

React/Vite, Express and MongoDB Atlas are the approved technology direction. The proposed
component organization and future AI boundary are preliminary; see the architecture plan.

## Functional requirements

### FR-01 - Authentication and course access

**Origin:** Task 2 D-01; supports all original workflows and NFR-03. This is not an
additional original user story or use case.

The system shall register and authenticate users, securely hash passwords and associate
accounts with server-controlled roles and preassigned memberships. The backend shall enforce
role, course and student-ownership checks on every relevant operation, independent of UI
visibility or client-supplied identity. Unauthorized requests shall neither expose protected
data nor perform prohibited writes. Registration shall not confer Teacher privileges or
arbitrary course access. Authentication/session strategy and provisioning remain Q-01.

### FR-02 - Lecture material upload

**Mapping:** UC-01 / US-01. **Decisions:** D-01, D-02.

Students and Teachers shall upload provisional MP3, WAV, PDF or PPTX files to assigned
courses. The backend shall validate supported formats and nonempty contents, store accepted
bytes in protected local server storage and persist metadata, uploader, course, status and
file reference in Atlas. Users shall see meaningful upload, readiness and failure feedback.
Rejected or failed uploads shall not appear as valid ready materials. A failure to store
bytes or metadata shall not be reported as success. Readiness must not imply transcription
or semantic understanding. Detailed validation, limits and cross-store failure handling
remain Q-02/Q-03; no schema or state enumeration is fixed here.

### FR-03 - Quiz generation

**Mapping:** UC-02 / US-02. **Decisions:** D-03 and the phased interpretation above.

An authorized Student shall request a quiz for eligible material. The backend shall match
its supported topics to predefined questions and persist a real Quiz with question snapshots.
The student shall preview questions and answer options before starting. Missing/ineligible
material, insufficient matching content and generation/persistence failures shall produce
clear feedback without an empty/invalid quiz or changes to existing files and quizzes.
The UI shall disclose predefined content rather than AI analysis. The generation interface
shall allow later provider replacement. Topic sourcing, selection rules and quiz size remain
Q-04; the prototype's fixed ten-question bank is not a blanket Phase 1 design decision.

### FR-04 - Quiz submission and feedback

**Mapping:** UC-03 / US-03. **Supporting NFRs:** NFR-03, NFR-06.

The system shall save draft answers and identify unanswered required questions without
losing selected answers. The backend shall grade submissions against the quiz's preserved
question/answer snapshots and persist answers, score, feedback and submission timestamps.
Duplicate or retried final submissions shall not create additional final results or change
the original grade. Students shall revisit only their own results. Grading snapshots shall
remain stable when the source question bank changes. Durable writes and concurrent duplicate
handling are required outcomes; their mechanism remains Q-05. Draft acknowledgement and
recovery behavior remain Q-06 without relaxing the original NFR-06 outcome.

### FR-05 - Targeted follow-up practice

**Mapping:** UC-04 / US-04.

For a student's graded result with missed topics, the system shall choose distinct practice
questions focused on those topics, create a separate Quiz and Attempt and link the practice
to the original Result. Practice questions shall be distinct from the source quiz. Creating
and completing practice shall never modify the original Quiz, Attempt, answers, Result or
score. The student shall be able to return to the original result. A perfect result shall
explain that targeted review is unnecessary and create no practice quiz. An unsuccessful
request shall leave the original intact and create no invalid practice. Selection when the
bank lacks enough distinct questions and repeated-practice policy remain Q-04.

### FR-06 - Deadline management and visibility

**Mapping:** UC-05 / US-05, US-06.

Only assigned Teachers shall create, edit and delete course-wide lecture/homework deadlines.
Title, type and date shall be validated before saving. Teachers may manage past dates;
Students shall see today and future dates for assigned courses. Today through day +7
inclusive shall be marked Upcoming; day +8 and later remain visible without that label.
Past dates shall be omitted from student lists. Changes and removals shall update both the
dashboard and deadline view without stale reminders. Reminders are in-app only. These
calendar-window decisions are explicitly supplied in Task 2, not original numerical M2
requirements. The consistent server/client calendar-timezone rule remains Q-08.

### FR-07 - Teacher result review

**Mapping:** US-07; no separate sixth critical use case was specified in M2.

Assigned Teachers shall inspect submitted student scores and answers in their courses.
Drafts shall not appear as finished results. Backend checks shall prevent unassigned-course
access through lists and direct result requests. UI-01T remains the existing workflow
reference. This requirement does not introduce advanced analytics.

## Non-functional requirements

The original NFR IDs and conditions below were verified in M2 section 4, PDF p. 4,
including visual inspection. These are summarized original requirements, **not new targets**.
No production compliance is claimed. Proposed verification IDs NFV-01 through NFV-06 are
new planning labels, not original report identifiers.

| ID / area | Verified original requirement and conditions | Proposed verification and Phase 1 treatment |
| --- | --- | --- |
| NFR-01 / Performance | For an already processed lecture of at most 30 slides, at least 18 of 20 requests display a 10-question quiz within 30 seconds, with one active user and a working AI service. | NFV-01: time 20 attempts under those conditions. Preserve the AI precondition; Phase 1 bank-only timings do not establish compliance. Applicability/adaptation requires a recorded decision under Q-07. No replacement target is invented. |
| NFR-02 / Performance | With 100 saved quiz results and one active user, at least 19 of 20 result-page requests load within 3 seconds on a standard desktop browser and stable campus Wi-Fi. | NFV-02: load the results page 20 times with that dataset and environment. Applies to the future persisted system; timing boundaries/environment details still need a reproducible test protocol. |
| NFR-03 / Security | A Student account cannot create, change or delete course-wide deadlines or view another student's private quiz answers. | NFV-03: attempt all prohibited actions as a real Student, including direct backend requests. D-01/FR-01 extend enforcement to backend role and course checks; mock tests are not production evidence. |
| NFR-04 / Usability | Of five first-time student users, at least four upload a supported slide file, generate a quiz and submit answers without outside help within 10 minutes. | NFV-04: observe the five-user task set and record completion time and assistance. Participant/task preparation remains to be scheduled. Automated walkthroughs cannot replace this study. |
| NFR-05 / Accessibility | Upload, quiz answering and quiz submission are keyboard-operable with visible focus on interactive controls. | NFV-05: perform all three using Tab, Shift+Tab, Enter and Space without a mouse; include the native file-selection interaction. Existing automation supplies the file at the chooser boundary and is only partial evidence. |
| NFR-06 / Reliability | If submission fails because the connection drops, selected answers remain visible when the page reconnects during the same active session. | NFV-06: disconnect before submitting, reconnect and verify retained selections. Test real network failure and ambiguous server completion alongside AC-06; a mock interruption is insufficient. |

Secure password hashing, public-registration privilege restrictions, protected file storage
and backend authorization are Task 2 implementation requirements, not extra wording
attributed to NFR-03. No new numerical throughput, concurrency, upload-size or availability
target is approved here.

## Logical data requirements

These are domain concepts, not database collections or schemas. Field definitions,
relationships/cardinalities, indexes, document boundaries and persistence strategies belong
to AD-02. References needed by the workflows do not decide their storage representation.

| Entity | Required business meaning |
| --- | --- |
| User | Authenticated identity with a server-controlled role. |
| Course | Study context for course-scoped activities. |
| CourseMembership | Server-controlled assignment used to authorize course access. |
| LectureMaterial | An accepted upload with ownership/course context, status and a protected file reference. |
| Topic | A subject used to match questions and identify weak areas. |
| Question | Backend-managed predefined question content and grading information. |
| Quiz | A persisted lecture/practice question set with stable snapshots and ownership context. |
| Attempt | A student's draft answers and submission lifecycle, separate for follow-up practice. |
| Result | Persisted score, submitted-answer/feedback snapshot, missed topics and submission time. |
| Deadline | A teacher-managed course date and its reminder context. |

Question snapshots and grading snapshots must preserve historical meaning. Do not equate
client local storage with the required application persistence. Uploaded bytes reside in
protected local storage; the associated application data resides in Atlas (D-02).

## Explicitly deferred scope

Phase 1 excludes Whisper transcription, LLM-generated notes or quizzes, automatic PDF/PPTX
semantic extraction, knowledge graphs, custom model training, AI chat, course creation and
enrollment administration, external deadline notifications and advanced learning analytics.
These may be future enhancements; listing them does not commit Phase 2 to deliver them all.
Preassigning memberships for the MVP does not imply an enrollment-administration UI.

## Proposed acceptance criteria

AC IDs are new baseline test-planning identifiers. All scenarios below are **proposed and
not implemented or executed against a backend**. They elaborate the supplied decisions
without selecting architecture mechanisms. Use fictional accounts/data and approved test
storage. Record both backend state and user-visible outcomes; UI-only assertions cannot
prove persistence or authorization.

### AC-01 - Registration, authentication and privilege control

Given public registration, when an applicant supplies Teacher role or arbitrary course
assignments, then the server rejects or ignores the privilege-bearing fields and grants
neither privilege. Given valid provisioned memberships, a user can authenticate and access
only permitted workflows; invalid or missing authentication cannot access protected data.
Stored passwords are secure hashes, never plaintext. Provisioning details follow Q-01.

### AC-02 - Real upload and persistence

Given an authenticated Student or Teacher assigned to a course, when each provisional
supported, nonempty file is uploaded, then actual bytes are stored in protected local
storage and Atlas records the material's uploader, course, metadata, status and reference.
A later authenticated session can retrieve the persisted material state. Neither an
unauthenticated request nor an unassigned-course request can upload or bypass file access
controls. The UI distinguishes successful storage from readiness and discloses no AI analysis.

### AC-03 - Upload validation and storage failure

Given missing, empty or unsupported content, when it reaches the backend directly, then
it is rejected with an explanation and no valid ready material is added. Given a simulated
file-write or metadata-persistence failure, then the UI reports failure, no successful ready
material points to unavailable bytes, and existing materials remain unchanged. Reconciliation
and cleanup mechanics are selected in AD-02, not by this scenario.

### AC-04 - Persisted, topic-matched quiz and preview

Given eligible material with supported topics and a sufficient predefined bank, when its
authorized Student requests generation, then the backend creates a persisted Quiz and
question snapshots matched to those topics and presents questions/options before Start.
Reloading retrieves that Quiz. The UI explicitly says predefined content, not AI analysis.
Tests use the topic/readiness policy selected under Q-02/Q-04 rather than infer file semantics.

### AC-05 - Generation failure

Given ineligible material, no supported matches, or an induced provider/persistence failure,
when generation is requested, then the system explains the failure, creates no empty/invalid
Quiz and leaves existing quizzes and uploaded files unchanged. A subsequent successful
request follows AC-04. This does not decide whether repeated generation creates a new quiz.

### AC-06 - Drafts, backend grading and duplicate protection

Given a student's open quiz, when answers are saved and the page reloads, then acknowledged
drafts are recoverable. Submitting with missing answers identifies them and retains choices.
A completed submission is graded by the backend using its trusted snapshot, ignoring any
client-supplied grade; answers, score, feedback and timestamp persist and can be revisited.
Repeated/concurrent final submissions, including retry after a lost response, yield only one
final result for that Attempt and do not change its grade. Changes to the question bank do
not alter the completed result. Test network interruption and reconnect as specified in NFR-06.

### AC-07 - Targeted practice and immutable originals

Given an owned graded result with missed topics and distinct matching practice questions,
when practice is generated and completed, then it has a separate Quiz and Attempt, only
questions for missed topics, no source-quiz questions, and a link back to the source Result.
Compare the entire original Quiz, Attempt, answers, Result and score before/after: all remain
unchanged. Follow the return link and verify the original feedback.

### AC-08 - Practice alternatives

Given a perfect result, when practice is requested, then explain that no targeted review
is needed and create no practice Quiz. Given no distinct matching questions or a failed
practice request, then explain the failure and preserve all original records without an
invalid new Quiz. Repeated-practice selection policy remains Q-04.

### AC-09 - Deadlines and calendar boundaries

Given an assigned Teacher, when valid Lecture/Homework entries are created, edited and
deleted, then they persist and student course views reflect the current values. Missing
title/type or invalid date prevents saving. Teachers can manage past entries. Students see
today and future entries: days 0 and +7 are Upcoming, +8 is visible without the label, and
past dates are absent. Test both UI-01 and UI-08 after edits/removals and under the agreed
calendar policy (Q-08). No external notification service is required.

### AC-10 - Teacher review and course isolation

Given submitted results and drafts in two courses, when a Teacher assigned to only one
course opens UI-01T or directly requests results, then only submitted scores and answers
from that course are available. Drafts and unassigned-course data remain inaccessible.

### AC-11 - Student ownership and backend authorization

Given two Students and separate course assignments, when one forges another's identifiers
in quiz/draft/submission/result/practice requests, then the backend refuses access and
changes no protected records. Also deny Student deadline creation/edit/deletion and all
actors' unassigned-course operations, including material and file access. Verify both list
filtering and direct-object access; hiding a navigation link is insufficient.

### AC-12 - Core MVP independent of AI

Given the future Phase 1 deployment with no Python/AutoNote service running, no AI keys and
AI endpoints unavailable, when authenticated users perform upload, bank-based generation,
submission, practice, deadlines and teacher review, then these core workflows still succeed
using Express, Atlas and local storage. This is independence from AI, not an offline-database
requirement. Evidence must show no AI service is needed for startup or these operations.

### AC-13 - Frontend workflow preservation

Given the integrated Phase 1 application, when users traverse UI-01 through UI-08 and
UI-01T, then upload/preview/answer/feedback/practice/deadline/review paths remain available,
including validation, pending/failure feedback, source-result navigation and persisted drafts.
Verify navigation, reload and keyboard behavior. Real authentication must not rely on the
demo role switcher. Authentication UI design is new work without an invented original UI ID.

### AC-14 - Automated critical-path coverage

Before Phase 1 acceptance, automated service/API and browser tests shall exercise AC-01
through AC-13, including unauthorized requests, invalid uploads, failed writes/generation,
missing answers, duplicate/concurrent submissions, perfect-score practice and date boundaries.
Tests shall inspect persisted state where relevant and run with AI unavailable. Preserve the
existing mock tests as regression evidence while adding backend tests during implementation.
Test names/files and infrastructure are AD-04 work; this documentation task adds no tests.
Human usability and native keyboard checks remain distinct NFR verification activities.

## Open design questions and change control

Questions below remain unresolved. Their work-package assignments are planning responsibilities,
not named-person ownership or answers. Resolving one must preserve the approved outcomes or
explicitly record a reviewed baseline amendment.

| ID | Question | Design work |
| --- | --- | --- |
| Q-01 | Session vs token approach; credential policy/hash configuration; logout/expiry/recovery; trusted Teacher provisioning; linking public registrations to preassigned memberships without self-enrollment. | AD-01, AD-02, AD-03 |
| Q-02 | What makes stored material eligible/ready without semantic extraction? Which statuses/transitions and failures are shown, and who controls the topic association? | AD-01, AD-02, AD-03 |
| Q-03 | Upload size/count/resource limits, server-side format validation, naming/path protection, file access delivery, retention, backup and recovery across local files and Atlas. No numerical limits approved yet. | AD-01, AD-02, AD-03 |
| Q-04 | Trusted topic source, deterministic matching/ordering, bank authoring, quiz size, insufficient matches, repeat generation and repeated-practice selection. | AD-01, AD-02, AD-03 |
| Q-05 | How to ensure one final result per Attempt under concurrency, retries and partial persistence without mutating snapshots. No idempotency key/index/transaction strategy selected. | AD-02, AD-03 |
| Q-06 | Draft-save acknowledgement, interruption recovery, conflicting sessions and retry feedback while meeting NFR-06. | AD-02, AD-03, AD-04 |
| Q-07 | How should NFR-01's original AI-service condition be applied across phases? Define reproducible NFR-01/02 timing protocols; do not waive or replace original thresholds implicitly. | AD-04; requirements decision needed |
| Q-08 | Calendar timezone/date comparison across server and browsers, preserving the approved day 0/+7/+8 rules. | AD-02, AD-03 |
| Q-09 | Where can all teammates access the authoritative M2 report, and how will future requirement revisions and approvals be recorded? | AD-04 |
| Q-10 | Future AI provider contract, optional service boundary, processing lifecycle, privacy and failure isolation; which AutoNote components can pass validation? | AD-01, AD-03, AD-04 |

## Baseline review record

Version 1.0 records the Task 2 decisions and verified M2 identifiers/conditions. All five
critical UCs and all seven USs, including US-07, are traced in the companion matrix.
Existing behavior was checked against the source and tests; it is not labeled a working
full-stack implementation. Architecture questions remain open. No application, test,
configuration, database or AutoNote changes are part of this baseline.
