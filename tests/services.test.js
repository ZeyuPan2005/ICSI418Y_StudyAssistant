import { test } from 'node:test'
import assert from 'node:assert/strict'
import { createDemo, storageKey, validDate } from '../src/services/demo.js'
import { questionById, localDate } from '../src/data/fixtures.js'

function setup() {
  const memory = new Map()
  const storage = { getItem: key => memory.get(key), setItem: (key, value) => memory.set(key, value) }
  let now = new Date('2026-11-10T12:00:00')
  return { svc: createDemo(storage, () => now), dump: () => JSON.parse(memory.get(storageKey)), storage,
    advance: ms => { now = new Date(now.getTime() + ms) } }
}
test('UC-01 rejects missing, empty and unsupported files; processing survives a reload', () => {
  const { svc, dump, advance, storage } = setup()
  const count = dump().lectures.length
  for (const file of [null, { name: 'empty.wav', size: 0 }, { name: 'bad.exe', size: 4 }])
    assert.throws(() => svc.upload('se', file))
  assert.equal(dump().lectures.length, count)
  for (const ext of ['MP3','wav','PDF','pptx']) {
    const id = svc.upload('se', { name: 'Week 1.' + ext, size: 100 })
    assert.equal(svc.lecture('se', id).status, 'processing')
    assert.throws(() => svc.generate('se', id), /No usable/)
    advance(2300)
    assert.equal(svc.lecture('se', id).status, 'ready')
    assert.equal(createDemo(storage, () => new Date('2026-11-11T00:00:00')).lecture('se', id).status, 'ready')
  }
})
test('UC-02 leaves quizzes unchanged on failure, retries once, and generates topic-specific items in both courses', () => {
  const { svc, dump } = setup(), before = dump().quizzes
  assert.throws(() => svc.generate('se', 'empty'), /No usable/)
  assert.throws(() => svc.generate('se', 'retry'), /Simulated generation failed/)
  assert.deepEqual(dump().quizzes, before)
  for (const [course, lecture, topics] of [['se','retry',['Requirements','Acceptance criteria']],['db','keys',['Relational keys','Transactions']]]) {
    const q = svc.quiz(course, svc.generate(course, lecture))
    assert.equal(q.questions.length, 10)
    assert.ok(q.questions.every(row => topics.includes(row.topic) && row.options.length === 3 && !('key' in row)))
  }
})
test('UC-03 validates drafts, restores answers, grades once and rejects post-submit edits', () => {
  const { svc, storage, dump } = setup(), q = svc.quiz('se','draft'), first = q.items[0]
  svc.answer('se', q.id, first, 0)
  assert.throws(() => svc.submit('se', q.id), e => e.missing.length === 9)
  const reopened = createDemo(storage)
  assert.equal(reopened.quiz('se',q.id).attempt.answers[first], 0)
  for (const id of q.items) reopened.answer('se',q.id,id,questionById[id].key)
  const count = dump().results.length
  assert.throws(() => reopened.submit('se',q.id,true), /interruption/)
  assert.equal(dump().results.length, count)
  const rid = reopened.submit('se',q.id)
  assert.equal(reopened.result('se',rid).score,10)
  assert.equal(reopened.submit('se',q.id),rid)
  assert.equal(dump().results.length, count + 1)
  assert.throws(() => reopened.answer('se',q.id,first,1), /already been submitted/)
})
test('UC-04 saves distinct quiz and attempt and preserves original quiz, attempt, answers and entire result', () => {
  const { svc, dump } = setup()
  const source = db => [db.quizzes.find(q => q.id === 'mixed'), db.attempts.find(a => a.quizId === 'mixed'), db.results.find(r => r.id === 'r-mixed')]
  const before = source(dump())
  const practice = svc.quiz('se', svc.practice('se','r-mixed'))
  assert.notEqual(practice.id, before[0].id)
  assert.notEqual(practice.attempt.id, before[1].id)
  assert.equal(practice.sourceResult,'r-mixed')
  assert.ok(practice.questions.every(q => before[2].missed.includes(q.topic) && !before[0].items.includes(q.id)))
  for (const id of practice.items) svc.answer('se', practice.id, id, 0)
  svc.submit('se',practice.id)
  assert.deepEqual(source(dump()), before)
  const count = dump().quizzes.length
  assert.throws(() => svc.practice('se','r-perfect'), /No weak/)
  assert.equal(dump().quizzes.length,count)
})
test('UC-05 validates dates, accepts past dates, computes local day 0/7/8 boundaries and removes stale reminders', () => {
  const { svc, advance } = setup()
  svc.switchRole('Teacher')
  const fields = { title: 'Milestone demo', type: 'Homework', date: '2026-11-10' }
  for (const invalid of [{title:'  '},{type:''},{date:'2026-02-29'},{date:''}]) assert.throws(() => svc.saveDeadline('se',{...fields,...invalid}))
  assert.ok(validDate('2024-02-29'))
  const id = svc.saveDeadline('se',fields)
  function visible() { return svc.deadlines('se').find(d => d.id === id) }
  assert.equal(visible().upcoming,true)
  for (const [offset, expected] of [[7,true],[8,false],[-1,undefined]]) {
    const date = localDate(offset, new Date('2026-11-10T12:00:00'))
    svc.saveDeadline('se',{...fields,date},id)
    assert.equal(visible()?.upcoming,expected)
    assert.equal(svc.deadlines('se',true).find(d => d.id === id).date,date)
  }
  svc.saveDeadline('se',fields,id); advance(86400000)
  assert.equal(visible(),undefined)
  svc.removeDeadline('se',id)
  assert.ok(!svc.deadlines('se',true).some(d => d.id === id))
})
test('US-07 and service guards reject cross-course, teacher-only and other-student operations', () => {
  const { svc, dump } = setup()
  for (const call of [() => svc.saveDeadline('se',{}),() => svc.saveDeadline('se',{},'brief'),() => svc.removeDeadline('se','brief'),
    () => svc.deadlines('se',true),() => svc.quiz('se','peer'),() => svc.result('se','r-peer'),() => svc.practice('se','r-peer'),
    () => svc.answer('se','peer','q0-0',1),() => svc.result('db','r-mixed')]) assert.throws(call)
  assert.ok(svc.results('se').every(r => r.student === 'maya'))
  svc.selectCourse('db'); svc.switchRole('Teacher')
  assert.equal(svc.session().course,'se')
  assert.ok(svc.results('se').some(r => r.student === 'eli' && r.rows.length))
  assert.ok(!svc.results('se').some(r => r.quizId === 'draft'))
  for (const call of [() => svc.generate('se','requirements'),() => svc.submit('se','draft'),() => svc.practice('se','r-mixed'),
    () => svc.results('db'),() => svc.result('db','r-database'),() => svc.upload('db',{name:'x.pdf',size:1}),
    () => svc.selectCourse('db'),() => svc.saveDeadline('db',{}),() => svc.removeDeadline('db','brief')]) assert.throws(call)
  const id = svc.upload('se',{name:'teacher.wav',size:12})
  assert.ok(dump().lectures.some(l => l.id === id && l.uploader === 'reed'))
})
test('reset restores original identity, selected course, seeds and removes demo mutations', () => {
  const { svc, storage } = setup()
  svc.switchRole('Teacher'); const id = svc.saveDeadline('se',{title:'Temporary', type:'Lecture', date:'2024-01-01'})
  assert.equal(createDemo(storage).session().actor.role,'Teacher')
  svc.reset()
  assert.equal(svc.session().actor.role,'Student')
  assert.equal(svc.session().course,'se')
  svc.switchRole('Teacher')
  assert.ok(!svc.deadlines('se',true).some(d => d.id === id))
})
