import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { API_URL } from '../services/api'

export default function AdminRegister() {
  const navigate = useNavigate()

  const [form, setForm] = useState({
    name: '',
    email: '',
    phone: '',
    age: '',
    college: '',
    password: '',
  })

  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const handleChange = (e) => {
    setForm({
      ...form,
      [e.target.name]: e.target.value,
    })
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setLoading(true)

    try {
      const response = await fetch(`${API_URL}/auth/register-admin`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          ...form,
          age: form.age ? Number(form.age) : null,
        }),
      })

      const data = await response.json()

      if (!response.ok) {
        throw new Error(data.detail || 'Admin account creation failed')
      }

      navigate('/login', {
        replace: true,
        state: {
          accountType: 'admin',
          message: 'Admin account created successfully. Please sign in.',
        },
      })
    } catch (err) {
      setError(err.message || 'Unable to create admin account')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="auth-page">
      <section className="auth-showcase">
        <div className="auth-brand">
          <span>✦</span> Evently
        </div>

        <div className="auth-copy">
          <span className="eyebrow">SMART EVENT MANAGEMENT</span>

          <h1>
            Create your
            <br />
            admin workspace.
          </h1>

          <p>
            Set up the first administrator account to manage events,
            venues, registrations and the platform.
          </p>
        </div>

        <div className="soft-orb orb-one" />
        <div className="soft-orb orb-two" />
      </section>

      <section className="auth-panel">
        <form className="auth-card" onSubmit={handleSubmit}>
          <div className="login-heading">
            <span className="account-badge admin">
              Admin setup
            </span>

            <h2>Create Admin Account</h2>

            <p className="muted">
              Enter your details to create the first admin account.
            </p>
          </div>

          <label>
            Full name
            <input
              name="name"
              type="text"
              required
              value={form.name}
              onChange={handleChange}
              placeholder="Admin name"
            />
          </label>

          <label>
            Admin email
            <input
              name="email"
              type="email"
              required
              value={form.email}
              onChange={handleChange}
              placeholder="admin@example.com"
            />
          </label>

          <label>
            Phone
            <input
              name="phone"
              type="tel"
              value={form.phone}
              onChange={handleChange}
              placeholder="Phone number"
            />
          </label>

          <label>
            Age
            <input
              name="age"
              type="number"
              min="1"
              max="119"
              value={form.age}
              onChange={handleChange}
              placeholder="Age"
            />
          </label>

          <label>
            College / Organization
            <input
              name="college"
              type="text"
              value={form.college}
              onChange={handleChange}
              placeholder="College or organization"
            />
          </label>

          <label>
            Password
            <input
              name="password"
              type="password"
              required
              minLength="6"
              value={form.password}
              onChange={handleChange}
              placeholder="Create a password"
            />
          </label>

          {error && (
            <div className="form-error">
              {error}
            </div>
          )}

          <button
            className="primary-button"
            type="submit"
            disabled={loading}
          >
            {loading ? 'Creating account...' : 'Create Admin Account'}
          </button>

          <p className="auth-footer">
            Already have an admin account?{' '}
            <Link to="/login" state={{ accountType: 'admin' }}>
              Admin sign in
            </Link>
          </p>
        </form>
      </section>
    </div>
  )
}