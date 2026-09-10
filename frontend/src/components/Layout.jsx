import Navbar from './Navbar'

function Layout({ children }) {
  return (
    <div className="min-h-screen bg-gray-100">
      <Navbar />
      {children}
    </div>
  )
}

export default Layout