import React, { useState } from 'react'
import StatusBadge from '../ui/StatusBadge'

const TRANSITIONS = {
  'PENDING': ['CONFIRMED', 'CANCELLED'],
  'CONFIRMED': ['SHIPPED', 'CANCELLED'],
  'SHIPPED': ['DELIVERED'],
  'DELIVERED': [],
  'CANCELLED': []
}

export default function AdminActions({ order, onTransition, disabled=false }){
  const [loading, setLoading] = useState(false)
  const allowed = TRANSITIONS[order.status] || []

  const handle = async (newStatus) => {
    setLoading(true)
    try{
      await onTransition({ orderId: order.id, status: newStatus })
    }finally{
      setLoading(false)
    }
  }

  if(!allowed || allowed.length === 0) return null

  return (
    <div className="flex gap-2">
      {allowed.map(s => (
        <button key={s} disabled={loading || disabled} onClick={()=>handle(s)} className="px-2 py-1 bg-blue-600 text-white rounded text-sm disabled:opacity-60">
          {s}
        </button>
      ))}
    </div>
  )
}
