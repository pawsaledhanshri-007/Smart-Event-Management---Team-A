
import { useCallback, useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import Layout from '../components/Layout'
import { apiFetch } from '../services/api'
import { useAuthContext } from '../context/AuthContext'

export default function Registrations() {
    const { user } = useAuthContext()

    const [regs, setRegs] = useState([])
    const [events, setEvents] = useState({})
    const [error, setError] = useState('')
    const [loading, setLoading] = useState(true)

    const load = useCallback(async () => {
        if (!user?.id) return

        try {
            setError('')

            const registrations = await apiFetch(
                `/registrations/me?user_id=${user.id}`
            )

            setRegs(registrations)

            // Fetch event details only for active registrations.
            const activeRegistrations = registrations.filter(
                registration =>
                    (registration.status || '').toLowerCase() !== 'cancelled'
            )

            const ids = [
                ...new Set(activeRegistrations.map(r => r.event_id))
            ]

            const pairs = await Promise.all(
                ids.map(async id => [
                    id,
                    await apiFetch(`/events/${id}`)
                ])
            )

            setEvents(Object.fromEntries(pairs))
        } catch (e) {
            setError(e.message)
        } finally {
            setLoading(false)
        }
    }, [user?.id])

    useEffect(() => {
        load()
    }, [load])

    const cancel = async registration => {
        try {
            await apiFetch(
                `/events/${registration.event_id}/register?user_id=${user.id}`,
                { method: 'DELETE' }
            )

            // Refresh registrations after successful cancellation.
            await load()
        } catch (e) {
            setError(e.message)
        }
    }

    // Never display cancelled registrations in the active list.
    const activeRegs = regs.filter(
        registration =>
            (registration.status || '').toLowerCase() !== 'cancelled'
    )

    return (
        <Layout>
            <main className="page-container">
                <div className="page-heading">
                    <span className="eyebrow">YOUR BOOKINGS</span>
                    <h1>My Registrations</h1>
                    <p>Only your own active registrations are visible here.</p>
                </div>

                {error && (
                    <div className="form-error">{error}</div>
                )}

                {loading ? (
                    <div className="empty-state panel">
                        Loading your registrations...
                    </div>
                ) : (
                    <div className="registration-list">
                        {activeRegs.map(r => {
                            const event = events[r.event_id]

                            return (
                                <article
                                    className="registration-card"
                                    key={r.id}
                                >
                                    <div>
                                        <span
                                            className={`status-pill ${r.status === 'confirmed'
                                                ? 'success'
                                                : r.status === 'pending_payment'
                                                    ? 'warning'
                                                    : ''
                                                }`}
                                        >
                                            {(r.status || 'unknown').replace('_', ' ')}
                                        </span>

                                        <h3>{event?.title || 'Event'}</h3>

                                        <p>
                                            {event
                                                ? new Date(event.start_time).toLocaleString()
                                                : ''}
                                        </p>
                                    </div>

                                    <div className="registration-actions">
                                        <Link
                                            className="secondary-button compact"
                                            to={`/events/${r.event_id}`}
                                        >
                                            {r.status === 'pending_payment'
                                                ? 'Complete payment'
                                                : 'View event'}
                                        </Link>

                                        <button
                                            className="text-danger"
                                            onClick={() => cancel(r)}
                                        >
                                            Cancel
                                        </button>
                                    </div>
                                </article>
                            )
                        })}

                        {!error && activeRegs.length === 0 && (
                            <div className="empty-state panel">
                                You have no active event registrations.{' '}
                                <Link to="/events">Explore events →</Link>
                            </div>
                        )}
                    </div>
                )}
            </main>
        </Layout>
    )
}
