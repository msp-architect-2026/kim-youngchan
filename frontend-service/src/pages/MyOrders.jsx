import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { orderAPI } from '../api'
import { useAuthStore } from '../store/auth'

const STATUS_COLOR = {
  CONFIRMED: '#22c55e',
  RESERVED: 'var(--red)',
  CANCELLED: '#555',
  FAILED: '#444',
}

export default function MyOrders() {
  const { token } = useAuthStore()
  const navigate = useNavigate()
  const [orders, setOrders] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (!token) { navigate('/login'); return }
    orderAPI.myOrders(token).then(d => {
      setOrders(d.orders || [])
      setLoading(false)
    }).catch(() => setLoading(false))
  }, [token])

  return (
    <div style={{ paddingTop: '52px', minHeight: '100vh' }}>
      <div style={{ maxWidth: '900px', margin: '0 auto', padding: '60px 32px' }}>
        <h1 style={{ fontFamily: 'var(--font-display)', fontSize: '48px', marginBottom: '8px' }}>MY ORDERS</h1>
        <p style={{ fontFamily: 'var(--font-mono)', fontSize: '11px', color: 'var(--gray-light)', marginBottom: '48px' }}>
          {orders.length} orders
        </p>

        {loading ? (
          <div style={{ fontFamily: 'var(--font-mono)', fontSize: '12px', color: 'var(--gray-light)', display: 'flex', gap: '8px', alignItems: 'center' }}>
            <div style={{ width: '8px', height: '8px', background: 'var(--red)', borderRadius: '50%', animation: 'pulse 1s infinite' }} />
            Loading...
          </div>
        ) : orders.length === 0 ? (
          <div style={{ textAlign: 'center', padding: '80px 0' }}>
            <div style={{ fontFamily: 'var(--font-display)', fontSize: '32px', color: '#333', marginBottom: '12px' }}>NO ORDERS YET</div>
            <button onClick={() => navigate('/')} style={{
              fontFamily: 'var(--font-mono)', fontSize: '11px', letterSpacing: '0.1em',
              padding: '10px 24px', background: 'var(--white)', color: 'var(--black)', borderRadius: '2px',
              textTransform: 'uppercase', marginTop: '16px',
            }}>Browse Drops →</button>
          </div>
        ) : (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '1px', background: '#1a1a1a' }}>
            {orders.map(order => (
              <div key={order.id} style={{
                background: 'var(--black)', padding: '24px 28px',
                display: 'grid', gridTemplateColumns: '1fr auto', gap: '16px', alignItems: 'center',
              }}>
                <div>
                  <div style={{ display: 'flex', gap: '16px', alignItems: 'center', marginBottom: '8px' }}>
                    <span style={{ fontFamily: 'var(--font-mono)', fontSize: '10px', color: 'var(--gray-mid)' }}>
                      #{String(order.id).padStart(6, '0')}
                    </span>
                    <span style={{
                      fontFamily: 'var(--font-mono)', fontSize: '10px', letterSpacing: '0.1em',
                      padding: '2px 8px', borderRadius: '2px', textTransform: 'uppercase',
                      background: `${STATUS_COLOR[order.status]}20`,
                      color: STATUS_COLOR[order.status],
                      border: `1px solid ${STATUS_COLOR[order.status]}40`,
                    }}>
                      {order.status}
                    </span>
                  </div>
                  <div style={{ fontFamily: 'var(--font-mono)', fontSize: '13px', color: 'var(--white)', marginBottom: '4px' }}>
                    Sneaker #{order.sneaker_id} · Size {order.size}
                  </div>
                  <div style={{ fontFamily: 'var(--font-mono)', fontSize: '10px', color: 'var(--gray-mid)' }}>
                    {new Date(order.created_at).toLocaleString('ko-KR')}
                  </div>
                </div>
                <div style={{ fontFamily: 'var(--font-mono)', fontSize: '10px', color: 'var(--gray-mid)', textAlign: 'right', maxWidth: '200px', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                  {order.reserve_token?.slice(0, 16)}...
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}
