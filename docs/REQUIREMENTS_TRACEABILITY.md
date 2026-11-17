# Requirements Traceability

**Baseline:** [Requirements Baseline v1.0](REQUIREMENTS_BASELINE.md)
**Status:** Working traceability for the Approved Working Baseline
**Reviewed:** 2026-11-17 against repository `5833fc5` and the M2 report identified in the baseline.

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
and open Q-02/Q-04.

## Supporting and cross-cutting coverage

| Requirement / decision | Scope | Proposed acceptance |
| --- | --- | --- |
| FR-01 / D-01 | All five UCs and all seven USs; actual registration/login has no current screen or original UI ID | AC-01 identity and privilege controls; AC-11 ownership/course restrictions; NFV-03 |
| D-02 | FR-02 and protected material access | AC-02 actual bytes and Atlas metadata; AC-03 partial-write failures; AC-11 file access |
| D-03 | FR-03 and FR-05; replaceable bank provider | AC-04/05 generation; AC-07/08 practice; AC-12 no Python/AI dependency |
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
| FR-03 | Service case beginning `UC-02 leaves quizzes unchanged on failure`; browser no-content/failure/retry/preview flow | Client fixtures supply questions; no backend Quiz/snapshot persistence or agreed material-topic policy. |
| FR-04 | Service case beginning `UC-03 validates drafts`; browser incomplete answers, reload, simulated interruption and grading | Local storage and synchronous client grading; no server grading, concurrent duplicate handling or real network-recovery proof. |
| FR-05 | Service case beginning `UC-04 saves distinct quiz and attempt`; browser linked-practice/return/perfect-score flow | Original-object comparison exists locally; persisted backend invariants and bank exhaustion cases need tests. |
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
