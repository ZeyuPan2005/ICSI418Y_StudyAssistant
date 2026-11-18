import { useState } from 'react'
import { Link, Navigate, Route, Routes, useLocation, useNavigate, useParams } from 'react-router-dom'
import { useDemo } from './state/Demo'
import { Heading, Notice } from './components/Common'
import { Dashboard } from './screens/Dashboard'
import { Upload, Lecture } from './screens/Materials'
import { Taking, Results, Practice } from './screens/Quizzes'
import { Management, Deadlines } from './screens/Deadlines'

function CourseScreen({ Page, screen, role, home, student }) {
  const service = useDemo(), { course, id } = useParams(), location = useLocation()
  try {
    service.access(course, role)
    if (Page === Lecture) service.lecture(course, id)
    if (Page === Taking) service.quiz(course, id)
    if (Page === Results || Page === Practice) service.result(course, id)
    if (Page === Dashboard) {
      const view = new URLSearchParams(location.search).get('view') || 'overview'
      if (!['overview', 'materials', student ? 'quizzes' : 'results'].includes(view))
        throw Error('This dashboard section is unavailable for your role.')
    }
  } catch (error) {
    return <><Heading id={screen} title="Access unavailable"/><Notice error>{error.message}</Notice>
      <Link to={home}>Return to accessible dashboard</Link>{student && <> · <Link to={home + '/deadlines'}>View course deadlines</Link></>}</>
  }
  return <Page/>
}
const screens = [
  ['', 'UI-01', Dashboard], ['upload', 'UI-02', Upload], ['lectures/:id', 'UI-03', Lecture],
  ['quizzes/:id', 'UI-04', Taking, 'Student'], ['results/:id', 'UI-05', Results, 'Student'],
  ['practice/:id', 'UI-06', Practice, 'Student'], ['manage', 'UI-07', Management, 'Teacher'], ['deadlines', 'UI-08', Deadlines, 'Student']
]
export default function App() {
  const service = useDemo(), { actor, courses, course: saved } = service.session()
  const location = useLocation(), navigate = useNavigate()
  const routeCourse = location.pathname.split('/')[2]
  const current = courses.find(c => c.id === routeCourse) || courses.find(c => c.id === saved)
  const base = '/c/' + current.id
  const student = actor.role === 'Student'
  const [confirm, setConfirm] = useState(false), [notice, setNotice] = useState('')
  const nav = [['Course Dashboard', ''], ['Lecture Materials', '?view=materials'],
    ...(student ? [['Quizzes / Results', '?view=quizzes'], ['Upcoming Deadlines', '/deadlines']] : [['Deadline Management', '/manage'], ['Student Quiz Results', '?view=results']])]
  function home() { navigate('/c/' + service.session().course); setConfirm(false) }
  return <><a className="skip" href="#main">Skip to content</a><header className="top"><Link to={base} className="brand">Study Assistant</Link><span className="demo-label">Demo · local sample data</span><label className="switcher">Demo role <select value={actor.role} onChange={e => { service.switchRole(e.target.value); setNotice(''); home() }}><option>Student</option><option>Teacher</option></select></label></header>
    <div className="workspace"><aside><label className="side-label" htmlFor="course">Course</label><select id="course" value={current.id} onChange={e => { service.selectCourse(e.target.value); setNotice(''); home() }}>{courses.map(c => <option key={c.id} value={c.id}>{c.name}</option>)}</select>
      <nav aria-label="Course navigation">{nav.map(([name, tail]) => {
        const active = location.pathname + location.search === base + tail
        return <Link key={name} className={active ? 'active' : ''} aria-current={active ? 'page' : undefined} to={base + tail}>{name}</Link>
      })}</nav><div className="persona"><strong>{actor.name}</strong><small>{actor.role} demo profile</small>
      {confirm ? <div><p>Restore sample data and discard demo changes?</p><button onClick={() => { service.reset(); setNotice('Demo data restored.'); home() }}>Confirm reset</button> <button onClick={() => setConfirm(false)}>Cancel</button></div> : <button className="text-button" onClick={() => setConfirm(true)}>Reset demo data</button>}</div></aside>
      <main id="main" tabIndex="-1"><div className="breadcrumb">{current.code} <span>/</span> {current.name}</div>{notice && <Notice>{notice} <button className="text-button" onClick={() => setNotice('')}>Dismiss</button></Notice>}
      <Routes><Route path="/" element={<Navigate replace to={base}/>}/>
      {screens.map(([tail,id,Page,role]) => <Route key={id} path={'/c/:course' + (tail ? '/' + tail : '')} element={<CourseScreen key={location.key + actor.id} Page={Page} screen={id} role={role} home={base} student={student}/>}/>)}
      <Route path="*" element={<><h1>Page unavailable</h1><Link to={base}>Course dashboard</Link></>}/></Routes></main></div></>
}
