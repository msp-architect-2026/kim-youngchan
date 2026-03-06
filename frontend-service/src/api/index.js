const BASE = '/api'

const headers = (token) => ({
  'Content-Type': 'application/json',
  ...(token ? { Authorization: `Bearer ${token}` } : {})
})

export const authAPI = {
  signup: (data) =>
    fetch(`${BASE}/auth/signup`, { method: 'POST', headers: headers(), body: JSON.stringify(data) }).then(r => r.json()),
  login: (data) =>
    fetch(`${BASE}/auth/login`, { method: 'POST', headers: headers(), body: JSON.stringify(data) }).then(r => r.json()),
  me: (token) =>
    fetch(`${BASE}/auth/me`, { headers: headers(token) }).then(r => r.json()),
}

export const productAPI = {
  list: () =>
    fetch(`${BASE}/sneakers`).then(r => r.json()),
  detail: (id) =>
    fetch(`${BASE}/sneakers/${id}`).then(r => r.json()),
  liveStock: (id) =>
    fetch(`${BASE}/sneakers/${id}/stock/live`).then(r => r.json()),
}

export const orderAPI = {
  reserve: (token, data) =>
    fetch(`${BASE}/orders/reserve`, { method: 'POST', headers: headers(token), body: JSON.stringify(data) }).then(r => r.json()),
  confirm: (token, data) =>
    fetch(`${BASE}/orders/confirm`, { method: 'POST', headers: headers(token), body: JSON.stringify(data) }).then(r => r.json()),
  myOrders: (token) =>
    fetch(`${BASE}/orders`, { headers: headers(token) }).then(r => r.json()),
}

export const adminAPI = {
  metrics: (token) =>
    fetch(`${BASE}/admin/metrics`, { headers: headers(token) }).then(r => r.json()),
  orders: (token) =>
    fetch(`${BASE}/admin/orders`, { headers: headers(token) }).then(r => r.json()),
  killPod: (token) =>
    fetch(`${BASE}/admin/kill-pod`, { method: 'POST', headers: headers(token) }).then(r => r.json()),
}
