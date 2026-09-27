import { useState } from 'react'
import { Link, NavLink, useNavigate } from 'react-router-dom'
import { useAuthContext } from '../context/AuthContext'
import { publicAssetUrl } from '../services/api'

export default function Navbar() {
  const { user, isSystemAdmin, logout } = useAuthContext()
  const [open, setOpen] = useState(false)
  const navigate = useNavigate()
  const nav = [
    ['/agent', 'Agent'], ['/dashboard', 'Dashboard'], ['/events', 'Events'],
    ['/venues', 'Venues'], ['/registrations', 'Registrations'],
  ]
  const doLogout = async () => { await logout(); navigate('/login') }
  return <header className="topbar">
    <div className="brand"><Link to={isSystemAdmin ? '/admin' : '/agent'}><span className="brand-mark">✦</span> Evently</Link></div>
    <nav className={`main-nav ${open ? 'open' : ''}`}>
      {isSystemAdmin && <NavLink to="/admin" className={({isActive}) => isActive ? 'active' : ''}>Admin</NavLink>}
      {nav.map(([to, label]) => <NavLink key={to} to={to} className={({isActive}) => isActive ? 'active' : ''}>{label}</NavLink>)}
    </nav>
    <div className="profile-menu-wrap">
      <button className="profile-chip" onClick={() => setOpen(!open)}>
        {user?.profile_image_url ? <img src={publicAssetUrl(user.profile_image_url)} alt="Profile" /> : <span>{user?.name?.[0]?.toUpperCase() || 'U'}</span>}
        <div><strong>{user?.name || 'Profile'}</strong><small>{isSystemAdmin ? 'Administrator' : 'User'}</small></div><span>⌄</span>
      </button>
      {open && <div className="profile-popover">
        <Link to="/profile" onClick={() => setOpen(false)}>My Profile</Link>
        {isSystemAdmin && <Link to="/admin" onClick={() => setOpen(false)}>Admin Workspace</Link>}
        <button onClick={doLogout}>Sign out</button>
      </div>}
    </div>
  </header>
}
