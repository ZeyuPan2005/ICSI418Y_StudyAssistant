# AI model ↔ Express internal integration contract

**Status:** v0.1 **TEAM REVIEW PROPOSAL**, not implemented and not yet reconciled with the earlier predefined-question-bank AD-03/04 plan. This contract describes the team's desired direction: **Express calls the AI model and receives structured results; Express validates, applies business rules, persists data, and responds to React.**

**Owners:** Backend B owns the AI adapter/model prompts/transcription/conversion/validation-at-edge; Backend C owns Quiz/Attempt/Result business orchestration and immutable grading/Result state; Backend A owns shared authentication, authorization and transport; Database owns persistence interfaces. Frontend is a consumer of Express only.

## 1. One architecture boundary (not three extra public APIs)

`Browser → Express controller (A middleware) → application service (B material processing / C quiz or result) → AiGateway (B-owned) → model SDK or protected Python sidecar → AiGateway normalized JSON → Express validate/domain rules → Database repositories → safe HTTP response to browser.`

- **Default preference:** `AiGateway` is a Node interface imported by Express application services. The implementation may call a third-party hosted model through its SDK/HTTPS. **No separate public REST port for AI is required**.
- **Alternative:** if Python/Whisper/legacy conversion requires its own runtime, implement a private local authenticated HTTP bridge behind the *same* `AiGateway` shape; only Express speaks to it, never React. Host/port, timeout, authentication, request/response schemas, limits and lifecycle must be explicitly approved before implementing a sidecar. The historical `legacy/AutoNote/` is **not** approved for direct import.
- The AI module never reads browser sessions, decides privileges, writes Atlas collections, publishes private file paths, or finalizes grades. AI outputs are **untrusted input** even if schema-valid.

## 2. Proposed common TypeScript-style interface (can be implemented in JavaScript)

```ts
interface AiGateway {
  convertMaterial(input: {
    materialId: string;
    filename: string;
    mimeType: string;
    bytes: Uint8Array;        // trusted, size-bounded server-side bytes
    requestId: string;
  }): Promise<ConvertedContent>;

  generateQuiz(input: {
    materialId: string;
    courseId: string;
    content: ConvertedContent; // server-verified converted lecture
    topicIds: string[];
    questionCount: 10;
    requestId: string;
  }): Promise<GeneratedQuizDraft>;

  generateFeedback(input: {
    resultId: string;
    score: number; total: number; // authoritative Express-computed values
    missed: Array<{
      snapshotQuestionId: string;
      prompt: string;
      chosenOptionText: string;
      correctOptionText: string;
      topicIds: string[];
    }>;
    requestId: string;
  }): Promise<FeedbackDraft>;
}
```

`requestId` is diagnostic correlation, **not** proof of identity or idempotency. Do not place passwords, user emails, session tokens, raw file paths, or answer-key maps into model logs. The input `bytes` is provided by a protected server-side file adapter, never a client path. Review memory/size limits, especially for audio.

## 3. Conversion: raw lecture → structured educational content

**Trigger owner:** Backend B's Material Service, after protected bytes and metadata have been accepted. Convert PDF/PPTX text or transcribe MP3/WAV; optionally structure lecture notes with AI. Deterministic extraction may precede the model, but the **Conversion capability** is model-integrated as requested by the team.

**Proposed response:**

```json
{
  "language":"en",
  "plainText":"Functional requirements describe system behaviors...",
  "sections":[{"sectionId":"s1","title":"Requirements","text":"Functional requirements ..."}],
  "warnings":[]
}
```

Express checks nonempty usable content, size/language/structure, source association and status, then stores *authorized* converted data. **Uploading file bytes is not proof of completed conversion**. Show Material `conversionStatus` such as `notStarted | processing | ready | failed`; approved state transitions and whether processing happens at upload or via `POST .../process` remain OPEN. Do not claim a background worker exists. Audio conversion may exceed a request timeout: choose bounded synchronous requests or an explicit queued design before coding.

## 4. AI Quiz Generation: converted material → ten question candidates

**Trigger owner:** Backend C's Quiz Service. It loads the authorized converted material and calls Backend B's `generateQuiz`. AI returns **candidates**, not persisted Quizzes, Attempts or Results.

```json
{
  "questions":[
    {
      "prompt":"Which behavior is a functional requirement?",
      "options":[
        {"optionId":"a","text":"The system allows file upload"},
        {"optionId":"b","text":"Page loads in under two seconds"}
      ],
      "correctOptionId":"a",
      "explanation":"File upload is a functional behavior.",
      "topicIds":["topic-1"],
      "sourceRefs":[{"sectionId":"s1","quote":"The system allows file upload"}]
    }
  ]
}
```

The example shows **one item only** for readability. A successful regular Quiz requires **exactly 10 validated, distinct items**. Backend C validates schema, unique options/questions, correct key within options, approved Topics and source relevance; a sourceRefs string is a clue for review, **not proof of factual grounding**. Reject invalid/partial generation rather than quietly replacing it with unrelated bank questions; disclose actual model/source in internal provenance.

Backend C assigns stable question snapshot IDs and stores answer keys/explanations privately. The **browser preview** gets only `{snapshotQuestionId,prompt,options,topics}` — never `correctOptionId`, correct-answer rationale, prompt, or provider secrets. Generation returns persisted Quiz and **does not create an Attempt**; Start does.

## 5. AI Feedback: graded Result → explanatory suggestions

**Trigger owner:** Backend C's Result Service *after* validating answers, deterministic score computation and immutable Result persistence. Calls Backend B's `generateFeedback` with minimum required question text/choices, **without user identity or session data**.

```json
{
  "summary":"Review the difference between functional and non-functional requirements.",
  "perQuestion":[{"snapshotQuestionId":"item-3","explanation":"A latency limit is a performance constraint, not a user action."}],
  "suggestions":["Compare examples from section s1 of the lecture."]
}
```

**Separation:** AI produces explanations/suggestions, not the final score or which options are marked correct. If AI feedback times out/fails, the submitted score/answers/Result **remain valid and unchanged**. Proposed handling: separate `ResultFeedback` record/status (`pending / available / failed`), linked to Result and versioned; frontend can show “Score ready; AI explanation unavailable”. Do not mutate the immutable final Result to hide the failure. Whether to add `GET /api/results/:resultId/ai-feedback` or embed a safe separate feedback projection is OPEN. Basic correctness feedback required by M2 US-03 should still work without AI.

## 6. Error, timeout, safety and test contract

- Shared error classes are **proposed**: `AI_UNAVAILABLE`, `CONVERSION_FAILED`, `AI_INVALID_OUTPUT`, `AI_TIMEOUT`, `AI_UNSAFE_CONTENT`. Express converts them to safe HTTP error/status under the [HTTP contract](../../contracts/HTTP_API.md); raw model errors, stack traces, keys and prompt data must not go to browser.
- All outgoing model requests must have bounded timeouts, bounded input/output sizes, validation and cost/rate controls; do not automatically retry a possibly charged or non-idempotent model call without explicit policy. The Express operation ID controls **persistence idempotency**, not provider billing.
- Treat uploaded lecture text as **untrusted prompt content**: ignore instructions embedded in the lecture that try to override system behavior or reveal keys. Use schema validation and server-side constraints; never trust generated JSON to grant roles, select another Course, or mark grade authoritative.
- External provider transfer is subject to team/instructor-approved privacy and data-handling policy. Test first on **fictional lecture material**, not real class recordings or student answers. API keys are environment injected and never checked into Git.
- Backend B supplies **fixture responses** for all 3 methods, including malformed JSON, nonempty/empty conversion, exactly 9/10/11 candidate counts, invalid correct option, irrelevant topic/source, provider timeout and network error. Backend C tests no partial Quiz/Result mutation, safe preview and grade preservation. DB tests stored versions/uniqueness and idempotent attempts.
- Integration evidence: **Express → AI stub → Express validation/persistence → authorized HTTP response** first, then opt-in live provider smoke with redacted logs. The current frontend Demo service tests do **not** prove this path.

## 7. Decision checklist to freeze before implementation

1. Node SDK direct integration versus private Python sidecar; approved model/provider for transcription/notes/quiz/feedback and key management.
2. Conversion at upload versus explicit `process`; synchronous timeout versus queued status/lifecycle; accepted file sizes/types and sanitized output storage.
3. Exactly ten quiz items, output JSON validation and human source-grounding review; model-output rejection/retry policy and immutable snapshot provenance.
4. AI feedback timing, storage/GET shape, privacy policy and cost cap; grades remain deterministic regardless.
5. Update/reconcile [AD-03](../../API_CONTRACT.md) and [AD-04](../../IMPLEMENTATION_PLAN.md) to record approved AI scope deviations. Do not label proposed interfaces production-ready.
