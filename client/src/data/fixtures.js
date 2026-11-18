export const formats = ['mp3', 'wav', 'pdf', 'pptx']
export const reminderDays = 7

export const users = [
  { id: 'maya', name: 'Maya Chen', role: 'Student' },
  { id: 'eli', name: 'Eli Brooks', role: 'Student' },
  { id: 'reed', name: 'Jordan Reed', role: 'Teacher' }
]
export const courses = [
  { id: 'se', code: 'ICSI 418Y', name: 'Software Engineering', topics: ['Requirements', 'Acceptance criteria'] },
  { id: 'db', code: 'ICSI 410', name: 'Database Systems', topics: ['Relational keys', 'Transactions'] }
]
export const memberships = { maya: ['se', 'db'], eli: ['se'], reed: ['se'] }

// Each row contains the stem, correct answer, and two distractors.
const banks = {
  'Requirements': [
    ['Which statement describes a functional requirement?', 'A student can submit answers.', 'Results load within three seconds.', 'The page meets a contrast target.'],
    ['Who supplies the goal in a user story?', 'The actor who needs the feature', 'The database engine', 'The deployment script'],
    ['Which requirement describes performance?', 'A result opens within three seconds.', 'Teachers can post dates.', 'Students can upload slides.'],
    ['What identifies an MVP use case?', 'An essential user goal', 'A preferred library', 'A possible future extension'],
    ['What does a use-case precondition describe?', 'What must already be true', 'The final score', 'Every screen color'],
    ['A student wants to review missed items. What is the goal?', 'Understand incorrect answers', 'Choose a database', 'Assign a course code'],
    ['Which constraint is measurable?', 'Four of five users finish in ten minutes.', 'The layout feels easy.', 'The service is nice.']
  ],
  'Acceptance criteria': [
    ['Which criterion is directly testable?', 'Blank titles prevent saving.', 'Deadlines feel intuitive.', 'The feature is elegant.'],
    ['What outcome follows a rejected upload?', 'No lecture is added.', 'A draft quiz is graded.', 'A result is removed.'],
    ['What should a quiz submission test check?', 'Each required question has an answer.', 'Every student chose option A.', 'The teacher is online.'],
    ['Which example tests the reminder boundary?', 'Compare due dates seven and eight days away.', 'Change a username.', 'Open a lecture twice.'],
    ['What evidence supports a passing acceptance check?', 'The observed outcome matches the criterion.', 'The screen exists.', 'The implementation is short.'],
    ['Which check covers a failed submission?', 'Previously selected answers remain visible.', 'A new deadline appears.', 'The original lecture disappears.'],
    ['Which check tests course isolation?', 'An unassigned teacher is denied course results.', 'A student opens the homepage.', 'A file has a readable name.']
  ],
  'Relational keys': [
    ['What uniquely identifies a row?', 'A primary key', 'A display label', 'A table alias'],
    ['Which value references another table?', 'A foreign key', 'A row count', 'A query limit'],
    ['What is a composite key?', 'A key made of multiple attributes', 'A duplicate key', 'A generated report'],
    ['What enforces a unique identifier?', 'A uniqueness constraint', 'An ORDER BY clause', 'A column alias'],
    ['What links enrollment to a course?', 'A course foreign key', 'A display order', 'A date format'],
    ['Which pair could identify an enrollment?', 'Student ID and course ID', 'First name and nickname', 'Course title and color'],
    ['What does referential integrity protect?', 'Valid links between records', 'Screen brightness', 'Column width']
  ],
  'Transactions': [
    ['What does atomicity guarantee?', 'All operations commit together or none do.', 'Rows sort automatically.', 'Queries always succeed.'],
    ['What ends a successful transaction?', 'Commit', 'Rollback', 'Rename'],
    ['What discards an uncommitted transaction?', 'Rollback', 'A select query', 'A page refresh'],
    ['What does durability preserve?', 'Committed changes', 'Draft screen positions', 'Sorted output'],
    ['Which operation benefits from a transaction?', 'Moving funds between accounts', 'Changing a page title', 'Printing a column name'],
    ['Which property limits interference between transactions?', 'Isolation', 'Formatting', 'Compression'],
    ['What should happen after a failed debit in a transfer?', 'Roll back the transfer.', 'Commit only the credit.', 'Duplicate the debit.']
  ]
}

export const questions = Object.entries(banks).flatMap(([topic, rows], group) =>
  rows.map(([prompt, correct, ...others], i) => {
    const key = (group + i) % 3
    const options = [...others]
    options.splice(key, 0, correct)
    return { id: 'q' + group + '-' + i, topic, prompt, options, key, practice: i >= 5 }
  })
)
export const questionById = Object.fromEntries(questions.map(q => [q.id, q]))

export function localDate(offset = 0, from = new Date()) {
  const date = new Date(from)
  date.setDate(date.getDate() + offset)
  return [date.getFullYear(), String(date.getMonth() + 1).padStart(2, '0'), String(date.getDate()).padStart(2, '0')].join('-')
}

export function grade(quiz, attempt, id, submittedAt) {
  const rows = quiz.items.map(qid => {
    const q = questionById[qid]
    const selected = attempt.answers[qid]
    return { ...q, options: [...q.options], selected, correct: selected === q.key }
  })
  return { id, quizId: quiz.id, attemptId: attempt.id, course: quiz.course, student: quiz.student,
    submittedAt, rows, score: rows.filter(row => row.correct).length,
    missed: [...new Set(rows.filter(row => !row.correct).map(row => row.topic))] }
}

export function seed() {
  const lectures = [
    ['requirements', 'se', 'Requirements and acceptance criteria', 'ready'],
    ['empty', 'se', 'Unavailable lecture content', 'unusable'],
    ['retry', 'se', 'Requirements review', 'ready'],
    ['keys', 'db', 'Relational keys and transactions', 'ready']
  ].map(([id, course, title, status]) => ({ id, course, title, status, uploader: course === 'se' ? 'reed' : 'maya',
    filename: title + '.pdf', size: 24576, fixture: course, failNext: id === 'retry' }))
  const db = { version: 1, actor: 'maya', course: 'se', lectures, quizzes: [], attempts: [], results: [],
    deadlines: [{ id: 'brief', course: 'se', author: 'reed', title: 'Requirements brief', type: 'Homework', date: localDate(3) },
      { id: 'session', course: 'se', author: 'reed', title: 'Design review', type: 'Lecture', date: localDate(10) }] }
  for (const [id, student, course, outcome] of [
    ['mixed', 'maya', 'se', 'mixed'], ['perfect', 'maya', 'se', 'perfect'], ['draft', 'maya', 'se', 'draft'],
    ['peer', 'eli', 'se', 'mixed'], ['database', 'maya', 'db', 'perfect']
  ]) {
    const topics = courses.find(c => c.id === course).topics
    const items = questions.filter(q => topics.includes(q.topic) && !q.practice).map(q => q.id)
    const quiz = { id, title: course === 'se' ? 'Requirements and acceptance criteria' : 'Relational keys and transactions',
      student, course, lectureId: course === 'se' ? 'requirements' : 'keys', items, kind: 'Lecture', sourceResult: null }
    const attempt = { id: 'a-' + id, quizId: id, answers: {}, status: outcome === 'draft' ? 'draft' : 'submitted' }
    db.quizzes.push(quiz)
    db.attempts.push(attempt)
    if (outcome === 'draft') continue
    items.forEach((qid, index) => {
      const key = questionById[qid].key
      attempt.answers[qid] = outcome === 'mixed' && index < 2 ? (key + 1) % 3 : key
    })
    db.results.push(grade(quiz, attempt, 'r-' + id, new Date().toISOString()))
  }
  return db
}
