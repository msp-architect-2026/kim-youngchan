/**
 * DropX Load Test - scenario-b-stock-drain.js
 * 목적: 1,000 VU로 재고 소진 시뮬레이션 (실제 드롭 상황)
 * 관찰: DB 커넥션 풀 한계, Redis 원자성 보장, 초과 선점 방지
 * 예상 소요: ~75초
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

const BASE_PRODUCT = 'http://192.168.10.99:30801'
const BASE_ORDER   = 'http://192.168.10.99:30800'
const SIZES = [255, 260, 265, 270, 275, 280]

const tokens = new SharedArray('tokens', function () {
  return JSON.parse(open('./tokens-rampup.json'))
})

export const options = {
  scenarios: {
    stock_drain: {
      executor: 'ramping-vus',
      startVUs: 0,
      stages: [
        { duration: '15s', target: 1000 },
        { duration: '30s', target: 1000 },
        { duration: '10s', target: 0    },
      ],
    },
  },
  thresholds: {
    http_req_failed:          ['rate<0.1'  ],
    http_req_duration:        ['p(95)<2000'],
    'dropx_reserve_duration': ['p(95)<1500'],
    'dropx_confirm_duration': ['p(95)<1500'],
    'dropx_reserve_success':  ['rate>0.01' ],
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
    const res = http.get(`${BASE_PRODUCT}/api/sneakers`, { headers })
    listDuration.add(Date.now() - s)
    check(res, { 'list 200': r => r.status === 200 })
    try {
      const items = JSON.parse(res.body).items
      if (items?.length) sneakerId = items[0].id
    } catch (_) {}
  })

  sleep(0.2)

  group('2_detail', () => {
    const s   = Date.now()
    const res = http.get(`${BASE_PRODUCT}/api/sneakers/${sneakerId}`, { headers })
    detailDuration.add(Date.now() - s)
    check(res, { 'detail 200': r => r.status === 200 })
  })

  sleep(0.1)

  let reserveToken = null
  group('3_reserve', () => {
    const s   = Date.now()
    const res = http.post(`${BASE_ORDER}/api/orders/reserve`,
      JSON.stringify({ sneaker_id: sneakerId, size }),
      { headers }
    )
    reserveDuration.add(Date.now() - s)

    if (res.status === 409) {
      soldOut.add(1)
      reserveSuccess.add(false)
      return
    }

    const ok = check(res, {
      'reserve 200':        r => r.status === 200,
      'reserve_token 존재': r => { try { return !!JSON.parse(r.body).reserve_token } catch { return false } },
    })
    reserveSuccess.add(ok)
    if (ok) try { reserveToken = JSON.parse(res.body).reserve_token } catch (_) {}
  })

  if (!reserveToken) { sleep(0.1); return }

  sleep(0.3)

  group('4_confirm', () => {
    const s   = Date.now()
    const res = http.post(`${BASE_ORDER}/api/orders/confirm`,
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