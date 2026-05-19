import React, { useEffect, useState, useContext } from 'react'
import MainLayout from '../layouts/MainLayout'
import orderService from '../services/orderService'
import Loader from '../components/Loader'
import EnhancedOrderTable from '../components/orders/EnhancedOrderTable'
import OrderDrawer from '../components/orders/OrderDrawer'
import Timeline from '../components/timeline/Timeline'
import EmptyState from '../components/ui/EmptyState'
import TableSkeleton from '../components/skeletons/TableSkeleton'
import Pagination from '../components/Pagination'
import { AuthContext } from '../context/AuthContext'
import useDebounce from '../hooks/useDebounce'
import { useToast } from '../context/ToastContext'

export default function OrdersPage(){
  const { user } = useContext(AuthContext)
  const [orders, setOrders] = useState([])
  const [drawerOpen, setDrawerOpen] = useState(false)
  const [activeOrder, setActiveOrder] = useState(null)
  const [auditEvents, setAuditEvents] = useState([])
  const [page, setPage] = useState(1)
  const [limit] = useState(10)
  const [totalPages, setTotalPages] = useState(1)
  const [status, setStatus] = useState('')
  const [search, setSearch] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const toast = useToast()

  const debouncedFetch = useDebounce((p, s) => fetch(p, s), 300)

  const fetch = async (p=1, searchTerm='') => {
    setLoading(true)
    setError(null)
    try{
      let payload
      if(user?.role === 'admin'){
        payload = await orderService.adminListOrders({ page: p, limit, status: status || undefined, search: searchTerm || undefined })
      } else {
        payload = await orderService.listOrders({ page: p, limit, status: status || undefined })
      }
      // payload might be { items, page, total_pages } or { data: { items,...}}
      const data = payload || {}
      const items = data.items || data.results || []
      const pageNum = data.page || data.current_page || p
      const total = data.total_pages || data.totalPages || data.total || 1
      setOrders(items)
      setPage(pageNum)
      setTotalPages(total)
    }catch(err){
      console.error(err)
      setError(err?.response?.data?.detail || err.message || 'Failed to load orders')
      toast?.addToast(err?.response?.data?.detail || err.message || 'Failed to load orders', 'error')
    }finally{
      setLoading(false)
    }
  }

  useEffect(()=>{ fetch(1) }, [status])
  useEffect(()=>{ debouncedFetch(1, search) }, [search])

  const handleCancel = async (order) => {
    if(!window.confirm('Cancel this order?')) return
    try{
      await orderService.transitionOrder({ orderId: order.id, status: 'CANCELLED' })
      toast?.addToast('Order cancelled', 'info')
      fetch(page)
    }catch(err){
      const msg = err?.response?.data?.detail || err.message || 'Failed'
      toast?.addToast(msg, 'error')
    }
  }

  const handleTransition = async (orderId, newStatus) => {
    try{
      await orderService.transitionOrder({ orderId, status: newStatus })
      toast?.addToast(`Order transitioned to ${newStatus}`, 'success')
      fetch(page)
      if(activeOrder?.id === orderId) {
        fetchAudit(orderId)
      }
    }catch(err){
      const msg = err?.response?.data?.detail || err.message || 'Failed'
      toast?.addToast(msg, 'error')
    }
  }

  return (
    <MainLayout>
      <div className="p-6">
        <div className="flex items-center justify-between">
          <h1 className="text-xl font-bold">My Orders</h1>
          <div className="flex items-center gap-2">
            <select value={status} onChange={e=>setStatus(e.target.value)} className="p-2 border rounded">
              <option value="">All</option>
              <option>PENDING</option>
              <option>CONFIRMED</option>
              <option>SHIPPED</option>
              <option>DELIVERED</option>
              <option>CANCELLED</option>
            </select>
            <input value={search} onChange={e=>setSearch(e.target.value)} placeholder="Search external id" className="p-2 border rounded" />
          </div>
        </div>

        <div className="mt-4">
          {loading ? <TableSkeleton /> : (
            <>
              {error && <div className="text-red-600 mb-3">{error}</div>}
              {orders.length === 0 ? (
                <EmptyState 
                  title="No orders found"
                  description={search || status ? "Try clearing your filters or search term." : "Create your first order to get started."}
                  onRetry={() => fetch(page)}
                  onReset={() => { setSearch(''); setStatus(''); fetch(1) }}
                />
              ) : (
                <>
                      <EnhancedOrderTable orders={orders} onCancel={handleCancel} onOpen={(o)=>{ setActiveOrder(o); setDrawerOpen(true); fetchAudit(o.id) }} onTransition={handleTransition} />
                  <div className="mt-3">
                    <Pagination page={Math.max(1, page)} totalPages={Math.max(1, totalPages)} onPageChange={(p)=>{ setPage(p); fetch(p) }} />
                  </div>
                </>
              )}
            </>
          )}
        </div>
            <OrderDrawer open={drawerOpen} order={activeOrder} onClose={()=>setDrawerOpen(false)} audit={auditEvents} />
      </div>
    </MainLayout>
  )

      async function fetchAudit(orderId){
        try{
          const res = await orderService.getOrderAudit(orderId)
          setAuditEvents(res?.items || res || [])
        }catch(e){ setAuditEvents([]) }
      }
}
