import { Link } from 'react-router-dom'
import Layout from '../components/Layout'

function Venues() {
  const venues = [
    {
      id: 1,
      name: 'Main Auditorium',
      location: 'Block A',
      capacity: 500,
      status: 'Available',
      description: 'Large auditorium suitable for workshops, seminars and major events.',
    },
    {
      id: 2,
      name: 'Seminar Hall',
      location: 'Block B',
      capacity: 200,
      status: 'Available',
      description: 'Comfortable hall suitable for seminars, meetings and presentations.',
    },
    {
      id: 3,
      name: 'Computer Lab 1',
      location: 'Block C',
      capacity: 60,
      status: 'Occupied',
      description: 'Computer laboratory equipped for technical workshops and bootcamps.',
    },
  ]

  return (
    <Layout>
      <main className="max-w-7xl mx-auto p-6">

        {/* Header */}
        <div className="mb-8">
          <h2 className="text-3xl font-bold text-gray-800">
            Venues
          </h2>

          <p className="mt-2 text-gray-600">
            Explore available venues and check their availability.
          </p>
        </div>

        {/* Venue Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">

          {venues.map((venue) => (
            <div
              key={venue.id}
              className="bg-white rounded-2xl shadow hover:shadow-xl transition overflow-hidden"
            >

              {/* Card Header */}
              <div className="bg-gradient-to-r from-indigo-600 to-purple-600 p-6 text-white">
                <div className="text-3xl">
                  🏢
                </div>

                <h3 className="text-xl font-bold mt-3">
                  {venue.name}
                </h3>

                <p className="text-indigo-100 mt-1">
                  📍 {venue.location}
                </p>
              </div>

              {/* Card Body */}
              <div className="p-6">

                <p className="text-gray-600 text-sm leading-6">
                  {venue.description}
                </p>

                <div className="mt-5">

                  <div className="flex items-center justify-between py-3 border-b">
                    <span className="text-gray-500">
                      Capacity
                    </span>

                    <span className="font-semibold text-gray-800">
                      👥 {venue.capacity}
                    </span>
                  </div>

                  <div className="flex items-center justify-between py-3">
                    <span className="text-gray-500">
                      Status
                    </span>

                    <span
                      className={`px-3 py-1 rounded-full text-sm font-medium ${
                        venue.status === 'Available'
                          ? 'bg-green-100 text-green-700'
                          : 'bg-red-100 text-red-700'
                      }`}
                    >
                      {venue.status === 'Available' ? '🟢' : '🔴'}{' '}
                      {venue.status}
                    </span>
                  </div>

                </div>

                <button
                  onClick={() =>
                    alert(`${venue.name} is currently ${venue.status}.`)
                  }
                  className={`mt-5 w-full py-3 rounded-lg font-semibold transition ${
                    venue.status === 'Available'
                      ? 'bg-blue-600 text-white hover:bg-blue-700'
                      : 'bg-gray-300 text-gray-600 cursor-not-allowed'
                  }`}
                  disabled={venue.status !== 'Available'}
                >
                  {venue.status === 'Available'
                    ? 'Check Availability'
                    : 'Currently Occupied'}
                </button>

              </div>
            </div>
          ))}

        </div>

        {/* Back to Dashboard */}
        <div className="mt-8">
          <Link
            to="/dashboard"
            className="text-blue-600 hover:underline"
          >
            ← Back to Dashboard
          </Link>
        </div>

      </main>
    </Layout>
  )
}

export default Venues