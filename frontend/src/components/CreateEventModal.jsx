import { useEffect, useState } from 'react'
import { apiFetch } from '../services/api'

const empty = { title:'', description:'', venue_id:'', start_time:'', end_time:'', capacity:'', is_free:true, registration_fee:'', accepts_stripe:true, accepts_qr:false }

export default function CreateEventModal({ open, onClose, onCreated }) {
  const [form,setForm]=useState(empty); const[venues,setVenues]=useState([]); const[qr,setQr]=useState(null); const[error,setError]=useState(''); const[loading,setLoading]=useState(false)
  useEffect(()=>{if(open)apiFetch('/venues').then(setVenues).catch(e=>setError(e.message))},[open])
  if(!open)return null
  const set=(k)=>(e)=>setForm(v=>({...v,[k]:e.target.type==='checkbox'?e.target.checked:e.target.value}))
  const submit=async(e)=>{e.preventDefault();setError('');setLoading(true);try{
    const payload={...form,capacity:Number(form.capacity),registration_fee:form.is_free?0:Number(form.registration_fee||0),start_time:new Date(form.start_time).toISOString(),end_time:new Date(form.end_time).toISOString(),accepts_stripe:form.is_free?false:form.accepts_stripe,accepts_qr:form.is_free?false:form.accepts_qr}
    const created=await apiFetch('/events',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload)})
    if(qr && !form.is_free){const fd=new FormData();fd.append('image',qr);await apiFetch(`/events/${created.id}/payment-qr`,{method:'POST',body:fd})}
    setForm(empty);setQr(null);onCreated?.();onClose()
  }catch(err){setError(err.message)}finally{setLoading(false)}}
  return <div className="modal-backdrop"><div className="modal-card event-modal"><button className="modal-close" onClick={onClose}>×</button><div className="modal-heading"><span className="icon-bubble">✦</span><div><h2>Create New Event</h2><p>Fill in the details and publish when you're ready.</p></div></div>
    <form onSubmit={submit} className="event-create-grid">
      <section><h3>Event details</h3><label>Event name *<input required value={form.title} onChange={set('title')} placeholder="e.g. Tech Summit 2026"/></label><label>Description<textarea rows="4" value={form.description} onChange={set('description')} placeholder="Tell people about your event..."/></label><div className="form-grid two"><label>Date & start *<input required type="datetime-local" value={form.start_time} onChange={set('start_time')}/></label><label>End *<input required type="datetime-local" value={form.end_time} onChange={set('end_time')}/></label></div><label>Venue *<select required value={form.venue_id} onChange={set('venue_id')}><option value="">Select a venue</option>{venues.map(v=><option value={v.id} key={v.id}>{v.name} · {v.capacity}</option>)}</select></label><label>Capacity *<input required type="number" min="1" value={form.capacity} onChange={set('capacity')}/></label></section>
      <section><h3>Registration & payment</h3><label className="toggle-row"><span><strong>Free of cost event</strong><small>No payment required from attendees.</small></span><input type="checkbox" checked={form.is_free} onChange={set('is_free')}/></label>{!form.is_free&&<><label>Registration fee (₹) *<input required type="number" min="1" step="0.01" value={form.registration_fee} onChange={set('registration_fee')}/></label><div className="payment-options"><label><input type="checkbox" checked={form.accepts_stripe} onChange={set('accepts_stripe')}/> Stripe online payment</label><label><input type="checkbox" checked={form.accepts_qr} onChange={set('accepts_qr')}/> QR / UPI payment</label></div>{form.accepts_qr&&<label className="upload-box">Payment QR image <input type="file" accept="image/png,image/jpeg,image/webp" onChange={e=>setQr(e.target.files?.[0]||null)}/><span>{qr?qr.name:'Upload QR code image (optional now, can add later)'}</span></label>}</>}
      <div className="live-summary"><span>Capacity <strong>{form.capacity||0}</strong></span><span>Fee <strong>{form.is_free?'Free':`₹${form.registration_fee||0}`}</strong></span></div>{error&&<div className="form-error">{error}</div>}<div className="modal-actions"><button type="button" className="secondary-button" onClick={onClose}>Cancel</button><button className="primary-button" disabled={loading}>{loading?'Creating...':'Create Event'}</button></div></section>
    </form></div></div>
}
