import Layout from '../components/Layout'

function AdminAgentActivity() {
  const activities = [
    {
      id: 1,
      user: 'Kaif Ansari',
      action: 'Search Events',
      tool: 'search_events',
      status: 'Success',
    },
    {
      id: 2,
      user: 'Kaif Ansari',
      action: 'Check Venue Availability',
      tool: 'check_venue_availability',
      status: 'Success',
    },
    {
      id: 3,
      user: 'Rahul Sharma',
      action: 'Register Participant',
      tool: 'register_participant',
      status: 'Success',
    },
  ]

  return (
    <Layout>
      <main className="max-w-6xl mx-auto p-6">

        <h2 className="text-3xl font-bold text-gray-800">
          Agent Activity
        </h2>

        <p className="mt-2 text-gray-600">
          Monitor AI agent actions and tool usage.
        </p>

        <div className="bg-white rounded-xl shadow mt-8 overflow-hidden">

          <div className="overflow-x-auto">
            <table className="w-full">

              <thead className="bg-gray-100">
                <tr>
                  <th className="text-left px-6 py-4">User</th>
                  <th className="text-left px-6 py-4">Action</th>
                  <th className="text-left px-6 py-4">Tool</th>
                  <th className="text-left px-6 py-4">Status</th>
                </tr>
              </thead>

              <tbody>
                {activities.map((activity) => (
                  <tr key={activity.id} className="border-t">

                    <td className="px-6 py-4 font-medium">
                      {activity.user}
                    </td>

                    <td className="px-6 py-4">
                      {activity.action}
                    </td>

                    <td className="px-6 py-4 text-gray-600">
                      {activity.tool}
                    </td>

                    <td className="px-6 py-4 text-green-600">
                      {activity.status}
                    </td>

                  </tr>
                ))}
              </tbody>

            </table>
          </div>

        </div>

      </main>
    </Layout>
  )
}

export default AdminAgentActivity