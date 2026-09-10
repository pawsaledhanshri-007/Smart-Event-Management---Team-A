import { Link } from 'react-router-dom'
import Layout from '../components/Layout'

function Dashboard() {
  return (
    <Layout>
      <main className="max-w-7xl mx-auto p-6">

        {/* Header */}
        <div className="mb-8">
          <h2 className="text-3xl font-bold text-gray-800">
            Dashboard
          </h2>

          <p className="mt-2 text-gray-600">
            Welcome back! Manage your events and registrations from here.
          </p>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">

          <Link
            to="/events"
            className="bg-white p-6 rounded-2xl shadow hover:shadow-lg transition"
          >
            <p className="text-gray-500 font-medium">
              Upcoming Events
            </p>

            <h3 className="text-4xl font-bold text-blue-600 mt-3">
              3
            </h3>

            <p className="text-blue-600 mt-3">
              View all events →
            </p>
          </Link>

          <Link
            to="/registrations"
            className="bg-white p-6 rounded-2xl shadow hover:shadow-lg transition"
          >
            <p className="text-gray-500 font-medium">
              My Registrations
            </p>

            <h3 className="text-4xl font-bold text-green-600 mt-3">
              2
            </h3>

            <p className="text-green-600 mt-3">
              View registrations →
            </p>
          </Link>

          <Link
            to="/venues"
            className="bg-white p-6 rounded-2xl shadow hover:shadow-lg transition"
          >
            <p className="text-gray-500 font-medium">
              Available Venues
            </p>

            <h3 className="text-4xl font-bold text-purple-600 mt-3">
              2
            </h3>

            <p className="text-purple-600 mt-3">
              Explore venues →
            </p>
          </Link>

        </div>

        {/* AI Assistant */}
        <div className="mt-8 bg-gradient-to-r from-blue-600 to-indigo-600 text-white rounded-2xl p-8 shadow">

          <div className="flex flex-col md:flex-row items-center justify-between gap-6">

            <div>
              <h3 className="text-2xl font-bold">
                🤖 AI Event Assistant
              </h3>

              <p className="mt-2 text-blue-100 max-w-xl">
                Find events, check venue availability, manage registrations,
                and get event policy information using our AI assistant.
              </p>
            </div>

            <Link
              to="/ai-assistant"
              className="bg-white text-blue-600 px-6 py-3 rounded-lg font-semibold hover:bg-gray-100 transition whitespace-nowrap"
            >
              Open AI Assistant
            </Link>

          </div>

        </div>

        {/* Quick Actions */}
        <div className="mt-8 bg-white rounded-2xl shadow p-6">

          <h3 className="text-xl font-bold text-gray-800">
            Quick Actions
          </h3>

          <p className="text-gray-500 mt-1">
            Quickly access common event management tasks.
          </p>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mt-6">

            <Link
              to="/events"
              className="border border-gray-200 rounded-xl p-5 hover:border-blue-500 hover:shadow transition"
            >
              <div className="text-2xl">📅</div>
              <h4 className="font-semibold mt-3">
                Browse Events
              </h4>
              <p className="text-sm text-gray-500 mt-1">
                Find upcoming events
              </p>
            </Link>

            <Link
              to="/venues"
              className="border border-gray-200 rounded-xl p-5 hover:border-green-500 hover:shadow transition"
            >
              <div className="text-2xl">🏢</div>
              <h4 className="font-semibold mt-3">
                View Venues
              </h4>
              <p className="text-sm text-gray-500 mt-1">
                Check venue availability
              </p>
            </Link>

            <Link
              to="/registrations"
              className="border border-gray-200 rounded-xl p-5 hover:border-purple-500 hover:shadow transition"
            >
              <div className="text-2xl">🎟️</div>
              <h4 className="font-semibold mt-3">
                My Registrations
              </h4>
              <p className="text-sm text-gray-500 mt-1">
                Manage your registrations
              </p>
            </Link>

            <Link
              to="/ai-assistant"
              className="border border-gray-200 rounded-xl p-5 hover:border-indigo-500 hover:shadow transition"
            >
              <div className="text-2xl">🤖</div>
              <h4 className="font-semibold mt-3">
                AI Assistant
              </h4>
              <p className="text-sm text-gray-500 mt-1">
                Ask the event assistant
              </p>
            </Link>

          </div>

        </div>

      </main>
    </Layout>
  )
}

export default Dashboard