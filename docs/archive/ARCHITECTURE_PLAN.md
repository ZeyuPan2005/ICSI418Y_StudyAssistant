# Preliminary Architecture Plan

**Direction:** Modular Monolith + Future AI Service
**Requirements reference:** [Requirements Baseline v1.2](../requirements/REQUIREMENTS_BASELINE.md)
**Status:** AD-01 components, AD-02 data, AD-03 API contract and AD-04 implementation plan **Prepared for Review**; IMP work not started. Unresolved proposals are not approved designs.
**Date:** 2026-11-18

## Purpose and boundaries

Organize the next architecture tasks without implementing features or selecting schemas,
authentication/session mechanisms, endpoints or deployment details. The approved Task 2
requirements and D-01 through D-03 constrain the design. Task 3 additionally confirms
AD01-D01/D02/D05/D09; Task 4 confirms AD02-D01 through AD02-D06. The
[component architecture](../design/COMPONENT_ARCHITECTURE.md) and [data model](../design/DATA_MODEL.md) are
prepared for review; their proposed details do not imply implementation or formal approval.

The repository currently contains a React/Vite prototype with browser-local services and
fixtures. It has no Express application, Atlas integration or protected server uploads.
`legacy/AutoNote/` is preserved legacy source and must remain outside the Phase 1 runtime.

## Approved direction and proposed responsibilities

| Layer / component | Phase | Responsibility to design |
| --- | --- | --- |
| React/Vite presentation | Phase 1, existing foundation | Preserve screens, routing and core workflows; later connect an API-facing service boundary while clearly disclosing bank-based generation. Authentication UI remains to be designed. Keep `client/src/` in place for this task. |
| Node.js/Express application | Phase 1, not implemented | Real authentication, backend authorization, business rules, API handling and coordination of application persistence/file storage. |
| MongoDB Atlas | Phase 1, not integrated | Required application data for the logical entities in the baseline, including stable quiz/result snapshots and material file references. Collection/schema design is proposed in [AD-02](../design/DATA_MODEL.md), awaiting review. |
| Protected local server storage | Phase 1, not implemented | Accepted file bytes, separated from public static assets and guarded by server-controlled access. Exact storage layout and delivery mechanism are unresolved. |
| Deterministic question provider | Phase 1, not implemented | Backend-managed predefined questions matched to supported topics; an implementation inside the monolith is proposed. Regular quizzes have exactly 10 distinct questions; practice has 1-10 with source exclusions. Detailed selection policy and provider contract remain open. |
| Optional Python processing service | Potential Phase 2 | Selected, validated AutoNote capabilities behind a replaceable interface; not required for Phase 1 startup, uploads, readiness, generation, grading or any other core workflow. |

### Component design reference

Use the [AD-01 system context](../design/COMPONENT_ARCHITECTURE.md#3-phase-1-system-context),
[component diagram and responsibility matrix](../design/COMPONENT_ARCHITECTURE.md#4-component-architecture)
and [trust boundaries](../design/COMPONENT_ARCHITECTURE.md#5-authentication-authorization-and-trust-boundaries)
as the component-design source. All Phase 1 business modules, the bank provider and storage
adapters are logical parts of one Express application, not separately deployed microservices.
The future AI service is optional and absent from the Phase 1 dependency path.

## Requirement constraints for design

- D-01 / FR-01: registration/login must enforce server-controlled roles and preassigned
  memberships. Public requests cannot promote accounts to Teacher or self-enroll.
- D-02 / FR-02: real bytes go to protected local storage and application metadata to Atlas.
  The design must account for a file-write failure and a database-write failure without
  falsely reporting a valid ready upload. No particular transaction/cleanup strategy is chosen.
- D-03 / FR-03: Phase 1 readiness and matching cannot depend on semantic extraction. Show
  predefined-content disclosure. Keep generation replaceable without requiring Python.
- FR-04 / FR-05: preserve question/grading snapshots, one final result per Attempt and
  original records across practice. Concurrency and retry behavior need explicit design.
- FR-06 / FR-07: enforce Teacher permissions and course isolation at the backend; preserve
  calendar boundaries and exclude drafts from submitted-result views.
- NFRs: retain all original conditions in the baseline. In particular, do not remove the
  AI precondition from NFR-01 or claim current mock timing proves production compliance.

## Architecture work packages

AD-01 through AD-04 documentation is prepared for review; IMP implementation is future work, and
none of the architecture is implemented by these documentation changes.
Their deliverables and review questions are proposed; team member assignments and dates
remain open. Requirement definitions are not repeated here.

| Package | Deliverable to prepare | Required review evidence | Dependencies |
| --- | --- | --- | --- |
| AD-01 Component Architecture | [Completed design document for review](../design/COMPONENT_ARCHITECTURE.md): diagrams, module ownership, workflows, invariants, decisions/proposals and handoff | FR-01 through FR-07 mapping, all original NFRs, AI independence and distinction between confirmed decisions and unresolved proposals; not implementation approval | Baseline v1.2 preserves four Task 3 and adds six Task 4 confirmations; unresolved design feeds AD-03 |
| AD-02 Data Model | [Prepared for Review](../design/DATA_MODEL.md): ten entities, ERD, proposed fields/indexes/snapshots, upload recovery and atomic submission; verified M2/M3 mapping and disclosed evolution | Six confirmed AD-02 decisions; at most one Attempt per Quiz, exactly one Result per submitted Attempt; independent practice history, offering isolation, derived alerts and explicit storage/transaction limits | Baseline v1.2 and AD-01 responsibilities; physical design proposals require review with AD-03 |
| AD-03 API Contract | [Prepared for Review](../design/API_CONTRACT.md): ten confirmed decisions, 30 proposed endpoints, DTOs, session/CSRF rules, revision conflicts and operation recovery | Trace all FRs and original UCs/USs/NFR limits; safe preview, independent practice and definite/unknown persistence outcomes | AD-01/AD-02 foundation; Task 6 subsequent confirmations; physical mechanisms and exact DTO/status choices await review |
| AD-04 Implementation Plan | [Prepared for Review](../design/IMPLEMENTATION_PLAN.md): small vertical slices, dual-adapter async migration, blocking gates, traceability and task-specific verification/DoD | Assign AC-01 through AC-14 and NFV-01 through NFV-06 to verification work; identify AI-independent integration checks, NFR studies, rollback/recovery needs and scope decisions | Outputs of AD-01/02/03 plus resolution or explicit deferral of blocking questions |

AD-02 fields/indexes remain proposals. Subsequent AD03-D01 confirms server-side cookie
sessions; AD03-D02 through D10 settle further behavior in the API contract. AD-04 should produce
a sequenced implementation plan only after contracts and invariants are sufficiently clear.

## Open design register

The canonical questions are in the [baseline](../requirements/REQUIREMENTS_BASELINE.md#open-design-questions-and-change-control).
This table preserves the AD-01/AD-02 handoff context. Subsequent AD-03 confirmations
supersede its earlier open alternatives: Q-01 session direction/trusted provisioning
(AD03-D01/D02/D09), Q-02 synchronous upload (D03), Q-04 Regular-only practice source (D06),
Q-05 generation identity/Start lifecycle/errors (D04/D05/D10), Q-06 draft revisions (D08),
and Q-08 backend course-local IANA calendar policy (D07). The table's older proposal/open
wording records that earlier review stage; remaining implementation choices are canonical
in [AD-03 open choices](../design/API_CONTRACT.md#12-open-choices-and-implementation-handoff).

| Baseline question | Design analysis needed | Decision still open |
| --- | --- | --- |
| Q-01 Authentication and provisioning - partially resolved | AD01-D02/AD02-D01 confirm global role, trusted memberships and no public self-enrollment; evaluate session/cookie vs token options and provisioning mechanics | No authentication mechanism, hashing configuration or account-to-membership association flow selected; sessions/cookies remain a proposal |
| Q-02 Material readiness - partially resolved | AD01-D01 confirms manual course-specific topics; AD01-D05 prevents bank shortage invalidating material | AD02-D03 confirms at least one Topic at upload; editing/feedback remain open, AD-02 storage/recovery states are proposed |
| Q-03 Upload policy and storage | Define size/type/resource limits, validation and file access; assess path safety, local disk capacity, retention and cross-store recovery | No numeric upload limits, disk layout or file-serving endpoint selected |
| Q-04 Question matching - partially resolved | AD01-D05 fixes exactly 10 regular questions; AD01-D09 fixes 1-10 practice questions, source exclusions and zero/perfect-source behavior | AD02-D04 confirms favored selected-Topic coverage with compensation; exact balancing/order, practice size/repetition and bank maintenance remain open; AD-02 proposes stable identity/snapshots |
| Q-05 Submission idempotency | Analyze duplicate/concurrent submissions and lost responses; separately review proposed generation retry deduplication vs intentional regeneration | AD02-D05 fixes at most one Attempt per Quiz, immutable submissions and new Quiz for deliberate learning; AD-02 proposes unique indexes/conditional updates/transactions; retry contracts remain open |
| Q-06 Drafts and recovery | Define save acknowledgement, reconnect behavior and competing sessions without losing selected answers | No autosave interval, conflict policy or client/server reconciliation protocol selected |
| Q-07 NFR verification | Resolve AI-dependent NFR-01 treatment and document timing boundaries/fixtures for performance checks | No new Phase 1 performance target or original requirement waiver approved |
| Q-08 Calendar semantics | Choose consistent date/timezone interpretation while keeping today through +7 inclusive and +8 unmarked | AD02-D06 confirms date-only YYYY-MM-DD; specific course timezone remains open |
| Q-09 Authority and review process | Agree a shared M2 source location and how decisions/baseline changes are recorded | No new approval authority or team sign-off inferred |
| Q-10 Future AI integration | Evaluate provider contract, synchronous/asynchronous processing, output validation, privacy, costs, failure isolation and safe AutoNote reuse | No queue, provider/model, deployment protocol or AutoNote module selected |

## Future AI evaluation boundary

The [AutoNote import review](AUTONOTE_IMPORT_REVIEW.md) documents incomplete dependencies,
import-time execution, unsafe historical parsing/shell construction, inconsistent schemas
and credential-remediation follow-up. Keeping the source does not certify it as deployable.
Do not import or run it during Phase 1 setup or these architecture documentation tasks.

For a later Phase 2 proposal, compare candidates with synthetic fixtures and controlled
provider substitutes before approved live processing. Define input/output contracts and
privacy/cost controls before connecting real recordings or model APIs. Transcription,
structured notes and AI question generation remain potential enhancements. Keep core
identity, course rules, quiz ownership, grading snapshots and persistence within the
application's trusted business boundary; a provider must not decide authorization.

## Design handoff checklist

Before implementing a work package, review its requirement mapping and unresolved questions.
Document chosen mechanisms and tradeoffs separately from the baseline's required outcomes.
Changes to approved scope or original NFR conditions require an explicit recorded requirement
decision rather than an implicit architecture substitution.

Use the [traceability matrix](../requirements/REQUIREMENTS_TRACEABILITY.md) to confirm that US-07 and all
five critical use cases remain represented. Preserve the current frontend workflows and
regression tests while later replacing mocks deliberately. This planning document creates
no backend, database schema, API endpoint, infrastructure resource or new dependency.

## AD-01 review handoff

The [Task 3 confirmed decisions](../design/COMPONENT_ARCHITECTURE.md#2-confirmed-architecture-decisions)
remain AD01-D01, AD01-D02, AD01-D05 and AD01-D09. Task 4 adds the six
[AD-02 confirmations](../design/DATA_MODEL.md#confirmed-ad-02-decisions). The
[proposal and handoff register](../design/COMPONENT_ARCHITECTURE.md#15-proposal-evaluation-and-unresolved-design-handoff)
evaluates nine proposals and assigns unresolved portions of Q-01 through Q-10 to later work.
Baseline v1.2 and its traceability revision record the confirmed implications without changing
original M2 IDs, numerical NFR conditions or source provenance. Completion of AD-01 means
the design deliverable is ready for review, not that every proposed detail has been approved.

## AD-02 review handoff

[Milestone consistency and evolution](../design/DATA_MODEL.md#2-milestone-consistency-and-design-evolution)
records the original ERD mapping, file-derived Concepts versus manual Topics, the changed
latest-score-only retake assumption, derived Alerts and assigned-Teacher result access.
The original lecture-content goal and AI-dependent NFR-01 are not claimed satisfied.

[Proposed persistence and lifecycle](../design/DATA_MODEL.md#5-proposed-mongodb-storage-design)
refine AD-01 responsibilities; [open items](../design/DATA_MODEL.md#14-open-questions-proposals-and-risks)
and the [AD-03 handoff](../design/DATA_MODEL.md#15-ad-03-and-implementation-handoff) identify contract,
calendar, recovery and concurrency decisions still needed. Confirmed requirements do not
approve physical fields/indexes/transactions. No implementation or formal team sign-off
is asserted by marking AD-01/AD-02 Prepared for Review.

## AD-03 review handoff

[API Contract v1.0](../design/API_CONTRACT.md) records Task 6 confirmations AD03-D01 through AD03-D10
as later refinements, preserving AD-01/AD-02 historical decisions. Paths, DTOs, status codes,
headers, session/CSRF libraries, transaction mechanisms and detailed selection/recovery
policies remain proposals or open choices. See its [traceability](../design/API_CONTRACT.md#11-requirements-components-and-data-traceability)
and [implementation gates](../design/API_CONTRACT.md#12-open-choices-and-implementation-handoff).
AD-04 is now [Prepared for Review](../design/IMPLEMENTATION_PLAN.md); that status asserts no implementation or formal approval.

## AD-04 review handoff

[Implementation Plan v1.0](../design/IMPLEMENTATION_PLAN.md) records Confirmed AD04-D01 incremental
vertical slices and AD04-D02 dual-adapter migration. IMP-01 through IMP-07 are decomposed
into reviewable future tasks; IMP-06A Deadlines depends on IMP-01, while IMP-06B Teacher
review depends on IMP-04. [Blocking gates](../design/IMPLEMENTATION_PLAN.md#5-blocking-decision-register)
retain technical choices as Open/Proposed. The [first-task handoff](../design/IMPLEMENTATION_PLAN.md#8-first-implementation-handoff-and-future-prompt-structure)
recommends IMP-01A only after its prerequisite decisions. No IMP work, formal team approval
or runtime validation is asserted by completing the planning document.
