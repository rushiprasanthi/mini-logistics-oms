import React, { useContext, useState } from 'react'
import { Link } from 'react-router-dom'
import { AuthContext } from '../context/AuthContext'

export default function Navbar(){
  const { user, logout } = useContext(AuthContext)
  const [open, setOpen] = useState(false)
  return (
    <nav className="bg-white shadow p-4 flex justify-between items-center">
      <div className="flex items-center gap-4">
        <Link to="/dashboard" className="font-bold text-lg">Mini OMS</Link>
        <div className="hidden sm:flex gap-3">
          <Link to="/orders" className="text-sm text-gray-600" onClick={()=>setOpen(false)}>Orders</Link>
        </div>
        <button className="sm:hidden ml-2 p-2" onClick={()=>setOpen(o=>!o)} aria-label="menu">
          <svg className="h-6 w-6" viewBox="0 0 24 24" fill="none" stroke="currentColor"><path strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" d={open? 'M6 18L18 6M6 6l12 12' : 'M4 6h16M4 12h16M4 18h16'} /></svg>
        </button>
      </div>
      {open && (
        <div className="sm:hidden absolute top-16 left-0 right-0 bg-white border-t p-4">
          <Link to="/orders" className="block py-1" onClick={()=>setOpen(false)}>Orders</Link>
        </div>
      )}
      <div className="flex items-center gap-4">
        {user ? (
          <>
            <span className="text-sm text-gray-700">{user.username || user.email || 'User'}</span>
            <button onClick={logout} className="px-3 py-1 bg-red-500 text-white rounded">Logout</button>
          </>
        ) : (
          <Link to="/login" className="px-3 py-1 bg-blue-500 text-white rounded">Login</Link>
        )}
      </div>
    </nav>
  )
}
