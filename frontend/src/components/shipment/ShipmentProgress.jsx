import React from 'react'

const STEPS = ['PENDING', 'CONFIRMED', 'SHIPPED', 'DELIVERED']

export default function ShipmentProgress({ status }){
  const isCancelled = status === 'CANCELLED'
  const currentIdx = STEPS.indexOf(status)

  const getColor = (step, idx) => {
    if(isCancelled) return 'bg-gray-300 text-gray-700'
    if(idx < currentIdx) return 'bg-green-500 text-white'
    if(idx === currentIdx) return 'bg-blue-500 text-white'
    return 'bg-gray-200 text-gray-600'
  }

  return (
    <div className="flex items-center gap-2">
      {isCancelled ? (
        <div className="px-3 py-1 rounded bg-gray-200 text-gray-800 text-sm font-medium">Cancelled</div>
      ) : (
        <>
          {STEPS.map((step, i) => (
            <div key={step} className="flex items-center gap-1">
              <div className={`w-8 h-8 rounded-full ${getColor(step, i)} flex items-center justify-center text-xs font-bold`}>{i+1}</div>
              {i < STEPS.length - 1 && <div className={`h-1 w-8 ${i < currentIdx ? 'bg-green-500' : 'bg-gray-200'}`}></div>}
            </div>
          ))}
        </>
      )}
    </div>
  )
}
