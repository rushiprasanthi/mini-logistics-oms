import React from 'react'
import StatusBadge from '../ui/StatusBadge'

export default function OrderCard({ order, onOpen, onCancel }){
  return (
    <article className="bg-white p-4 rounded shadow mb-3">
      <div className="flex items-start justify-between">
        <div>
          <h3 className="font-semibold">{order.external_id}</h3>
          <div className="text-sm text-gray-600">Customer: {order.customer_id || '—'}</div>
        </div>
        <div className="text-right">
          <StatusBadge status={order.status} />
          <div className="mt-2">
            <button onClick={()=>onOpen(order)} className="px-3 py-1 bg-blue-600 text-white rounded mr-2">Details</button>
            {onCancel && order.status !== 'CANCELLED' && (
              <button onClick={()=>onCancel(order)} className="px-3 py-1 bg-red-500 text-white rounded">Cancel</button>
            )}
          </div>
        </div>
      </div>
    </article>
  )
}
