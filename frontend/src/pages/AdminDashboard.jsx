import { Link } from 'react-router-dom'
import Layout from '../components/Layout'
import { useAuthContext } from '../context/AuthContext'

export default function AdminDashboard() {
  const { user } = useAuthContext()
  return <Layout><main className="page-container">
    <div className="page-heading"><span className="eyebrow">ADMIN WORKSPACE</span><h1>Welcome, {user?.name || 'Admin'}</h1><p>Manage the event platform from one secure workspace.</p></div>
    <section className="manager-actions">
      <Link to="/events" className="action-card"><span>◫</span><strong>Manage Events</strong><small>Review and create events</small></Link>
      <Link to="/venues" className="action-card"><span>⌖</span><strong>Manage Venues</strong><small>Review venue information</small></Link>
      <Link to="/registrations" className="action-card"><span>◎</span><strong>Registrations</strong><small>Review event registrations</small></Link>
      <Link to="/agent" className="action-card"><span>✦</span><strong>AI Agent</strong><small>Open the Evently assistant</small></Link>
    </section>
    <div className="form-warning">Admin access is protected by both your selected login type and the role stored in the database.</div>
  </main></Layout>
}
