import React from 'react'

const COLORS = {
  DELIVERED: 'bg-green-100 text-green-800',
  SHIPPED: 'bg-blue-100 text-blue-800',
  PENDING: 'bg-yellow-100 text-yellow-800',
  CANCELLED: 'bg-gray-100 text-gray-800',
  FAILED: 'bg-red-100 text-red-800'
}

export default function StatusBadge({ status }){
  const cls = COLORS[status] || 'bg-gray-100 text-gray-800'
  return (
    <span className={`px-2 py-0.5 rounded text-xs font-medium ${cls}`}>{status}</span>
  )
}
