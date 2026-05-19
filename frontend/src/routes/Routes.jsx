import React from 'react'
import { Routes, Route } from 'react-router-dom'
import LoginPage from '../pages/LoginPage'
import SignupPage from '../pages/SignupPage'
import DashboardPage from '../pages/DashboardPage'
import OrdersPage from '../pages/OrdersPage'
import CreateOrderPage from '../pages/CreateOrderPage'
import ProtectedRoute from '../components/ProtectedRoute'

export default function RoutesList(){
  return (
    <Routes>
      <Route path="/login" element={<LoginPage />} />
      <Route path="/signup" element={<SignupPage />} />

      <Route element={<ProtectedRoute />}>
        <Route path="/dashboard" element={<DashboardPage />} />
        <Route path="/orders" element={<OrdersPage />} />
        <Route path="/orders/create" element={<CreateOrderPage />} />
      </Route>

      <Route path="*" element={<LoginPage />} />
    </Routes>
  )
}
