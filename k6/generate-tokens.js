import http from 'k6/http'
import { sleep } from 'k6'

const BASE = 'http://192.168.10.231'

export const options = {
  vus: 1,
  iterations: 1,
}

export default function () {
  const tokens = []
  for (let i = 0; i < 5000; i++) {
    const r = http.post(
      `${BASE}/api/auth/login`,
      JSON.stringify({ email: `user${i}@dropx.com`, password: 'Test1234!' }),
      { headers: { 'Content-Type': 'application/json' }, timeout: '10s' }
    )
    try {
      const b = JSON.parse(r.body)
      if (b.access_token) tokens.push(b.access_token)
    } catch (_) {}
    if (i % 100 === 0) {
      console.log(`progress: ${i}/5000`)
      console.log(`CHECKPOINT:${JSON.stringify(tokens)}`)
    }
  }
  console.log('TOKENS:' + JSON.stringify(tokens))
}