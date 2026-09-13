import { useState } from 'react'
import { Link } from 'react-router-dom'

function Navbar() {
  const [menuOpen, setMenuOpen] = useState(false)

  const closeMenu = () => {
    setMenuOpen(false)
  }

  return (
    <nav className="bg-white shadow-sm px-6 md:px-8 py-4">
      <div className="max-w-7xl mx-auto">

        {/* Top Bar */}
        <div className="flex items-center justify-between">

          <Link
            to="/dashboard"
            onClick={closeMenu}
            className="text-xl md:text-2xl font-bold text-blue-600"
          >
            Smart Event Management
          </Link>

          {/* Desktop Navigation */}
          <div className="hidden lg:flex items-center gap-5">

            <Link
              to="/dashboard"
              className="text-gray-700 hover:text-blue-600"
            >
              Dashboard
            </Link>

            <Link
              to="/events"
              className="text-gray-700 hover:text-blue-600"
            >
              Events
            </Link>

            <Link
              to="/venues"
              className="text-gray-700 hover:text-blue-600"
            >
              Venues
            </Link>

            <Link
              to="/registrations"
              className="text-gray-700 hover:text-blue-600"
            >
              Registrations
            </Link>

            <Link
              to="/ai-assistant"
              className="text-gray-700 hover:text-blue-600"
            >
              AI Assistant 🤖
            </Link>

            <Link
              to="/admin/users"
              className="text-gray-700 hover:text-blue-600"
            >
              Users
            </Link>

            <Link
              to="/admin/agent-activity"
              className="text-gray-700 hover:text-blue-600"
            >
              Agent Activity
            </Link>

            <button
              onClick={() => {
                window.location.href = '/login'
              }}
              className="bg-red-600 text-white px-4 py-2 rounded-lg hover:bg-red-700"
            >
              Logout
            </button>

          </div>

          {/* Mobile Menu Button */}
          <button
            onClick={() => setMenuOpen(!menuOpen)}
            className="lg:hidden text-gray-700 text-2xl"
          >
            {menuOpen ? '✕' : '☰'}
          </button>

        </div>

        {/* Mobile Navigation */}
        {menuOpen && (
          <div className="lg:hidden mt-4 pt-4 border-t border-gray-200 space-y-2">

            <Link
              to="/dashboard"
              onClick={closeMenu}
              className="block px-4 py-3 rounded-lg text-gray-700 hover:bg-gray-100"
            >
              Dashboard
            </Link>

            <Link
              to="/events"
              onClick={closeMenu}
              className="block px-4 py-3 rounded-lg text-gray-700 hover:bg-gray-100"
            >
              Events
            </Link>

            <Link
              to="/venues"
              onClick={closeMenu}
              className="block px-4 py-3 rounded-lg text-gray-700 hover:bg-gray-100"
            >
              Venues
            </Link>

            <Link
              to="/registrations"
              onClick={closeMenu}
              className="block px-4 py-3 rounded-lg text-gray-700 hover:bg-gray-100"
            >
              Registrations
            </Link>

            <Link
              to="/ai-assistant"
              onClick={closeMenu}
              className="block px-4 py-3 rounded-lg text-gray-700 hover:bg-gray-100"
            >
              AI Assistant 🤖
            </Link>

            <Link
              to="/admin/users"
              onClick={closeMenu}
              className="block px-4 py-3 rounded-lg text-gray-700 hover:bg-gray-100"
            >
              Users
            </Link>

            <Link
              to="/admin/agent-activity"
              onClick={closeMenu}
              className="block px-4 py-3 rounded-lg text-gray-700 hover:bg-gray-100"
            >
              Agent Activity
            </Link>

            <button
              onClick={() => {
                window.location.href = '/login'
              }}
              className="w-full text-left bg-red-600 text-white px-4 py-3 rounded-lg hover:bg-red-700"
            >
              Logout
            </button>

          </div>
        )}

      </div>
    </nav>
  )
}

export default Navbar