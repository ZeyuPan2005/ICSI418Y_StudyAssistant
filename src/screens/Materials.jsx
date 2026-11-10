import { useEffect, useRef, useState } from 'react'
import { useParams } from 'react-router-dom'
import { courses, formats } from '../data/fixtures'
import { validateFile } from '../services/demo'
import { useDemo } from '../state/Demo'
import { Heading, CourseLink, Notice, Questions } from '../components/Common'

export function Upload() {
  const { course } = useParams(), service = useDemo()
  const [file, setFile] = useState(null), [error, setError] = useState(''), [id, setId] = useState('')
  const material = id && service.lecture(course, id)
  function select(value) {
    setFile(value); setError('')
    try { validateFile(value) } catch (e) { setError(e.message) }
  }
  function upload(e) {
    e.preventDefault()
    try { setId(service.upload(course, file)); setError('') } catch (e) { setError(e.message) }
  }
  return <><Heading id="UI-02" title="Upload lecture material" detail="Choose a course in the sidebar, then select an audio recording or a slide file."/>
    <section><h2>Lecture file</h2><p>Accepted demo formats: {formats.join(', ').toUpperCase()}.</p>
    <p className="muted">Only file details are saved locally. Processing uses sample course content. Audio and slides are never analyzed.</p>
    {!material ? <form onSubmit={upload}><label className="button file-choice">Choose file<input title="Choose lecture file" type="file" accept={formats.map(f => '.' + f).join(',')} onChange={e => select(e.target.files[0])}/></label>
    {file ? <p>Selected: <strong>{file.name}</strong> · {file.size.toLocaleString('en-US')} bytes</p> : <p>No file selected.</p>}
    <Notice error>{error}</Notice><button className="primary">Confirm upload</button></form> :
    <><Notice>Upload accepted. {material.status === 'processing' ? 'Simulated processing in progress…' : 'Ready for quiz generation using sample course content.'}</Notice>
    <p>{material.filename} · {material.size.toLocaleString('en-US')} bytes</p><div className="actions"><CourseLink to={'/lectures/' + id} button>Open lecture</CourseLink><button onClick={() => { setFile(null); setId('') }}>Upload another file</button></div></>}</section></>
}

export function Lecture() {
  const { course, id } = useParams(), service = useDemo()
  const l = service.lecture(course, id), student = service.session().actor.role === 'Student'
  const [busy, setBusy] = useState(false), [error, setError] = useState(''), [quizId, setQuiz] = useState('')
  const timer = useRef(null)
  useEffect(() => () => clearTimeout(timer.current), [])
  function generate() {
    setBusy(true); setError('')
    timer.current = setTimeout(() => {
      try { setQuiz(service.generate(course, id)) } catch (e) { setError(e.message) } finally { setBusy(false) }
    }, 1400)
  }
  const quiz = quizId && service.quiz(course, quizId)
  return <><Heading id="UI-03" title={l.title} detail="Lecture details and quiz generation"/>
    <section><h2>Lecture content</h2><p>{l.filename} · {(l.size / 1024).toFixed(1)} KB</p>
    <p className="muted">Fixture-based sample content. The demo does not read or analyze the file.</p>
    {l.status === 'ready' ? <><p><span className="tag">Ready</span></p><p>Sample topics: {courses.find(c => c.id === l.fixture).topics.join(' · ')}</p></> :
      <Notice error={l.status === 'unusable'}>{l.status === 'unusable' ? 'No usable lecture content. Select a ready lecture to generate a quiz.' : 'Upload accepted. Simulated processing in progress…'}</Notice>}</section>
    {student && l.status === 'ready' && <section><h2>{quiz ? 'Quiz preview' : 'Lecture quiz'}</h2>
    {quiz ? <><Notice>Quiz available · {quiz.items.length} fixture-based questions.</Notice><CourseLink to={'/quizzes/' + quiz.id} button>Start quiz</CourseLink><Questions rows={quiz.questions}/></> :
    <><p>Generate ten questions from the course’s sample question bank.</p><Notice error>{error}</Notice>{busy && <Notice>Generating sample quiz…</Notice>}
      <button className="primary" disabled={busy} onClick={generate}>{error ? 'Retry generation' : 'Generate quiz'}</button></>}</section>}
    <CourseLink to="?view=materials">Back to lecture materials</CourseLink></>
}
