import { createContext, useContext, useEffect, useMemo, useState } from 'react'
import { apiFetch, clearSession, getRefreshToken, getToken, saveTokens } from '../services/api'

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [user, setUser] = useState(() => {
    try { return JSON.parse(localStorage.getItem('current_user') || 'null') } catch { return null }
  })
  const [loading, setLoading] = useState(Boolean(getToken()))

  const refreshUser = async () => {
    if (!getToken()) { setUser(null); setLoading(false); return null }
    try {
      const me = await apiFetch('/auth/me')
      localStorage.setItem('current_user', JSON.stringify(me)); setUser(me); return me
    } catch {
      clearSession(); setUser(null); return null
    } finally { setLoading(false) }
  }

  useEffect(() => { refreshUser() }, [])

  const finishLogin = async (data) => {
    saveTokens(data)
    return refreshUser()
  }

  const logout = async () => {
    const refreshToken = getRefreshToken()
    if (refreshToken) {
      try {
        await apiFetch('/auth/logout', {
          method: 'POST', headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ refresh_token: refreshToken }),
        }, false)
      } catch { /* local sign-out still proceeds */ }
    }
    clearSession(); setUser(null)
  }

  const value = useMemo(() => ({
    user, setUser, loading, isAuthenticated: Boolean(user && getToken()),
    isEventManager: ['organizer', 'admin'].includes(user?.role),
    isSystemAdmin: user?.role === 'admin', finishLogin, refreshUser, logout,
  }), [user, loading])

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export const useAuthContext = () => useContext(AuthContext)
