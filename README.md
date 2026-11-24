# Study Assistant

ICSI 418Y Software Engineering team project. A React study assistant for lecture materials, quizzes, feedback, targeted practice, teacher deadlines, and review of submitted results.

## Project status

- **Working now:** React/Vite **Demo** with fictional accounts, predefined questions, client-side grading, and browser-local state.
- **Designed, not implemented:** Express modular-monolith backend, MongoDB Atlas, secure sessions, server-side grading, and protected lecture uploads.
- **Next development unit:** IMP-01A, subject to its blocking technical decisions in the [Implementation Plan](docs/IMPLEMENTATION_PLAN.md).
- **Phase 1 does not require AI or Python.** Historical AutoNote experiments are isolated under `legacy/`.

Do not mistake the current Demo's role switcher or local storage for real authentication or persisted application data.

## Repository layout

| Path | Purpose |
| --- | --- |
| [client/](client/) | Runnable React/Vite Demo and its test suites; future real API adapter |
| [server/](server/README.md) | Reserved for Express backend; no implementation yet |
| [docs/](docs/README.md) | Current requirements, architecture, API and delivery plan |
| [legacy/](legacy/README.md) | Preserved AutoNote experiments, excluded from Phase 1 |
| [.gitignore](.gitignore) | Local environment, build and cache exclusions |

The older Milestone 3 report/checklist documents are no longer tracked here; the team keeps its own local copy. The existing React UI remains the foundation for real-mode migration.

## Run the current frontend

**Requirements:** Node.js 22.12+ and npm. From the repository root:

```sh
cd client
npm ci
npm run dev
```

Open the address printed by Vite. No backend, Atlas credentials, or Python runtime is required.

Demo walkthrough: choose the Student role to select a nonempty PDF/PPTX/MP3/WAV, generate a sample quiz, submit and review feedback. Switch to Teacher to manage course deadlines and inspect submitted results. Use **Reset demo data** and **Confirm reset** for repeatable examples. Use one active browser editing tab.

## Test the current frontend

Run from `client/` after `npm ci`:

```sh
npm test
npm run build
npm run test:browser
```

The service and browser tests validate the **Demo**, not Express/Atlas. `npm run test:browser` defaults to Microsoft Edge; set `BROWSER_PATH` to an installed compatible Chromium executable when necessary. Screenshots are generated in ignored `client/test-results/screens/` by default.

## Documents and implementation handoff

Read in this order:

1. [Requirements Baseline](docs/REQUIREMENTS_BASELINE.md) and [Traceability](docs/REQUIREMENTS_TRACEABILITY.md)
2. [AD-01 Component Architecture](docs/COMPONENT_ARCHITECTURE.md)
3. [AD-02 Data Model](docs/DATA_MODEL.md)
4. [AD-03 API Contract](docs/API_CONTRACT.md)
5. [AD-04 Implementation Plan](docs/IMPLEMENTATION_PLAN.md) — task dependencies, 14 decision gates, verification and Definition of Done

AD04-D01 adopts incremental vertical slices. AD04-D02 preserves the Demo while introducing a separate real API/state adapter. Both decisions are Confirmed; proposed libraries, schemas, precise DTOs and physical mechanisms remain review gates.

**Layout change:** Frontend code/tests and package scripts moved into `client/`; `server/` has only a placeholder README. Project documentation has been updated to the new locations. This restructure does **not** implement IMP-01A.

## Development handoff by responsibility

**Start here: [docs/README.md](docs/README.md)**. It contains a short all-team reading sequence and separate, focused guides for [Frontend](docs/frontend/README.md), [Database](docs/database/README.md), [Backend A / Express](docs/backend/express/README.md), [Backend B / AI & Materials](docs/backend/ai/README.md), and [Backend C / Quiz & Grading](docs/backend/learning/README.md).

The team's next selected stories are **US-01/02/03/05/06** (target 5 of 7 MVP stories, subject to acceptance evidence). The **proposed** [HTTP API agreement](docs/contracts/HTTP_API.md), [internal AI ↔ Express contract](docs/backend/ai/AI_MODEL_CONTRACT.md), and [persistence agreement](docs/database/PERSISTENCE_CONTRACT.md) specify work boundaries. **Express**, not the React browser, invokes AI conversion, quiz generation and feedback; Express validates/persists before returning safe data.

**Design transition:** The earlier full Phase 1 plan deliberately relied on a predefined Question Bank. The current team is considering content-grounded AI generation for the selected stories; these contracts describe that desired design, but are **not yet team-approved or implemented**. Resolve it and review external-model privacy/credentials before live calls. `client/` currently remains Demo-only and `server/` remains unimplemented.

## Working as a team

1. Pull current `main`, create a task-focused feature branch and use a Pull Request.
2. Review the relevant AD-04 task and settle only its blocking technical gates before coding.
3. Keep Demo behavior available until real API integration replaces a workflow; never use Demo identities as a real authorization fallback.
4. Run relevant checks and report exact results, skipped checks and remaining limitations.
5. Do not commit credentials, real student data, recordings, model outputs, local environment files or generated build/test artifacts.
6. Seek human review before merging. Small, scoped implementation increments are preferred.

### Legacy and security warning

[`legacy/AutoNote/`](legacy/AutoNote/README.md) contains unverified experimental Python code; some scripts may execute model calls or file operations upon import. Do not install or run it as part of Phase 1. See the [import/security review](docs/AUTONOTE_IMPORT_REVIEW.md). Historical credentials removed from source may still need owner-managed revocation and rotation.
