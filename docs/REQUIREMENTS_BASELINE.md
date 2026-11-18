# Requirements Baseline

| Document control | Value |
| --- | --- |
| Version | 1.2 |
| Requirements status | Approved Working Baseline for explicitly supplied requirements and decisions only |
| Document status | **Prepared for Review** (v1.2 revision); no formal team approval of AD-01/AD-02 designs is asserted |
| Established | 2026-11-17 |
| Repository reference | `ZeyuPan2005/ICSI418Y_StudyAssistant`, inspected at `5833fc5` |
| Approval scope | Task 2 decisions, four explicitly confirmed Task 3 decisions and six explicitly confirmed Task 4 decisions; no additional formal team sign-off is asserted. |
| Revision review | AD-01/AD-02 revision prepared for review on 2026-11-17 against `e310d1b`; existing AD-01 work retained and architecture proposals remain unapproved. |


> Subsequent refinement (Task 6, 2026-11-18): [AD-03 decisions AD03-D01 through D10](API_CONTRACT.md#1-confirmed-decisions-and-review-boundary)
> now confirm cookie sessions/trusted provisioning, synchronous upload, generation replay,
> Start-time Attempt creation, Regular-only practice sources, course-configured IANA calendar
> policy, revision conflicts and CSRF/Origin/error behavior. Earlier open/proposed wording
> below records the AD-01/AD-02 review stage; those decisions are preserved. Exact mechanisms
> remain proposed/open in AD-03; no formal team approval is asserted.

## Purpose and scope

Define the requirements for converting the existing frontend prototype into a working
Study Assistant application before detailed architecture design. This baseline preserves
the five critical use cases and seven original user stories and introduces Phase 1
implementation requirements without renumbering the original requirements.

This document defines required outcomes. The [traceability matrix](REQUIREMENTS_TRACEABILITY.md)
connects them to existing screens and proposed tests; the [architecture plan](ARCHITECTURE_PLAN.md)
organizes subsequent design work. The [AD-01 component design](COMPONENT_ARCHITECTURE.md)
and [AD-02 data model](DATA_MODEL.md) are prepared for review, distinguishing confirmed
decisions from proposals. None of these documents implements a backend or finalizes schemas,
API routes, authentication mechanisms or deployment details.

## Requirements authority and provenance

| Source | Authority and use |
| --- | --- |
| M2: submitted Milestone 2 report, local copy `Team01- Milestone 2- Report.pdf` | Original requirements authority. Section 1, p. 1: actors and open questions; section 2, pp. 1-2: US-01 through US-07; section 3, pp. 2-4: UC-01 through UC-05; section 4, p. 4: NFR-01 through NFR-06. Read and checked for this baseline. |
| Task 2: Establish Requirements Baseline v1.0 | Explicitly approved phased strategy, D-01 through D-03 and Phase 1 requirements. These are new development decisions, not quotations from M2. |
| Task 3: AD-01 Component Architecture | Explicit confirmations AD01-D01, AD01-D02, AD01-D05 and AD01-D09, recorded in the [component design](COMPONENT_ARCHITECTURE.md#2-confirmed-architecture-decisions). Other architecture details remain proposals or open questions. |
| Task 4: AD-02 Data Model | Explicit confirmations AD02-D01 through AD02-D06; [milestone audit](DATA_MODEL.md#2-milestone-consistency-and-design-evolution) verifies original M2/M3 and discloses the retake-policy and Concept-to-Topic changes. Physical designs remain proposed. |
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

Descriptions below summarize the verified report unless identified as Task 2, Task 3 or Task 4 decisions.
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
it must not claim to have interpreted file contents. Task 3 confirms manual selection from
predefined course-specific topics, with backend validation and multiple-topic support.
Task 4 requires at least one Topic at upload and favors Topic coverage; exact readiness
representation and selection algorithms remain Q-02/Q-04.
Meeting this phased acceptance is not evidence that the original
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
component organization and future AI boundary are documented for review in AD-01; see the
architecture plan. Task 3 confirms the following refinements without approving all design proposals:

| ID | Confirmed refinement | Affected requirements |
| --- | --- | --- |
| AD01-D01 | Manual selection from predefined course-specific topics, multiple-topic materials, backend validation and predefined-content disclosure; no semantic extraction. | FR-02, FR-03 |
| AD01-D02 | Server-controlled roles and trusted preassigned memberships; no public Teacher/self-enrollment privilege or enrollment-administration UI. | FR-01 and all course-scoped operations |
| AD01-D05 | Successful regular quizzes contain exactly 10 distinct eligible questions; fewer than 10 fails without a partial Quiz or invalidating uploaded material. | FR-03 |
| AD01-D09 | Successful targeted practice contains 1-10 distinct eligible questions on missed topics, excluding source-quiz questions; zero eligible questions or a perfect source creates no practice. Separate linked records preserve the original record set. | FR-05 |

Task 4 confirms the following business refinements; [AD-02](DATA_MODEL.md) records their
implications and the inspected M3 evolution without approving physical designs.

| ID | Confirmed refinement | Affected requirements |
| --- | --- | --- |
| AD02-D01 | Backend-controlled global Student/Teacher role plus trusted CourseMembership; authorize using role, membership and ownership. Public registration grants no Teacher/arbitrary membership privileges. | FR-01, AC-01/11 |
| AD02-D02 | Separate Course offerings for different terms/years of the same code; isolate memberships, materials, topics, questions, quizzes, results and deadlines. Exact uniqueness key remains proposed. | FR-01 through FR-07, AC-11 |
| AD02-D03 | At upload require at least one predefined Topic of the selected Course; allow multiple and validate the entire association. No semantic extraction; storage success does not guarantee sufficient questions. | FR-02/03, AC-02/03/05 |
| AD02-D04 | Exactly 10 distinct eligible regular questions matching Course and selected Topics, favoring coverage. Empty Topics may be compensated by others; fewer than 10 overall fails without partial Quiz or invalidated material. Algorithm/ties remain proposed. | FR-03, AC-04/05 |
| AD02-D05 | One owning Student and at most one Attempt per Quiz; submitted Attempts never reopen/overwrite. New deliberate learning uses a new Quiz; preserve historical Quiz/Attempt/Result, including independent linked practice. | FR-03/04/05, AC-04/06/07 |
| AD02-D06 | YYYY-MM-DD date-only Deadline, not a cutoff timestamp; day 0 through +7 Upcoming, +8 visible/unmarked, past hidden from Students. Consistent course timezone required; specific zone unconfirmed. | FR-06, AC-09 |

Request format, exact balancing/ties, practice size/repetition, retry identities, seed scripts,
sessions/cookies, MongoDB fields/indexes/transactions and upload recovery remain proposals.
AD02-D05 intentionally supersedes M3's most-recent-score retake assumption; AD02-D03 preserves
the explicit Phase 1 limitation relative to M3 file-derived Concepts.

## Functional requirements

### FR-01 - Authentication and course access

**Origin:** Task 2 D-01; supports all original workflows and NFR-03. This is not an
additional original user story or use case.

The system shall register and authenticate users, securely hash passwords and associate
accounts with server-controlled roles and preassigned memberships. The backend shall enforce
role, course and student-ownership checks on every relevant operation, independent of UI
visibility or client-supplied identity. Unauthorized requests shall neither expose protected
data nor perform prohibited writes. Registration shall not confer Teacher privileges or
arbitrary course access. AD01-D02 confirms trusted provisioning as the membership authority
and excludes an enrollment-administration UI. Authentication/session strategy and the trusted
provisioning mechanism remain Q-01. AD02-D01 makes the role global; AD02-D02 isolates
assignments and resources by offering, including identical course codes in different terms/years.

### FR-02 - Lecture material upload

**Mapping:** UC-01 / US-01. **Decisions:** D-01, D-02.

Students and Teachers shall upload provisional MP3, WAV, PDF or PPTX files to assigned
courses. The backend shall validate supported formats and nonempty contents, store accepted
bytes in protected local server storage and persist metadata, uploader, course, status and
file reference in Atlas. Users shall see meaningful upload, readiness and failure feedback.
Rejected or failed uploads shall not appear as valid ready materials. A failure to store
bytes or metadata shall not be reported as success. Readiness must not imply transcription
or semantic understanding. Detailed validation, limits and cross-store failure handling
remain Q-02/Q-03; no schema or state enumeration is fixed here. Under AD01-D01 users select
predefined course-specific topics manually; a material may have multiple topics, and the
backend validates the entire topic/course association. AD02-D03 requires at least one
predefined Topic at upload; empty or foreign-course selections cannot be accepted.
Question-bank insufficiency must not invalidate an otherwise valid uploaded material (AD01-D05).

### FR-03 - Quiz generation

**Mapping:** UC-02 / US-02. **Decisions:** D-03 and the phased interpretation above.

An authorized Student shall request a quiz for eligible material. The backend shall match
its supported topics to predefined questions and persist a real Quiz with question snapshots.
The student shall preview questions and answer options before starting. Missing/ineligible
material, insufficient matching content and generation/persistence failures shall produce
clear feedback without an empty/invalid quiz or changes to existing files and quizzes.
The UI shall disclose predefined content rather than AI analysis. The generation interface
shall allow later provider replacement. AD01-D01 confirms manual, validated course-topic
association. AD01-D05 requires exactly 10 distinct eligible questions per successful regular
quiz; fewer than 10 fails clearly, creates no partial Quiz and does not invalidate the
uploaded material. AD02-D04 favors selected-Topic coverage and permits empty Topics to
be compensated by others. Exact balancing/ordering and retry mechanisms remain Q-04/Q-05;
AD02-D05 requires a new Quiz for a deliberate new learning attempt.
This regular-quiz size does not apply to targeted practice or waive the original NFR-01.

### FR-04 - Quiz submission and feedback

**Mapping:** UC-03 / US-03. **Supporting NFRs:** NFR-03, NFR-06.

The system shall save draft answers and identify unanswered required questions without
losing selected answers. The backend shall grade submissions against the quiz's preserved
question/answer snapshots and persist answers, score, feedback and submission timestamps.
Duplicate or retried final submissions shall not create additional final results or change
the original grade. Students shall revisit only their own results. Grading snapshots shall
remain stable when the source question bank changes. Durable writes and concurrent duplicate
handling are required outcomes; their mechanism remains Q-05. Draft acknowledgement and
recovery behavior remain Q-06 without relaxing NFR-06. AD02-D05 limits each Student-owned
Quiz to at most one Attempt; submitted Attempts never reopen/overwrite. Deliberate new
learning creates a new Quiz and preserves historical Quiz, Attempt and Result records.

### FR-05 - Targeted follow-up practice

**Mapping:** UC-04 / US-04.

For a student's graded result with missed topics, the system shall choose distinct practice
questions focused on those topics, create a separate Quiz and its own Attempt, then its own
Result on successful submission. The practice Quiz links to the original Result; that
source link never substitutes for the practice Result, which does not exist before
submission. Practice questions shall be distinct from the source quiz. Creating
and completing practice shall never modify the original Quiz, Attempt, answers, Result or
score. The student shall be able to return to the original result. A perfect result shall
explain that targeted review is unnecessary and create no practice quiz. An unsuccessful
request shall leave the original intact and create no invalid practice. AD01-D09 requires
1-10 distinct eligible questions for successful practice and at least one eligible question
after source-quiz exclusions. With zero, explain the failure and create no practice. Exact
size within this range, coverage/ordering and repeated-practice policy remain Q-04; ten
questions are not a practice minimum.

### FR-06 - Deadline management and visibility

**Mapping:** UC-05 / US-05, US-06.

Only assigned Teachers shall create, edit and delete course-wide lecture/homework deadlines.
Title, type and date shall be validated before saving. Teachers may manage past dates;
Students shall see today and future dates for assigned courses. Today through day +7
inclusive shall be marked Upcoming; day +8 and later remain visible without that label.
Past dates shall be omitted from student lists. Changes and removals shall update both the
dashboard and deadline view without stale reminders. Reminders are in-app only. These
calendar-window decisions are explicitly supplied in Task 2, not original numerical M2
requirements. AD02-D06 confirms YYYY-MM-DD date-only values, not cutoff timestamps.
Alerts remain derived, preserving M3. The specific course calendar timezone remains Q-08.

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
relationships/cardinalities, indexes, document boundaries and persistence strategies are
proposed in [AD-02](DATA_MODEL.md), prepared for review. Workflow references do not approve
their storage representation.

| Entity | Required business meaning |
| --- | --- |
| User | Authenticated identity with a server-controlled role. |
| Course | Separate term/year offering; all course-scoped activities remain isolated. |
| CourseMembership | Server-controlled assignment used to authorize course access. |
| LectureMaterial | An accepted upload with ownership/course context, status and a protected file reference. |
| Topic | A subject used to match questions and identify weak areas. |
| Question | Backend-managed predefined question content and grading information. |
| Quiz | A persisted lecture/practice question set with stable snapshots and ownership context. |
| Attempt | A student's draft answers and submission lifecycle, separate for follow-up practice. |
| Result | Persisted score, submitted-answer/feedback snapshot, missed topics and submission time. |
| Deadline | Teacher-managed date-only course entry; reminders are derived, not persistent Alert entities. |

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
controls. Users can manually associate multiple predefined course topics, and the backend
validates the entire set at upload. Require at least one Topic; reject empty and foreign-course
selections, including mixed valid/foreign sets (AD02-D03). Test isolation across offerings
sharing one code.
The UI distinguishes successful storage from readiness and discloses no AI analysis.

### AC-03 - Upload validation and storage failure

Given missing, empty or unsupported content, when it reaches the backend directly, then
it is rejected with an explanation and no valid ready material is added. Given a simulated
file-write or metadata-persistence failure, then the UI reports failure, no successful ready
material points to unavailable bytes, and existing materials remain unchanged. Reconciliation
and cleanup mechanics are selected in AD-02, not by this scenario.

### AC-04 - Persisted, topic-matched quiz and preview

Given eligible material with supported topics and a sufficient predefined bank, when its
authorized Student requests generation with at least 10 eligible distinct questions, then
the backend persists a regular Quiz with exactly 10 distinct question snapshots matched to
those topics and presents questions/options before Start. Test eligible pools of 10 and 11;
both successful results contain exactly 10, counting unique questions rather than tag matches.
Check favored Topic coverage and an empty selected Topic compensated by others; exact
balancing remains proposed (AD02-D04).
Reloading retrieves that Quiz. The UI explicitly says predefined content, not AI analysis.
Tests use the confirmed manual topic association and the remaining readiness/matching policy
selected under Q-02/Q-04 rather than infer file semantics.

### AC-05 - Generation failure

Given ineligible material, fewer than 10 eligible distinct regular questions (including zero
or nine), or an induced provider/persistence failure,
when generation is requested, then the system explains the failure, creates no empty/invalid
Quiz and leaves existing quizzes and uploaded files unchanged. Insufficient question-bank
coverage must not invalidate a successfully uploaded material. A subsequent successful
request follows AC-04. Deliberate new learning creates a new Quiz (AD02-D05); retransmission
and unknown-outcome reconciliation remain separate AD-02/AD-03 mechanism proposals.

### AC-06 - Drafts, backend grading and duplicate protection

Given a student's open quiz, when answers are saved and the page reloads, then acknowledged
drafts are recoverable. Submitting with missing answers identifies them and retains choices.
A completed submission is graded by the backend using its trusted snapshot, ignoring any
client-supplied grade; answers, score, feedback and timestamp persist and can be revisited.
Repeated/concurrent final submissions, including retry after a lost response, yield only one
final result for that Attempt and do not change its grade. Changes to the question bank do
not alter the completed result. Verify at most one Attempt per Quiz under concurrent Start,
no reopening after submission, and new Quiz identity with preserved history for deliberate
new learning (AD02-D05). Test network interruption/reconnect as specified in NFR-06.

### AC-07 - Targeted practice and immutable originals

Given an owned graded result with missed topics and distinct matching practice questions,
when practice is generated and completed, then it has a separate Quiz, its own Attempt
and its own submitted Result. The practice Quiz contains
1-10 distinct questions for missed topics, no source-quiz questions, and a link back to the
source Result. Test eligible pools of 1, 9, 10 and 11: successful practice is nonempty, at
most 10 and never exceeds the pool; exact size follows the reviewed policy, not a ten-item minimum.
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
calendar policy (Q-08). Validate actual YYYY-MM-DD dates without treating them as cutoff
timestamps; alerts remain derived. No external notification service is required.

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
| Q-01 | Partially resolved: AD01-D02/AD02-D01 confirm global role and trusted memberships with no self-enrollment. Still open: session/token mechanism, credential policy/hash configuration, logout/expiry/recovery and provisioning/account association process. | AD-02, AD-03 |
| Q-02 | Partially resolved: AD01-D01 fixes manual predefined course-topic association; AD01-D05 separates bank insufficiency from material validity. AD02-D03 fixes at least one Topic at upload. Still open: editing rights, storage/readiness/eligibility states, recovery and feedback; AD-02 proposes mechanisms. | AD-02, AD-03 |
| Q-03 | Upload size/count/resource limits, server-side format validation, naming/path protection, file access delivery, retention, backup and recovery across local files and Atlas. No numerical limits approved yet. | AD-01, AD-02, AD-03 |
| Q-04 | Partially resolved: manual topics, exactly 10 regular questions, 1-10 practice questions, source exclusions and insufficient-pool outcomes confirmed by AD01-D01/D05/D09. AD02-D04 favors coverage and permits compensation from other selected Topics; AD02-D05 requires new Quiz identity for deliberate learning. Still open: exact balancing/ordering, bank identity/versioning/authoring, practice size/repetition and topic/material changes. | AD-02, AD-03 |
| Q-05 | How to ensure one final result per Attempt under concurrency, retries and partial persistence without mutating snapshots. Separately evaluate proposed generation retry deduplication versus intentional regeneration. AD02-D05 fixes at most one Attempt per Quiz and immutable submissions/history; AD-02 proposes keys/indexes/transactions, without approving a mechanism. | AD-02, AD-03 |
| Q-06 | Draft-save acknowledgement, interruption recovery, conflicting sessions and retry feedback while meeting NFR-06. | AD-02, AD-03, AD-04 |
| Q-07 | How should NFR-01's original AI-service condition be applied across phases? Define reproducible NFR-01/02 timing protocols; do not waive or replace original thresholds implicitly. | AD-04; requirements decision needed |
| Q-08 | AD02-D06 confirms date-only YYYY-MM-DD and day 0/+7/+8; specific course timezone and server/browser rollover policy remain open. | AD-02, AD-03 |
| Q-09 | Where can all teammates access the authoritative M2 and M3 reports, and how will future requirement revisions and approvals be recorded? | AD-04 |
| Q-10 | Future AI provider contract, optional service boundary, processing lifecycle, privacy and failure isolation; which AutoNote components can pass validation? | AD-01, AD-03, AD-04 |

## Baseline review record

Version 1.0 recorded the Task 2 decisions and verified M2 identifiers/conditions. All five
critical UCs and all seven USs, including US-07, are traced in the companion matrix.
Existing behavior was checked against the source and tests; it is not labeled a working
full-stack implementation. Architecture questions remain open. No application, test,
configuration, database or AutoNote changes are part of this baseline.

### Revision history

| Version | Change and authority | Review boundary |
| --- | --- | --- |
| 1.0 | Task 2 baseline established at `e310d1b`, following cleanup `5833fc5`; M2 provenance and NFR conditions verified. | Original Approved Working Baseline; no backend implementation or additional formal team approval asserted. |
| 1.1 | Task 3 explicitly confirms AD01-D01/D02/D05/D09. Refine FR-01/02/03/05 and AC-02/04/05/07/08 implications; partially resolve Q-01/02/04 and clarify Q-05. | Documentation revision prepared for review; only supplied decisions are confirmed. AD-01 proposals remain unapproved. Original UC/US/NFR IDs, numerical NFR conditions, source fingerprint and deferred scope are unchanged. |
| 1.2 | Task 4 confirms AD02-D01 through AD02-D06, refines affected FR/AC/Q entries, and verifies M3 evolution in AD-02. | Prepared for Review; clarifies confirmed requirements versus proposed designs and independent practice Result. Original UC/US/NFR meanings and numerical conditions preserved; no formal team approval asserted. |
