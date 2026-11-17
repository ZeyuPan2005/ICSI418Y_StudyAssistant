# Study Assistant

Team 01 · ICSI 418Y · Milestone 3, Part 4

An interactive grayscale React prototype of the five critical workflows in the submitted Milestone 2 requirements. Eight labeled screens cover US-01 through US-07. Two fictional profiles demonstrate student and teacher access.

## Run locally

Use Node.js 22.12 or newer and npm. From this folder:

```sh
npm ci
npm run dev
```

Open the local URL Vite prints. Use the same browser and origin to keep your demo data between visits. To serve the production bundle, run `npm run build` followed by `npm run preview`.

## Demonstrate the workflows

- **Student.** Open Software Engineering, choose **Upload material**, select a nonempty PDF, PPTX, MP3 or WAV, and confirm. Open the ready lecture, generate the sample quiz, review its questions and choices, and start. Submit with at least one wrong answer. From the result, choose **Review weak topics** and complete the separate practice quiz. **View original result** returns to the saved source.
- **Teacher.** Switch the demo role in the header. **Deadline Management** accepts lecture and homework dates. Publish an item due within seven days, switch back to Student, and open **Upcoming Deadlines**. Edit or remove it as Teacher to see both student lists update. **Student Quiz Results** (UI-01T) on the teacher dashboard shows the submitted scores and responses for Software Engineering.
- **Alternative flows.** The seeded lectures *Unavailable lecture content* and *Requirements review* demonstrate unusable content and a one-time generator failure. On UI-04, expand **Demo controls** for an interrupted submission. The seeded 10/10 lecture result demonstrates the no-weak-topics case.
- **Reset.** Choose **Reset demo data**, then **Confirm reset**. This restores all fixtures, the default student profile, and the Software Engineering dashboard.

See [the demo checklist](docs/demo-checklist.md) for reproducible steps and verification results, [the UI mapping](docs/ui-mapping.md) for report figures, and [the design assumptions](docs/design-assumptions.md) for scope decisions.

## Structure and stack

| Path | Responsibility |
|---|---|
| `src/App.jsx`, `src/main.jsx` | React entry, role switcher, accessible course picker, navigation and React Router routes |
| `src/screens/`, `src/components/` | Eight screen views, shared question and deadline lists, labels and feedback |
| `src/data/fixtures.js` | Fictional users, course assignments, material references, question banks and seed records |
| `src/services/demo.js` | File/date validation, course access, quiz generation, grading snapshots, practice and deadlines |
| `src/state/Demo.jsx` | React subscription, browser persistence and simulated processing timer |
| `src/styles/app.css` | Plain CSS, grayscale layouts, keyboard focus and narrow-screen rules |
| `tests/` | Node service tests and Playwright browser walkthrough |
| `docs/screens/` | PNG captures from the production browser walkthrough |

## Mock behavior and limitations

The browser file picker, file metadata checks, route navigation, answer selection, date validation and grading work locally. An accepted upload stores file details and the course fixture ID. A short timer displays processing and ready states. The file bytes never leave the browser and are not parsed or transcribed. Both quiz generation and weak-topic practice select predefined questions. Reusing a lecture result may produce the same practice items.

The demo uses a versioned local-storage key, `study-assistant.demo.v1`. It saves course data, generated quizzes, draft answers, completed results and the active role. Use one active editing tab for demonstrations. Refresh and navigation preserve work. The local profile, browser storage and service checks illustrate access rules. Users who control the browser can inspect or change its data. Production deployment needs authenticated identities and server-enforced authorization.

## Verify

```sh
npm test
npm run build
npm run test:browser
```

The browser test starts and closes its own loopback production preview and isolated browser profile. It uses installed Microsoft Edge by default. Set `BROWSER_PATH` to a compatible Chromium executable when needed. The test saves PNGs in `test-results/screens/`; set `SCREENSHOT_DIR` to choose a different output folder. The operating system’s native file dialog is supplied with a file by the test harness.

To reproduce the eleven report figures in PowerShell, build first and run the following from the repository root. The walkthrough uses fictional data in a fresh browser profile.

```powershell
$env:SCREENSHOT_DIR = 'docs/screens'
npm run test:browser
```

## Future backend integration

Replace the mock service operations with Express endpoints for materials, quizzes, attempts, results and deadlines. Resolve the actor and course permissions on the server. MongoDB can persist the relationships represented by the local records. A processing worker would store the upload, extract usable lecture content and dispatch a generation service. Keep stable quiz IDs, original-result references and immutable grading snapshots when replacing the fixtures. Verify the Milestone 2 performance, usability, privacy and connection-recovery requirements against the deployed system.

## Legacy AutoNote import

`AutoNote/` preserves a legacy Python project for evaluating reusable audio transcription,
lecture-note generation and knowledge-network components. It is not integrated into Study
Assistant; the Milestone 3 React/Vite prototype continues to use mock services. Historical
implementations are retained for review, and runtime functionality has not been verified.
See [the import review](docs/AUTONOTE_IMPORT_REVIEW.md) for module relationships, security
remediation, environment limitations and proposed next steps before any integration.
