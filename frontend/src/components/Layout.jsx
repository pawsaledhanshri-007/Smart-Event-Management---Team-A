import BackButton from './BackButton'
import Navbar from './Navbar'

export default function Layout({ children, showBack = true }) {
  return <div className="app-shell"><Navbar />{showBack && <div className="back-row"><BackButton /></div>}{children}</div>
}
