import { Navigate, useLocation } from 'react-router-dom'
import { useAuthContext } from '../context/AuthContext'

export default function ProtectedRoute({ children }) {
  const { isAuthenticated, loading } = useAuthContext()
  const location = useLocation()
  if (loading) return <div className="page-loader">Loading...</div>
  if (!isAuthenticated) return <Navigate to="/login" replace state={{ from: location.pathname }} />
  return children
}
