import { useNavigate } from 'react-router-dom'
export default function BackButton() {
  const navigate = useNavigate()
  return <button className="back-button" onClick={() => navigate(-1)} aria-label="Go back">← <span>Back</span></button>
}
