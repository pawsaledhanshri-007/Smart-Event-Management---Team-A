import { useNavigate } from 'react-router-dom'
import { useEffect, useMemo, useState } from 'react'
import { useParams } from 'react-router-dom'
import { useAuthContext } from '../context/AuthContext'
import Layout from '../components/Layout'
import { apiFetch, publicAssetUrl } from '../services/api'

export default function EventDetails(){
  const { id } = useParams()
  const navigate = useNavigate()
  const { user } = useAuthContext();const[event,setEvent]=useState(null);const[venue,setVenue]=useState(null);const[registration,setRegistration]=useState(null);const[error,setError]=useState('');const[msg,setMsg]=useState('');const[txn,setTxn]=useState('');const[proof,setProof]=useState(null);const[busy,setBusy]=useState(false)
  const load=async()=>{try{const[e,regs]=await Promise.all([apiFetch(`/events/${id}`),apiFetch(`/registrations/me?user_id=${user.id}`)]);setEvent(e);setRegistration(regs.find(r=>r.event_id===id)||null);const v=await apiFetch(`/venues/${e.venue_id}`);setVenue(v)}catch(err){setError(err.message)}};useEffect(()=>{load()},[id])
  const needsPayment=registration?.status==='pending_payment'&&!event?.is_free
  const register = () => {
  navigate('/agent', {
    state: {
      eventId: id,
      eventTitle: event.title
    }
  })
}
  const stripePay=async()=>{setBusy(true);setError('');try{const d=await apiFetch('/payments/stripe/checkout',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({event_id:id})});window.location.href=d.checkout_url}catch(err){setError(err.message);setBusy(false)}}
  const qrPay=async(e)=>{e.preventDefault();setBusy(true);setError('');try{const fd=new FormData();fd.append('event_id',id);fd.append('transaction_reference',txn);if(proof)fd.append('proof',proof);const d=await apiFetch('/payments/qr/submit',{method:'POST',body:fd});setMsg(`QR payment submitted. Status: ${d.status}. Event Manager will verify it.`);setTxn('');setProof(null)}catch(err){setError(err.message)}finally{setBusy(false)}}
  if(!event)return <Layout><main className="page-container">{error?<div className="form-error">{error}</div>:<div className="page-loader">Loading event…</div>}</main></Layout>
  return <Layout><main className="page-container"><div className="event-detail-hero"><div><span className="eyebrow">{event.status.toUpperCase()}</span><h1>{event.title}</h1><p>{event.description||'No description provided.'}</p></div><div className="event-price">{event.is_free?<><strong>Free</strong><small>No registration fee</small></>:<><strong>₹{event.registration_fee}</strong><small>per registration</small></>}</div></div><div className="detail-grid"><section className="panel"><h2>Event details</h2><div className="detail-list"><span>📅 <b>{new Date(event.start_time).toLocaleString()}</b></span><span>⌛ Ends {new Date(event.end_time).toLocaleString()}</span><span>⌖ {venue?.name||'Venue'} · {venue?.location||''}</span><span>◎ Capacity {event.capacity}</span></div>{registration?.status ? (
  <div className={`registration-state ${registration.status}`}>
    Your registration: <strong>{registration.status}</strong>
  </div>
) : event.status === 'completed' ? (
  <button className="primary-button" disabled>
    Event Closed
  </button>
) : event.status === 'cancelled' ? (
  <button className="primary-button" disabled>
    Event Cancelled
  </button>
) : (
  <button className="primary-button" disabled={busy} onClick={register}>
    {busy ? 'Working...' : 'Register for this event'}
  </button>
)}{msg&&<div className="form-success">{msg}</div>}{error&&<div className="form-error">{error}</div>}</section>{needsPayment&&<section className="panel payment-panel"><h2>Complete payment</h2><p className="muted">Your seat is pending until payment is completed.</p>{event.accepts_stripe&&<button className="stripe-button" disabled={busy} onClick={stripePay}>Pay ₹{event.registration_fee} with Stripe</button>}{event.accepts_qr&&<><div className="divider"><span>or pay using QR / UPI</span></div>{event.payment_qr_image_url?<img className="payment-qr" src={publicAssetUrl(event.payment_qr_image_url)} alt="Event payment QR"/>:<div className="form-warning">Event Manager has enabled QR payment but has not uploaded a QR image yet.</div>}<form onSubmit={qrPay}><label>UPI / transaction reference<input required value={txn} onChange={e=>setTxn(e.target.value)} placeholder="e.g. UTR123456789"/></label><label>Payment proof <span className="optional">(optional)</span><input type="file" accept="image/*" onChange={e=>setProof(e.target.files?.[0]||null)}/></label><button className="secondary-button" disabled={busy}>Submit payment for verification</button></form></>}</section>}</div></main></Layout>}
