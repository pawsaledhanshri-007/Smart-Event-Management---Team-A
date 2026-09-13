import { Link, useNavigate } from 'react-router-dom'
import { useState } from 'react'

function Register() {
    const navigate = useNavigate()
    const [registered, setRegistered] = useState(false)
    const [name, setName] = useState('')
    const [email, setEmail] = useState('')
    const [phone, setPhone] = useState('')
    const [password, setPassword] = useState('')
    const [error, setError] = useState('')

    const handleRegister = async () => {
    setError('')

    try {
        const response = await fetch('http://localhost:8000/api/auth/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                name: name,
                email: email,
                phone: phone,
                password: password
            })
        })

        const data = await response.json()

        if (!response.ok) {
            setError(data.detail || 'Registration failed')
            return
        }

        setRegistered(true)
        navigate('/login')

    } catch (err) {
        setError('Backend connection failed')
    }
}

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
                        value={name}
                        onChange={(e) => setName(e.target.value)}
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
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        className="w-full border border-gray-300 rounded-lg px-4 py-3"
                    />
                </div>

                <div className="mt-4">
    <label className="block text-gray-700 mb-2">
        Phone
    </label>

    <input
        type="tel"
        placeholder="Enter your phone number"
        value={phone}
        onChange={(e) => setPhone(e.target.value)}
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
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        className="w-full border border-gray-300 rounded-lg px-4 py-3"
                    />
                </div>
                <button
                onClick={handleRegister}
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