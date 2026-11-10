# UI mapping for Milestone 3 Part 4

Use the screen IDs printed above each page heading in report captions and in the section 5 consistency table. Each linked PNG is a browser capture of the local prototype. Use UI-01 for the course dashboard and UI-01T for its dedicated Student Quiz Results view. Both use the same dashboard component.

| UI ID and screen | Use case | User stories | Actions and states | Report capture |
|---|---|---|---|---|
| UI-01 Course Dashboard | Entry to UC-01–05, student display for UC-05 | US-01–07 by role | Course selection, lecture list, draft quizzes, saved results and reminders. | [Student dashboard](screens/UI-01-dashboard.png) |
| UI-01T Student Quiz Results (UI-01 variant) | Dashboard review | US-07 | Assigned-course teacher expands a submitted attempt to inspect the score and responses. | [Teacher results](screens/UI-01T-teacher-results.png) |
| UI-02 Upload Lecture Material | UC-01 Upload lecture material | US-01 | Choose a course and file, review metadata, confirm. Missing, unsupported or empty selection yields an inline error. Accepted upload shows simulated processing and ready. | [Rejected file](screens/UI-02-invalid-file.png), [processing](screens/UI-02-processing.png) |
| UI-03 Lecture Details and Quiz Generation | UC-01, UC-02 Generate a lecture quiz | US-01, US-02 | Ready and unusable fixtures, generation in progress, failed request, retry, question and choice preview before Start. | [Generation failure](screens/UI-03-generation-failure.png), [preview](screens/UI-03-preview.png) |
| UI-04 Quiz Taking | UC-03 Submit and review quiz answers, reused by UC-04 | US-03, US-04 | Unanswered, answered, validation with retained selections, simulated interrupted submission, retry and completion. | [Incomplete submission](screens/UI-04-incomplete.png) |
| UI-05 Quiz Results and Feedback | UC-03, UC-04 Generate follow-up practice | US-03, US-04 | Saved score, selected answers, correct/incorrect feedback, missed topics, link to practice or a perfect-score explanation. | [Graded result](screens/UI-05-result.png) |
| UI-06 Follow-up Practice | UC-04 | US-04 | Source result, weak topics, separate practice quiz preview, Start practice. A perfect source has no applicable questions. | [Generated practice](screens/UI-06-practice.png) |
| UI-07 Teacher Deadline Management | UC-05 Publish and display a course deadline | US-05, US-06 | Enter title, type and date, resolve field errors, publish, edit, remove. Direct student requests are denied. | [Published deadline](screens/UI-07-published.png) |
| UI-08 Student Deadline View | UC-05 | US-05, US-06 | Read-only dated list, Upcoming within the window, later dates without a badge, empty list. Changed and removed dates update here and on UI-01. | [Student reminder](screens/UI-08-upcoming.png) |

## Paths through the screens

- UC-01 · UI-01 → UI-02 → UI-03.
- UC-02 · UI-01 → UI-03 → UI-04 after preview.
- UC-03 · UI-04 → UI-05. An incomplete or interrupted submission stays on UI-04.
- UC-04 · UI-05 → UI-06 → UI-04 → UI-05. The practice result links back to the original result.
- UC-05 · Teacher UI-07 → Student UI-01 and UI-08. Changing roles demonstrates the same course from both sides.
- US-07 · Teacher UI-01 → UI-01T Student Quiz Results → expand a submitted attempt. The course selector and mock service apply the teacher’s course assignments.
