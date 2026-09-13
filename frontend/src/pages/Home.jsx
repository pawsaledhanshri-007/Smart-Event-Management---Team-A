import { Link } from 'react-router-dom'
import Navbar from '../components/Navbar'

function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-white to-blue-50">
      <Navbar />

      {/* Hero Section */}
      <main className="max-w-7xl mx-auto px-6 lg:px-8">

        <section className="grid lg:grid-cols-2 gap-10 lg:gap-14 items-center pt-14 pb-12">

          {/* Left Content */}
          <div>

            <div className="inline-flex items-center gap-2 bg-blue-100 text-blue-700 px-4 py-2 rounded-full text-sm font-medium">
              🎉 Plan&nbsp; • &nbsp;Manage&nbsp; • &nbsp;Experience
            </div>

            <h1 className="mt-6 text-5xl lg:text-6xl font-extrabold leading-tight text-slate-900">
              Smart Event
              <span className="block text-blue-600">
                Management System
              </span>
            </h1>

            <p className="mt-6 text-lg text-slate-600 leading-8 max-w-xl">
              Plan, manage and organize events effortlessly with the power of AI.
              Discover events, book venues, and create memorable experiences.
            </p>

            {/* Buttons */}
            <div className="flex flex-wrap gap-4 mt-8">

              <Link
                to="/login"
                className="bg-blue-600 text-white px-7 py-3.5 rounded-xl font-semibold hover:bg-blue-700 transition shadow-lg shadow-blue-200"
              >
                Get Started&nbsp; →
              </Link>

              <Link
                to="/events"
                className="border border-slate-300 bg-white text-slate-700 px-7 py-3.5 rounded-xl font-semibold hover:border-blue-400 hover:text-blue-600 transition"
              >
                ▶ &nbsp;Watch Demo
              </Link>

            </div>

            {/* Stats */}
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-6 mt-10">

              <div>
                <div className="w-11 h-11 bg-blue-100 rounded-xl flex items-center justify-center text-xl">
                  📅
                </div>
                <p className="text-2xl font-bold text-slate-900 mt-3">
                  3+
                </p>
                <p className="text-sm text-slate-500">
                  Events
                </p>
              </div>

              <div>
                <div className="w-11 h-11 bg-green-100 rounded-xl flex items-center justify-center text-xl">
                  👥
                </div>
                <p className="text-2xl font-bold text-slate-900 mt-3">
                  100+
                </p>
                <p className="text-sm text-slate-500">
                  Participants
                </p>
              </div>

              <div>
                <div className="w-11 h-11 bg-pink-100 rounded-xl flex items-center justify-center text-xl">
                  📍
                </div>
                <p className="text-2xl font-bold text-slate-900 mt-3">
                  5+
                </p>
                <p className="text-sm text-slate-500">
                  Venues
                </p>
              </div>

              <div>
                <div className="w-11 h-11 bg-yellow-100 rounded-xl flex items-center justify-center text-xl">
                  ⚡
                </div>
                <p className="text-2xl font-bold text-slate-900 mt-3">
                  AI
                </p>
                <p className="text-sm text-slate-500">
                  Powered
                </p>
              </div>

            </div>

          </div>

          {/* Right Illustration */}
          <div className="relative">

            <div className="absolute -top-10 right-10 w-40 h-40 bg-blue-200 rounded-full blur-3xl opacity-50" />
            <div className="absolute -bottom-10 left-10 w-48 h-48 bg-indigo-200 rounded-full blur-3xl opacity-40" />

            <div className="relative bg-gradient-to-br from-blue-100 via-sky-50 to-indigo-100 rounded-3xl p-5 shadow-xl border border-white">

              {/* Building */}
              <div className="bg-gradient-to-b from-sky-300 to-blue-100 rounded-2xl h-[360px] overflow-hidden relative">

                <div className="absolute top-10 left-1/2 -translate-x-1/2 w-4/5 bg-slate-200 rounded-t-xl shadow-lg">

                  <div className="bg-blue-600 text-white text-center font-bold text-xl p-5">
                    EVENTS
                    <br />
                    CONNECT
                    <br />
                    PEOPLE
                  </div>

                  <div className="grid grid-cols-5 gap-2 p-5 bg-slate-100">
                    {[1, 2, 3, 4, 5].map((item) => (
                      <div
                        key={item}
                        className="h-24 bg-blue-200 rounded"
                      />
                    ))}
                  </div>

                  <div className="h-24 bg-slate-300 flex items-end justify-center gap-3">
                    <span className="text-3xl">🧑</span>
                    <span className="text-3xl">🧑</span>
                    <span className="text-3xl">🧑</span>
                    <span className="text-3xl">🧑</span>
                    <span className="text-3xl">🧑</span>
                  </div>

                </div>

                {/* Trees */}
                <div className="absolute bottom-5 left-5 text-5xl">
                  🌳
                </div>

                <div className="absolute bottom-5 right-5 text-5xl">
                  🌳
                </div>

              </div>

              {/* Checklist */}
              <div className="absolute top-10 right-0 translate-x-5 bg-white rounded-2xl shadow-xl p-5 w-56">

                <div className="flex items-center gap-3 py-2">
                  <span className="bg-blue-100 p-2 rounded-lg">
                    📅
                  </span>
                  <span className="font-semibold text-sm">
                    Plan Events
                  </span>
                  <span className="ml-auto text-blue-600">
                    ✓
                  </span>
                </div>

                <div className="flex items-center gap-3 py-2">
                  <span className="bg-pink-100 p-2 rounded-lg">
                    📍
                  </span>
                  <span className="font-semibold text-sm">
                    Check Venues
                  </span>
                  <span className="ml-auto text-blue-600">
                    ✓
                  </span>
                </div>

                <div className="flex items-center gap-3 py-2">
                  <span className="bg-green-100 p-2 rounded-lg">
                    👥
                  </span>
                  <span className="font-semibold text-sm">
                    Register Easily
                  </span>
                  <span className="ml-auto text-blue-600">
                    ✓
                  </span>
                </div>

                <div className="flex items-center gap-3 py-2">
                  <span className="bg-indigo-100 p-2 rounded-lg">
                    🤖
                  </span>
                  <span className="font-semibold text-sm">
                    AI Assistance
                  </span>
                  <span className="ml-auto text-blue-600">
                    ✓
                  </span>
                </div>

              </div>

              {/* Slogan */}
              <div className="absolute bottom-2 right-8 bg-white/80 backdrop-blur-sm px-5 py-3 rounded-xl">
                <p className="text-lg font-semibold italic text-blue-900">
                  Events Make Memories
                </p>
              </div>

            </div>

          </div>

        </section>

        {/* Features */}
        <section className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 pb-14">

          <Link
            to="/events"
            className="bg-white rounded-2xl p-6 shadow-sm hover:shadow-xl transition border border-slate-100"
          >
            <div className="w-12 h-12 bg-blue-100 rounded-xl flex items-center justify-center text-2xl">
              📅
            </div>

            <h3 className="text-xl font-bold text-slate-900 mt-5">
              Discover Events
            </h3>

            <p className="text-slate-500 mt-2 leading-6">
              Explore upcoming events, workshops, seminars and more.
            </p>
          </Link>

          <Link
            to="/venues"
            className="bg-white rounded-2xl p-6 shadow-sm hover:shadow-xl transition border border-slate-100"
          >
            <div className="w-12 h-12 bg-green-100 rounded-xl flex items-center justify-center text-2xl">
              📍
            </div>

            <h3 className="text-xl font-bold text-slate-900 mt-5">
              Book Venues
            </h3>

            <p className="text-slate-500 mt-2 leading-6">
              Check venue availability and manage event locations.
            </p>
          </Link>

          <Link
            to="/registrations"
            className="bg-white rounded-2xl p-6 shadow-sm hover:shadow-xl transition border border-slate-100"
          >
            <div className="w-12 h-12 bg-pink-100 rounded-xl flex items-center justify-center text-2xl">
              👥
            </div>

            <h3 className="text-xl font-bold text-slate-900 mt-5">
              Manage Registrations
            </h3>

            <p className="text-slate-500 mt-2 leading-6">
              Register for events and track your participation.
            </p>
          </Link>

          <Link
            to="/ai-assistant"
            className="bg-white rounded-2xl p-6 shadow-sm hover:shadow-xl transition border border-slate-100"
          >
            <div className="w-12 h-12 bg-purple-100 rounded-xl flex items-center justify-center text-2xl">
              🤖
            </div>

            <h3 className="text-xl font-bold text-slate-900 mt-5">
              AI Assistant
            </h3>

            <p className="text-slate-500 mt-2 leading-6">
              Get instant help with events, venues and registrations.
            </p>
          </Link>

        </section>

      </main>
    </div>
  )
}

export default Home