import { Link, useParams } from 'react-router-dom'

export function usePath() {
  const { course } = useParams()
  return (tail = '') => '/c/' + course + tail
}
export function Heading({ id, title, detail }) {
  return <header className="heading"><span className="screen-id">{id}</span><h1>{title}</h1>{detail && <p>{detail}</p>}</header>
}
export function Notice({ children, error = false }) {
  if (!children) return null
  return <div className={'notice' + (error ? ' error' : '')} role={error ? 'alert' : 'status'}>{children}</div>
}
export function CourseLink({ to = '', children, button }) {
  const path = usePath()
  return <Link className={button ? 'button primary' : undefined} to={path(to)}>{children}</Link>
}
export function DeadlineList({ items, actions }) {
  if (!items.length) return <p className="empty">No deadlines to display.</p>
  return <ul className="rows">{items.map(item => <li key={item.id}><div><strong>{item.title}</strong><small>{item.type} · <time dateTime={item.date}>{item.date}</time></small></div><div className="actions">{item.upcoming && <span className="tag">Upcoming</span>}{actions?.(item)}</div></li>)}</ul>
}
export function Questions({ rows, answers, onAnswer, missing = [], review = false }) {
  return <div className="questions">{rows.map((q, i) => <fieldset key={q.id} className={missing.includes(q.id) || (review && !q.correct) ? 'flagged' : ''}>
    <legend>{i + 1}. {q.prompt}</legend><small>{q.topic}</small>
    {review ? <><strong>{q.correct ? 'Correct' : 'Incorrect'}</strong><p>Your answer: {q.options[q.selected]}</p>{!q.correct && <p>Correct answer: {q.options[q.key]}</p>}</>
      : onAnswer ? q.options.map((o, index) => <label className="option" key={o}><input type="radio" name={q.id} checked={answers[q.id] === index} onChange={() => onAnswer(q.id, index)} />{o}</label>)
      : <ul>{q.options.map(o => <li key={o}>{o}</li>)}</ul>}
    {missing.includes(q.id) && <p className="field-error">Choose an answer for question {i + 1}.</p>}
  </fieldset>)}</div>
}
