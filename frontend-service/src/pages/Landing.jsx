import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { productAPI } from '../api'

// drop_at까지 남은 시간 계산
function useCountdown(dropAt) {
  const [diff, setDiff] = useState(null)

  useEffect(() => {
    if (!dropAt) return
    const calc = () => {
      const now = new Date()
      const target = new Date(dropAt)
      const ms = target - now
      if (ms <= 0) { setDiff(0); return }
      setDiff(ms)
    }
    calc()
    const t = setInterval(calc, 1000)
    return () => clearInterval(t)
  }, [dropAt])

  if (diff === null) return null
  if (diff <= 0) return { hours: 0, minutes: 0, seconds: 0, started: true }

  const totalSec = Math.floor(diff / 1000)
  return {
    hours: Math.floor(totalSec / 3600),
    minutes: Math.floor((totalSec % 3600) / 60),
    seconds: totalSec % 60,
    started: false,
  }
}

export default function Landing() {
  const [sneakers, setSneakers] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    productAPI.list().then(d => {
      setSneakers(d.items || [])
      setLoading(false)
    }).catch(() => setLoading(false))
  }, [])

  return (
    <div style={{ minHeight: '100vh', paddingTop: '52px' }}>
      {/* Hero */}
      <div style={{
        padding: '80px 32px 60px',
        borderBottom: '1px solid #1a1a1a',
        position: 'relative', overflow: 'hidden',
      }}>
        <div style={{
          position: 'absolute', top: 0, left: 0, right: 0, bottom: 0,
          background: 'radial-gradient(ellipse 60% 50% at 50% 0%, rgba(230,51,41,0.08) 0%, transparent 70%)',
          pointerEvents: 'none',
        }} />
        <div style={{ maxWidth: '1200px', margin: '0 auto' }}>
          <div style={{ fontFamily: 'var(--font-mono)', fontSize: '11px', color: 'var(--red)', letterSpacing: '0.2em', marginBottom: '16px', textTransform: 'uppercase' }}>
            ● Live Drop
          </div>
          <h1 style={{
            fontFamily: 'var(--font-display)', fontSize: 'clamp(72px, 12vw, 140px)',
            lineHeight: 0.9, letterSpacing: '-0.02em', color: 'var(--white)',
            marginBottom: '24px',
          }}>
            SECURE<br />YOUR PAIR
          </h1>
          <p style={{ fontFamily: 'var(--font-mono)', fontSize: '12px', color: 'var(--gray-light)', maxWidth: '400px', lineHeight: 1.8 }}>
            한정판 스니커즈 드롭. 선착순 선점 시스템.<br />
            재고 소진 즉시 종료됩니다.
          </p>
        </div>
      </div>

      {/* Ticker */}
      <div style={{ overflow: 'hidden', borderBottom: '1px solid #1a1a1a', padding: '10px 0', background: '#111' }}>
        <div style={{ display: 'flex', animation: 'ticker 20s linear infinite', whiteSpace: 'nowrap' }}>
          {[...Array(6)].map((_, i) => (
            <span key={i} style={{ fontFamily: 'var(--font-mono)', fontSize: '11px', color: 'var(--gray-mid)', letterSpacing: '0.15em', marginRight: '48px' }}>
              DROP NOW &nbsp;·&nbsp; LIMITED STOCK &nbsp;·&nbsp; ATOMIC RESERVE &nbsp;·&nbsp; DROPX SYSTEM &nbsp;·&nbsp;
            </span>
          ))}
        </div>
      </div>

      {/* Products */}
      <div style={{ maxWidth: '1200px', margin: '0 auto', padding: '60px 32px' }}>
        <div style={{ display: 'flex', alignItems: 'baseline', justifyContent: 'space-between', marginBottom: '32px' }}>
          <h2 style={{ fontFamily: 'var(--font-display)', fontSize: '32px', letterSpacing: '0.05em' }}>CURRENT DROPS</h2>
          <span style={{ fontFamily: 'var(--font-mono)', fontSize: '11px', color: 'var(--gray-light)' }}>
            {sneakers.length} items
          </span>
        </div>

        {loading ? (
          <div style={{ display: 'flex', gap: '8px', alignItems: 'center', color: 'var(--gray-light)', fontFamily: 'var(--font-mono)', fontSize: '12px' }}>
            <div style={{ width: '8px', height: '8px', background: 'var(--red)', borderRadius: '50%', animation: 'pulse 1s infinite' }} />
            Loading drops...
          </div>
        ) : (
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(320px, 1fr))', gap: '1px', background: '#1a1a1a' }}>
            {sneakers.map(s => (
              <SneakerCard key={s.id} sneaker={s} />
            ))}
          </div>
        )}
      </div>
    </div>
  )
}

function SneakerCard({ sneaker }) {
  const [stock, setStock] = useState(null)
  const countdown = useCountdown(sneaker.drop_at)

  useEffect(() => {
    productAPI.liveStock(sneaker.id).then(d => setStock(d)).catch(() => {})
    const interval = setInterval(() => {
      productAPI.liveStock(sneaker.id).then(d => setStock(d)).catch(() => {})
    }, 5000)
    return () => clearInterval(interval)
  }, [sneaker.id])

  const totalStock = stock ? Object.values(stock).reduce((a, b) => a + b, 0) : null
  const isLow = totalStock !== null && totalStock < 20
  const isSoldOut = totalStock === 0
  const dropStarted = countdown?.started ?? true

  const pad = n => String(n).padStart(2, '0')

  return (
    <Link to={`/drop/${sneaker.id}`} style={{
      display: 'block', background: 'var(--black)', padding: '32px',
      transition: 'background 0.2s', textDecoration: 'none',
    }}
      onMouseEnter={e => e.currentTarget.style.background = '#0d0d0d'}
      onMouseLeave={e => e.currentTarget.style.background = 'var(--black)'}
    >
      {/* 상품 이미지 영역 */}
      <div style={{
        height: '200px', background: '#111', borderRadius: '4px',
        border: '1px solid #1a1a1a', display: 'flex', alignItems: 'center',
        justifyContent: 'center', marginBottom: '24px', position: 'relative',
      }}>
        <span style={{ fontSize: '64px' }}>👟</span>

        {/* 드롭 상태 뱃지 */}
        {!dropStarted ? (
          <div style={{
            position: 'absolute', top: '12px', left: '12px',
            background: 'rgba(0,0,0,0.85)', border: '1px solid #2a2a2a',
            borderRadius: '2px', padding: '6px 10px',
            fontFamily: 'var(--font-mono)', fontSize: '10px', color: 'var(--gray-light)',
          }}>
            DROP IN &nbsp;
            <span style={{ color: 'var(--white)', letterSpacing: '0.05em' }}>
              {pad(countdown.hours)}:{pad(countdown.minutes)}:{pad(countdown.seconds)}
            </span>
          </div>
        ) : (
          <div style={{
            position: 'absolute', top: '12px', left: '12px',
            background: 'rgba(230,51,41,0.15)', border: '1px solid rgba(230,51,41,0.4)',
            borderRadius: '2px', padding: '6px 10px',
            fontFamily: 'var(--font-mono)', fontSize: '10px', color: 'var(--red)',
            display: 'flex', alignItems: 'center', gap: '6px',
          }}>
            <span style={{ width: '6px', height: '6px', background: 'var(--red)', borderRadius: '50%', animation: 'pulse 1.5s infinite', display: 'inline-block' }} />
            LIVE NOW
          </div>
        )}

        {/* 품절 오버레이 */}
        {isSoldOut && (
          <div style={{
            position: 'absolute', inset: 0, background: 'rgba(0,0,0,0.7)',
            display: 'flex', alignItems: 'center', justifyContent: 'center',
            borderRadius: '4px',
          }}>
            <span style={{ fontFamily: 'var(--font-display)', fontSize: '28px', color: '#555', letterSpacing: '0.1em' }}>SOLD OUT</span>
          </div>
        )}
      </div>

      {/* 브랜드 */}
      <div style={{ fontFamily: 'var(--font-mono)', fontSize: '10px', color: 'var(--gray-mid)', letterSpacing: '0.15em', textTransform: 'uppercase', marginBottom: '6px' }}>
        {sneaker.brand}
      </div>

      {/* 상품명 */}
      <div style={{ fontFamily: 'var(--font-display)', fontSize: '22px', color: 'var(--white)', marginBottom: '16px', lineHeight: 1.1 }}>
        {sneaker.name}
      </div>

      {/* 하단: 가격 + 재고 */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div style={{ fontFamily: 'var(--font-display)', fontSize: '24px', color: 'var(--white)' }}>
          ₩{sneaker.price?.toLocaleString()}
        </div>
        <div style={{
          fontFamily: 'var(--font-mono)', fontSize: '10px', letterSpacing: '0.1em',
          padding: '4px 10px', borderRadius: '2px',
          background: isSoldOut ? '#111' : isLow ? 'rgba(230,51,41,0.1)' : 'rgba(34,197,94,0.08)',
          color: isSoldOut ? '#333' : isLow ? 'var(--red)' : '#22c55e',
          border: `1px solid ${isSoldOut ? '#222' : isLow ? 'rgba(230,51,41,0.3)' : 'rgba(34,197,94,0.2)'}`,
        }}>
          {totalStock === null ? '...' : isSoldOut ? 'SOLD OUT' : `${totalStock} LEFT`}
        </div>
      </div>

      {/* 드롭 시간 */}
      <div style={{ marginTop: '12px', fontFamily: 'var(--font-mono)', fontSize: '10px', color: 'var(--gray-mid)' }}>
        DROP {new Date(sneaker.drop_at).toLocaleString('ko-KR')}
      </div>
    </Link>
  )
}