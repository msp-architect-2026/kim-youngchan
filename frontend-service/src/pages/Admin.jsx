import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { adminAPI } from '../api'
import { useAuthStore } from '../store/auth'

export default function Admin() {
  const { token, user } = useAuthStore()
  const navigate = useNavigate()
  const [metrics, setMetrics] = useState(null)
  const [orders, setOrders] = useState([])
  const [killing, setKilling] = useState(false)
  const [killResult, setKillResult] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (!token) { navigate('/login'); return }
    if (user && user.role !== 'ADMIN') { navigate('/'); return }
    fetchData()
    const interval = setInterval(fetchData, 5000)
    return () => clearInterval(interval)
  }, [token, user])

  const fetchData = async () => {
    try {
      const [m, o] = await Promise.all([
        adminAPI.metrics(token),
        adminAPI.orders(token),
      ])
      setMetrics(m)
      setOrders(Array.isArray(o) ? o : [])
      setLoading(false)
    } catch (e) {
      setLoading(false)
    }
  }

  const handleKillPod = async () => {
    if (!confirm('Pod를 강제 종료합니까? K8s가 자동 복구합니다.')) return
    setKilling(true)
    setKillResult(null)
    try {
      const res = await adminAPI.killPod(token)
      setKillResult({ success: true, message: res.message, pod: res.pod_name })
    } catch (e) {
      setKillResult({ success: false, message: 'Kill failed' })
    }
    setKilling(false)
    setTimeout(() => setKillResult(null), 5000)
  }

  if (loading) return (
    <div style={{ paddingTop: '52px', minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
      <div style={{ fontFamily: 'var(--font-mono)', fontSize: '12px', color: 'var(--gray-light)', display: 'flex', gap: '8px', alignItems: 'center' }}>
        <div style={{ width: '8px', height: '8px', background: 'var(--red)', borderRadius: '50%', animation: 'pulse 1s infinite' }} />
        Loading admin data...
      </div>
    </div>
  )

  const successRate = metrics?.success_rate ?? 0

  return (
    <div style={{ paddingTop: '52px', minHeight: '100vh' }}>
      <div style={{ maxWidth: '1400px', margin: '0 auto', padding: '48px 32px' }}>

        {/* Header */}
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-end', marginBottom: '48px' }}>
          <div>
            <div style={{ fontFamily: 'var(--font-mono)', fontSize: '10px', color: 'var(--red)', letterSpacing: '0.2em', marginBottom: '8px', textTransform: 'uppercase' }}>
              ● Admin Console
            </div>
            <h1 style={{ fontFamily: 'var(--font-display)', fontSize: '48px' }}>SYSTEM METRICS</h1>
          </div>
          <div style={{ fontFamily: 'var(--font-mono)', fontSize: '10px', color: 'var(--gray-mid)' }}>
            Auto-refresh 5s
          </div>
        </div>

        {/* Metrics Grid */}
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(5, 1fr)', gap: '1px', background: '#1a1a1a', marginBottom: '1px' }}>
          {[
            { label: 'Total Orders', value: metrics?.total_orders ?? 0, unit: '' },
            { label: 'Confirmed', value: metrics?.confirmed_orders ?? 0, unit: '', color: '#22c55e' },
            { label: 'Reserved', value: metrics?.reserved_orders ?? 0, unit: '', color: 'var(--red)' },
            { label: 'Cancelled', value: metrics?.cancelled_orders ?? 0, unit: '', color: '#555' },
            { label: 'Success Rate', value: successRate.toFixed(1), unit: '%', color: successRate > 80 ? '#22c55e' : successRate > 50 ? '#f59e0b' : 'var(--red)' },
          ].map(({ label, value, unit, color }) => (
            <div key={label} style={{ background: 'var(--black)', padding: '28px 24px' }}>
              <div style={{ fontFamily: 'var(--font-mono)', fontSize: '10px', color: 'var(--gray-mid)', letterSpacing: '0.1em', textTransform: 'uppercase', marginBottom: '12px' }}>
                {label}
              </div>
              <div style={{ fontFamily: 'var(--font-display)', fontSize: '40px', color: color || 'var(--white)', lineHeight: 1 }}>
                {value}{unit}
              </div>
            </div>
          ))}
        </div>

        {/* Kill Pod Panel */}
        <div style={{ background: '#0d0d0d', border: '1px solid #1a1a1a', borderTop: 'none', padding: '28px 24px', marginBottom: '48px' }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
            <div>
              <div style={{ fontFamily: 'var(--font-mono)', fontSize: '11px', color: 'var(--red)', letterSpacing: '0.1em', textTransform: 'uppercase', marginBottom: '4px' }}>
                Chaos Engineering
              </div>
              <div style={{ fontFamily: 'var(--font-mono)', fontSize: '12px', color: 'var(--gray-light)' }}>
                Pod 강제 종료 → K8s 자동 복구 테스트
              </div>
            </div>
            <div style={{ display: 'flex', gap: '16px', alignItems: 'center' }}>
              {killResult && (
                <div style={{
                  fontFamily: 'var(--font-mono)', fontSize: '11px',
                  color: killResult.success ? '#22c55e' : 'var(--red)',
                  padding: '8px 16px', background: killResult.success ? 'rgba(34,197,94,0.1)' : 'rgba(230,51,41,0.1)',
                  border: `1px solid ${killResult.success ? 'rgba(34,197,94,0.3)' : 'rgba(230,51,41,0.3)'}`,
                  borderRadius: '2px', maxWidth: '300px',
                }}>
                  {killResult.message}
                </div>
              )}
              <button onClick={handleKillPod} disabled={killing} style={{
                padding: '12px 24px', background: killing ? '#1a1a1a' : 'rgba(230,51,41,0.15)',
                border: '1px solid rgba(230,51,41,0.4)', color: killing ? 'var(--gray-mid)' : 'var(--red)',
                fontFamily: 'var(--font-mono)', fontSize: '11px', letterSpacing: '0.1em',
                textTransform: 'uppercase', borderRadius: '2px', transition: 'all 0.2s',
                display: 'flex', gap: '8px', alignItems: 'center',
              }}>
                {killing && <div style={{ width: '10px', height: '10px', border: '2px solid #444', borderTopColor: 'var(--red)', borderRadius: '50%', animation: 'spin 0.8s linear infinite' }} />}
                Kill Pod
              </button>
            </div>
          </div>
        </div>

        {/* Orders Table */}
        <div>
          <h2 style={{ fontFamily: 'var(--font-display)', fontSize: '28px', marginBottom: '24px' }}>ALL ORDERS</h2>
          <div style={{ background: '#111', border: '1px solid #1a1a1a', borderRadius: '2px', overflow: 'hidden' }}>
            <div style={{
              display: 'grid', gridTemplateColumns: '80px 80px 80px 60px 120px 1fr',
              padding: '12px 20px', borderBottom: '1px solid #1a1a1a',
              fontFamily: 'var(--font-mono)', fontSize: '10px', color: 'var(--gray-mid)', letterSpacing: '0.1em', textTransform: 'uppercase',
            }}>
              <span>Order ID</span><span>User</span><span>Sneaker</span><span>Size</span><span>Status</span><span>Created</span>
            </div>
            {orders.slice(0, 20).map(o => (
              <div key={o.order_id} style={{
                display: 'grid', gridTemplateColumns: '80px 80px 80px 60px 120px 1fr',
                padding: '14px 20px', borderBottom: '1px solid #161616',
                fontFamily: 'var(--font-mono)', fontSize: '12px', color: 'var(--gray-light)',
              }}>
                <span style={{ color: 'var(--white)' }}>#{o.order_id}</span>
                <span>#{o.user_id}</span>
                <span>#{o.sneaker_id}</span>
                <span>{o.size}</span>
                <span style={{
                  color: o.status === 'CONFIRMED' ? '#22c55e' : o.status === 'RESERVED' ? 'var(--red)' : '#555',
                  fontSize: '10px', letterSpacing: '0.1em',
                }}>
                  {o.status}
                </span>
                <span style={{ fontSize: '10px', color: 'var(--gray-mid)' }}>
                  {new Date(o.created_at).toLocaleString('ko-KR')}
                </span>
              </div>
            ))}
            {orders.length === 0 && (
              <div style={{ padding: '32px', textAlign: 'center', fontFamily: 'var(--font-mono)', fontSize: '12px', color: 'var(--gray-mid)' }}>
                No orders yet
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}
