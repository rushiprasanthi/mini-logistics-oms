import React from 'react'

export default function ActivityFeed({ events = [] }){
  if(!events || events.length === 0) return (
    <div className="bg-white p-4 rounded shadow text-sm text-gray-500">No recent activity.</div>
  )

  return (
    <div className="bg-white rounded shadow">
      <div className="divide-y">
        {events.slice(0, 10).map(e => (
          <div key={e.id} className="p-3 text-sm">
            <div className="flex justify-between">
              <div className="font-medium">{e.event_type}</div>
              <div className="text-xs text-gray-500">{new Date(e.created_at).toLocaleTimeString()}</div>
            </div>
            <div className="text-gray-600 text-xs mt-1">{e.note || e.actor || 'system event'}</div>
          </div>
        ))}
      </div>
    </div>
  )
}
