import { useState } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import { useDemo } from '../state/Demo'
import { CourseLink, Heading, Notice, Questions, usePath } from '../components/Common'

export function Taking() {
  const { course, id } = useParams(), service = useDemo(), navigate = useNavigate(), path = usePath()
  const quiz = service.quiz(course, id)
  const [missing, setMissing] = useState([]), [error, setError] = useState(''), [interrupt, setInterrupt] = useState(false)
  if (quiz.resultId) return <><Heading id="UI-04" title={quiz.title}/><Notice>Quiz already submitted.</Notice><CourseLink to={'/results/' + quiz.resultId}>View saved result</CourseLink></>
  function answer(qid, choice) {
    service.answer(course, id, qid, choice)
    const left = missing.filter(x => x !== qid)
    setMissing(left)
    if (!left.length) setError('')
  }
  function submit(e) {
    e.preventDefault()
    try { const rid = service.submit(course, id, interrupt); navigate(path('/results/' + rid)) }
    catch (err) {
      setError(err.message); setMissing(err.missing || [])
      if (err.missing) document.getElementsByName(err.missing[0])[0]?.focus()
      else setInterrupt(false)
    }
  }
  return <><Heading id="UI-04" title={quiz.title} detail={quiz.kind + ' quiz · Choose one answer per question.'}/>
    <form onSubmit={submit}><div className="section-head"><h2>Your answers</h2><span>{Object.keys(quiz.attempt.answers).length} of {quiz.items.length} answered</span></div>
    <Notice error>{error}</Notice><Questions rows={quiz.questions} answers={quiz.attempt.answers} onAnswer={answer} missing={missing}/>
    <details className="demo-control"><summary>Demo controls</summary><label className="option"><input type="checkbox" checked={interrupt} onChange={e => setInterrupt(e.target.checked)}/>Simulate one interrupted submission</label></details>
    <button className="primary">Submit answers</button></form></>
}
export function Results() {
  const service = useDemo(), { course, id } = useParams()
  const result = service.result(course, id), quiz = service.quiz(course, result.quizId)
  return <><Heading id="UI-05" title="Quiz results" detail={quiz.title + ' · ' + quiz.kind + ' quiz'}/><section><Notice>Quiz submitted. Answers and feedback saved locally.</Notice>
    <div className="score"><strong>{result.score} / {result.rows.length}</strong><span>Score</span></div>
    {quiz.sourceResult && <p><CourseLink to={'/results/' + quiz.sourceResult}>View original result</CourseLink></p>}
    {result.missed.length ? <><p>Missed topics: {result.missed.join(' · ')}</p>{quiz.kind === 'Lecture' && <CourseLink to={'/practice/' + id} button>Review weak topics</CourseLink>}</> : <p>No weak topics. You answered every question correctly.</p>}</section>
    <h2>Answer feedback</h2><Questions rows={result.rows} review/></>
}
export function Practice() {
  const service = useDemo(), { course, id } = useParams()
  const result = service.result(course, id), [quizId, setQuiz] = useState(''), [error, setError] = useState('')
  const parent = service.quiz(course, result.quizId).sourceResult
  if (parent) return <><Heading id="UI-06" title="Follow-up practice"/><p>Start practice from the original lecture result.</p><CourseLink to={'/results/' + parent}>View original result</CourseLink></>
  const quiz = quizId && service.quiz(course, quizId)
  function generate() {
    try { setQuiz(service.practice(course, id)) } catch (e) { setError(e.message) }
  }
  return <><Heading id="UI-06" title="Follow-up practice" detail="Practice the topics you missed on the original quiz."/>
    <section><h2>Weak topics</h2>{result.missed.length ? <p>{result.missed.join(' · ')}</p> : <Notice>No weak topics. Targeted practice is unnecessary.</Notice>}
    <p><CourseLink to={'/results/' + result.id}>View original result</CourseLink> · {result.score} / {result.rows.length}</p>
    {result.missed.length > 0 && !quiz && <button className="primary" onClick={generate}>Generate practice quiz</button>}<Notice error>{error}</Notice></section>
    {quiz && <section><h2>Practice preview</h2><Notice>Practice quiz generated · {quiz.items.length} new questions.</Notice><CourseLink to={'/quizzes/' + quiz.id} button>Start practice</CourseLink><Questions rows={quiz.questions}/></section>}</>
}
