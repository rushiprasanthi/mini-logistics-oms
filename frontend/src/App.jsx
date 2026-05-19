import React from 'react'
import { Routes, Route, Navigate } from 'react-router-dom'
import RoutesList from './routes/Routes'

export default function App(){
  return (
    <Routes>
      <Route path="/*" element={<RoutesList />} />
      <Route path="/" element={<Navigate to="/dashboard" replace />} />
    </Routes>
  )
}
