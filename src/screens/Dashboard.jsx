import { useParams, useSearchParams } from 'react-router-dom'
import { useDemo } from '../state/Demo'
import { CourseLink, DeadlineList, Heading, Questions } from '../components/Common'

export function Dashboard() {
  const service = useDemo(), { course } = useParams(), [query] = useSearchParams()
  const student = service.session().actor.role === 'Student'
  const view = query.get('view') || 'overview'
  const overview = view === 'overview'
  const titles = { overview: 'Course dashboard', materials: 'Lecture materials', quizzes: 'Quizzes / Results', results: 'Student quiz results' }
  const lectures = service.materials(course), results = service.results(course)
  return <><Heading id={view === 'results' ? 'UI-01T' : 'UI-01'} title={titles[view]}/>
    {(overview || view === 'materials') && <section><div className="section-head"><h2>Lecture materials</h2><CourseLink to="/upload" button>Upload material</CourseLink></div>
    <ul className="rows">{lectures.map(l => <li key={l.id}><div><CourseLink to={'/lectures/' + l.id}>{l.title}</CourseLink><small>{l.failNext ? 'Fixture · first generation fails' : 'Fixture-based lecture content'}</small></div><span className="tag">{l.status === 'unusable' ? 'No content' : l.status === 'ready' ? 'Ready' : 'Processing'}</span></li>)}</ul></section>}
    {student && overview && <section><div className="section-head"><h2>Course deadlines</h2><CourseLink to="/deadlines">View deadlines</CourseLink></div><DeadlineList items={service.deadlines(course)}/></section>}
    {!student && overview && <p><CourseLink to="/manage">Manage course deadlines</CourseLink></p>}
    {(overview || view === 'quizzes' || view === 'results') && <section>{student && <><h2>Unsubmitted quizzes</h2>
      {service.drafts(course).length ? <ul className="rows">{service.drafts(course).map(q => <li key={q.id}><div><CourseLink to={'/quizzes/' + q.id}>{q.title}</CourseLink><small>{q.kind} quiz · Draft</small></div></li>)}</ul> : <p>No unsubmitted quizzes.</p>}</>}
      <h2>{student ? 'Submitted results' : 'Student quiz results'}</h2>
      {results.length ? <ul className="rows">{results.map(r => <li key={r.id}>{student ? <><div><CourseLink to={'/results/' + r.id}>{r.quiz.title}</CourseLink><small>{r.quiz.kind} quiz · Submitted</small></div><strong>{r.score} / {r.rows.length}</strong></> :
        <details><summary>{r.studentName} · {r.quiz.title} · {r.score} / {r.rows.length}</summary><Questions rows={r.rows} review/></details>}</li>)}</ul> : <p>No submitted results.</p>}</section>}</>
}
