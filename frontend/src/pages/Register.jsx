import { Link, useNavigate } from 'react-router-dom'
import { useState } from 'react'

function Register() {
    const navigate = useNavigate()
    const [registered, setRegistered] = useState(false)
    return (
        <div className="min-h-screen bg-gray-100 flex items-center justify-center">
            <div className="bg-white p-8 rounded-xl shadow-lg w-full max-w-md">

                <h1 className="text-3xl font-bold text-center text-blue-600">
                    Create Account
                </h1>

                <div className="mt-6">
                    <label className="block text-gray-700 mb-2">
                        Name
                    </label>

                    <input
                        type="text"
                        placeholder="Enter your name"
                        className="w-full border border-gray-300 rounded-lg px-4 py-3"
                    />
                </div>

                <div className="mt-4">
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
                        placeholder="Create a password"
                        className="w-full border border-gray-300 rounded-lg px-4 py-3"
                    />
                </div>

                <button
                    onClick={() => {
                        setRegistered(true)
                        navigate('/login')
                    }}
                    disabled={registered}
                    className={`w-full mt-6 text-white py-3 rounded-lg ${registered
                        ? 'bg-green-600 cursor-not-allowed'
                        : 'bg-blue-600 hover:bg-blue-700'
                        }`}
                >
                    {registered ? '✓ Account Created' : 'Create Account'}
                </button>

                <p className="text-center mt-4 text-gray-600">
                    Already have an account?{' '}
                    <Link
                        to="/login"
                        className="text-blue-600 hover:underline"
                    >
                        Login
                    </Link>
                </p>

            </div>
        </div>
    )
}

export default Register