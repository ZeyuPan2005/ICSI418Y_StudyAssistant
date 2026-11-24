# Database owner — read here

**Owner:** one Atlas/persistence developer. All five selected stories need durable data; you own the shared storage boundary, not individual HTTP routes.

## Read in order
1. [Team responsibilities](../TEAM_ASSIGNMENTS.md) + [acceptance](../ACCEPTANCE_MATRIX.md).
2. [Persistence contract](PERSISTENCE_CONTRACT.md) — method ownership, uniqueness, isolation, stored file references and AI artifacts.
3. [AD-02 Data Model `3](../DATA_MODEL.md#3-logical-entities-and-proposed-fields), [`5](../DATA_MODEL.md#5-proposed-mongodb-storage-design) and [`8](../DATA_MODEL.md#8-proposed-attempt-and-result-lifecycle).
4. [HTTP API DTOs](../contracts/HTTP_API.md), [AI internal outputs](../backend/ai/AI_MODEL_CONTRACT.md).

## Your delivery
- Controlled nonproduction Atlas config, dev/test isolation, safe connection and retry/close, data schema/index proposal and idempotent fictional seed.
- Named repository methods to Backend A/B/C; let business owners apply permissions, never trust a client-supplied user/role/score.
- Persist actual uploaded-file metadata and server-owned file reference, converted content/safe provenance, Quiz snapshots/answer keys, one Attempt per Quiz, immutable submitted Result, deadlines. Keep raw files in **protected server storage**, not the Vite public directory.
- Reconcile failure when disk bytes succeeded but Atlas metadata failed. Keep sensitive AI/model keys out of MongoDB, source and logs; review any external model disclosure of lecture content.
- Coordinate whether AI feedback is stored as separate status/version record linked to immutable Result.

**First artifact:** schema/index/seed and repository API proposal, reviewed with all three Backend owners. Do not claim actual Atlas verification until a permitted dev database is connected and exercised.
