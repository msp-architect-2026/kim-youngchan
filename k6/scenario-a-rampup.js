/**
 * DropX Load Test - scenario-a-rampup.js
 * 목적: 정상 부하 기준선 측정 (100 VU)
 * 재고: 사이즈별 10~30개 (총 100개)
 * 예상 소요: ~60초
 */
import http from 'k6/http'
import { check, sleep, group } from 'k6'
import { Trend, Rate, Counter } from 'k6/metrics'

const listDuration    = new Trend('dropx_list_duration',    true)
const detailDuration  = new Trend('dropx_detail_duration',  true)
const reserveDuration = new Trend('dropx_reserve_duration', true)
const confirmDuration = new Trend('dropx_confirm_duration', true)
const reserveSuccess  = new Rate('dropx_reserve_success')
const confirmSuccess  = new Rate('dropx_confirm_success')
const soldOut         = new Counter('dropx_sold_out')
const realErrorRate   = new Rate('dropx_real_error_rate')

const BASE  = 'http://192.168.10.231'
const SIZES = [255, 260, 265, 270, 275, 280]

export const options = {
  setupTimeout: '3m',
  scenarios: {
    load_100: {
      executor: 'ramping-vus',
      startVUs: 0,
      stages: [
        { duration: '10s', target: 100 },  // ramp up
        { duration: '30s', target: 100 },  // steady
        { duration: '10s', target: 0   },  // ramp down
      ],
    },
  },
  thresholds: {
    'dropx_real_error_rate':  ['rate<0.05'],
    http_req_duration:        ['p(95)<1000'],
    'dropx_reserve_duration': ['p(95)<800' ],
    'dropx_confirm_duration': ['p(95)<800' ],
  },
}

export function setup() {
  const tokens = []
  // 유저는 사전에 생성됨 — login만 실행
  for (let i = 0; i < 100; i++) {
    const email = `rampup_${i}@gmail.com`
    const pw    = 'Test1234!'
    const r = http.post(`${BASE}/api/auth/login`,
      JSON.stringify({ email, password: pw }),
      { headers: { 'Content-Type': 'application/json' } }
    )
    try {
      const b = JSON.parse(r.body)
      if (b.access_token) tokens.push(b.access_token)
    } catch (_) {}
  }
  console.log(`✅ [rampup] tokens: ${tokens.length}`)
  return { tokens }
}

export default function (data) {
  const token   = data.tokens[__VU % data.tokens.length]
  const size    = SIZES[Math.floor(Math.random() * SIZES.length)]
  const headers = {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`,
  }

  let sneakerId = 1

  group('1_list', () => {
    const s   = Date.now()
    const res = http.get(`${BASE}/api/sneakers`, { headers })
    listDuration.add(Date.now() - s)
    check(res, { 'list 200': r => r.status === 200 })
    if (res.status !== 200) console.log(`list fail: ${res.status} ${res.body.slice(0,100)}`)
    try {
      const items = JSON.parse(res.body).items
      if (items?.length) sneakerId = items[0].id
    } catch (_) {}
  })

  sleep(0.3)

  group('2_detail', () => {
    const s   = Date.now()
    const res = http.get(`${BASE}/api/sneakers/${sneakerId}`, { headers })
    detailDuration.add(Date.now() - s)
    check(res, { 'detail 200': r => r.status === 200 })
  })

  sleep(0.2)

  let reserveToken = null
  group('3_reserve', () => {
    const s   = Date.now()
    const res = http.post(`${BASE}/api/orders/reserve`,
      JSON.stringify({ sneaker_id: sneakerId, size }),
      { headers }
    )
    reserveDuration.add(Date.now() - s)

    if (res.status === 409) { soldOut.add(1); reserveSuccess.add(false); realErrorRate.add(false); return }
    if (res.status >= 500) { realErrorRate.add(true); return }
    realErrorRate.add(false)

    const ok = check(res, {
      'reserve 200':        r => r.status === 200,
      'reserve_token 존재': r => { try { return !!JSON.parse(r.body).reserve_token } catch { return false } },
    })
    reserveSuccess.add(ok)
    if (ok) try { reserveToken = JSON.parse(res.body).reserve_token } catch (_) {}
  })

  if (!reserveToken) { sleep(0.1); return }

  sleep(0.5)

  group('4_confirm', () => {
    const s   = Date.now()
    const res = http.post(`${BASE}/api/orders/confirm`,
      JSON.stringify({ reserve_token: reserveToken }),
      { headers }
    )
    confirmDuration.add(Date.now() - s)
    const ok = check(res, {
      'confirm 200':   r => r.status === 200,
      'order_id 존재': r => { try { return !!JSON.parse(r.body).order_id } catch { return false } },
    })
    confirmSuccess.add(ok)
  })

  sleep(0.1)
}