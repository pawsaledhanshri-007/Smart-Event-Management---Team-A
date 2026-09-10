import Layout from '../components/Layout'

function AdminUsers() {
  const users = [
    {
      id: 1,
      name: 'Kaif Ansari',
      email: 'kaif@example.com',
      role: 'User',
      status: 'Active',
    },
    {
      id: 2,
      name: 'Admin User',
      email: 'admin@example.com',
      role: 'Admin',
      status: 'Active',
    },
    {
      id: 3,
      name: 'Rahul Sharma',
      email: 'rahul@example.com',
      role: 'User',
      status: 'Active',
    },
  ]

  return (
    <Layout>

      

      <main className="max-w-6xl mx-auto p-6">

        <h2 className="text-3xl font-bold text-gray-800">
          Manage Users
        </h2>

        <p className="mt-2 text-gray-600">
          View and manage registered users.
        </p>

        <div className="bg-white rounded-xl shadow mt-8 overflow-hidden">

          <div className="overflow-x-auto">
            <table className="w-full">

              <thead className="bg-gray-100">
                <tr>
                  <th className="text-left px-6 py-4">Name</th>
                  <th className="text-left px-6 py-4">Email</th>
                  <th className="text-left px-6 py-4">Role</th>
                  <th className="text-left px-6 py-4">Status</th>
                </tr>
              </thead>

              <tbody>
                {users.map((user) => (
                  <tr key={user.id} className="border-t">
                    <td className="px-6 py-4 font-medium">
                      {user.name}
                    </td>

                    <td className="px-6 py-4 text-gray-600">
                      {user.email}
                    </td>

                    <td className="px-6 py-4">
                      {user.role}
                    </td>

                    <td className="px-6 py-4 text-green-600">
                      {user.status}
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

export default AdminUsers