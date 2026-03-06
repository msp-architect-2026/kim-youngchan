import { Link, useNavigate } from 'react-router-dom'
import { useAuthStore } from '../store/auth'

export default function Navbar() {
  const { token, user, logout } = useAuthStore()
  const navigate = useNavigate()

  const handleLogout = () => {
    logout()
    navigate('/')
  }

  return (
    <nav style={{
      position: 'fixed', top: 0, left: 0, right: 0, zIndex: 100,
      display: 'flex', alignItems: 'center', justifyContent: 'space-between',
      padding: '0 32px', height: '52px',
      background: 'rgba(10,10,10,0.95)',
      backdropFilter: 'blur(10px)',
      borderBottom: '1px solid #1a1a1a',
    }}>
      <Link to="/" style={{ fontFamily: 'var(--font-display)', fontSize: '24px', letterSpacing: '0.05em', color: 'var(--white)' }}>
        DROP<span style={{ color: 'var(--red)' }}>X</span>
      </Link>

      <div style={{ display: 'flex', gap: '24px', alignItems: 'center' }}>
        <Link to="/" style={{ fontFamily: 'var(--font-mono)', fontSize: '11px', letterSpacing: '0.1em', color: 'var(--gray-light)', textTransform: 'uppercase' }}>Drops</Link>
        {token && (
          <>
            <Link to="/orders" style={{ fontFamily: 'var(--font-mono)', fontSize: '11px', letterSpacing: '0.1em', color: 'var(--gray-light)', textTransform: 'uppercase' }}>My Orders</Link>
            {user?.role === 'ADMIN' && (
              <Link to="/admin" style={{ fontFamily: 'var(--font-mono)', fontSize: '11px', letterSpacing: '0.1em', color: 'var(--red)', textTransform: 'uppercase' }}>Admin</Link>
            )}
          </>
        )}
        {token ? (
          <button onClick={handleLogout} style={{
            fontFamily: 'var(--font-mono)', fontSize: '11px', letterSpacing: '0.1em',
            color: 'var(--gray-light)', textTransform: 'uppercase',
            padding: '6px 14px', border: '1px solid #333', borderRadius: '2px',
          }}>Logout</button>
        ) : (
          <Link to="/login" style={{
            fontFamily: 'var(--font-mono)', fontSize: '11px', letterSpacing: '0.1em',
            color: 'var(--black)', background: 'var(--white)',
            padding: '6px 14px', borderRadius: '2px', textTransform: 'uppercase',
          }}>Login</Link>
        )}
      </div>
    </nav>
  )
}
