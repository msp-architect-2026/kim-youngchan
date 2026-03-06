import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { productAPI } from '../api'

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

  return (
    <Link to={`/drop/${sneaker.id}`} style={{
      display: 'block', background: 'var(--black)', padding: '32px',
      transition: 'background 0.2s',
    }}
      onMouseEnter={e => e.currentTarget.style.background = '#111'}
      onMouseLeave={e => e.currentTarget.style.background = 'var(--black)'}
    >
      {/* Badge */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '32px' }}>
        <span style={{
          fontFamily: 'var(--font-mono)', fontSize: '10px', letterSpacing: '0.15em',
          padding: '4px 10px', borderRadius: '2px', textTransform: 'uppercase',
          background: isSoldOut ? '#222' : isLow ? 'rgba(230,51,41,0.15)' : 'rgba(255,255,255,0.06)',
          color: isSoldOut ? 'var(--gray-mid)' : isLow ? 'var(--red)' : 'var(--gray-light)',
          border: `1px solid ${isSoldOut ? '#333' : isLow ? 'rgba(230,51,41,0.3)' : '#2a2a2a'}`,
        }}>
          {isSoldOut ? 'Sold Out' : isLow ? `⚡ Only ${totalStock} left` : '● Live'}
        </span>
        <span style={{ fontFamily: 'var(--font-mono)', fontSize: '10px', color: 'var(--gray-mid)' }}>
          #{String(sneaker.id).padStart(4, '0')}
        </span>
      </div>

      {/* Sneaker visual placeholder */}
      <div style={{
        height: '140px', background: '#111', borderRadius: '4px', marginBottom: '24px',
        display: 'flex', alignItems: 'center', justifyContent: 'center',
        border: '1px solid #1a1a1a',
      }}>
        <span style={{ fontSize: '48px' }}>👟</span>
      </div>

      <div style={{ fontFamily: 'var(--font-mono)', fontSize: '10px', color: 'var(--gray-light)', letterSpacing: '0.1em', textTransform: 'uppercase', marginBottom: '6px' }}>
        {sneaker.brand}
      </div>
      <div style={{ fontFamily: 'var(--font-display)', fontSize: '22px', letterSpacing: '0.02em', marginBottom: '16px' }}>
        {sneaker.name}
      </div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <span style={{ fontFamily: 'var(--font-mono)', fontSize: '16px', color: 'var(--white)' }}>
          ₩{sneaker.price?.toLocaleString()}
        </span>
        <span style={{
          fontFamily: 'var(--font-mono)', fontSize: '11px', color: 'var(--red)',
          display: 'flex', alignItems: 'center', gap: '6px',
        }}>
          Reserve →
        </span>
      </div>
    </Link>
  )
}
