import React from 'react'
import ReactDOM from 'react-dom/client'
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import './index.css'
import Navbar from './components/Navbar'
import Landing from './pages/Landing'
import DropDetail from './pages/DropDetail'
import Login from './pages/Login'
import MyOrders from './pages/MyOrders'
import Admin from './pages/Admin'

ReactDOM.createRoot(document.getElementById('root')).render(
  <BrowserRouter>
    <Navbar />
    <Routes>
      <Route path="/" element={<Landing />} />
      <Route path="/drop/:id" element={<DropDetail />} />
      <Route path="/login" element={<Login />} />
      <Route path="/orders" element={<MyOrders />} />
      <Route path="/admin" element={<Admin />} />
    </Routes>
  </BrowserRouter>
)
