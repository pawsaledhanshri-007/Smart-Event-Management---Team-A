import { useState } from 'react'
import Layout from '../components/Layout'

function Registrations() {
  const [myRegistrations, setMyRegistrations] = useState([
    {
      id: 1,
      event: 'AI & Machine Learning Workshop',
      date: '10 September 2026',
      time: '10:00 AM - 2:00 PM',
      venue: 'Main Auditorium',
      status: 'Confirmed',
    },
    {
      id: 2,
      event: 'Data Science Seminar',
      date: '20 September 2026',
      time: '11:00 AM - 2:00 PM',
      venue: 'Seminar Hall',
      status: 'Confirmed',
    },
  ])

  const [cancelledEvent, setCancelledEvent] = useState('')

  const handleCancel = (registration) => {
    setMyRegistrations((prev) =>
      prev.filter((item) => item.id !== registration.id)
    )

    setCancelledEvent(registration.event)
  }

  return (
    <Layout>
      <main className="max-w-7xl mx-auto p-6">

        {/* Header */}
        <div className="mb-8">
          <h2 className="text-3xl font-bold text-gray-800">
            My Registrations
          </h2>

          <p className="mt-2 text-gray-600">
            View and manage your registered events.
          </p>
        </div>

        {/* Cancellation Message */}
        {cancelledEvent && (
          <div className="mb-6 bg-red-50 border border-red-200 rounded-xl p-5">
            <p className="font-semibold text-red-700">
              Registration Cancelled
            </p>

            <p className="mt-1 text-red-600">
              Your registration for "{cancelledEvent}" has been cancelled successfully.
            </p>
          </div>
        )}

        {/* Registrations */}
        {myRegistrations.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">

            {myRegistrations.map((registration) => (
              <div
                key={registration.id}
                className="bg-white rounded-2xl shadow hover:shadow-lg transition overflow-hidden"
              >

                {/* Card Header */}
                <div className="bg-gradient-to-r from-green-600 to-emerald-600 p-6 text-white">

                  <div className="flex items-center justify-between gap-4">

                    <div>
                      <p className="text-green-100 text-sm">
                        Registered Event
                      </p>

                      <h3 className="text-xl font-bold mt-1">
                        {registration.event}
                      </h3>
                    </div>

                    <span className="bg-white/20 px-3 py-1 rounded-full text-sm whitespace-nowrap">
                      ✓ {registration.status}
                    </span>

                  </div>

                </div>

                {/* Card Body */}
                <div className="p-6">

                  <div className="space-y-4">

                    <div className="flex items-start gap-3">
                      <span className="text-xl">📅</span>

                      <div>
                        <p className="text-sm text-gray-500">
                          Date
                        </p>

                        <p className="font-medium text-gray-800">
                          {registration.date}
                        </p>
                      </div>
                    </div>

                    <div className="flex items-start gap-3">
                      <span className="text-xl">🕐</span>

                      <div>
                        <p className="text-sm text-gray-500">
                          Time
                        </p>

                        <p className="font-medium text-gray-800">
                          {registration.time}
                        </p>
                      </div>
                    </div>

                    <div className="flex items-start gap-3">
                      <span className="text-xl">📍</span>

                      <div>
                        <p className="text-sm text-gray-500">
                          Venue
                        </p>

                        <p className="font-medium text-gray-800">
                          {registration.venue}
                        </p>
                      </div>
                    </div>

                  </div>

                  {/* Cancel */}
                  <button
                    onClick={() => handleCancel(registration)}
                    className="mt-6 w-full bg-red-600 text-white py-3 rounded-lg font-semibold hover:bg-red-700 transition"
                  >
                    Cancel Registration
                  </button>

                </div>
              </div>
            ))}

          </div>
        ) : (
          /* Empty State */
          <div className="bg-white rounded-2xl shadow p-10 text-center">

            <div className="text-5xl">
              🎟️
            </div>

            <h3 className="text-xl font-bold text-gray-800 mt-4">
              No Registrations Yet
            </h3>

            <p className="text-gray-600 mt-2">
              You have not registered for any events yet.
            </p>

          </div>
        )}

      </main>
    </Layout>
  )
}

export default Registrations