import React from 'react'

export default function TableSkeleton({ rows=5 }){
  return (
    <div className="bg-white rounded shadow p-4">
      <div className="animate-pulse">
        <div className="h-6 bg-gray-200 rounded w-1/4 mb-4"></div>
        {Array.from({ length: rows }).map((_,i)=> (
          <div key={i} className="flex items-center gap-4 mb-3">
            <div className="h-8 bg-gray-200 rounded w-20"></div>
            <div className="h-8 bg-gray-200 rounded flex-1"></div>
            <div className="h-8 bg-gray-200 rounded w-32"></div>
          </div>
        ))}
      </div>
    </div>
  )
}
