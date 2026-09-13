import { Link, useNavigate } from 'react-router-dom'
import { useState } from 'react'


function Login() {
    const [loggedIn, setLoggedIn] = useState(false)
    const navigate = useNavigate()
    const [email, setEmail] = useState('')
    const [password, setPassword] = useState('')
    const [error, setError] = useState('')

    const handleLogin = async () => {
    setError('')

    const formData = new URLSearchParams()
    formData.append('username', email)
    formData.append('password', password)

    try {
        const response = await fetch('http://localhost:8000/api/auth/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: formData
        })

        const data = await response.json()

        if (!response.ok) {
            setError(data.detail || 'Login failed')
            return
        }

        localStorage.setItem('access_token', data.access_token)
        setLoggedIn(true)
        navigate('/dashboard')

    } catch (err) {
        setError('Backend connection failed')
    }
}

    return (
        <div className="min-h-screen bg-gray-100 flex items-center justify-center">
            <div className="bg-white p-8 rounded-xl shadow-lg w-full max-w-md">

                <h1 className="text-3xl font-bold text-center text-blue-600">
                    Login
                </h1>

                <div className="mt-6">
                    <label className="block text-gray-700 mb-2">
                        Email
                    </label>

                    <input
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        type="email"
                        placeholder="Enter your email"
                        className="w-full border border-gray-300 rounded-lg px-4 py-3"
                    />
                </div>

                <div className="mt-4">
                    <label className="block text-gray-700 mb-2">
                        Password
                    </label>

                    <input
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        type="password"
                        placeholder="Enter your password"
                        className="w-full border border-gray-300 rounded-lg px-4 py-3"
                    />
                </div>

                {error && (
                    <p className="text-red-600 mt-3">{error}</p>
                )}

                <button
                    onClick={handleLogin}
                    disabled={loggedIn}
                    className={`w-full mt-6 text-white py-3 rounded-lg ${loggedIn
                        ? 'bg-green-600 cursor-not-allowed'
                        : 'bg-blue-600 hover:bg-blue-700'
                        }`}
                >
                    {loggedIn ? '✓ Logged In' : 'Login'}
                </button>

                <p className="text-center mt-4 text-gray-600">
                    Don't have an account?{' '}
                    <Link to="/register" className="text-blue-600 hover:underline">
                        Create Account
                    </Link>
                </p>

            </div>
        </div>
    )
}

export default Login