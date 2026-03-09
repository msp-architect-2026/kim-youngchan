import { useEffect, useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { productAPI, orderAPI } from '../api'
import { useAuthStore } from '../store/auth'

const SIZES = [255, 260, 265, 270, 275, 280]

export default function DropDetail() {
  const { id } = useParams()
  const navigate = useNavigate()
  const { token } = useAuthStore()

  const [sneaker, setSneaker] = useState(null)
  const [stock, setStock] = useState({})   // { 255: 10, 260: 20, ... }
  const [selectedSize, setSelectedSize] = useState(null)
  const [phase, setPhase] = useState('idle')
  const [reserveToken, setReserveToken] = useState(null)
  const [orderId, setOrderId] = useState(null)
  const [error, setError] = useState('')
  const [countdown, setCountdown] = useState(180)

  useEffect(() => {
    productAPI.detail(id).then(setSneaker).catch(() => {})

    const fetchStock = () =>
      productAPI.liveStock(id)
        .then(d => {
          // d = { sneaker_id, total_stock, sizes: [{size, stock}, ...], source }
          const map = {}
          d.sizes?.forEach(s => { map[s.size] = s.stock })
          setStock(map)
        })
        .catch(() => {})

    fetchStock()
    const interval = setInterval(fetchStock, 3000)
    return () => clearInterval(interval)
  }, [id])

  useEffect(() => {
    if (phase !== 'reserved') return
    setCountdown(180)
    const t = setInterval(() => {
      setCountdown(c => {
        if (c <= 1) { clearInterval(t); setPhase('idle'); setReserveToken(null); return 0 }
        return c - 1
      })
    }, 1000)
    return () => clearInterval(t)
  }, [phase])

  const handleReserve = async () => {
    if (!token) { navigate('/login'); return }
    if (!selectedSize) { setError('사이즈를 선택해주세요.'); return }
    setError('')
    setPhase('reserving')
    const res = await orderAPI.reserve(token, { sneaker_id: parseInt(id), size: selectedSize })
    if (res.success) {
      setReserveToken(res.reserve_token)
      setPhase('reserved')
    } else {
      setError(res.detail || '선점에 실패했습니다.')
      setPhase('idle')
    }
  }

  const handleConfirm = async () => {
    setPhase('confirming')
    const res = await orderAPI.confirm(token, { reserve_token: reserveToken })
    if (res.success) {
      setOrderId(res.order_id)
      setPhase('done')
    } else {
      setError(res.detail || '주문 확정에 실패했습니다.')
      setPhase('idle')
    }
  }

  if (!sneaker) return (
    <div style={{ paddingTop: '52px', minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
      <div style={{ fontFamily: 'var(--font-mono)', fontSize: '12px', color: 'var(--gray-light)', display: 'flex', gap: '8px', alignItems: 'center' }}>
        <div style={{ width: '8px', height: '8px', background: 'var(--red)', borderRadius: '50%', animation: 'pulse 1s infinite' }} />
        Loading...
      </div>
    </div>
  )

  if (phase === 'done') return (
    <div style={{ paddingTop: '52px', minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
      <div style={{ textAlign: 'center', animation: 'fadeIn 0.5s ease' }}>
        <div style={{ fontSize: '64px', marginBottom: '24px' }}>✓</div>
        <h1 style={{ fontFamily: 'var(--font-display)', fontSize: '48px', marginBottom: '12px' }}>ORDER CONFIRMED</h1>
        <p style={{ fontFamily: 'var(--font-mono)', fontSize: '12px', color: 'var(--gray-light)', marginBottom: '8px' }}>
          Order ID: <span style={{ color: 'var(--white)' }}>#{orderId}</span>
        </p>
        <p style={{ fontFamily: 'var(--font-mono)', fontSize: '12px', color: 'var(--gray-light)', marginBottom: '32px' }}>
          {sneaker.name} · Size {selectedSize}
        </p>
        <button onClick={() => navigate('/orders')} style={{
          fontFamily: 'var(--font-mono)', fontSize: '11px', letterSpacing: '0.1em',
          padding: '12px 32px', background: 'var(--white)', color: 'var(--black)',
          borderRadius: '2px', textTransform: 'uppercase',
        }}>View Orders →</button>
      </div>
    </div>
  )

  return (
    <div style={{ paddingTop: '52px', minHeight: '100vh' }}>
      <div style={{ maxWidth: '1200px', margin: '0 auto', padding: '60px 32px', display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '80px', alignItems: 'start' }}>

        {/* Left */}
        <div className="fade-in">
          <div style={{ fontFamily: 'var(--font-mono)', fontSize: '10px', color: 'var(--gray-light)', letterSpacing: '0.15em', textTransform: 'uppercase', marginBottom: '12px' }}>
            {sneaker.brand}
          </div>
          <h1 style={{ fontFamily: 'var(--font-display)', fontSize: 'clamp(32px, 5vw, 56px)', lineHeight: 0.95, marginBottom: '24px' }}>
            {sneaker.name}
          </h1>
          <div style={{
            height: '300px', background: '#111', borderRadius: '4px', border: '1px solid #1a1a1a',
            display: 'flex', alignItems: 'center', justifyContent: 'center', marginBottom: '32px',
          }}>
            <span style={{ fontSize: '96px' }}>👟</span>
          </div>
          <div style={{ fontFamily: 'var(--font-display)', fontSize: '36px', color: 'var(--white)' }}>
            ₩{sneaker.price?.toLocaleString()}
          </div>
        </div>

        {/* Right */}
        <div className="fade-in" style={{ position: 'sticky', top: '72px' }}>

          {/* 실시간 재고 */}
          <div style={{
            padding: '16px 20px', background: '#111', border: '1px solid #1a1a1a',
            borderRadius: '4px', marginBottom: '32px',
            display: 'flex', justifyContent: 'space-between', alignItems: 'center',
          }}>
            <span style={{ fontFamily: 'var(--font-mono)', fontSize: '11px', color: 'var(--gray-light)', display: 'flex', gap: '8px', alignItems: 'center' }}>
              <span style={{ display: 'inline-block', width: '6px', height: '6px', background: 'var(--red)', borderRadius: '50%', animation: 'pulse 1.5s infinite' }} />
              LIVE STOCK
            </span>
            <span style={{ fontFamily: 'var(--font-mono)', fontSize: '11px', color: 'var(--white)' }}>
              {Object.values(stock).reduce((a, b) => a + b, 0)} units remaining
            </span>
          </div>

          {/* 사이즈 선택 */}
          <div style={{ marginBottom: '32px' }}>
            <div style={{ fontFamily: 'var(--font-mono)', fontSize: '11px', color: 'var(--gray-light)', letterSpacing: '0.1em', textTransform: 'uppercase', marginBottom: '16px' }}>
              Select Size (mm)
            </div>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '8px' }}>
              {SIZES.map(size => {
                const sizeStock = stock[size] ?? 0
                const isSelected = selectedSize === size
                const isOut = sizeStock === 0
                return (
                  <button
                    key={size}
                    disabled={isOut || phase !== 'idle'}
                    onClick={() => setSelectedSize(size)}
                    style={{
                      padding: '14px', borderRadius: '2px', fontFamily: 'var(--font-mono)', fontSize: '13px',
                      border: isSelected ? '1px solid var(--white)' : '1px solid #2a2a2a',
                      background: isSelected ? 'var(--white)' : isOut ? '#0d0d0d' : '#111',
                      color: isSelected ? 'var(--black)' : isOut ? '#333' : 'var(--white)',
                      cursor: isOut ? 'not-allowed' : 'pointer',
                      transition: 'all 0.15s',
                      position: 'relative',
                    }}
                  >
                    {size}
                    {!isOut && (
                      <span style={{ position: 'absolute', bottom: '3px', right: '5px', fontSize: '8px', color: 'var(--gray-mid)', fontFamily: 'var(--font-mono)' }}>
                        {sizeStock}
                      </span>
                    )}
                    {isOut && (
                      <span style={{ position: 'absolute', inset: 0, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>✕</span>
                    )}
                  </button>
                )
              })}
            </div>
          </div>

          {error && (
            <div style={{
              padding: '12px 16px', background: 'rgba(230,51,41,0.1)', border: '1px solid rgba(230,51,41,0.3)',
              borderRadius: '2px', fontFamily: 'var(--font-mono)', fontSize: '12px', color: 'var(--red)',
              marginBottom: '16px',
            }}>
              {error}
            </div>
          )}

          {phase === 'reserved' && (
            <div style={{
              padding: '20px', background: 'rgba(230,51,41,0.06)', border: '1px solid rgba(230,51,41,0.2)',
              borderRadius: '4px', marginBottom: '16px',
            }}>
              <div style={{ fontFamily: 'var(--font-mono)', fontSize: '11px', color: 'var(--gray-light)', marginBottom: '8px' }}>
                선점 완료 · 확정까지 남은 시간
              </div>
              <div style={{ fontFamily: 'var(--font-display)', fontSize: '36px', color: countdown < 30 ? 'var(--red)' : 'var(--white)' }}>
                {String(Math.floor(countdown / 60)).padStart(2, '0')}:{String(countdown % 60).padStart(2, '0')}
              </div>
            </div>
          )}

          {phase === 'idle' && (
            <button onClick={handleReserve} style={{
              width: '100%', padding: '18px', background: 'var(--red)', color: 'var(--white)',
              fontFamily: 'var(--font-mono)', fontSize: '12px', letterSpacing: '0.15em', textTransform: 'uppercase',
              borderRadius: '2px', transition: 'background 0.2s',
            }}
              onMouseEnter={e => e.currentTarget.style.background = '#c0392b'}
              onMouseLeave={e => e.currentTarget.style.background = 'var(--red)'}
            >
              Reserve Now →
            </button>
          )}

          {phase === 'reserving' && (
            <button disabled style={{
              width: '100%', padding: '18px', background: '#222', color: 'var(--gray-mid)',
              fontFamily: 'var(--font-mono)', fontSize: '12px', letterSpacing: '0.15em', textTransform: 'uppercase',
              borderRadius: '2px', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '10px',
            }}>
              <div style={{ width: '12px', height: '12px', border: '2px solid #444', borderTopColor: 'var(--white)', borderRadius: '50%', animation: 'spin 0.8s linear infinite' }} />
              Reserving...
            </button>
          )}

          {phase === 'reserved' && (
            <button onClick={handleConfirm} style={{
              width: '100%', padding: '18px', background: 'var(--white)', color: 'var(--black)',
              fontFamily: 'var(--font-mono)', fontSize: '12px', letterSpacing: '0.15em', textTransform: 'uppercase',
              borderRadius: '2px',
            }}>
              Confirm Order →
            </button>
          )}

          {phase === 'confirming' && (
            <button disabled style={{
              width: '100%', padding: '18px', background: '#222', color: 'var(--gray-mid)',
              fontFamily: 'var(--font-mono)', fontSize: '12px', letterSpacing: '0.15em', textTransform: 'uppercase',
              borderRadius: '2px', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '10px',
            }}>
              <div style={{ width: '12px', height: '12px', border: '2px solid #444', borderTopColor: 'var(--white)', borderRadius: '50%', animation: 'spin 0.8s linear infinite' }} />
              Confirming...
            </button>
          )}
        </div>
      </div>
    </div>
  )
}
