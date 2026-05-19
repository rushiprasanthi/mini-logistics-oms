import React from 'react'

export default function Pagination({ page, totalPages, onPageChange }){
  const pages = []
  for(let i=1;i<=totalPages;i++) pages.push(i)
  return (
    <div className="flex items-center gap-2 p-2">
      {pages.map(p => (
        <button key={p} onClick={() => onPageChange(p)} className={`px-3 py-1 rounded ${p===page? 'bg-blue-600 text-white':'bg-white text-gray-700 border'}`}>
          {p}
        </button>
      ))}
    </div>
  )
}
