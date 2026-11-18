# Legacy AutoNote experiments

AutoNote explored lecture audio transcription, structured note generation and
knowledge-network generation through experimental Python scripts, FastAPI entry points
and external model integrations. The source and versioned/collaborator variants are
preserved for historical comparison and possible future evaluation.

**AutoNote is not part of the current Study Assistant Phase 1 runtime.** The React/Vite
Demo and planned core backend do not require these scripts or their services.

Dependencies are incomplete and runtime behavior is unverified. Some historical scripts
perform file processing, model calls or other work at import time; some also contain unsafe
parsing or shell patterns. Do not run/import them automatically during setup, application
startup, tests or cleanup, and do not treat `Test.py` or similarly named experiments as a
safe automated test suite.

Any future reuse needs a separately reviewed security/dependency evaluation, controlled
inputs, explicit credential handling and validation of the selected entry point. This
README does not authorize installing dependencies, downloading models or calling services.

See the [AutoNote import review](../docs/AUTONOTE_IMPORT_REVIEW.md) for module relationships,
known risks and credential-remediation history. For the runnable prototype and team setup,
use the [root README](../README.md). Historical credentials previously removed from source
still require owner-managed revocation/rotation; removal alone does not establish that.
