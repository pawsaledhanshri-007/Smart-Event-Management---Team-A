export const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api'
export const RAG_API_URL = import.meta.env.VITE_RAG_API_URL || 'http://localhost:8001'
export const BACKEND_ORIGIN = new URL(API_URL).origin

export const getToken = () => localStorage.getItem('access_token')
export const getRefreshToken = () => localStorage.getItem('refresh_token')

export function saveTokens(data) {
  if (data?.access_token) localStorage.setItem('access_token', data.access_token)
  if (data?.refresh_token) localStorage.setItem('refresh_token', data.refresh_token)
}

export function clearSession() {
  localStorage.removeItem('access_token')
  localStorage.removeItem('refresh_token')
  localStorage.removeItem('current_user')
}

export function authHeaders(extra = {}) {
  const token = getToken()
  return { ...extra, ...(token ? { Authorization: `Bearer ${token}` } : {}) }
}

async function parseResponse(response) {
  const contentType = response.headers.get('content-type') || ''
  if (response.status === 204) return null
  return contentType.includes('application/json') ? response.json() : response.text()
}

async function refreshAccessToken() {
  const refreshToken = getRefreshToken()
  if (!refreshToken) return false
  const response = await fetch(`${API_URL}/auth/refresh`, {
    method: 'POST', headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ refresh_token: refreshToken }),
  })
  if (!response.ok) {
    clearSession(); return false
  }
  const data = await response.json()
  saveTokens(data)
  return true
}

export async function apiFetch(path, options = {}, retry = true) {
  const headers = authHeaders(options.headers || {})
  const response = await fetch(`${API_URL}${path}`, { ...options, headers })
  if (response.status === 401 && retry && !path.startsWith('/auth/login') && !path.startsWith('/auth/refresh')) {
    if (await refreshAccessToken()) return apiFetch(path, options, false)
  }
  const data = await parseResponse(response)
  if (!response.ok) {
    const detail = data?.detail
    const message = Array.isArray(detail)
      ? detail.map((item) => item.msg || JSON.stringify(item)).join(', ')
      : detail || data?.message || data || `Request failed (${response.status})`
    const error = new Error(String(message)); error.status = response.status; throw error
  }
  return data
}

export function publicAssetUrl(path) {
  if (!path) return ''
  if (/^https?:\/\//.test(path)) return path
  return `${BACKEND_ORIGIN}${path}`
}
