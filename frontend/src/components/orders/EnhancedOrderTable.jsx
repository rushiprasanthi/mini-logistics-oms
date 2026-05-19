import React, { useState, useContext } from 'react'
import StatusBadge from '../ui/StatusBadge'
import ShipmentProgress from '../shipment/ShipmentProgress'
import AdminActions from './AdminActions'
import OrderCard from './OrderCard'
import { AuthContext } from '../../context/AuthContext'

export default function EnhancedOrderTable({ orders = [], onCancel, onOpen, onTransition }){
  const { user } = useContext(AuthContext)
  const [sortBy, setSortBy] = useState('created_at')
  const [dir, setDir] = useState('desc')

  const sort = (a,b) => {
    const av = a[sortBy] || ''
    const bv = b[sortBy] || ''
    if(dir === 'asc') return (''+av).localeCompare(''+bv)
    return (''+bv).localeCompare(''+av)
  }

  const toggle = (col) => {
    if(col === sortBy) setDir(d => d === 'asc' ? 'desc' : 'asc')
    else { setSortBy(col); setDir('asc') }
  }

  const sorted = [...orders].sort(sort)

  return (
    <div>
      {/* table for desktop */}
      <div className="hidden md:block bg-white rounded shadow overflow-auto">
        <table className="min-w-full table-auto">
          <thead className="bg-gray-50 sticky top-0">
            <tr>
              <th className="p-3 cursor-pointer" onClick={()=>toggle('external_id')}>External ID</th>
              <th className="p-3 cursor-pointer" onClick={()=>toggle('customer_id')}>Customer</th>
              <th className="p-3">Progress</th>
              <th className="p-3 cursor-pointer" onClick={()=>toggle('created_at')}>Created</th>
              <th className="p-3">Actions</th>
            </tr>
          </thead>
          <tbody>
            {sorted.map(o => (
              <tr key={o.id || o.external_id} className="border-t">
                <td className="p-3">{o.external_id}</td>
                <td className="p-3">{o.customer_id || '—'}</td>
                <td className="p-3"><ShipmentProgress status={o.status} /></td>
                <td className="p-3">{new Date(o.created_at || o.created || Date.now()).toLocaleString()}</td>
                <td className="p-3">
                  <div className="flex gap-2 flex-col">
                    <div className="flex gap-2">
                      <button onClick={()=>onOpen && onOpen(o)} className="px-2 py-1 bg-blue-600 text-white rounded">Details</button>
                      {onCancel && o.status !== 'CANCELLED' && (
                        <button onClick={()=>onCancel(o)} className="px-2 py-1 bg-red-500 text-white rounded">Cancel</button>
                      )}
                    </div>
                    {user?.role === 'admin' && onTransition && (
                      <AdminActions order={o} onTransition={onTransition} />
                    )}
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* card layout for mobile */}
      <div className="md:hidden">
        {orders.map(o => (
          <OrderCard key={o.id||o.external_id} order={o} onOpen={onOpen} onCancel={onCancel} />
        ))}
      </div>
    </div>
  )
}
