import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { authAPI } from '../api'
import { useAuthStore } from '../store/auth'

export default function Login() {
  const navigate = useNavigate()
  const { setToken, setUser } = useAuthStore()
  const [mode, setMode] = useState('login') // login | signup
  const [form, setForm] = useState({ email: '', password: '', name: '' })
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const handleSubmit = async () => {
    setError('')
    setLoading(true)
    try {
      if (mode === 'login') {
        const res = await authAPI.login({ email: form.email, password: form.password })
        if (res.access_token) {
          setToken(res.access_token)
          const me = await authAPI.me(res.access_token)
          setUser(me)
          navigate('/')
        } else {
          setError(res.detail || '로그인에 실패했습니다.')
        }
      } else {
        const res = await authAPI.signup({ email: form.email, password: form.password, name: form.name })
        if (res.id) {
          const loginRes = await authAPI.login({ email: form.email, password: form.password })
          setToken(loginRes.access_token)
          navigate('/')
        } else {
          setError(res.detail || '회원가입에 실패했습니다.')
        }
      }
    } catch (e) {
      setError('네트워크 오류가 발생했습니다.')
    }
    setLoading(false)
  }

  return (
    <div style={{
      paddingTop: '52px', minHeight: '100vh',
      display: 'flex', alignItems: 'center', justifyContent: 'center',
    }}>
      <div style={{ width: '100%', maxWidth: '400px', padding: '0 32px', animation: 'fadeIn 0.4s ease' }}>
        <h1 style={{ fontFamily: 'var(--font-display)', fontSize: '52px', marginBottom: '8px' }}>
          {mode === 'login' ? 'SIGN IN' : 'JOIN'}
        </h1>
        <p style={{ fontFamily: 'var(--font-mono)', fontSize: '11px', color: 'var(--gray-light)', marginBottom: '48px' }}>
          {mode === 'login' ? 'Access your DROPX account' : 'Create your DROPX account'}
        </p>

        <div style={{ display: 'flex', flexDirection: 'column', gap: '12px', marginBottom: '24px' }}>
          {mode === 'signup' && (
            <input
              placeholder="Name"
              value={form.name}
              onChange={e => setForm(f => ({ ...f, name: e.target.value }))}
              style={inputStyle}
            />
          )}
          <input
            placeholder="Email"
            type="email"
            value={form.email}
            onChange={e => setForm(f => ({ ...f, email: e.target.value }))}
            style={inputStyle}
          />
          <input
            placeholder="Password"
            type="password"
            value={form.password}
            onChange={e => setForm(f => ({ ...f, password: e.target.value }))}
            onKeyDown={e => e.key === 'Enter' && handleSubmit()}
            style={inputStyle}
          />
        </div>

        {error && (
          <div style={{
            padding: '12px 16px', marginBottom: '16px',
            background: 'rgba(230,51,41,0.1)', border: '1px solid rgba(230,51,41,0.3)',
            borderRadius: '2px', fontFamily: 'var(--font-mono)', fontSize: '12px', color: 'var(--red)',
          }}>
            {error}
          </div>
        )}

        <button onClick={handleSubmit} disabled={loading} style={{
          width: '100%', padding: '16px', marginBottom: '16px',
          background: loading ? '#222' : 'var(--red)', color: 'var(--white)',
          fontFamily: 'var(--font-mono)', fontSize: '12px', letterSpacing: '0.15em', textTransform: 'uppercase',
          borderRadius: '2px', transition: 'background 0.2s',
          display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '10px',
        }}>
          {loading && <div style={{ width: '12px', height: '12px', border: '2px solid #555', borderTopColor: 'var(--white)', borderRadius: '50%', animation: 'spin 0.8s linear infinite' }} />}
          {mode === 'login' ? 'Sign In' : 'Create Account'}
        </button>

        <button onClick={() => { setMode(m => m === 'login' ? 'signup' : 'login'); setError('') }} style={{
          width: '100%', padding: '12px',
          fontFamily: 'var(--font-mono)', fontSize: '11px', color: 'var(--gray-light)',
          letterSpacing: '0.1em', textTransform: 'uppercase',
          border: '1px solid #222', borderRadius: '2px',
        }}>
          {mode === 'login' ? 'Create Account →' : '← Back to Login'}
        </button>
      </div>
    </div>
  )
}

const inputStyle = {
  width: '100%', padding: '14px 16px',
  background: '#111', border: '1px solid #2a2a2a', borderRadius: '2px',
  color: 'var(--white)', fontFamily: 'var(--font-mono)', fontSize: '13px',
  outline: 'none',
}
