import { useRef, useEffect } from 'react'

export default function useDebounce(fn, delay=300){
  const t = useRef(null)
  useEffect(()=>{
    return ()=>{ if(t.current) clearTimeout(t.current) }
  },[])
  return (...args) => {
    if(t.current) clearTimeout(t.current)
    t.current = setTimeout(()=> fn(...args), delay)
  }
}
