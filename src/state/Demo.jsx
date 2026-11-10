import { createContext, useContext, useEffect, useSyncExternalStore } from 'react'
import { createDemo, storageKey } from '../services/demo.js'

const service = createDemo(window.localStorage)
const Context = createContext(null)
export function DemoProvider({ children }) {
  const version = useSyncExternalStore(service.subscribe, service.revision)
  const { course } = service.session()
  useEffect(() => {
    const onStorage = event => { if (event.key === storageKey || event.key === null) service.refresh() }
    window.addEventListener('storage', onStorage)
    return () => window.removeEventListener('storage', onStorage)
  }, [])
  useEffect(() => {
    const pending = service.session().courses.flatMap(c => service.materials(c.id)).filter(l => l.status === 'processing')
    if (!pending.length) return
    const next = Math.min(...pending.map(l => l.readyAt))
    const timer = setTimeout(service.refresh, Math.max(1, next - Date.now() + 10))
    return () => clearTimeout(timer)
  }, [version, course])
  return <Context.Provider value={{ service, version }}>{children}</Context.Provider>
}
export function useDemo() { return useContext(Context).service }
