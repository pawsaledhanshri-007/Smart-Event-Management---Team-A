import { useEffect, useState } from 'react'
import { Link, useLocation, useNavigate } from 'react-router-dom'
import { useAuthContext } from '../context/AuthContext'
import { API_URL } from '../services/api'

export default function Login() {
  const navigate = useNavigate()
  const location = useLocation()
  const { finishLogin } = useAuthContext()
  const [accountType, setAccountType] = useState(location.state?.accountType || 'user')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [showPassword, setShowPassword] = useState(false)
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const [adminExists, setAdminExists] = useState(true)

  const selectType = (type) => {
    setAccountType(type)
    setEmail('')
    setPassword('')
    setError('')
  }


  useEffect(() => {
    const checkAdmin = async () => {
      try {
        const response = await fetch(`${API_URL}/auth/admin-status`)
        const data = await response.json()
        setAdminExists(data.admin_exists)
      } catch {
        setAdminExists(true)
      }
    }

    checkAdmin()
  }, [])

  const handleLogin = async (event) => {
    event.preventDefault()
    setError('')
    setLoading(true)
    try {
      const body = new URLSearchParams({ username: email.trim(), password, role: accountType })
      const response = await fetch(`${API_URL}/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body,
      })
      const data = await response.json()
      if (!response.ok) throw new Error(data.detail || 'Login failed')
      const user = await finishLogin(data)
      if (!user || (accountType === 'admin' && user.role !== 'admin') || (accountType === 'user' && user.role !== 'participant')) {
        throw new Error('This account does not match the selected login type.')
      }
      navigate(user.role === 'admin' ? '/admin' : '/agent', { replace: true })
    } catch (err) {
      setError(err.message || 'Unable to sign in')
    } finally {
      setLoading(false)
    }
  }

  return <div className="auth-page">
    <section className="auth-showcase">
      <div className="auth-brand"><span>✦</span> Evently</div>
      <div className="auth-copy">
        <span className="eyebrow">SMART EVENT MANAGEMENT</span>
        <h1>One secure login.<br />The right workspace.</h1>
        <p>Choose your account type and sign in with the credentials assigned to that role.</p>
      </div>
      <div className="soft-orb orb-one" /><div className="soft-orb orb-two" />
    </section>
    <section className="auth-panel">
      <form className="auth-card" onSubmit={handleLogin}>
        <div className="account-type-switch" aria-label="Choose account type">
          <button type="button" className={accountType === 'user' ? 'active' : ''} onClick={() => selectType('user')}>
            <span>◎</span><div><strong>User</strong><small>Attend and register</small></div>
          </button>
          <button type="button" className={accountType === 'admin' ? 'active' : ''} onClick={() => selectType('admin')}>
            <span>◇</span><div><strong>Admin</strong><small>Manage the system</small></div>
          </button>
        </div>
        <div className="login-heading">
          <span className={`account-badge ${accountType}`}>{accountType === 'admin' ? 'Admin access' : 'User access'}</span>
          <h2>{accountType === 'admin' ? 'Admin sign in' : 'Welcome back'}</h2>
          <p className="muted">Enter your {accountType} email and password.</p>
        </div>
        {location.state?.message && <div className="form-success">{location.state.message}</div>}
        <label>{accountType === 'admin' ? 'Admin email / ID' : 'User email / ID'}
          <input type="email" required autoComplete="username" value={email} onChange={e => setEmail(e.target.value)} placeholder={accountType === 'admin' ? 'admin@example.com' : 'you@example.com'} />
        </label>
        <label>Password
          <div className="password-field">
            <input required autoComplete="current-password" type={showPassword ? 'text' : 'password'} value={password} onChange={e => setPassword(e.target.value)} placeholder="Enter your password" />
            <button type="button" onClick={() => setShowPassword(!showPassword)}>{showPassword ? 'Hide' : 'Show'}</button>
          </div>
        </label>
        {error && <div className="form-error">{error}</div>}
        <button className="primary-button" disabled={loading}>{loading ? 'Checking account...' : `Sign in as ${accountType === 'admin' ? 'Admin' : 'User'}`}</button>
        {accountType === 'user'
          ? <p className="auth-footer">
            New to Evently? <Link to="/register">Create a user account</Link>
          </p>
          : <p className="auth-footer">
            Don't have an admin account?{' '}
            <Link to="/register-admin">Create an admin account</Link>
          </p>}
      </form>
    </section>
  </div>
}
