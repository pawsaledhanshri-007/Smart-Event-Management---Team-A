import { useEffect, useMemo, useState } from 'react'
import { Link } from 'react-router-dom'
import Layout from '../components/Layout'
import CreateEventModal from '../components/CreateEventModal'
import { useAuthContext } from '../context/AuthContext'
import { apiFetch } from '../services/api'

export default function Events() {
  const { isEventManager } = useAuthContext(); const [events, setEvents] = useState([]); const [venues, setVenues] = useState({}); const [q, setQ] = useState(''); const [open, setOpen] = useState(false);
  const [deleteMode, setDeleteMode] = useState(false);
  const [selectedEvent, setSelectedEvent] = useState('');
  const [error, setError] = useState(''); const load = async () => { try { const [e, v] = await Promise.all([apiFetch('/events'), apiFetch('/venues')]); setEvents(e); setVenues(Object.fromEntries(v.map(x => [x.id, x]))) } catch (err) { setError(err.message) } }; const deleteEvent = async () => {
    if (!selectedEvent) return;

    try {
      await apiFetch(`/events/${selectedEvent}`, {
        method: 'DELETE'
      });

      setSelectedEvent('');
      setDeleteMode(false);
      load();
    } catch (err) {
      setError(err.message);
    }
  }; useEffect(() => { load() }, []); const filtered = useMemo(() => events.filter(e => `${e.title} ${e.description || ''}`.toLowerCase().includes(q.toLowerCase())), [events, q]); return <Layout><main className="page-container"><div className="page-heading split"><div><span className="eyebrow">DISCOVER • ATTEND • MANAGE</span><h1>Events</h1><p>Everything here comes from the event database.</p></div>{isEventManager && (
    <div style={{ display: 'flex', gap: '12px', alignItems: 'center' }}>
      <button
        className="primary-button compact"
        onClick={() => setOpen(true)}
      >
        ＋ Create Event
      </button>

      <button
        className="primary-button compact"
        onClick={() => {
          setDeleteMode(!deleteMode);
          setSelectedEvent('');
        }}
      >
        Delete Event
      </button>
    </div>
  )}</div><div className="toolbar"><input value={q} onChange={e => setQ(e.target.value)} placeholder="Search events…" /><span>{filtered.length} events</span></div>{deleteMode && (
    <div className="inline-create panel">
      <select
        value={selectedEvent}
        onChange={e => setSelectedEvent(e.target.value)}
      >
        <option value="">Select event to delete</option>

        {events.map(e => (
          <option key={e.id} value={e.id}>
            {e.title}
          </option>
        ))}
      </select>

      <button
        className="primary-button compact"
        onClick={deleteEvent}
        disabled={!selectedEvent}
      >
        Delete Selected
      </button>
    </div>
  )}{error && <div className="form-error">{error}</div>}<div className="card-grid">{filtered.map(e => <Link to={`/events/${e.id}`} className="event-card" key={e.id}><div className="event-card-top"><span className="date-chip">{new Date(e.start_time).toLocaleDateString('en-IN', { day: '2-digit', month: 'short' })}</span><span className={`status-pill ${e.status === 'scheduled' ? 'success' : ''}`}>{e.status}</span></div><h3>{e.title}</h3><p>{e.description || 'No description provided.'}</p><div className="event-meta"><span>⌖ {venues[e.venue_id]?.name || 'Venue'}</span><span>◎ {e.capacity} seats</span><span>
    {Number(e.registration_fee) > 0
      ? `₹${Number(e.registration_fee).toFixed(2)}`
      : 'Free'}
  </span></div></Link>)}</div><CreateEventModal open={open} onClose={() => setOpen(false)} onCreated={load} /></main></Layout>
}
