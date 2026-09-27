import { Navigate } from 'react-router-dom'
import { useAuthContext } from '../context/AuthContext'

export default function RoleRoute({ roles, children }) {
  const { user, loading } = useAuthContext()
  if (loading) return <div className="page-loader">Loading...</div>
  if (!user) return <Navigate to="/login" replace />
  if (!roles.includes(user.role)) return <Navigate to="/agent" replace />
  return children
}
