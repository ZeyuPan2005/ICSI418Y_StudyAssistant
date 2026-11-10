import { useState } from 'react'
import { useParams } from 'react-router-dom'
import { useDemo } from '../state/Demo'
import { Heading, Notice, DeadlineList } from '../components/Common'
import { reminderDays } from '../data/fixtures'
const blank = { title: '', type: '', date: '' }
export function Management() {
  const { course } = useParams(), service = useDemo()
  const list = service.deadlines(course, true)
  const [fields, setFields] = useState(blank), [id, setId] = useState(''), [errors, setErrors] = useState({}), [notice, setNotice] = useState('')
  function clear() { setId(''); setFields(blank); setErrors({}) }
  function props(key) {
    return { id: key, value: fields[key], 'aria-invalid': !!errors[key], 'aria-describedby': errors[key] ? key + '-error' : undefined,
      onChange: e => { setFields({ ...fields, [key]: e.target.value }); setErrors({ ...errors, [key]: '' }); setNotice('') } }
  }
  function message(key) { return errors[key] && <span className="field-error" id={key + '-error'}>{errors[key]}</span> }
  function save(e) {
    e.preventDefault()
    try {
      service.saveDeadline(course, fields, id || null)
      setNotice(`${id ? 'Updated' : 'Published'} “${fields.title.trim()}” for ${fields.date}.`); clear()
    } catch (err) { setErrors(err.fields || {}); setNotice(err.message); document.getElementById(Object.keys(err.fields || {})[0])?.focus() }
  }
  return <><Heading id="UI-07" title="Deadline management"/><section><h2>{id ? 'Edit deadline' : 'Publish a deadline'}</h2>
    <form noValidate onSubmit={save}><label htmlFor="title">Title</label><input {...props('title')}/>{message('title')}
    <div className="pair"><div><label htmlFor="type">Deadline type</label><select {...props('type')}><option value="">Choose type</option><option>Lecture</option><option>Homework</option></select>{message('type')}</div>
    <div><label htmlFor="date">Date</label><input type="text" placeholder="YYYY-MM-DD" maxLength={10} {...props('date')} aria-describedby={errors.date ? 'date-format date-error' : 'date-format'}/><small id="date-format">Use year-month-day (YYYY-MM-DD).</small>{message('date')}</div></div>
    <div className="actions"><button className="primary">{id ? 'Save changes' : 'Publish deadline'}</button>{id && <button type="button" onClick={() => { clear(); setNotice('') }}>Cancel edit</button>}</div></form>
    <Notice error={Object.values(errors).some(Boolean)}>{notice}</Notice></section>
    <section><h2>Published deadlines</h2><DeadlineList items={list} actions={d => <><button onClick={() => { setId(d.id); setFields({ title: d.title, type: d.type, date: d.date }); setErrors({}); setNotice(''); document.getElementById('title')?.focus() }}>Edit</button><button onClick={() => { service.removeDeadline(course, d.id); if (id === d.id) clear(); setNotice(`Removed “${d.title}”.`) }}>Remove</button></>}/></section></>
}
export function Deadlines() {
  const service = useDemo(), { course } = useParams()
  return <><Heading id="UI-08" title="Upcoming deadlines" detail={'Dates due today or within the next ' + reminderDays + ' days are marked Upcoming.'}/><section><h2>Course dates</h2><DeadlineList items={service.deadlines(course)}/></section></>
}
