# Requirements Traceability

**Baseline:** [Requirements Baseline v1.2](REQUIREMENTS_BASELINE.md)
**Status:** Prepared for Review; traces confirmed working requirements without approving architecture proposals
**Reviewed:** 2026-11-17; v1.0 evidence was inspected at `5833fc5`, with Task 3 decision implications reviewed against `e310d1b`. M2 provenance is unchanged; Task 4 also inspected original M2/M3 and records the comparison in AD-02.
**Revision:** v1.2 preserves AD01-D01/D02/D05/D09 and records AD02-D01 through AD02-D06; [AD-01](COMPONENT_ARCHITECTURE.md) and [AD-02](DATA_MODEL.md) remain Prepared for Review.

## Reading the matrix

UC/US/NFR identifiers are preserved from M2. UI identifiers come from the archived
[Milestone 3 UI mapping](archive/milestone-3/ui-mapping.md), not from invented M2 screens.
FR, AC and NFV identifiers are new baseline/planning identifiers. AC scenarios are defined
once in the [baseline acceptance criteria](REQUIREMENTS_BASELINE.md#proposed-acceptance-criteria);
NFV procedures and original conditions are in its [NFR section](REQUIREMENTS_BASELINE.md#non-functional-requirements).

All Phase 1 backend acceptance tests below are **proposed, not implemented or passed**.
Existing mock tests and browser walkthroughs provide workflow evidence only. Source
inspection does not prove authentication, real uploads, Atlas persistence, server grading,
production security or NFR compliance.

## Original scope to Phase 1 acceptance

Feature labels summarize M2 section 2, pp. 1-2; UC mappings were checked against section 3,
pp. 2-4. FR-01 is a supporting implementation requirement across every row.

| Original use case | Original user story / feature | Primary Phase 1 FR | Existing UI screens | Proposed acceptance tests |
| --- | --- | --- | --- | --- |
| UC-01: Upload lecture material | US-01: Submit lecture material | FR-02 | UI-01 course/material entry -> UI-02 upload -> UI-03 material readiness | AC-02 real file/metadata persistence; AC-03 invalid upload/storage failure; AC-11 course/file access |
| UC-02: Generate a lecture quiz | US-02: Generate a quiz | FR-03 | UI-01 entry -> UI-03 generation and preview -> UI-04 start | AC-04 persisted topic-matched preview; AC-05 no invalid quiz on failure; AC-11 ownership/course access |
| UC-03: Submit and review quiz answers | US-03: Take and grade a quiz | FR-04 | UI-04 answering -> UI-05 results; UI-01 quiz/result index | AC-06 draft recovery, backend grading and duplicate protection; AC-11 private-answer protection |
| UC-04: Generate follow-up practice | US-04: Practice weak topics | FR-05 | UI-05 source -> UI-06 practice preview -> UI-04 answering -> UI-05 practice result and source return | AC-07 separate practice and immutable originals; AC-08 perfect-score/insufficient-content alternatives; AC-11 ownership |
| UC-05: Publish and display a course deadline | US-05: Manage course deadlines | FR-06 | UI-07 Teacher management -> UI-01/UI-08 Student visibility | AC-09 validation, persistence, edits/removal and past-date management; AC-11 Teacher-only writes |
| UC-05: Publish and display a course deadline | US-06: View upcoming alerts | FR-06 | UI-01 Student dashboard and UI-08 upcoming dates; UI-07 is the source of changes | AC-09 day 0/+7/+8, no stale reminders, course visibility; AC-11 membership filtering |
| No dedicated critical UC in M2 | US-07: Review quiz results | FR-07 | UI-01 Teacher dashboard -> UI-01T Student Quiz Results | AC-10 submitted scores/answers, drafts excluded and assigned-course access; AC-11 cross-course restrictions |

US-07 is deliberately retained despite not having a sixth critical use case. UC-05 covers
two distinct stories; these are not collapsed into one story. UC-04 reuses quiz-taking and
result screens without renumbering UC-03 or creating a new original UC.

For US-01/US-02, Phase 1's stored-file/topic-bank readiness is the explicit Task 2 staging
of the original content-based intent, not a claim that the file has been semantically
processed. See the [scope interpretation](REQUIREMENTS_BASELINE.md#current-system-versus-development-phases)
and partially resolved Q-02/Q-04. AD01-D01 confirms manual topic association; AD01-D05
confirms ten distinct regular questions, while AD01-D09 permits 1-10 practice questions.
These decisions do not imply semantic analysis or compliance with AI-dependent NFR-01.

## Supporting and cross-cutting coverage

| Requirement / decision | Scope | Proposed acceptance |
| --- | --- | --- |
| FR-01 / D-01 | All five UCs and all seven USs; actual registration/login has no current screen or original UI ID | AC-01 identity and privilege controls; AC-11 ownership/course restrictions; NFV-03 |
| D-02 | FR-02 and protected material access | AC-02 actual bytes and Atlas metadata; AC-03 partial-write failures; AC-11 file access |
| D-03 | FR-03 and FR-05; replaceable bank provider | AC-04/05 generation; AC-07/08 practice; AC-12 no Python/AI dependency |
| AD01-D01 | FR-02/03: manual predefined course-topic selection, multiple-topic support and backend validation | AC-02 rejects foreign-course associations; AC-04/05 use validated manual topics and disclose predefined questions |
| AD01-D02 | FR-01: trusted preassigned memberships and server-controlled roles | AC-01/11 prevent public promotion, self-enrollment and unauthorized resource access |
| AD01-D05 | FR-03: exactly 10 distinct regular questions; insufficient coverage does not invalidate material | AC-04 with 10/11 eligible candidates yields exactly 10; AC-05 with fewer than 10 yields no partial Quiz and leaves stored material valid |
| AD01-D09 | FR-05: 1-10 practice questions, source exclusions and separate immutable-original workflow | AC-07 with positive pools respects 1-10 bounds; AC-08 with zero candidates/perfect source creates no practice |
| AD02-D01 | FR-01: global role plus trusted membership and ownership | AC-01/11 deny public privilege/membership forgery |
| AD02-D02 | All FRs: isolation by course offering | AC-11 rejects cross-term/year IDs even when course codes match |
| AD02-D03 | FR-02/03: at least one predefined course Topic at upload | AC-02/03 reject empty/foreign/mixed associations; AC-05 preserves valid stored material despite bank shortage |
| AD02-D04 | FR-03: favor selected-Topic coverage; compensate empty Topics, exactly ten distinct | AC-04/05 cover multi-tag deduplication, 9/10/11 candidate bounds and empty-Topic compensation; exact balancing remains proposed |
| AD02-D05 | FR-03/04/05: at most one Attempt per Student-owned Quiz; immutable submission/history | AC-04/06/07 cover concurrent Start, no reopen/overwrite, new Quiz for deliberate learning and independent practice Result |
| AD02-D06 | FR-06: date-only YYYY-MM-DD and consistent course calendar | AC-09 calendar validity, day 0/+7/+8, past hidden and derived alerts; zone remains open |
| Phase 1 without AI | All FR-01 through FR-07 | AC-12 runs core workflows with Python services absent and AI endpoints unavailable |
| Frontend continuity | UI-01 through UI-08 plus UI-01T | AC-13 workflow/navigation/reload/keyboard regression |
| Automated critical success/failure cases | AC-01 through AC-13 | AC-14 backend-state assertions and browser coverage; NFR human studies remain separate |

No new original story, use case or UI number is assigned to authentication or other
supporting work. Authentication UI and API designs belong to later AD tasks.

## Existing evidence and remaining implementation gap

The existing [Node service tests](../tests/services.test.js) and
[Playwright browser tests](../tests/browser.mjs) remain unchanged. The following references
identify inspectable cases, not future backend test files.

| Area | Existing evidence | Gap to Phase 1 acceptance |
| --- | --- | --- |
| FR-01 | Service test `US-07 and service guards reject cross-course, teacher-only and other-student operations`; role/course navigation in browser tests | Fictional role switching and browser guards must be replaced at the trust boundary by real backend authentication and authorization; registration/hash tests do not exist. |
| FR-02 | Service case beginning `UC-01 rejects missing, empty and unsupported files`; browser upload/processing flow | File metadata and a timer only; no file bytes or Atlas persistence. |
| FR-03 | Service case beginning `UC-02 leaves quizzes unchanged on failure`; browser no-content/failure/retry/preview flow | Client fixtures select all course topics; manual association is confirmed but not implemented. No backend Quiz/snapshot persistence; favored coverage is confirmed, exact balancing/ordering remains open. |
| FR-04 | Service case beginning `UC-03 validates drafts`; browser incomplete answers, reload, simulated interruption and grading | Local storage and synchronous client grading; no server grading, concurrent duplicate handling or real network-recovery proof. |
| FR-05 | Service case beginning `UC-04 saves distinct quiz and attempt`; browser linked-practice/return/perfect-score flow | Original-object comparison exists locally; persisted backend invariants, 1-10 practice bounds and empty-bank cases need tests. |
| FR-06 | Service case beginning `UC-05 validates dates`; browser validation, day boundaries, edits/removal and both Student views | Calendar behavior is demonstrated locally; no protected writes, shared database or agreed deployment timezone. |
| FR-07 | US-07 service case; browser UI-01T expansion, drafts exclusion and unassigned-course denial | No protected teacher result API or real accounts. |
| Prototype regression | Seventh service test covers reset; browser tests cover navigation, reload, keyboard operation and narrow-screen dashboard | Demo reset remains a test/development control, not a new production business requirement. Real-auth entry flows still need design. |

## Original NFR traceability

The full original conditions and numerical targets live in the baseline to avoid divergent
copies. M2 section 4, PDF p. 4, is the source for all six rows.

| Original ID | Related functional scope / UI | Proposed verification | Evidence limitation / open item |
| --- | --- | --- | --- |
| NFR-01 | FR-03; UI-03 preview | NFV-01 original quiz-generation timing protocol | Original condition requires a working AI service; bank-only Phase 1 does not prove compliance. Q-07 must resolve phase applicability without silently changing targets. |
| NFR-02 | FR-04, FR-07; UI-05, UI-01T | NFV-02 repeated result-page loads with the original saved-result dataset | No full-stack timing study exists; test protocol needs the stated browser/network conditions. |
| NFR-03 | FR-01, FR-04, FR-06; UI-04/UI-05/UI-07 and direct backend access | NFV-03 prohibited Student actions; AC-01/11 | Mock guards do not prove server security; teacher course isolation is additionally covered by FR-07/AC-10. |
| NFR-04 | FR-02, FR-03, FR-04; UI-02 -> UI-03 -> UI-04 -> UI-05 | NFV-04 original first-time-user study | No five-user production usability study is claimed. |
| NFR-05 | FR-02, FR-04; UI-02, UI-04, UI-05 | NFV-05 keyboard and visible-focus verification; AC-13 | Existing automated file chooser boundary does not verify native keyboard-only file selection. |
| NFR-06 | FR-04; UI-04 interruption/reconnect, then UI-05 | NFV-06 actual disconnection; AC-06 duplicate/retry cases | Current interruption is simulated. Draft acknowledgement/recovery policy is Q-06. |

## Coverage and maintenance rules

The matrix contains **5 unique original UCs**, **7 original USs**, **7 Phase 1 FRs**, and
**6 original NFRs**. Every existing screen UI-01 through UI-08 plus UI-01T is represented.
All **14 proposed ACs** and **6 proposed NFV procedures** have a requirement connection.

When requirements change, update the baseline first, then these links and the relevant
[architecture work package](ARCHITECTURE_PLAN.md#architecture-work-packages). Do not mark
an acceptance test passed solely because its prototype equivalent passes. Record the
implementation revision, test environment and actual results when backend tests exist.

## AD-01 component handoff

The [requirements-to-components mapping](COMPONENT_ARCHITECTURE.md#14-requirements-and-verification-traceability)
assigns each FR to a primary domain owner and collaborators. The component responsibility
matrix distinguishes Quiz creation, Attempt/Result ownership, material/file coordination,
deadline writes and read-only Teacher queries. AD-02/AD-03 must preserve these invariants
while resolving schemas, contracts, authentication, readiness and retry mechanisms.

The original seven-row UC/US/UI matrix and six NFR mappings are retained. New confirmation
rows refine acceptance expectations; they do not introduce original stories or claim test
execution. Version 1.0 is recoverable from `e310d1b`; version 1.2 accompanies the documented
baseline revision and awaits documentation review without broader formal approval.

## AD-02 data-model handoff

The [data-model traceability](DATA_MODEL.md#13-requirements-traceability) maps all ten entities
and persistence invariants to FR-01 through FR-07, all original UC/US/NFR IDs and AC-01
through AC-14. Its [milestone audit](DATA_MODEL.md#2-milestone-consistency-and-design-evolution)
discloses the M3 latest-score-only retake policy change and file-derived Concept/manual
Topic limitation, while preserving calculated Alerts and assigned-Teacher review.
Practice uses its own Quiz, Attempt and Result after submission, linked to the unchanged
source Result. Proposed mechanisms and verification cases are not implemented tests.
