import { useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import Layout from '../components/Layout'

function EventDetails() {
  const { id } = useParams()
  const [registered, setRegistered] = useState(false)

  const events = [
    {
      id: 1,
      title: 'AI & Machine Learning Workshop',
      date: '10 September 2026',
      time: '10:00 AM - 2:00 PM',
      venue: 'Main Auditorium',
      seats: 50,
      category: 'Technology',
      organizer: 'Smart Event Management Team',
      description:
        'Learn the fundamentals of Artificial Intelligence and Machine Learning through an interactive workshop.',
    },
    {
      id: 2,
      title: 'Web Development Bootcamp',
      date: '15 September 2026',
      time: '10:00 AM - 4:00 PM',
      venue: 'Computer Lab 1',
      seats: 30,
      category: 'Development',
      organizer: 'Smart Event Management Team',
      description:
        'Learn modern web development concepts and build interactive web applications.',
    },
    {
      id: 3,
      title: 'Data Science Seminar',
      date: '20 September 2026',
      time: '11:00 AM - 2:00 PM',
      venue: 'Seminar Hall',
      seats: 100,
      category: 'Data Science',
      organizer: 'Smart Event Management Team',
      description:
        'Explore data science concepts, analytics techniques and real-world applications.',
    },
  ]

  const event = events.find((event) => event.id === Number(id))

  if (!event) {
    return (
      <Layout>
        <main className="max-w-4xl mx-auto p-6">
          <div className="bg-white rounded-2xl shadow p-10 text-center">
            <div className="text-5xl">🔍</div>

            <h2 className="text-2xl font-bold text-gray-800 mt-4">
              Event Not Found
            </h2>

            <p className="text-gray-600 mt-2">
              The event you are looking for does not exist.
            </p>

            <Link
              to="/events"
              className="inline-block mt-6 bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700"
            >
              ← Back to Events
            </Link>
          </div>
        </main>
      </Layout>
    )
  }

  return (
    <Layout>
      <main className="max-w-5xl mx-auto p-6">

        {/* Back */}
        <Link
          to="/events"
          className="inline-block mb-6 text-blue-600 hover:underline"
        >
          ← Back to Events
        </Link>

        {/* Main Card */}
        <div className="bg-white rounded-2xl shadow overflow-hidden">

          {/* Hero */}
          <div className="bg-gradient-to-r from-blue-600 to-indigo-600 p-8 text-white">

            <span className="inline-block bg-white/20 px-3 py-1 rounded-full text-sm">
              {event.category}
            </span>

            <h1 className="text-3xl md:text-4xl font-bold mt-4">
              {event.title}
            </h1>

            <p className="mt-3 text-blue-100">
              Organized by {event.organizer}
            </p>

          </div>

          {/* Details */}
          <div className="p-8">

            <h2 className="text-2xl font-bold text-gray-800">
              Event Details
            </h2>

            <p className="mt-4 text-gray-600 leading-7">
              {event.description}
            </p>

            {/* Information Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-5 mt-8">

              <div className="bg-gray-50 rounded-xl p-5">
                <p className="text-sm text-gray-500">
                  Date
                </p>
                <p className="font-semibold text-gray-800 mt-1">
                  📅 {event.date}
                </p>
              </div>

              <div className="bg-gray-50 rounded-xl p-5">
                <p className="text-sm text-gray-500">
                  Time
                </p>
                <p className="font-semibold text-gray-800 mt-1">
                  🕐 {event.time}
                </p>
              </div>

              <div className="bg-gray-50 rounded-xl p-5">
                <p className="text-sm text-gray-500">
                  Venue
                </p>
                <p className="font-semibold text-gray-800 mt-1">
                  📍 {event.venue}
                </p>
              </div>

              <div className="bg-gray-50 rounded-xl p-5">
                <p className="text-sm text-gray-500">
                  Available Seats
                </p>
                <p className="font-semibold text-gray-800 mt-1">
                  🎟️ {event.seats} seats
                </p>
              </div>

            </div>

            {/* Registration */}
            <div className="mt-8 border-t pt-8">

              {!registered ? (
                <button
                  onClick={() => setRegistered(true)}
                  className="bg-blue-600 text-white px-8 py-3 rounded-lg font-semibold hover:bg-blue-700 transition"
                >
                  Register for Event →
                </button>
              ) : (
                <div>
                  <div className="bg-green-50 border border-green-200 rounded-xl p-5">
                    <p className="font-bold text-green-700">
                      🎉 Registration Successful!
                    </p>

                    <p className="mt-1 text-green-600">
                      You have successfully registered for this event.
                    </p>
                  </div>

                  <Link
                    to="/registrations"
                    className="inline-block mt-4 bg-green-600 text-white px-6 py-3 rounded-lg font-semibold hover:bg-green-700"
                  >
                    View My Registrations →
                  </Link>
                </div>
              )}

            </div>

          </div>
        </div>

      </main>
    </Layout>
  )
}

export default EventDetails