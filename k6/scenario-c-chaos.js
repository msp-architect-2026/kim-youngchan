/**
 * DropX Load Test - scenario-c-chaos.js
 * 목적: 5,000 VU 최대 부하 + Pod Kill 카오스 시뮬레이션
 * 관찰: HPA 스케일 아웃, Pod 재시작 중 서비스 연속성, OOMKilled 여부
 * 예상 소요: ~80초
 *
 * Pod Kill 실행 (별도 터미널):
 *   ADMIN_TOKEN=$(curl -s -X POST http://192.168.10.231/api/auth/login \
 *     -H "Content-Type: application/json" \
 *     -d '{"email":"admin@gmail.com","password":"admin1234!"}' \
 *     | python3 -c "import sys,json; print(json.load(sys.stdin)['access_token'])")
 *   curl -s -X POST http://192.168.10.231/api/admin/kill-pod \
 *     -H "Authorization: Bearer $ADMIN_TOKEN"
 */
import http from 'k6/http'
import { check, sleep, group } from 'k6'
import { Trend, Rate, Counter } from 'k6/metrics'
import { SharedArray } from 'k6/data'

const listDuration    = new Trend('dropx_list_duration',    true)
const detailDuration  = new Trend('dropx_detail_duration',  true)
const reserveDuration = new Trend('dropx_reserve_duration', true)
const confirmDuration = new Trend('dropx_confirm_duration', true)
const reserveSuccess  = new Rate('dropx_reserve_success')
const confirmSuccess  = new Rate('dropx_confirm_success')
const soldOut         = new Counter('dropx_sold_out')

const BASE  = 'http://192.168.10.231'
const SIZES = [255, 260, 265, 270, 275, 280]

const tokens = new SharedArray('tokens', function () {
  return JSON.parse(open('./tokens-rampup.json'))
})

export const options = {
  scenarios: {
    chaos_5000: {
      executor: 'ramping-vus',
      startVUs: 0,
      stages: [
        { duration: '10s', target: 500  },
        { duration: '20s', target: 5000 },
        { duration: '30s', target: 5000 },
        { duration: '10s', target: 0    },
      ],
    },
  },
  thresholds: {
    http_req_failed:          ['rate<0.5'  ],  // Pod Kill 감안 50% 미만
    http_req_duration:        ['p(95)<8000'],  // 8초
    'dropx_reserve_duration': ['p(95)<5000'],  // 5초
    'dropx_confirm_duration': ['p(95)<5000'],
    'dropx_reserve_success':  ['rate>0.005'],  // 0.5% 이상
  },
}

export default function () {
  const token   = tokens[__VU % tokens.length]
  const size    = SIZES[Math.floor(Math.random() * SIZES.length)]
  const headers = {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`,
  }

  let sneakerId = 1

  group('1_list', () => {
    const s   = Date.now()
    const res = http.get(`${BASE}/api/sneakers`, { headers, timeout: '10s' })
    listDuration.add(Date.now() - s)
    check(res, { 'list 200': r => r.status === 200 })
    try {
      const items = JSON.parse(res.body).items
      if (items?.length) sneakerId = items[0].id
    } catch (_) {}
  })

  sleep(0.1)

  group('2_detail', () => {
    const s   = Date.now()
    const res = http.get(`${BASE}/api/sneakers/${sneakerId}`, { headers, timeout: '10s' })
    detailDuration.add(Date.now() - s)
    check(res, { 'detail 200': r => r.status === 200 })
  })

  sleep(0.05)

  let reserveToken = null
  group('3_reserve', () => {
    const s   = Date.now()
    const res = http.post(`${BASE}/api/orders/reserve`,
      JSON.stringify({ sneaker_id: sneakerId, size }),
      { headers, timeout: '10s' }
    )
    reserveDuration.add(Date.now() - s)

    if (res.status === 409) { soldOut.add(1); reserveSuccess.add(false); return }

    const ok = check(res, {
      'reserve 200':        r => r.status === 200,
      'reserve_token 존재': r => { try { return !!JSON.parse(r.body).reserve_token } catch { return false } },
    })
    reserveSuccess.add(ok)
    if (ok) try { reserveToken = JSON.parse(res.body).reserve_token } catch (_) {}
  })

  if (!reserveToken) { sleep(0.05); return }

  sleep(0.2)

  group('4_confirm', () => {
    const s   = Date.now()
    const res = http.post(`${BASE}/api/orders/confirm`,
      JSON.stringify({ reserve_token: reserveToken }),
      { headers, timeout: '10s' }
    )
    confirmDuration.add(Date.now() - s)
    const ok = check(res, {
      'confirm 200':   r => r.status === 200,
      'order_id 존재': r => { try { return !!JSON.parse(r.body).order_id } catch { return false } },
    })
    confirmSuccess.add(ok)
  })

  sleep(0.05)
}
