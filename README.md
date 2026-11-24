# Study Assistant

ICSI 418Y Software Engineering team project. Study Assistant supports lecture materials, study quizzes, feedback, upcoming deadlines, and future targeted practice and teacher review.

## Project status

- **Working now:** React/Vite **Demo** using fictional accounts, predefined questions, client-side grading and browser-local state. Its tests prove Demo behavior only.
- **Planned, not implemented:** Express application backend, real authentication/course permissions, MongoDB Atlas persistence, real lecture uploads, server-side grading, and the **separate private Python AI HTTP service**.
- **Current implementation target:** **US-01, US-02, US-03, US-05, US-06** (five of seven original MVP user stories). A story is Complete only after all its original acceptance criteria are verified. US-04 and US-07 remain later work.
- **Architecture choice:** React calls **Express**; Express authorizes, calls **private Python AI HTTP endpoints** for Conversion, Quiz Generation and optional explanatory Feedback, validates model outputs, persists via Atlas repositories, then responds to React. The earlier Phase 1 predefined-question-bank approach is preserved as design history, **not the intended implementation for US-02**.

**Start here: [Team documentation and role-specific reading guide](docs/README.md).** Read the shared handoff first, then your responsibility folder. The older AD-01–04 are detailed references, **not required cover-to-cover reading for everybody**.

## Repository layout

| Path | Purpose |
| --- | --- |
| [client/](client/) | Runnable React/Vite Demo; future real API client |
| [server/](server/README.md) | Planned Node/Express application, currently a placeholder |
| [docs/](docs/README.md) | Role-first onboarding, HTTP/AI/persistence contracts, requirements and design references |
| [legacy/](legacy/README.md) | Historical AutoNote experiments; **not** the approved Python AI service |
| [.gitignore](.gitignore) | Ignore environment files and generated artifacts |

### Who reads what?

| Responsibility | First document |
| --- | --- |
| **All five** | [docs/README.md](docs/README.md), [team roles](docs/team/TEAM_ASSIGNMENTS.md), [acceptance](docs/requirements/ACCEPTANCE_MATRIX.md), [public HTTP agreement](docs/contracts/HTTP_API.md) |
| **Frontend** | [Frontend guide](docs/frontend/README.md) |
| **Database** | [Database guide](docs/database/README.md) |
| **Backend A — Express/Auth/Deadlines** | [Backend A guide](docs/backend/express/README.md) |
| **Backend B — Materials/Python AI** | [Backend B guide](docs/backend/ai/README.md) |
| **Backend C — Quiz/Grading/Results** | [Backend C guide](docs/backend/learning/README.md) |

The central cross-service agreement is [Express ↔ Python AI HTTP protocol](docs/backend/ai/PYTHON_HTTP_PROTOCOL.md). The [decision register](docs/team/DECISIONS.md) separates selected architectural choices from proposed transport details.

## Run the current frontend Demo

**Requirements:** Node.js 22.12+ and npm. From the repository root:

```sh
cd client
npm ci
npm run dev
```

Open the local address printed by Vite. Running the **Demo** does not require Express, Atlas or Python. Choose a Student or Teacher Demo role; uploaded files, quiz questions, grades and deadlines are simulated and stored locally, not on the server.

## Test the existing frontend Demo

Run from `client/` after `npm ci`:

```sh
npm test
npm run build
npm run test:browser
```

These verify **Demo** behavior, not the future backend. Browser tests default to Edge; `BROWSER_PATH` can select a compatible Chromium executable. Test screenshots are generated in ignored `client/test-results/screens/`.

## Development collaboration

1. Read [role ownership](docs/team/TEAM_ASSIGNMENTS.md) and your role guide; agree the interface details marked OPEN before integration.
2. Create a task-focused branch; prefer small Pull Requests and review by another team member.
3. Preserve Demo behavior while implementing real API-backed flows. Never fall back to Demo identities, simulated grades or fixtures when a real API fails.
4. Backend A owns shared Express configuration/security; Backend B owns private Python AI processing and Material routes; Backend C owns Quiz/Attempt/Result workflows; Database owns the persistence boundary; Frontend consumes Express only.
5. Run and report relevant tests, plus real end-to-end evidence for every story marked Complete. Document limitations and individual contributions.
6. Do not commit model/API keys, service-to-service secrets, authentic student recordings/answers, local environment files or generated artifacts.

**Security:** Historical [AutoNote](legacy/AutoNote/README.md) is experimental and must not be executed or imported as the current Python service without separate review. See the [security audit](docs/archive/AUTONOTE_IMPORT_REVIEW.md); historical exposed credentials may still require revocation/rotation.
