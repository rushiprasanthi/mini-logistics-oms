import React from 'react'

export default function OrderTable({ orders = [], onCancel }){
  return (
    <div className="bg-white shadow rounded overflow-x-auto">
      <div className="min-w-full">
        <table className="w-full text-left table-auto">
          <thead className="bg-gray-50">
            <tr>
              <th className="p-3">External ID</th>
              <th className="p-3">Customer</th>
              <th className="p-3">Status</th>
              <th className="p-3">Created</th>
              <th className="p-3">Actions</th>
            </tr>
          </thead>
          <tbody>
            {orders.map(o => (
              <tr key={o.id || o.external_id} className="border-t">
                <td className="p-3 break-words max-w-xs">{o.external_id}</td>
                <td className="p-3">{o.customer_id || o.customer || '—'}</td>
                <td className="p-3">{o.status}</td>
                <td className="p-3">{new Date(o.created_at || o.createdAt || o.created || Date.now()).toLocaleString()}</td>
                <td className="p-3">
                  {onCancel && o.status !== 'CANCELLED' && (
                    <button onClick={() => onCancel(o)} className="px-2 py-1 bg-red-500 text-white rounded">Cancel</button>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}
