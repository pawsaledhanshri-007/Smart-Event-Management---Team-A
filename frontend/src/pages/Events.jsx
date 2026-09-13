import { useState } from 'react'
import { Link } from 'react-router-dom'
import Layout from '../components/Layout'

function Events() {
  const [search, setSearch] = useState('')

  const events = [
    {
      id: 1,
      title: 'AI & Machine Learning Workshop',
      date: '10 September 2026',
      time: '10:00 AM - 2:00 PM',
      venue: 'Main Auditorium',
      seats: 50,
      category: 'Technology',
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
      description:
        'Explore data science concepts, analytics techniques and real-world applications.',
    },
  ]

  const filteredEvents = events.filter((event) =>
    event.title.toLowerCase().includes(search.toLowerCase())
  )

  return (
    <Layout>
      <main className="max-w-7xl mx-auto p-6">

        {/* Header */}
        <div className="mb-8">
          <h2 className="text-3xl font-bold text-gray-800">
            Upcoming Events
          </h2>

          <p className="mt-2 text-gray-600">
            Discover and register for upcoming events.
          </p>
        </div>

        {/* Search */}
        <div className="bg-white rounded-2xl shadow p-5 mb-8">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Search Events
          </label>

          <input
            type="text"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Search by event name..."
            className="w-full border border-gray-300 rounded-lg px-4 py-3 outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>

        {/* Event Cards */}
        {filteredEvents.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">

            {filteredEvents.map((event) => (
              <div
                key={event.id}
                className="bg-white rounded-2xl shadow hover:shadow-xl transition overflow-hidden"
              >

                {/* Card Header */}
                <div className="bg-gradient-to-r from-blue-600 to-indigo-600 p-6 text-white">
                  <span className="text-sm bg-white/20 px-3 py-1 rounded-full">
                    {event.category}
                  </span>

                  <h3 className="text-xl font-bold mt-4">
                    {event.title}
                  </h3>
                </div>

                {/* Card Body */}
                <div className="p-6">

                  <p className="text-gray-600 text-sm leading-6">
                    {event.description}
                  </p>

                  <div className="mt-5 space-y-3 text-sm">

                    <p className="text-gray-700">
                      📅 <span className="font-medium">{event.date}</span>
                    </p>

                    <p className="text-gray-700">
                      🕐 <span className="font-medium">{event.time}</span>
                    </p>

                    <p className="text-gray-700">
                      📍 <span className="font-medium">{event.venue}</span>
                    </p>

                    <p className="text-gray-700">
                      🎟️ <span className="font-medium">{event.seats} seats</span>
                    </p>

                  </div>

                  <Link
                    to={`/events/${event.id}`}
                    className="block text-center mt-6 w-full bg-blue-600 text-white py-3 rounded-lg font-medium hover:bg-blue-700 transition"
                  >
                    View Event →
                  </Link>

                </div>
              </div>
            ))}

          </div>
        ) : (
          <div className="bg-white rounded-2xl shadow p-10 text-center">
            <div className="text-4xl">🔍</div>

            <h3 className="text-xl font-bold text-gray-800 mt-4">
              No Events Found
            </h3>

            <p className="text-gray-600 mt-2">
              Try searching with a different event name.
            </p>
          </div>
        )}

      </main>
    </Layout>
  )
}

export default Events