# Backend ↔ Persistence contract

**Status:** Proposed; physical collections, indexes, transactions and method signatures require Database + domain-owner review. See [full AD-02](../DATA_MODEL.md).

## Ownership map

| Data / repository boundary | Primary business owner | Database owner supplies / checks |
| --- | --- | --- |
| User, Course, CourseMembership, Session | Backend A | users, offerings, membership retrieval; nonproduction seed, valid uniqueness |
| Deadline | Backend A | atomic create/edit/delete, course listing; date-only index |
| LectureMaterial, protected file reference, converted content | Backend B | material/status and converted-content storage, file reference relationship |
| Question candidates / Quiz snapshots | Backend C (from B AI provider) | Quiz write with frozen keys, provenance, owner/course; unique operation identity |
| Attempt, Result, optional ResultFeedback | Backend C | conditional revision updates, one Attempt per Quiz, one final Result per Attempt, feedback isolation |

**Never let the AI adapter write Quiz, Answer, Result or grade rows directly.** Backend C validates AI candidates and calls repositories. Backend A authorizes identities/courses in the request path; downstream module owners re-check resource ownership/course.

## Suggested operation-level signatures — negotiate before implementation

- `findAssignedCourses(userId)`, `findCourseMembership(userId,courseId)`; `listDeadlines(courseId,actor)`, `saveDeadline(...)`.
- `createMaterialAndFileReference(metadata, operationId)`, `setMaterialConversionState(materialId, expectedState, conversion)`, `getAuthorizedMaterial(...)`.
- `createQuizSnapshot(ownerId,materialId,questions,operationId)`; `findQuizForOperation(...)`.
- `getOrCreateAttempt(quizId,ownerId)`, `replaceDraftAnswers(attemptId,expectedRevision,answers)`, `finalizeAttemptOnce(attemptId,expectedRevision,allAnswers,resultData)`, `getResultByAttempt(...)`.
- `storeOrUpdateAIExplanation(resultId, feedbackStatus, version, explanation)` — optional separate record; **never mutate final grade/answers**.

These are illustrative service interfaces, not permission to bypass data invariants.

## Invariants and proof

1. Identity/course ownership checked using server principal and trusted stored membership; no browser-provided membership/score.
2. Material success = bytes + associated Atlas metadata persisted. Converted content has separate status. Lost responses have recoverable operation IDs.
3. Quiz creation = exactly ten validated source-related question snapshots, with keys hidden in preview. An AI exception/invalid schema does not persist an invalid/partial Quiz.
4. Exactly one Draft Attempt per Quiz and one immutable submitted Result per Attempt. Conditional saves reject stale revisions; duplicate submits return the existing outcome without regrading.
5. Teacher deadline edits visible to authorized Students; student writes denied at backend.
6. Provide integration tests with actual nonproduction Atlas state and restart; test bad credentials/unavailable DB, uniqueness collision, loss of connection and cross-course data access.

**Team freeze points:** collection names, unique compound indexes, generation idempotency key, session store, file storage root and two-phase disk/Atlas cleanup, converted-content representation, AI-feedback storage. Never place secrets, real student recordings or private data in Git.
