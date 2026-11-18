# Legacy AutoNote import review

> Repository layout note: this document describes the historical import when `AutoNote/` was at the repository root. The preserved source now resides in `legacy/AutoNote/`; paths in the original audit below are historical.

Reviewed 2026-11-17. This is repository preparation only. AutoNote is **not integrated**
into the Study Assistant React/Vite prototype, and its runtime functionality has **not**
been verified. Findings below come from local source/configuration inspection unless
explicitly labeled as a proposal or an inference.

## 1. Original directory and entry points

Before cleanup, the imported directory contained:

```text
AutoNote/
  .python-version, pyproject.toml, uv.lock
  README.md                         (empty; retained)
  main.py, Test.py
  servers.py, servers_v1.py, servers_v2.py
  entities.py, entities_v1.py, entities_v2.py, entities_Gao.py
  models.py, models_v1.py, models_Gao.py
  recordAPI_helper.py, recordAPI_helper_v1.py
  noteAPI_helper.py, noteAPI_helper_v1.py, noteAPI_helper_v2.py
  networkAPI_helper.py
  note_Wu.py, note_Wu_v2.py, transcriber_Wang.py
  myLogging.py, myLogging_v2.py, exception_handler.py
  testConvertJsonToResponse.py, testGPU.py, testNoteAPI.py
  api.log
  __pycache__/                      (12 compiled Python files)
  .spyproject/config/               (12 local configuration/backup files)
  .venv/                            (copied local Python environment)
```

The repository root also contained `autonote-tree.txt`, an 18,865-line generated tree
listing dominated by the copied environment. No `files/` input/output directory or
standalone recordings, transcripts, uploaded documents or model outputs were present
outside `.venv/`; educational examples are embedded in Python source.

Verified entry relationships:

- `main.py` imports `Test.py`, starts its server thread and invokes recording and note
  endpoint diagnostics. `Test.py` imports `servers.app`, binds Uvicorn to loopback port
  8000 and references a developer-specific Desktop video path. This is an integration
  harness, not an isolated unit-test runner.
- `servers.py` defines FastAPI `/test`, `/record`, `/note` and `/network` routes and
  imports the unversioned helpers, `models.py`, `entities.py`, logging and exception handling.
  `servers:app` is an apparent ASGI entry point when the working directory/import path
  is `AutoNote/`; startup was not tested.
- `servers_v1.py` and `servers_v2.py` each define a separate `app`. Both retain real
  transcription paths and illustrative note responses; neither is selected by `main.py`.
- `note_Wu.py`, `note_Wu_v2.py` and `testNoteAPI.py` read local files and call model
  services at module top level. `transcriber_Wang.py` calls `main()` unconditionally.
  Importing these scripts can perform work and incur API costs.

## 2. Modules, relationships and intentionally retained variants

All **27 Python files** are retained. Filenames alone were not used to choose winners.

| Files | Verified responsibility / reason to retain |
| --- | --- |
| `servers.py`, `servers_v1.py`, `servers_v2.py` | Current harness target plus earlier inline transcription and mock-note implementations. The variants have materially different route bodies. |
| `recordAPI_helper.py`, `recordAPI_helper_v1.py` | Temporary uploads, FFmpeg extraction, CPU/GPU selection, Whisper timestamps and GLM topic/abstract calls. The unversioned helper changes error types and selects `turbo` on CUDA versus `base` in v1. |
| `noteAPI_helper.py`, `_v1.py`, `_v2.py` | Unversioned LangChain generation and JSON conversion; v1 formatting and `eval` parsing; v2 direct OpenAI-compatible SDK calls. Different prompting, fallback and conversion behavior merits later comparison. |
| `note_Wu.py`, `note_Wu_v2.py` | Standalone note experiments. v2 uses environment loading, finish-reason fallback, different prompts and optional JSON output. |
| `transcriber_Wang.py` | Standalone FFmpeg/Whisper and DeepSeek experiment, with a hardcoded CUDA selection. |
| `entities.py`, `_v1.py`, `_v2.py`, `_Gao.py` | Pydantic transcript, note and graph structures. v1/v2 are near duplicates; unversioned adds graph types and optional transcript text; Gao differs in required/optional fields. |
| `models.py`, `models_v1.py`, `models_Gao.py` | Request/response schemas and example responses. v1 has fewer types; Gao shares substantial code but imports `api.entities`, a package absent from this copy. |
| `networkAPI_helper.py` | Attempts to construct lecture/point nodes and categories; edge generation is currently an empty list. |
| `myLogging.py`, `myLogging_v2.py`, `exception_handler.py` | File/console logging and exception responses. Versions differ in path selection, error handling and import-time directory creation. |
| `main.py`, `Test.py` | Manual server and endpoint harness; includes synthetic example network data and a machine-specific media path. |
| `testConvertJsonToResponse.py`, `testGPU.py`, `testNoteAPI.py` | Conversion example, Torch/CUDA diagnostic and live model-call experiment; retained, not treated as an automated safe test suite. |

## 3. Dependencies and environment

- `.python-version` specifies **3.12**; `pyproject.toml` requires **Python >=3.12**.
- The only declared direct dependency is `openai-whisper>=20240930`. `uv.lock` includes
  Whisper, Torch and their transitive dependencies; it is preserved unchanged. Its
  download URLs use `pypi.org` and `files.pythonhosted.org`.
- Source also imports FastAPI, Pydantic, Uvicorn, Requests, OpenAI, LangChain,
  `langchain_core`, `langchain_openai` and `python-dotenv`. Most are not covered by the
  manifest/lock. FastAPI file uploads also need a multipart parser; that requirement
  has not been tested. No dependency versions were guessed or added during import.
- FFmpeg is invoked externally. Helper code can attempt installation through Chocolatey
  or Homebrew. Whisper model loading may download weights. None of these actions ran.
- The copied `.venv/` identifies Python 3.12.8 and includes Whisper/Torch, but lacks
  the server/model-client packages. It is retained locally and ignored, including its
  internal caches; portability and operability were not established.
- The system interpreter used for static checks is Python 3.14.5. Required AutoNote
  libraries were not available there. Static parsing also checked Python 3.12 grammar.

### Credential configuration after import

`AutoNote/.env.example` contains placeholders only. Previously embedded Zhipu credentials
now come from `os.environ["ZHIPU_API_KEY"]`; the DeepSeek caller uses
`os.environ["DEEPSEEK_API_KEY"]`. Missing variables fail instead of supplying a default
credential. Existing `note_Wu_v2.py` retains LangChain's `OPENAI_API_KEY` convention with
its Zhipu base URL: that variable must contain a Zhipu credential for that script.

Export variables into the process environment before any approved future execution.
Copying `.env.example` to `.env` alone is insufficient: only some legacy scripts call
`load_dotenv()`. Provider URLs and model names were preserved; availability was not
checked. Do not use a credential from one provider against another provider's URL.

## 4. Cleanup and Git rules

Removed only confirmed local/generated artifacts:

| Removed paths | Reason |
| --- | --- |
| `AutoNote/__pycache__/entities.cpython-311.pyc`, `exception_handler.cpython-311.pyc`, `models.cpython-311.pyc`, `myLogging.cpython-311.pyc`, `networkAPI_helper.cpython-311.pyc`, `noteAPI_helper.cpython-311.pyc`, `recordAPI_helper.cpython-311.pyc`, `requestResponse.cpython-311.pyc`, `servers.cpython-311.pyc`, `serves.cpython-311.pyc`, `serves.cpython-312.pyc`, `Test.cpython-311.pyc` | 12 compiled cache files; stale cache-only module names do not establish missing reusable source. All paths in this row are under `AutoNote/__pycache__/`. |
| `AutoNote/.spyproject/config/{codestyle,encoding,vcs,workspace}.ini` | Four machine-specific Spyder settings. |
| `AutoNote/.spyproject/config/backups/{codestyle,encoding,vcs,workspace}.ini.bak` | Four IDE backup files. |
| `AutoNote/.spyproject/config/defaults/defaults-{codestyle,encoding,vcs,workspace}-0.2.0.ini` | Four generated IDE defaults. |
| `AutoNote/api.log` | 1,437,913-byte runtime log containing note/transcription-related entries and local paths; excluded from publication. |
| `autonote-tree.txt` | Regenerable root directory listing; not source or project documentation. |

All removals were untracked and therefore appear as import exclusions, not Git deletions.
The existing empty AutoNote README, `.python-version`, `pyproject.toml` and `uv.lock`
were retained. Source edits are limited to credential remediation and trailing-whitespace/
end-of-file cleanup; no modules were renamed or integrated.

Root `.gitignore` retains existing JavaScript, IDE, `.env` and `*.log` rules, adds Python
bytecode/environments/tool caches/Spyder rules, and permits `.env.example`. Narrow AutoNote
rules cover the exact transcript/converted-audio/demo-video names and the `files/*.txt`
local inputs plus timestamped Markdown/JSON outputs used by `note_Wu_v2.py`. There is no
blanket exclusion for recordings, JSON, Markdown or all `files/` contents; documentation
and fixtures in dedicated fixture directories remain trackable. No such input/output
files existed in this import. Paths are relative to the intended `AutoNote/` working
directory; older scripts also write to the user's Desktop or OS temporary directory,
which Git ignore rules cannot protect.

## 5. Security review

- Found **three distinct credential values**: 14 executable `api_key` literals in eight
  files, plus a different credential in a comment in `transcriber_Wang.py`. Replaced the
  executable literals with environment lookups and removed the comment value before
  staging. No credential values are reproduced here. Their validity was not tested.
- **The credential owners should revoke/rotate all three values.** Local removal does
  not revoke credentials or establish whether they were previously exposed elsewhere.
- Reviewed source/configuration, endpoint strings, embedded examples, local runtime
  file inventory and log content indicators. Public provider endpoints, public reference
  links, synthetic/example study content and a loopback test server were identified.
  No additional private service endpoint or database credential was identified.
- Removed the runtime log and excluded the copied environment. No standalone personal
  media or transcript files were found in the proposed import. The hardcoded local video
  path remains as historical diagnostic code; the referenced private file was not read.
- The 35 intended files passed scanning for credential formats, private-key headers,
  credential-bearing URLs and private-network HTTP endpoints; all three removed
  credential fingerprints were absent. Staged bytes matched the scanned files. This is
  a scoped static review, not a full security audit of the ignored installed environment.

## 6. Known issues and limitations (static findings)

- `/network` passes a Pydantic request to code using dictionary subscripts, and the helper
  mixes dictionary and attribute access. Its link generator is a stub. This is not a
  verified working knowledge network.
- `noteAPI_helper.py` supplies `record_text` on fallback to a prompt expecting
  `formatted_text`. The v2 converter is passed model output text but indexes it as a
  dictionary. The unversioned converter drops transcript text and looks up links at
  the top level. These behaviors need contract tests before reuse.
- `noteAPI_helper_v1.py` evaluates generated output with `eval`; it must not be exposed
  to untrusted model output. Other versions are retained for comparison, not endorsed.
- FFmpeg commands interpolate paths with `shell=True`; uploads lack production limits
  and authentication. Conversion handling, temporary-file cleanup and error disclosure
  require review. No production authorization or privacy boundary was found in the routes.
- Fixed transcript filenames can collide; upload processing reads the entire file,
  blocking work is called inside async routes, and models are loaded per request.
  Several diagnostics read/write Desktop files or print/log generated content.
- `transcriber_Wang.py` forces CUDA even after detecting CPU; historical module imports
  and server schemas are inconsistent. `Test.py` also contains `logging.inof`.
- Prompt examples and response shapes are experimental. Character counts are used as
  token heuristics, and provider/model availability and output accuracy remain unverified.

## 7. Verification

- Existing `npm test`: **7 passed, 0 failed**, using Node 24.15.0.
- All **27** Python files parsed with Python 3.12 grammar and compiled in memory on
  Python 3.14.5. No legacy module was imported or executed; no bytecode was generated.
- Hash comparison confirms all previously tracked files remain byte-identical except
  the intended root README and `.gitignore` edits. Frontend code, tests, package manifests
  and existing docs/screens were not changed.
- Ignore checks cover **18** secret/cache/runtime paths and **36** paths that must remain
  trackable, including all Python sources, manifests, the example environment, review
  documentation and representative fixtures.
- `git diff --check` and `git diff --cached --check` passed. The staged allowlist contained
  exactly the 35 intended files, with no logs, caches, local environments or real secrets.
  Commit/push and final status are recorded in the task completion report.
- Frontend production build/browser tests were not run because this checkout has no
  `node_modules`; no dependency installation was needed for this preparation-only change.
- AutoNote runtime/API/GPU/conversion diagnostics were not run: dependencies are incomplete,
  several scripts call paid APIs or process local media, and model downloads were outside
  scope. A syntax pass does not demonstrate runtime functionality.

## 8. Potential reuse and proposed next steps

The following are proposals, not completed integrations:

1. Compare the retained variants using small synthetic fixtures and offline provider mocks.
   First define stable transcript, note, material and quiz contracts plus error behavior.
2. Consider timestamped transcription, FFmpeg media extraction, structured note generation,
   Pydantic validation and transcript-to-note references as reuse candidates. The existing
   code does not implement the prototype's full quiz, grading or deadline workflows.
3. Decide whether a separate Python processing worker behind the proposed Express API is
   appropriate. Preserve the React service boundary and enforce identity/course access on
   the server. Avoid embedding blocking model work directly into web request handlers.
4. Reconcile and pin required dependencies in an isolated environment, review provider
   credentials/endpoints, and remove import-time execution before controlled smoke tests.
5. Replace `eval`, unsafe shell construction and sensitive logging; add bounded uploads,
   unique temporary files, cleanup, timeouts and cost controls before any live processing.
6. Evaluate output quality, latency, retention/privacy and recovery with approved sample
   data before selecting implementations or changing application behavior.
