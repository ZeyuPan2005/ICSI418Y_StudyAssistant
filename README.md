# Study Assistant

Study Assistant is the ICSI 418Y Software Engineering team project for studying course
materials, reviewing quiz feedback and practicing weak topics, with Teacher deadline
management and submitted-result review.

The current runnable implementation is a **React/Vite Demo** using fictional profiles and
browser-local state. Express, MongoDB Atlas, real authentication and protected server uploads
have **not started**. AD-01 through AD-04 are prepared design deliverables; their documents
retain **Prepared for Review** status and distinguish confirmed decisions from proposals.
The next planned development task is **IMP-01A**, subject to its listed prerequisite decisions.

## Quick Start: React Prototype

Use Node.js **22.12 or newer** and npm. From the repository root:

```sh
npm ci
npm run dev
```

Open the URL printed by Vite. Use a browser with local storage enabled. The Demo needs no
backend, database, Python environment or API key. Do not run the legacy AutoNote scripts
as part of setup.

As Student, select a nonempty PDF/PPTX/MP3/WAV, open the ready lecture, generate a sample
quiz, submit answers and review weak topics. Switch to Teacher to manage deadlines and
inspect submitted results. **Reset demo data**, then **Confirm reset**, restores fixtures.
Use one active editing tab; changing host/port gives a separate browser-local dataset.

To build and preview the production bundle of the Demo:

```sh
npm run build
npm run preview
```

## Current and planned stack

| Area | Runnable now | Planned Phase 1 |
| --- | --- | --- |
| Frontend | React, React Router, Vite, JavaScript/JSX and CSS | Preserve workflows; separate real API client and async state alongside Demo |
| Identity/data | Fictional profiles, synchronous Demo Service, browser local storage | Express modular monolith, server-side sessions with HttpOnly cookie, CSRF/Origin protection, trusted course membership |
| Storage | File metadata only; local quiz/results/deadlines | MongoDB Atlas application records and protected local server file bytes |
| Questions | Predefined browser fixtures and client grading | Backend-managed predefined Question Bank, immutable snapshots and server grading |

Phase 1 requires no Python, Whisper, LLM, AutoNote service or external AI dependency.
Manual Topic matching does not interpret lecture contents or establish compliance with the
original AI-dependent NFR-01. Optional AI enhancements belong to later reviewed work.

## Tests

After installing the locked dependencies, run from the repository root:

```sh
npm test
npm run build
npm run test:browser
```

`npm test` runs seven Demo service tests. The browser suite uses the built bundle, starts
its own loopback preview and isolated profile, and closes both afterward. It checks Student
and Teacher workflows, navigation, local persistence, keyboard interactions and a narrow
layout. These are prototype regressions, not real API/Atlas, security or NFR evidence.

Microsoft Edge is the default. To use another installed compatible Chromium browser, set
`BROWSER_PATH` to its executable, for example in PowerShell:

```powershell
$env:BROWSER_PATH = 'C:\path\to\chrome.exe'
npm run test:browser
```

Screenshots go to ignored `test-results/screens/`; `SCREENSHOT_DIR` can select another
untracked output location. Automation supplies the file at the operating-system chooser
boundary; manual native keyboard file selection remains separate verification.

## Repository and documentation

| Path | Purpose |
| --- | --- |
| `src/main.jsx`, `src/App.jsx` | React entry, routes, shared navigation and prototype guards |
| `src/screens/`, `src/components/`, `src/styles/` | Existing views, reusable UI and styles |
| `src/services/demo.js` | Synchronous Demo workflows; preserve during migration |
| `src/state/Demo.jsx`, `src/data/fixtures.js` | Browser state and fictional users/courses/question banks |
| `tests/services.test.js`, `tests/browser.mjs` | Demo service and browser regression suites |
| `package.json`, `package-lock.json`, `vite.config.js`, `index.html` | Scripts, locked dependencies and frontend configuration/entry |
| `docs/` | Active requirements and design documents linked below |
| [Milestone 3 archive](docs/archive/milestone-3/README.md) | Historical planning, UI mapping and prior walkthrough/evidence |
| [AutoNote](AutoNote/README.md) | Preserved experimental Python source and variants; outside Phase 1 runtime |

Start with the baseline for required outcomes, then follow the design and task handoffs.
Confirmed requirements take precedence over earlier prototype conventions; proposed physical
schemas, libraries and algorithms are not approved merely because they appear in a design.

| Document | Role |
| --- | --- |
| [Requirements baseline](docs/REQUIREMENTS_BASELINE.md) | Original authority, phased scope, confirmed decisions and acceptance criteria |
| [Requirements traceability](docs/REQUIREMENTS_TRACEABILITY.md) | Original UC/US/NFR mapping to Phase 1 FRs, screens and proposed checks |
| [Architecture plan](docs/ARCHITECTURE_PLAN.md) | AD-01 through AD-04 status and review handoffs |
| [AD-01 Component Architecture](docs/COMPONENT_ARCHITECTURE.md) | Module responsibilities, trust boundaries and ownership |
| [AD-02 Data Model](docs/DATA_MODEL.md) | Ten logical entities, ERD, milestone evolution and proposed persistence/recovery |
| [AD-03 API Contract](docs/API_CONTRACT.md) | Confirmed API behavior, proposed endpoints/DTOs, authorization and retries |
| [AD-04 Implementation Plan](docs/IMPLEMENTATION_PLAN.md) | Small future tasks, dependencies, technical gates, migration and verification |
| [Historical prototype assumptions](docs/design-assumptions.md) | Milestone 3 conventions; retained at its existing path for established references |
| [AutoNote import review](docs/AUTONOTE_IMPORT_REVIEW.md) | Legacy module/dependency/security findings and reuse limitations |

Local `node_modules/`, `dist/`, `test-results/` and Python environments/caches are ignored
artifacts, not shared source. Contributors should install from the lockfile, not copy a
local environment. No generated or contributor-local files need deletion for this handoff.

## Phase 1 implementation roadmap

No IMP work has begun. [IMP-01A and its prerequisites](docs/IMPLEMENTATION_PLAN.md#8-first-implementation-handoff-and-future-prompt-structure)
are the next planned starting point; authentication, adapter/configuration and local test
boundaries need review before code starts. The [blocking register](docs/IMPLEMENTATION_PLAN.md#5-blocking-decision-register)
tracks remaining choices as Open/Proposed.

The delivery sequence is authentication/course access -> Topics/real upload -> regular
Quiz preview -> Attempt/Draft/Result -> targeted practice. Deadlines can follow authentication
independently; Teacher result review follows persisted Results. Final integration/regression
and NFR verification follow the included workflows. Each functional slice must connect the
UI, API/state and real persistence where applicable; backend handlers alone do not complete
it. Keep Demo available while introducing the real adapter and asynchronous states.

## Demo limitations and legacy boundary

- Upload validates extension/nonzero size and stores metadata; it sends no file bytes.
  Readiness is simulated by a timer. Quiz/practice questions are predefined fixture content.
- Drafts, grades, deadlines and active profile live under `study-assistant.demo.v1` in
  browser local storage. Client guards and the role selector demonstrate access rules;
  they do not authenticate users or enforce production authorization.
- Deadline comparisons use browser-local dates. Reminders are in-app; interrupted
  submission is simulated. Real network recovery, backend persistence and NFR compliance
  remain future verification work.

[AutoNote](AutoNote/README.md) explores transcription, notes and knowledge-network generation.
Its dependencies are incomplete/unverified and some scripts process files or call models
when imported. **Do not execute it automatically** during setup, tests or Phase 1 work.
Read the [import review](docs/AUTONOTE_IMPORT_REVIEW.md) before any separately authorized
reuse evaluation. Previously embedded credentials were removed during import; their owners
still need to revoke/rotate those historical values. This cleanup does not establish their
revocation. All Python variants remain preserved.

## Contribution and Git workflow

1. Start from current `main` and create a focused branch, for example
   `git switch -c codex/material-upload`. Coordinate the task scope and prerequisite decisions
   before changing shared contracts; use pull requests and human review.
2. Work on one AD-04 subtask or reviewed slice at a time. Preserve existing routes, Demo
   behavior and unrelated edits; report any change to agreed contracts explicitly.
3. Run relevant checks. For frontend behavior, use the service/build/browser commands above
   when available; for documentation, validate references and `git diff --check`. Report
   actual commands, failures and skipped checks. Demo tests never substitute for real API tests.
4. Keep commits small and limited to reviewed files. Stop for review before commit/push unless
   the specific task authorizes it; do not automatically proceed to the next implementation unit.
5. Commit lockfile changes only with intentional dependency work. Keep credentials, session
   secrets, real student data, recordings, transcripts, logs, environments and generated output
   out of Git. Placeholder `.env.example` files may be shared; real secrets belong in local
   environment configuration and must never be exposed through frontend Vite variables.
6. Describe changed behavior, validation and remaining limitations in the pull request.
   Use the requirements/design documents as shared authority; the archive supplies history.
