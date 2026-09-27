import { useEffect, useState } from 'react'
import { useLocation } from 'react-router-dom'
import Layout from '../components/Layout'
import { useAuthContext } from '../context/AuthContext'
import { apiFetch } from '../services/api'

const prompts = ['Find events this weekend', 'Suggest a venue for 200 people', 'What is the cancellation policy?', 'Show my registrations']
export default function AIAssistant() {
    const location = useLocation()
    const eventId = location.state?.eventId
    const eventTitle = location.state?.eventTitle
    const { user, isEventManager } = useAuthContext(); const [msg, setMsg] = useState(''); const [session, setSession] = useState(null); const [busy, setBusy] = useState(false); const [chat, setChat] = useState([{ role: 'assistant', text: `Hey 👋🏻! How can I help you?` }]); const send = async (text = msg) => { const q = eventId
  ? `Event context: "${eventTitle}" (Event ID: ${eventId}). User request: ${text.trim()}`
  : text.trim(); if (!q || busy) return; setMsg(''); setChat(v => [...v, { role: 'user', text: q }]); setBusy(true); try { const d = await apiFetch('/agent/chat', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({
  message: q,
  user_id: user.id,
  session_id: session
}) }); setSession(d.session_id); setChat(v => [...v, { role: 'assistant', text: d.response }]) } catch (e) { setChat(v => [...v, { role: 'assistant', text: `I couldn't complete that request: ${e.message}` }]) } finally { setBusy(false) } }; return <Layout showBack={false}><main className="agent-page"><section className="agent-hero"><div className="agent-badge">✦ Evently AI</div><div className="bot-orb">◉</div><h1>Hey 👋🏻!<br />How can I help you?</h1><p>Your intelligent event companion for planning, discovery and real database actions.</p><div className="prompt-row">{prompts.map(p => <button key={p} onClick={() => send(p)}>{p}</button>)}</div></section><section className="chat-shell"><div className="chat-messages">{chat.map((m, i) => <div className={`chat-message ${m.role}`} key={i}><span>{m.role === 'assistant' ? '✦' : 'You'}</span><p>{m.text}</p></div>)}{busy && <div className="chat-message assistant"><span>✦</span><p>Thinking and checking your event data…</p></div>}</div><form className="chat-input" onSubmit={e => { e.preventDefault(); send() }}><input value={msg} onChange={e => setMsg(e.target.value)} placeholder={isEventManager ? 'Ask me to create, update or analyze an event…' : 'Ask about events, venues, registrations or policies…'} /><button disabled={busy}>➜</button></form><small>Signed in as {user?.name} · {isEventManager ? 'Event Manager' : 'User'} · AI can make mistakes, verify important details.</small></section></main></Layout>
}
