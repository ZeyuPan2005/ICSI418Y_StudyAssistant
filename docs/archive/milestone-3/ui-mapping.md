# UI mapping for Milestone 3 Part 4

Archived screen-to-requirement mapping from the completed prototype. The report-only PNG
captures have been removed; see the [archive index](README.md) for their Git history and
current screenshot output location. UI-01 identifies the course dashboard and UI-01T
its dedicated Student Quiz Results view. Both use the same dashboard component.

| UI ID and screen | Use case | User stories | Actions and states |
|---|---|---|---|
| UI-01 Course Dashboard | Entry to UC-01–05, student display for UC-05 | US-01–07 by role | Course selection, lecture list, draft quizzes, saved results and reminders. |
| UI-01T Student Quiz Results (UI-01 variant) | Dashboard review | US-07 | Assigned-course teacher expands a submitted attempt to inspect the score and responses. |
| UI-02 Upload Lecture Material | UC-01 Upload lecture material | US-01 | Choose a course and file, review metadata, confirm. Missing, unsupported or empty selection yields an inline error. Accepted upload shows simulated processing and ready. |
| UI-03 Lecture Details and Quiz Generation | UC-01, UC-02 Generate a lecture quiz | US-01, US-02 | Ready and unusable fixtures, generation in progress, failed request, retry, question and choice preview before Start. |
| UI-04 Quiz Taking | UC-03 Submit and review quiz answers, reused by UC-04 | US-03, US-04 | Unanswered, answered, validation with retained selections, simulated interrupted submission, retry and completion. |
| UI-05 Quiz Results and Feedback | UC-03, UC-04 Generate follow-up practice | US-03, US-04 | Saved score, selected answers, correct/incorrect feedback, missed topics, link to practice or a perfect-score explanation. |
| UI-06 Follow-up Practice | UC-04 | US-04 | Source result, weak topics, separate practice quiz preview, Start practice. A perfect source has no applicable questions. |
| UI-07 Teacher Deadline Management | UC-05 Publish and display a course deadline | US-05, US-06 | Enter title, type and date, resolve field errors, publish, edit, remove. Direct student requests are denied. |
| UI-08 Student Deadline View | UC-05 | US-05, US-06 | Read-only dated list, Upcoming within the window, later dates without a badge, empty list. Changed and removed dates update here and on UI-01. |

## Paths through the screens

- UC-01 · UI-01 → UI-02 → UI-03.
- UC-02 · UI-01 → UI-03 → UI-04 after preview.
- UC-03 · UI-04 → UI-05. An incomplete or interrupted submission stays on UI-04.
- UC-04 · UI-05 → UI-06 → UI-04 → UI-05. The practice result links back to the original result.
- UC-05 · Teacher UI-07 → Student UI-01 and UI-08. Changing roles demonstrates the same course from both sides.
- US-07 · Teacher UI-01 → UI-01T Student Quiz Results → expand a submitted attempt. The course selector and mock service apply the teacher’s course assignments.
