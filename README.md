# Study Assistant

Study Assistant is an ICSI 418Y Software Engineering team project for helping students
study course materials, review quiz feedback and practice weak topics, while giving
teachers a way to manage course deadlines and review submitted work.

## Current development status

This repository is the team's starting point for full-stack development. The runnable
application is still a **React/Vite frontend prototype** with fictional profiles and
browser-local mock services. The backend, database integration, production authentication
and AI features are **planned, not implemented**.

The frontend already demonstrates material selection and validation, sample quiz previews,
answer submission and grading, follow-up practice, teacher result views and deadline
management. Its existing screens, routes, styles, state and tests provide the foundation
for future work.

## Frontend and mock limitations

The frontend uses React, React Router, JavaScript/JSX and plain CSS. The mock service
layer in `src/services/demo.js` supplies the behavior used by the screens.

- File selection checks the extension and nonzero size for PDF, PPTX, MP3 and WAV files.
  Only metadata is stored; file bytes are not uploaded, parsed or transcribed.
- Processing uses a timer. Quiz generation and targeted practice select predefined,
  topic-tagged questions from fictional fixtures; there are no AI calls.
- Drafts, results, deadlines and the active profile persist in local storage under
  `study-assistant.demo.v1`, per browser origin. Use one active editing tab. Changing
  the host or port gives a different local dataset.
- The demo role selector and service guards illustrate student, teacher, course and
  ownership rules. They do not provide production authentication or server authorization.
- Deadlines use local calendar dates and in-app reminders. No external notifications
  are sent. A simulated interrupted submission is not a real network recovery test.

For a quick walkthrough, use Student to upload a nonempty supported file, open the ready
lecture, generate a sample quiz, submit answers and review weak topics. Switch to Teacher
to manage deadlines and inspect submitted results, then switch back to Student to see
shared course changes. **Reset demo data** followed by **Confirm reset** restores the
fictional fixtures. Deterministic failure controls remain available for development tests.

## Repository structure

| Path | Purpose |
| --- | --- |
| `src/main.jsx`, `src/App.jsx` | React entry, shared navigation, routes and prototype access checks |
| `src/screens/`, `src/components/`, `src/styles/` | Views, reusable UI and styling |
| `src/services/demo.js` | Mock materials, quizzes, attempts, grading, practice and deadlines |
| `src/data/fixtures.js`, `src/state/Demo.jsx` | Fictional records, question banks and browser state |
| `tests/services.test.js` | Node tests for mock behavior and access rules |
| `tests/browser.mjs` | Playwright workflow, navigation, persistence and keyboard checks |
| `index.html`, `vite.config.js`, `package.json`, `package-lock.json` | Frontend entry, build configuration and locked dependencies |
| `AutoNote/` | Preserved legacy Python code for later AI/backend evaluation; outside the frontend runtime |
| [Design assumptions](docs/design-assumptions.md) | Existing requirement decisions and prototype conventions |
| [AutoNote import review](docs/AUTONOTE_IMPORT_REVIEW.md) | Legacy module relationships, security findings and known limitations |
| [Historical archive](docs/archive/milestone-3/README.md) | Prior planning, UI-to-requirement mapping and manual acceptance walkthrough |

`src/` remains at the repository root. Local `node_modules/`, `dist/` and `test-results/`
are generated and ignored by Git.

## Local setup and run

Use Node.js **22.12 or newer** and npm. From the repository root:

```sh
npm ci
npm run dev
```

Open the URL printed by Vite. No backend service, database, API key or Python environment
is needed to run the frontend. Use a local browser with storage enabled.

To build and preview the production bundle:

```sh
npm run build
npm run preview
```

## Tests

Run from the repository root after installing dependencies:

```sh
npm test
npm run build
npm run test:browser
```

`npm test` runs seven service tests covering upload validation, generation, grading,
practice, dates, access checks and reset behavior. The browser test uses the built bundle,
starts its own loopback preview and isolated browser profile, and closes both when done.
It checks the student and teacher workflows, navigation, persistence, keyboard interactions
and narrow-screen dashboard layout.

Microsoft Edge is the browser-test default. For another installed compatible Chromium
browser, set `BROWSER_PATH` to its executable. For example, in PowerShell, replace this
path with the browser installed on your machine:

```powershell
$env:BROWSER_PATH = 'C:\path\to\chrome.exe'
npm run test:browser
```

The test saves fresh screenshots in ignored `test-results/screens/`. `SCREENSHOT_DIR`
can override the output directory; keep generated captures outside tracked documentation.
The harness supplies a file at the operating system file-chooser boundary. This coverage
does not establish production performance, security or accessibility compliance.

## Legacy AutoNote

`AutoNote/` contains historical Python transcription, note-generation and knowledge-network
experiments retained for possible reuse. It is not connected to the frontend and has not
been verified as a working backend. Its dependency declarations are incomplete, and some
scripts execute model calls or process local media when imported.

Read the [import review](docs/AUTONOTE_IMPORT_REVIEW.md) before evaluating or running any
legacy module. Previously embedded credentials were removed during import; their owners
still need to revoke or rotate them. The example environment contains placeholders only.
The frontend setup above does not install or execute AutoNote.

## Planned full-stack development

The current direction is an Express API for materials, quizzes, attempts, results and
deadlines, with MongoDB persistence and a separately evaluated AI processing service.
Architecture and provider choices need team agreement before implementation.

Future work includes authenticated identities, server-enforced course permissions,
controlled file storage and processing, transcription/document extraction, generated
questions, durable results and real error recovery. Evaluate AutoNote components against
these contracts before reuse. Preserve stable IDs, original-result references and immutable
grading snapshots when replacing mocks, and verify performance and privacy against the
project requirements. None of these planned integrations is provided by this cleanup.

## Collaboration and contributions

1. Pull the latest `main`, then create a focused branch such as
   `git switch -c feature/material-api`. Use pull requests for team review.
2. Describe the problem, scope and acceptance criteria before changing shared contracts.
   Keep changes small; avoid combining feature work with unrelated formatting or moves.
3. Keep fixtures and mocks available until a reviewed integration replaces them. Update
   relevant tests and documentation when behavior or setup changes. Do not commit real
   student data, recordings, transcripts or credentials as test fixtures.
4. Run `npm test`, `npm run build`, `npm run test:browser` when the browser is available,
   and `git diff --check`. In the pull request, report results and explain skipped checks.
5. Commit dependency lockfile changes only with an intentional dependency update. Keep
   local environment files, caches, logs, builds and screenshots untracked. Never place
   private API keys in frontend code or client-exposed Vite variables.
6. Summarize behavior changes, validation and known limitations in the pull request.
   Coordinate changes to shared models or API boundaries with the team before merging.

The historical archive supplies context and prior acceptance steps; it is not the current
implementation plan. Keep active decisions in the design documentation and reviewed work.
