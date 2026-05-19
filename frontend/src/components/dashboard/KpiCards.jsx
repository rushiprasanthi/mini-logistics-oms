import React from 'react'

export default function KpiCards({ stats = {} }){
  const items = [
    { key: 'total', label: 'Total Orders' },
    { key: 'pending', label: 'Pending' },
    { key: 'shipped', label: 'Shipped' },
    { key: 'delivered', label: 'Delivered' },
    { key: 'cancelled', label: 'Cancelled' }
  ]

  return (
    <div className="grid grid-cols-2 sm:grid-cols-5 gap-3">
      {items.map(i => (
        <div key={i.key} className="bg-white p-3 rounded shadow flex flex-col">
          <div className="text-sm text-gray-500">{i.label}</div>
          <div className="text-2xl font-semibold">{stats[i.key] ?? 0}</div>
        </div>
      ))}
    </div>
  )
}
