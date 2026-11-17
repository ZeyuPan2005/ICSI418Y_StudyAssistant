# Demonstration and verification checklist

Archived manual acceptance walkthrough and historical test results. For current setup and
test commands, use the [root README](../../../README.md). Start the app and open Software
Engineering as Student; reset demo data before repeating the steps. The [UI mapping](ui-mapping.md)
preserves the workflow references. Report captures were removed as described in the [archive index](README.md).

## UC-01 · Upload lecture material

1. On UI-01 choose **Upload material**. On UI-02 confirm with no file. Expect a prompt to choose one.
2. Try an unsupported file and a zero-byte file with a supported extension. Each produces an inline error. The lecture list gains no entry.
3. Choose a nonempty PDF, PPTX, MP3 or WAV. Check its displayed name and byte count, then confirm. Capture the accepted/processing state. When ready, open UI-03 and check the fixture label and sample topics.
4. Repeat as Teacher in Software Engineering. The material is visible to the student in that course. The teacher lecture page offers no quiz generation action.

## UC-02 · Generate a lecture quiz

1. Open **Unavailable lecture content** for the no-content explanation.
2. Open **Requirements review** and choose **Generate quiz**. The first request after reset shows a failure. Reopen the quiz list to check that no empty quiz was added.
3. Retry generation. Observe the pending message, then the preview of ten topic-tagged questions and their answer choices. Choose **Start quiz**.
4. For the straight-through workflow, generate from a newly uploaded or seeded ready lecture. Software Engineering and Database Systems use different banks.

## UC-03 · Submit and review quiz answers

1. Answer just one question and submit. Expect the unanswered items to be identified, keyboard focus on the first missing answer, and the prior selection retained. Reload to confirm the draft persists.
2. Answer the remaining questions, deliberately missing at least one. Expand **Demo controls**, select **Simulate one interrupted submission**, and submit. Verify all answers remain visible.
3. Retry. Check the saved score, feedback labels, the corrections for missed questions and the weak-topic list on UI-05. Return through **Quizzes / Results** to reopen it.

## UC-04 · Generate follow-up practice

1. From the mixed result choose **Review weak topics**. Note its score and selected answers. Generate the practice quiz. Each item is new to the source quiz and belongs to a missed topic.
2. Start and submit practice. Use **View original result** to compare the original feedback. The automated tests also compare the entire original quiz, attempt, saved answers and result objects before and after completion.
3. Open the seeded 10/10 lecture result. Confirm the no-weak-topics explanation. A direct visit to `/c/se/practice/r-perfect` also ends without creating practice.

## UC-05 · Publish and display a course deadline

1. Switch to Teacher and open **Deadline Management**. Submit the empty form to see title, type and date errors. Type an impossible date such as 2026-02-30 using the YYYY-MM-DD field. Saving should explain the error and leave published items unchanged.
2. Publish a homework date seven days from today. After the form clears, check that the confirmation names the item and its saved date. As Student, check both the dashboard and **Upcoming Deadlines** for the item and its Upcoming badge. Switch to Database Systems and verify the item is absent.
3. Edit the date to eight days from today as Teacher. The student can still see the date and the badge is gone. Move the date into the past and confirm that the teacher can manage it and both student views omit it.
4. Move the date back to today and remove it. Confirm it disappears from both student views.
5. As Student, visit `/c/se/manage`. Expect an access message and a link to the read-only deadline view. Direct service tests also attempt student create, edit and delete operations.

## US-07, navigation and reset

1. As Teacher, open **Student Quiz Results** (UI-01T) and expand Eli Brooks’s submission. Check the score, selected answers and feedback. Drafts are excluded. Visit `/c/db?view=results` for an unassigned-course denial.
2. As Student, visit `/c/se/results/r-peer` for another student’s private result. Expect denial. Follow the dashboard link and reopen the current student’s own result.
3. Visit every role-specific navigation item. Refresh on a newly saved result. Reset once with Cancel, then confirm a reset. Expect the original fixtures, Software Engineering course and default student, including after reload.

## Historical executed checks

| Check | Observed result |
|---|---|
| Dependency install and production build | Installed the locked project dependencies and built the production bundle with Vite 7.3.8 on Node 24.15.0. Vite reported two ignored React Router client directives. The build exited successfully. |
| Mock services | Seven Node tests passed. They cover all supported extensions, processing, retry without empty records, two topic banks, grade-once behavior, immutable originals, calendar validation, day 0/7/8, role/course/ownership checks, reload and reset. |
| Browser workflows | The complete Playwright walkthrough passed in headless Microsoft Edge against the production bundle. It exercised all eight screens, both roles, US-07, all five critical workflows, and the alternative flows listed above. The final run reported zero uncaught page errors. |
| Keyboard and layout | The walkthrough used Tab, Shift+Tab, Enter and Space for upload, generation, answering and submission. Playwright supplied the chosen file when the native chooser opened. Validation moved focus to the first unanswered question. The dashboard had no horizontal overflow at 390 px. |
| Persistence and screenshots | Reload preserved the partial draft, saved result and published deadline. Cancel preserved demo changes and confirmed reset restored seeds. That historical run produced eleven report PNGs, since removed from the active tree. Current browser tests write to ignored `test-results/screens/`. |

Native operating-system file-dialog interaction, other browsers, a comprehensive assistive-technology audit, production load tests, real service/network recovery and the five-user usability study remain outside these executed checks.
