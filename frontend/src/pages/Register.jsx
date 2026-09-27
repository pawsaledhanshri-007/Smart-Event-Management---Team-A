import { useMemo, useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { apiFetch } from '../services/api'

const initial = { name: '', email: '', phone: '', age: '', college: '', password: '', confirmPassword: '' }

export default function Register() {
  const navigate = useNavigate()
  const [form, setForm] = useState(initial)
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const set = (key) => (event) => setForm(value => ({ ...value, [key]: event.target.value }))
  const rules = useMemo(() => ({
    length: form.password.length >= 8,
    upper: /[A-Z]/.test(form.password),
    lower: /[a-z]/.test(form.password),
    number: /\d/.test(form.password),
    match: Boolean(form.password) && form.password === form.confirmPassword,
  }), [form.password, form.confirmPassword])

  const submit = async (event) => {
    event.preventDefault()
    setError('')
    if (!Object.values(rules).every(Boolean)) { setError('Please satisfy all password requirements.'); return }
    setLoading(true)
    try {
      await apiFetch('/auth/register', {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          name: form.name, email: form.email, phone: form.phone || null,
          age: form.age ? Number(form.age) : null, college: form.college || null,
          password: form.password,
        }),
      })
      navigate('/login', { replace: true, state: { accountType: 'user', message: 'User account created. You can sign in now.' } })
    } catch (err) { setError(err.message) }
    finally { setLoading(false) }
  }

  return <div className="auth-page">
    <section className="auth-showcase"><div className="auth-brand"><span>✦</span> Evently</div><div className="auth-copy"><span className="eyebrow">CREATE • CONNECT • CELEBRATE</span><h1>Your events.<br/>Your possibilities.</h1><p>Create a User account to discover events, register and manage your profile.</p></div><div className="soft-orb orb-one"/><div className="soft-orb orb-two"/></section>
    <section className="auth-panel"><form className="auth-card auth-card-wide" onSubmit={submit}>
      <div className="auth-tabs"><Link to="/login">Sign In</Link><span className="active">User Signup</span></div>
      <h2>Create a user account</h2><p className="muted">Admin accounts cannot be created from this page.</p>
      <div className="form-grid two"><label>Full name<input required value={form.name} onChange={set('name')}/></label><label>Email<input required type="email" value={form.email} onChange={set('email')}/></label></div>
      <div className="form-grid two"><label>Phone <span className="optional">(optional)</span><input value={form.phone} onChange={set('phone')}/></label><label>Age <span className="optional">(optional)</span><input type="number" min="1" max="119" value={form.age} onChange={set('age')}/></label></div>
      <label>College / Organization <span className="optional">(optional)</span><input value={form.college} onChange={set('college')}/></label>
      <div className="form-grid two"><label>Password<input required type="password" value={form.password} onChange={set('password')}/></label><label>Confirm password<input required type="password" value={form.confirmPassword} onChange={set('confirmPassword')}/></label></div>
      <div className="password-rules">{[['length','8+ characters'],['upper','Uppercase'],['lower','Lowercase'],['number','Number'],['match','Passwords match']].map(([key,text]) => <span key={key} className={rules[key] ? 'ok' : ''}>{rules[key] ? '✓' : '○'} {text}</span>)}</div>
      {error && <div className="form-error">{error}</div>}
      <button className="primary-button" disabled={loading}>{loading ? 'Creating account...' : 'Create User Account'}</button>
      <p className="auth-footer">Already registered? <Link to="/login">Sign in</Link></p>
    </form></section>
  </div>
}
