import { Link, useNavigate } from 'react-router-dom'
import { useState } from 'react'

function Login() {
    const [loggedIn, setLoggedIn] = useState(false)
    const navigate = useNavigate()
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
                        type="password"
                        placeholder="Enter your password"
                        className="w-full border border-gray-300 rounded-lg px-4 py-3"
                    />
                </div>

                <button
                    onClick={() => {
                        setLoggedIn(true)
                        navigate('/dashboard')
                    }}
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