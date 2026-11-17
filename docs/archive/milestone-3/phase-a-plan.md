# Study Assistant UI prototype plan

> Archived from the completed Milestone 3 prototype. Folder layouts and approval steps
> below describe that historical plan. See the [current README](../../../README.md)
> and [design assumptions](../../design-assumptions.md) for present development context.

Team 01 · ICSI 418Y · Milestone 3 Part 4 · Phase A approved with refinements

The student demonstration follows a lecture from upload through quiz, feedback and targeted practice. The deadline demonstration follows one item from the teacher’s form to the student’s dashboard, including what the student sees after the teacher changes its date.

## Scope and repository

Build a standalone React prototype in the new Study-Assistant-Prototype folder under Milestone 3 after approval. Use Milestone 2 sections 1–4 as the requirements baseline. For Milestone 3 section 4, capture labeled screens and enough intermediate states to explain each workflow within the report. Reuse these screen IDs when the team connects its DFD and ERD to the use cases in section 5.

## Screen inventory and requirement mapping

| Screen and role | Use cases | User stories | Inputs, actions and feedback |
|---|---|---|---|
| UI-01 Course Dashboard · both | Entry to UC-01–05, deadline display in UC-05 | US-01–07 by role | Select an accessible course. Show lecture materials, student quizzes/results, and upcoming dates. The teacher’s results section expands a submitted score to show the student’s responses. Include empty lists and denied access to unassigned courses. |
| UI-02 Upload Lecture Material · both | UC-01 | US-01 | Choose course and file, validate, review name and size, then confirm. Missing, unsupported, and zero-byte files show inline errors and add no lecture. Accepted uploads show simulated processing, then ready with a link to UI-03. |
| UI-03 Lecture Details and Quiz Generation · both read, student generates | UC-01, UC-02 | US-01, US-02 | Show lecture, course, status and sample topics. From ready, generate a mock quiz, show progress, then preview every question and option before Start. Unusable content explains the block. Generator failure offers retry without creating an empty quiz or changing existing records. |
| UI-04 Quiz Taking · student | UC-03, UC-04 practice | US-03, US-04 | Select answers and submit. Identify unanswered items, focus the first error, and keep selected answers. Retain a draft through simulated interruption and retry. A complete submission saves one result and opens UI-05. |
| UI-05 Quiz Results and Feedback · student | UC-03, UC-04 | US-03, US-04 | Display score, selected and correct answers, text labels for missed items and their topics. Open follow-up practice from a mixed result. Explain why targeted review is unnecessary after a perfect result. |
| UI-06 Follow-up Practice · student | UC-04 | US-04 | Show missed topics for the source result. Generate a separate quiz using new questions on those topics, preview it and start in UI-04. Return to the source result at any time. A perfect result yields no new quiz. |
| UI-07 Teacher Deadline Management · assigned teacher | UC-05 | US-05, US-06 | Create, update and remove lecture or homework dates. Collect title, type and date, identify invalid fields inline, and confirm successful changes. Deny direct student access and provide a link to the read-only course view. |
| UI-08 Student Deadline View · student | UC-05 | US-05, US-06 | Show current and future course deadlines sorted by date, with title, type, date and an Upcoming text label inside the reminder window. Include empty, changed and removed states shared with UI-01. |

Use one shared header with the demo role switcher, course selector, reset action and simulation label. Student navigation exposes Course Dashboard, Lecture Materials, Quizzes / Results, and Upcoming Deadlines. Teacher navigation exposes Course Dashboard, Lecture Materials, Deadline Management, and Student Quiz Results. The lecture index, personal quiz index and teacher results are addressable sections of UI-01. The final teacher results view uses the variant label UI-01T. This reuse gives US-07 a direct navigation destination without adding a ninth screen. Changing roles returns to an accessible course.

## Proposed structure and component plan

```text
Study-Assistant-Prototype/
  phase-a-plan.md
  package.json, index.html, vite.config.js
  src/
    main.jsx, App.jsx      React entry, React Router routes and role checks
    screens/              One page component per UI ID
    components/           Layout, course picker, question list, deadline list, inline feedback
    state/                Demo provider, active identity/course and browser persistence
    services/             Mock materials, quizzes, submissions, results and deadlines
    data/                 Fictional seed records and topic-tagged question banks
    styles/               Plain CSS for layout, forms, validation and keyboard focus
  README.md
  docs/
    ui-mapping.md
    design-assumptions.md
    demo-checklist.md
```

Use Vite, React, JavaScript/JSX, React Router and plain CSS. A shared question list supports preview, answering and graded review. One deadline selector serves the dashboard and full deadline list so both show the same reminders. Screens call mock services that check course assignment, role and attempt ownership at read/write time. Demo role switching and browser storage provide no production authentication or authorization. These functions provide the integration points for a future Express backend, MongoDB and AI service.

Use a desktop-first grayscale layout, native rectangular controls, a small UI ID beside each heading, visible keyboard focus, grouped radio buttons, and textual validation and progress messages. Put “Demo · local sample data” in the header and label simulated operations where the user triggers them. Form labels, status feedback and screenshot captions should remain readable at report scale.

## Mock data model

| Records | Relationships and behavior |
|---|---|
| User, Course, CourseMembership | Store IDs, names, roles and course assignments. Seed two students, one teacher and two courses. Assign the teacher to course A only and the demo student to A and B. Seed submitted results in both courses to test isolation. |
| LectureMaterial, Topic | Track course, uploader, filename, size, processing status, fixture reference and topic IDs. Seed a ready lecture, an unusable-content lecture and a ready lecture that fails its first generation request. A valid new upload uses a labeled sample fixture for its course. |
| Question, Quiz | Each question has an ID, topic, prompt, options and answer key. A quiz records lecture, student, ordered questions, kind and optional source result ID. Use ten questions for the lecture demo, plus distinct practice items for every eligible topic. |
| Attempt, Answer, Result | A draft links student, quiz and selected answers by question ID. Successful submission saves a grading snapshot, score, missed topics and timestamp once. A practice quiz gets its own attempt and result linked back to the source result. Preserve the original quiz, attempt, answers, score and result when creating practice. Teacher review reads submitted attempts only. |
| Deadline | Store ID, course, author, title, type and local calendar date. Derive upcoming labels from current records and today's date whenever the course view opens or changes. |

Use Software Engineering as course A, with lecture topics such as requirements and acceptance criteria. Seed a mixed score, a perfect score, an unsubmitted attempt, and deadlines relative to the demo date. Persist records and drafts in local storage and provide a reset to restore the fixtures. Read file metadata for validation. Browser file selection, metadata validation and confirmation are interactive. The demo stores metadata and uses a course fixture. It does not transcribe audio, parse slides or extract concepts. Simulate processing, question selection and interruption locally.

## Decisions for review

| Requirement or ambiguity | Proposed treatment |
|---|---|
| Milestone 1 describes catered quizzes as a further goal. Milestone 2 makes follow-up practice MVP in US-04 and UC-04. | Follow the submitted Milestone 2 scope and demonstrate the complete practice workflow, including preservation of the source result. |
| Milestone 1 mentions both training a model and using an API. Milestone 2 leaves the generation method open. | Keep production model selection open. Use a predefined topic-tagged question bank for the prototype and identify the sample content on screen. |
| Milestone 2 allows a course or study area and leaves enrollment and formats open. | Use preassigned courses. Provisionally accept MP3 and WAV audio, PDF and PPTX slides. Validate supported extension and nonzero size before confirmation. |
| Reminder delivery, window and date rules need a demo convention. | Use in-app reminders. Propose a seven-day look-ahead including today and the date seven calendar days ahead. Day eight has no badge. Accept any valid local calendar date, including past dates. Show current and future items in student views. Keep the window configurable in one place. |
| US-07 is MVP outside the five critical use cases. | Provide scores and submitted answers in the teacher’s assigned-course dashboard. Defer analytics and additional reporting. |
| Milestone 2 includes six nonfunctional requirements. | Demonstrate NFR-03 role and ownership checks, NFR-05 keyboard operation and NFR-06 draft retention on simulated interruption. Defer real-service benchmarking (NFR-01/02), the five-user study (NFR-04), server authorization and real connection recovery verification. |

## Implementation and verification after approval

1. Build the mock services, shared components and eight views. Document startup, structure, roles, simulated behavior, limitations and integration in the README. Expand the screen table, design decisions and demo steps into the three planned documentation files.
2. Install dependencies, start the Vite app, traverse both navigation menus and run the production build. Use browser automation when available and record actual results.
3. **UC-01.** Try missing, unsupported and zero-byte files. Confirm the lecture list is unchanged. Upload a valid file as each role and follow accepted → processing → ready in the selected course.
4. **UC-02.** Try the no-content fixture and the generator failure. Check the quiz count before and after failure. Retry the latter successfully, then inspect the questions and choices before starting.
5. **UC-03.** Submit with one blank answer, check the field error and retained choices, then correct it. Interrupt one submission and retry. Check the single saved score and missed answers. Repeat upload, answering and submission with only the keyboard.
6. **UC-04.** Record the source result ID, score and answers. Generate and complete practice, verify all new items target missed topics, then reopen the original and compare the recorded values. Open a perfect result and verify no practice quiz is created.
7. **UC-05.** Try blank title, missing type and invalid date. Publish a valid deadline seven days ahead. Check the student dashboard and deadline view, move the date to day eight and check the badge disappears, then remove the deadline and check both lists. Verify course isolation and denial of student create, edit and delete actions.
8. **US-07 and privacy.** Verify an assigned teacher can see submitted answers and scores, a draft stays out of finished results, and an unassigned course is denied. Try another student's direct result link as the demo student and verify denial. Navigate, reload and reset to check reproducibility.
9. Capture labeled screens and selected error states for Milestone 3 Part 4. Record checks executed and remaining limitations.
