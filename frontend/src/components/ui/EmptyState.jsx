import React from 'react'

export default function EmptyState({ title, message, onRetry, onReset }){
  return (
    <div className="bg-white p-8 rounded shadow text-center">
      <div className="text-lg font-semibold text-gray-700">{title}</div>
      <div className="text-sm text-gray-500 mt-2">{message}</div>
      <div className="mt-4 flex gap-3 justify-center">
        {onRetry && <button onClick={onRetry} className="px-4 py-2 bg-blue-600 text-white rounded">Retry</button>}
        {onReset && <button onClick={onReset} className="px-4 py-2 bg-gray-500 text-white rounded">Clear Filters</button>}
      </div>
    </div>
  )
}
