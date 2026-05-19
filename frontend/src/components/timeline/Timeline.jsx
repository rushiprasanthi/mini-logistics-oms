import React from 'react'

export default function Timeline({ events = [] }){
  if(!events || events.length === 0) return <div className="text-gray-500">No timeline events.</div>
  return (
    <ol className="border-l ml-4">
      {events.map(e => (
        <li key={e.id} className="mb-4 pl-4">
          <div className="text-sm text-gray-600">{new Date(e.created_at).toLocaleString()}</div>
          <div className="font-medium">{e.event_type} <span className="text-xs text-gray-500">by {e.actor || 'system'}</span></div>
          {e.note && <div className="text-sm text-gray-700">{e.note}</div>}
        </li>
      ))}
    </ol>
  )
}
