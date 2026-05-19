import React from 'react'

const ICONS = {
  'ORDER_CREATED': '📋',
  'STATUS_CHANGED': '➡️',
  'DELIVERED': '✅',
  'CANCELLED': '❌'
}

export default function EnhancedTimeline({ events = [] }){
  if(!events || events.length === 0) return <div className="text-sm text-gray-500">No audit events.</div>

  return (
    <ol className="space-y-3">
      {events.map(e => (
        <li key={e.id} className="flex gap-3">
          <div className="text-lg">{ICONS[e.event_type] || '•'}</div>
          <div className="flex-1">
            <div className="font-medium text-sm">{e.event_type} <span className="text-xs text-gray-500">by {e.actor || 'system'}</span></div>
            <div className="text-xs text-gray-600">{new Date(e.created_at).toLocaleString()}</div>
            {e.note && <div className="text-sm text-gray-700 mt-1">{e.note}</div>}
          </div>
        </li>
      ))}
    </ol>
  )
}
