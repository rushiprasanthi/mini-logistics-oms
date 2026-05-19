import React from 'react'

export default function Toasts({ toasts = [], onRemove = ()=>{} }){
  return (
    <div aria-live="polite" className="fixed z-50 right-4 top-4 w-80 space-y-2">
      {toasts.map(t => (
        <div key={t.id} role="status" className={`p-3 rounded shadow ${t.type === 'error' ? 'bg-red-50 border border-red-200' : 'bg-white border'}`}>
          <div className="flex items-center justify-between">
            <div className="text-sm">{t.message}</div>
            <button aria-label="close" onClick={()=>onRemove(t.id)} className="ml-3 text-gray-500">×</button>
          </div>
        </div>
      ))}
    </div>
  )
}
