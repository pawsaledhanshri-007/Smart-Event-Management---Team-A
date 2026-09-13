import { Routes, Route } from 'react-router-dom'
import Home from './pages/Home'
import Login from './pages/Login'
import Register from './pages/Register'
import Dashboard from './pages/Dashboard'
import Events from './pages/Events'
import EventDetails from './pages/EventDetails'
import Venues from './pages/Venues'
import Registrations from './pages/Registrations'
import AIAssistant from './pages/AIAssistant'
import AdminUsers from './pages/AdminUsers'
import AdminAgentActivity from './pages/AdminAgentActivity'

function App() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />
      <Route path="/dashboard" element={<Dashboard />} />
      <Route path="/events" element={<Events />} />
      <Route path="/events/:id" element={<EventDetails />} />
      <Route path="/venues" element={<Venues />} />
      <Route path="/registrations" element={<Registrations />} />
      <Route path="/ai-assistant" element={<AIAssistant />} />
      <Route path="/admin/users" element={<AdminUsers />} />
      <Route path="/admin/agent-activity" element={<AdminAgentActivity />} />
    </Routes>
  )
}

export default App