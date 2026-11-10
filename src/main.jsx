import { createRoot } from 'react-dom/client'
import { BrowserRouter } from 'react-router-dom'
import App from './App'
import { DemoProvider } from './state/Demo'
import './styles/app.css'
createRoot(document.getElementById('root')).render(<DemoProvider><BrowserRouter><App/></BrowserRouter></DemoProvider>)
