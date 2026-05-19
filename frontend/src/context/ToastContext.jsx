import React, { createContext, useContext, useState, useCallback } from 'react'
import Toasts from '../components/Toasts'

const ToastContext = createContext(null)

export function ToastProvider({ children }){
  const [toasts, setToasts] = useState([])

  const addToast = useCallback((message, type='info', ttl=4000) => {
    const id = Math.random().toString(36).slice(2,9)
    const t = { id, message, type }
    setToasts(s => [t, ...s])
    if(ttl > 0){
      setTimeout(()=> setToasts(s => s.filter(x => x.id !== id)), ttl)
    }
    return id
  }, [])

  const removeToast = useCallback((id) => setToasts(s => s.filter(t => t.id !== id)), [])

  return (
    <ToastContext.Provider value={{ addToast, removeToast }}>
      {children}
      <Toasts toasts={toasts} onRemove={removeToast} />
    </ToastContext.Provider>
  )
}

export function useToast(){
  return useContext(ToastContext)
}

export default ToastContext
