import React from 'react'
import { Link } from 'react-router-dom'

export default function Sidebar(){
  return (
    <aside className="hidden sm:block w-56 bg-white p-4 border-r">
      <ul className="space-y-2">
        <li><Link to="/dashboard" className="text-gray-700">Dashboard</Link></li>
        <li><Link to="/orders" className="text-gray-700">Orders</Link></li>
        <li><Link to="/orders/create" className="text-gray-700">Create Order</Link></li>
      </ul>
    </aside>
  )
}
