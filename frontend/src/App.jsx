import { useLocation } from 'react-router-dom'
import { Navigate, Route, Routes } from 'react-router-dom'
import ProtectedRoute from './components/ProtectedRoute'
import RoleRoute from './components/RoleRoute'
import Login from './pages/Login'
import Register from './pages/Register'
import AIAssistant from './pages/AIAssistant'
import AdminDashboard from './pages/AdminDashboard'
import Dashboard from './pages/Dashboard'
import Events from './pages/Events'
import EventDetails from './pages/EventDetails'
import Venues from './pages/Venues'
import Registrations from './pages/Registrations'
import Profile from './pages/Profile'
import PaymentSuccess from './pages/PaymentSuccess'
import AdminRegister from './pages/AdminRegister'

const protect = (node) => <ProtectedRoute>{node}</ProtectedRoute>
const admin = (node) => <ProtectedRoute><RoleRoute roles={['admin']}>{node}</RoleRoute></ProtectedRoute>

export default function App() {
  return <Routes>
    <Route path="/" element={<Navigate to="/login" replace />} />
    <Route path="/login" element={<Login />} />
    <Route path="/register" element={<Register />} />
    <Route path="/register-admin" element={<AdminRegister />} />
    <Route path="/agent" element={protect(<AIAssistant />)} />
    <Route path="/ai-assistant" element={<Navigate to="/agent" replace />} />
    <Route path="/dashboard" element={protect(<Dashboard />)} />
    <Route path="/events" element={protect(<Events />)} />
    <Route path="/events/:id" element={protect(<EventDetails />)} />
    <Route path="/venues" element={protect(<Venues />)} />
    <Route path="/registrations" element={protect(<Registrations />)} />
    <Route path="/profile" element={protect(<Profile />)} />
    <Route path="/payment/success" element={protect(<PaymentSuccess />)} />
    <Route path="/admin" element={admin(<AdminDashboard />)} />

    <Route path="*" element={<Navigate to="/login" replace />} />
  </Routes>
}
