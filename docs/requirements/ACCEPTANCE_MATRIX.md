# Selected user-story acceptance matrix

**Authority:** Original submitted Milestone 2, `Team01- Milestone 2- Report.pdf`, section 2, not the later AD proposal. **Target:** US-01, US-02, US-03, US-05, US-06 (5/7 MVP = 71.4% **only if all pass**). US-04 and US-07 remain MVP but are outside the selected implementation target; report them truthfully as Incomplete unless actually accepted.

| Story | Original M2 acceptance substance | Required proof in actual working prototype | Primary owner | Status |
| --- | --- | --- | --- | --- |
| **US-01** Upload lecture material | Supported file uploads and appears in selected course; missing/unsupported rejected with clear message; readiness visible | Real PDF/PPTX/MP3/WAV accepted/rejected per agreed formats; stored bytes + metadata exist; after refresh course lists material and readiness correctly | B + DB + Frontend | **Unverified** |
| **US-02** Generate quiz | Usable uploaded material produces questions **based on that material**; preview shows questions and options before start; no usable material gives explanation | Show source lecture content → AI question relationship and ten safe preview items; missing/failed content explains why no Quiz; do not claim topic-bank simulation analyzes source | B AI + C + Frontend | **Unverified** |
| **US-03** Take and grade | Complete submission saves answers and shows score or right/wrong; missed items visible; incomplete answers identified before final submission | Start, attempt incomplete submit, fill missing, finalize once, reload authorized Result with missed-item feedback and no duplicate Result | C + DB + Frontend | **Unverified** |
| **US-05** Manage deadlines | Teacher saves title/date/type and Student sees it in course; missing title/invalid date rejected; Student cannot create/edit | Real Teacher creates/edits/removes, Student sees fresh saved course values, invalid writes error; direct Student API write denied | A + DB + Frontend | **Unverified** |
| **US-06** Upcoming alerts | Teacher-posted deadlines and dates in Student view; approaching date marked Upcoming in configured window; edits/deletes remove stale reminders | Day 0/+7 Upcoming, +8 not marked, edits/removals reflected in both Student locations after refresh | A + DB + Frontend | **Unverified** |

## Original MVP stories outside selected five

- **US-04:** follow-up practice on missed topics; preserve original result; show no-weak-topic alternative. Existing Demo behavior may remain visible but is not automatically a completed real story.
- **US-07:** Teacher sees submitted scores/answers in assigned course, never Drafts/foreign course. Existing Demo behavior may remain visible but is not automatically completed real access control.

## Evidence and report

For each story record: assignee, source M2 acceptance bullet, test/demo step, API route used, what data persisted, result (PASS/FAIL/BLOCKED), Git SHA and screenshot/video timestamp. **Complete** requires every original acceptance point to be satisfied by the working prototype; partial server endpoints or Demo-only tests do not prove it. Milestone 4 requires PDF report including team number/names, role-grouped status, scope changes since M3, incomplete gaps, numerator/denominator excluding stretch, joint and individual efforts; plus a 3–5 minute annotated video showing every Complete story ID with user action and observable result. Arrange one Brightspace submitter.
