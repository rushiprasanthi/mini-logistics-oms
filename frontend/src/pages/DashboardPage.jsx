import React, {
  useEffect,
  useState,
} from 'react'

import MainLayout from '../layouts/MainLayout'

import KpiCards from '../components/dashboard/KpiCards'

import ActivityFeed from '../components/dashboard/ActivityFeed'

import orderService from '../services/orderService'

import OrderCard from '../components/orders/OrderCard'

export default function DashboardPage() {
  const [stats, setStats] =
    useState({})

  const [pending, setPending] =
    useState([])

  const [recent, setRecent] =
    useState([])

  const [auditEvents, setAuditEvents] =
    useState([])

  const [loading, setLoading] =
    useState(true)

  const [error, setError] =
    useState(null)

  useEffect(() => {
    const load = async () => {
      try {
        setLoading(true)

        const res =
          await orderService.listOrders({
            page: 1,
            limit: 50,
          })

        console.log(
          'DASHBOARD RESPONSE:',
          res
        )

        const data = res || {}

        const items =
          data.items || []

        const total = items.length

        const pendingItems =
          items.filter(
            (i) =>
              i.status ===
              'PENDING'
          )

        const shipped =
          items.filter(
            (i) =>
              i.status ===
              'SHIPPED'
          )

        const delivered =
          items.filter(
            (i) =>
              i.status ===
              'DELIVERED'
          )

        const cancelled =
          items.filter(
            (i) =>
              i.status ===
              'CANCELLED'
          )

        setStats({
          total,
          pending:
            pendingItems.length,
          shipped:
            shipped.length,
          delivered:
            delivered.length,
          cancelled:
            cancelled.length,
        })

        setPending(
          pendingItems.slice(0, 5)
        )

        setRecent(
          items
            .sort(
              (a, b) =>
                new Date(
                  b.created_at ||
                    b.created
                ) -
                new Date(
                  a.created_at ||
                    a.created
                )
            )
            .slice(0, 5)
        )

        try {
          const auditPromises =
            items
              .slice(0, 3)
              .map((o) =>
                orderService.getOrderAudit(
                  o.id
                )
              )

          const auditResults =
            await Promise.all(
              auditPromises
            )

          const allEvents =
            auditResults.flatMap(
              (r) =>
                r?.items ||
                r ||
                []
            )

          setAuditEvents(
            allEvents
              .sort(
                (a, b) =>
                  new Date(
                    b.created_at
                  ) -
                  new Date(
                    a.created_at
                  )
              )
              .slice(0, 10)
          )
        } catch (e) {
          console.error(
            'AUDIT ERROR:',
            e
          )

          setAuditEvents([])
        }
      } catch (e) {
        console.error(
          'DASHBOARD ERROR:',
          e
        )

        setError(
          e.message ||
            'Dashboard failed to load'
        )
      } finally {
        setLoading(false)
      }
    }

    load()
  }, [])

  if (loading) {
    return (
      <div className="p-6">
        Loading dashboard...
      </div>
    )
  }

  if (error) {
    return (
      <div className="p-6 text-red-600">
        {error}
      </div>
    )
  }

  return (
    <MainLayout>
      <div className="p-6">
        <h1 className="text-2xl font-bold mb-4">
          Operational Dashboard
        </h1>

        <KpiCards stats={stats} />

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-6">
          <section>
            <h2 className="font-semibold mb-2">
              Pending Confirmations
            </h2>

            {pending.length ===
            0 ? (
              <div className="text-sm text-gray-500">
                No pending
                confirmations
              </div>
            ) : (
              pending.map((o) => (
                <OrderCard
                  key={
                    o.id ||
                    o.external_id
                  }
                  order={o}
                  onOpen={() => {}}
                />
              ))
            )}
          </section>

          <section>
            <h2 className="font-semibold mb-2">
              Recently Delivered
            </h2>

            {recent.length ===
            0 ? (
              <div className="text-sm text-gray-500">
                No recent activity
              </div>
            ) : (
              recent.map((o) => (
                <OrderCard
                  key={
                    o.id ||
                    o.external_id
                  }
                  order={o}
                  onOpen={() => {}}
                />
              ))
            )}
          </section>

          <section>
            <h2 className="font-semibold mb-2">
              Recent Activity
            </h2>

            <ActivityFeed
              events={auditEvents}
            />
          </section>
        </div>
      </div>
    </MainLayout>
  )
}