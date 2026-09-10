import { useState } from 'react'
import Layout from '../components/Layout'

function AIAssistant() {
  const [message, setMessage] = useState('')

  const [messages, setMessages] = useState([
    {
      sender: 'ai',
      text: 'Hello! 👋 I am your Event Management Assistant. How can I help you today?',
    },
  ])

  const handleSend = () => {
    if (!message.trim()) return

    const userMessage = {
      sender: 'user',
      text: message,
    }

    const aiMessage = {
      sender: 'ai',
      text: getAIResponse(message),
    }

    setMessages((prev) => [...prev, userMessage, aiMessage])
    setMessage('')
  }

  const getAIResponse = (text) => {
    const query = text.toLowerCase()

    if (query.includes('event')) {
      return 'Sure! 🤖 We currently have AI & Machine Learning Workshop, Web Development Bootcamp, and Data Science Seminar available.'
    }

    if (query.includes('venue')) {
      return 'I can help with venue availability. 🏢 Main Auditorium and Seminar Hall are currently available.'
    }

    if (query.includes('register')) {
      return 'You can register for an event by opening the event details and clicking the "Register for Event" button. 🎟️'
    }

    if (query.includes('cancel')) {
      return 'You can cancel your registration from the My Registrations page. ❌'
    }

    if (query.includes('hello') || query.includes('hi')) {
      return 'Hello! 👋 I can help you find events, check venue availability, and manage registrations.'
    }

    return 'I can help you with events, venue availability, registrations, and event policies. 🤖 Try asking me something like "Find upcoming events".'
  }

  const quickQuestions = [
    'Find upcoming events',
    'Check venue availability',
    'How can I register?',
    'How can I cancel my registration?',
  ]

  const handleQuickQuestion = (question) => {
    setMessage(question)
  }

  return (
    <Layout>
      <main className="max-w-5xl mx-auto p-6">

        {/* Header */}
        <div className="mb-6">
          <h2 className="text-3xl font-bold text-gray-800">
            AI Event Assistant 🤖
          </h2>

          <p className="mt-2 text-gray-600">
            Ask the assistant about events, venues and registrations.
          </p>
        </div>

        {/* Chat Container */}
        <div className="bg-white rounded-2xl shadow overflow-hidden">

          {/* Chat Header */}
          <div className="bg-gradient-to-r from-blue-600 to-indigo-600 p-5 text-white">
            <div className="flex items-center gap-3">
              <div className="w-11 h-11 bg-white/20 rounded-full flex items-center justify-center text-xl">
                🤖
              </div>

              <div>
                <h3 className="font-bold">
                  Smart Event Assistant
                </h3>

                <p className="text-sm text-blue-100">
                  Online • Ready to help
                </p>
              </div>
            </div>
          </div>

          {/* Messages */}
          <div className="h-[450px] overflow-y-auto p-6 bg-gray-50">

            {messages.map((msg, index) => (
              <div
                key={index}
                className={`flex mb-5 ${
                  msg.sender === 'user'
                    ? 'justify-end'
                    : 'justify-start'
                }`}
              >

                <div
                  className={`max-w-[75%] px-5 py-3 rounded-2xl ${
                    msg.sender === 'user'
                      ? 'bg-blue-600 text-white rounded-br-none'
                      : 'bg-white text-gray-800 shadow-sm rounded-bl-none'
                  }`}
                >
                  {msg.text}
                </div>

              </div>
            ))}

          </div>

          {/* Quick Questions */}
          <div className="px-6 pt-5">

            <p className="text-sm font-medium text-gray-500 mb-3">
              Quick Questions
            </p>

            <div className="flex flex-wrap gap-2">

              {quickQuestions.map((question) => (
                <button
                  key={question}
                  onClick={() => handleQuickQuestion(question)}
                  className="border border-gray-300 text-gray-700 px-4 py-2 rounded-full text-sm hover:border-blue-500 hover:text-blue-600 transition"
                >
                  {question}
                </button>
              ))}

            </div>

          </div>

          {/* Input */}
          <div className="p-6">

            <div className="flex gap-3">

              <input
                type="text"
                value={message}
                onChange={(e) => setMessage(e.target.value)}
                onKeyDown={(e) => {
                  if (e.key === 'Enter') {
                    handleSend()
                  }
                }}
                placeholder="Ask something about events..."
                className="flex-1 border border-gray-300 rounded-xl px-4 py-3 outline-none focus:ring-2 focus:ring-blue-500"
              />

              <button
                onClick={handleSend}
                className="bg-blue-600 text-white px-6 py-3 rounded-xl font-semibold hover:bg-blue-700 transition"
              >
                Send
              </button>

            </div>

          </div>

        </div>

      </main>
    </Layout>
  )
}

export default AIAssistant