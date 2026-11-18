import { courses, users, memberships, formats, questions, questionById, grade, localDate, reminderDays, seed } from '../data/fixtures.js'

export const storageKey = 'study-assistant.demo.v1'
export function validateFile(file) {
  if (!file) throw Error('Choose a lecture file before confirming the upload.')
  if (!formats.includes(file.name.split('.').pop().toLowerCase()) || !file.name.includes('.'))
    throw Error('Unsupported file. Choose MP3, WAV, PDF or PPTX.')
  if (!file.size) throw Error('This file is empty. Choose a file with content.')
}
export function validDate(value) {
  if (!/^\d{4}-\d{2}-\d{2}$/.test(value) || value.startsWith('0000')) return false
  const parsed = new Date(value + 'T00:00:00Z')
  return Number.isFinite(parsed.getTime()) && parsed.toISOString().slice(0, 10) === value
}
export function deadlineErrors(fields) {
  const errors = {}
  if (!fields.title?.trim()) errors.title = 'Enter a deadline title.'
  if (!['Lecture', 'Homework'].includes(fields.type)) errors.type = 'Choose a deadline type.'
  if (!validDate(fields.date)) errors.date = 'Enter a valid calendar date.'
  return errors
}

export function createDemo(storage, clock = () => new Date()) {
  function restore() {
    const raw = storage.getItem(storageKey)
    if (raw) {
      try { const saved = JSON.parse(raw); if (saved?.version === 1 && saved.lectures && saved.results) return saved } catch { /* Restore seeds after unreadable data. */ }
    }
    const initial = seed()
    storage.setItem(storageKey, JSON.stringify(initial))
    return initial
  }
  let db = restore()
  let revision = 0
  const subscribers = new Set()
  function notify() { revision++; subscribers.forEach(fn => fn()) }
  function save(next) {
    storage.setItem(storageKey, JSON.stringify(next))
    db = next
    notify()
  }
  function actor() { return users.find(user => user.id === db.actor) }
  function access(course, role) {
    if (role && actor().role !== role) throw Error(role + ' access required.')
    if (!memberships[db.actor].includes(course)) throw Error('You do not have access to this course.')
  }
  function record(list, id, course) {
    access(course)
    const found = list.find(item => item.id === id && item.course === course)
    if (!found) throw Error('This record is unavailable in this course.')
    return found
  }
  function own(item) {
    if (item.student !== db.actor) throw Error('You can only open your own quiz work.')
    return item
  }
  function studentQuiz(course, id) { access(course, 'Student'); return own(record(db.quizzes, id, course)) }
  function result(course, id) {
    const r = record(db.results, id, course)
    return actor().role === 'Student' ? own(r) : r
  }
  function lecture(course, id) {
    const l = record(db.lectures, id, course)
    if (l.status === 'processing' && clock().getTime() >= l.readyAt) return { ...l, status: 'ready' }
    return l
  }
  function addQuiz(course, material, items, sourceResult = null) {
    if (!items.length) throw Error('No matching sample questions are available.')
    const quiz = { id: crypto.randomUUID(), student: db.actor, course, lectureId: material.id, title: material.title,
      items: items.map(q => q.id), kind: sourceResult ? 'Practice' : 'Lecture', sourceResult }
    const attempt = { id: crypto.randomUUID(), quizId: quiz.id, answers: {}, status: 'draft' }
    save({ ...db, quizzes: [...db.quizzes, quiz], attempts: [...db.attempts, attempt] })
    return quiz.id
  }
  function attemptFor(id) { return db.attempts.find(a => a.quizId === id) }
  const api = {
    subscribe(fn) { subscribers.add(fn); return () => subscribers.delete(fn) },
    revision: () => revision,
    refresh() { db = restore(); notify() },
    reset() { save(seed()) },
    session() { return { actor: actor(), course: db.course, courses: courses.filter(c => memberships[db.actor].includes(c.id)) } },
    switchRole(role) {
      const user = users.find(u => u.role === role)
      if (!user) throw Error('Unknown role.')
      save({ ...db, actor: user.id, course: memberships[user.id].includes(db.course) ? db.course : memberships[user.id][0] })
    },
    selectCourse(course) { access(course); save({ ...db, course }) },
    access,
    materials(course) { access(course); return db.lectures.filter(l => l.course === course).map(l => lecture(course, l.id)) },
    lecture,
    upload(course, file) {
      access(course); validateFile(file)
      const material = { id: crypto.randomUUID(), course, fixture: course, uploader: db.actor, title: file.name, filename: file.name,
        size: file.size, status: 'processing', readyAt: clock().getTime() + 2200 }
      save({ ...db, lectures: [...db.lectures, material] })
      return material.id
    },
    generate(course, id) {
      access(course, 'Student')
      const l = lecture(course, id)
      if (l.status !== 'ready') throw Error('No usable lecture content is available for generation.')
      if (l.failNext) {
        save({ ...db, lectures: db.lectures.map(item => item.id === id ? { ...item, failNext: false } : item) })
        throw Error('Simulated generation failed. Your existing quizzes are saved. Try again.')
      }
      const { topics } = courses.find(c => c.id === l.fixture)
      return addQuiz(course, l, questions.filter(q => !q.practice && topics.includes(q.topic)))
    },
    quiz(course, id) {
      const q = studentQuiz(course, id)
      return { ...q, questions: q.items.map(qid => { const { id, topic, prompt, options } = questionById[qid]; return { id, topic, prompt, options } }),
        attempt: attemptFor(id), resultId: db.results.find(r => r.quizId === id)?.id }
    },
    drafts(course) {
      access(course, 'Student')
      return db.quizzes.filter(q => q.course === course && q.student === db.actor && attemptFor(q.id).status === 'draft')
    },
    answer(course, id, qid, choice) {
      const q = studentQuiz(course, id)
      const a = attemptFor(id)
      if (a.status !== 'draft') throw Error('This attempt has already been submitted.')
      if (!q.items.includes(qid) || !Number.isInteger(choice) || !questionById[qid].options[choice]) throw Error('Invalid answer selection.')
      save({ ...db, attempts: db.attempts.map(item => item.id === a.id ? { ...a, answers: { ...a.answers, [qid]: choice } } : item) })
    },
    submit(course, id, interrupt = false) {
      const q = studentQuiz(course, id)
      const a = attemptFor(id)
      if (a.status === 'submitted') return db.results.find(r => r.attemptId === a.id).id
      const missing = q.items.filter(qid => a.answers[qid] === undefined)
      if (missing.length) throw Object.assign(Error('Answer the highlighted questions before submitting.'), { missing })
      if (interrupt) throw Error('Simulated connection interruption. Your answers are saved. Submit again to retry.')
      const r = grade(q, a, crypto.randomUUID(), clock().toISOString())
      save({ ...db, attempts: db.attempts.map(item => item.id === a.id ? { ...a, status: 'submitted' } : item), results: [...db.results, r] })
      return r.id
    },
    results(course) {
      access(course)
      return db.results.filter(r => r.course === course && (actor().role === 'Teacher' || r.student === db.actor)).map(r => ({
        ...r, studentName: users.find(u => u.id === r.student).name, quiz: db.quizzes.find(q => q.id === r.quizId)
      })).reverse()
    },
    result,
    practice(course, resultId) {
      access(course, 'Student')
      const r = result(course, resultId)
      if (!r.missed.length) throw Error('No weak topics to practice.')
      const original = studentQuiz(course, r.quizId)
      if (original.sourceResult) throw Error('Open the original lecture result to generate follow-up practice.')
      const items = questions.filter(q => q.practice && r.missed.includes(q.topic) && !original.items.includes(q.id))
      return addQuiz(course, lecture(course, original.lectureId), items, r.id)
    },
    deadlines(course, management = false) {
      access(course, management ? 'Teacher' : undefined)
      const today = localDate(0, clock()), end = localDate(reminderDays, clock())
      return db.deadlines.filter(d => d.course === course && (management || d.date >= today))
        .map(d => ({ ...d, upcoming: d.date >= today && d.date <= end })).sort((a, b) => a.date.localeCompare(b.date))
    },
    saveDeadline(course, fields, id = null) {
      access(course, 'Teacher')
      if (id) record(db.deadlines, id, course)
      const errors = deadlineErrors(fields)
      if (Object.keys(errors).length) throw Object.assign(Error('Check the highlighted deadline fields.'), { fields: errors })
      const item = { id: id || crypto.randomUUID(), course, author: db.actor, title: fields.title.trim(), type: fields.type, date: fields.date }
      save({ ...db, deadlines: id ? db.deadlines.map(d => d.id === id ? item : d) : [...db.deadlines, item] })
      return item.id
    },
    removeDeadline(course, id) {
      access(course, 'Teacher'); record(db.deadlines, id, course)
      save({ ...db, deadlines: db.deadlines.filter(d => d.id !== id) })
    }
  }
  return api
}
