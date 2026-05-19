import React, {
  useContext,
  useEffect,
} from 'react'

import StatusBadge from '../ui/StatusBadge'

import { AuthContext } from '../../context/AuthContext'

import ShipmentProgress from '../shipment/ShipmentProgress'

import EnhancedTimeline from '../timeline/EnhancedTimeline'

export default function OrderDrawer({
  open,
  order,
  onClose,
  audit = [],
  onTransition,
}) {
  const { user } =
    useContext(AuthContext)

  if (!open || !order)
    return null

  // robust admin detection
  const roleValue =
    typeof user?.role ===
    'string'
      ? user.role.toUpperCase()
      : user?.role?.name
          ?.toUpperCase?.() ||
        ''

  console.log(
    'CURRENT USER:',
    user
  )

  console.log(
    'ROLE VALUE:',
    roleValue
  )

  const isAdmin =
    roleValue.includes(
      'ADMIN'
    )

  useEffect(() => {
    const handle = (e) => {
      if (e.key === 'Escape') {
        onClose()
      }
    }

    if (open) {
      document.addEventListener(
        'keydown',
        handle
      )
    }

    return () => {
      document.removeEventListener(
        'keydown',
        handle
      )
    }
  }, [open, onClose])

  const renderActions = () => {
    if (!isAdmin) return null

    return (
      <div className="flex flex-wrap gap-2">
        {order.status ===
          'PENDING' && (
          <>
            <button
              onClick={() =>
                onTransition(
                  order.id,
                  'CONFIRMED'
                )
              }
              className="px-3 py-2 bg-blue-600 text-white rounded"
            >
              Confirm
            </button>

            <button
              onClick={() =>
                onTransition(
                  order.id,
                  'CANCELLED'
                )
              }
              className="px-3 py-2 bg-red-600 text-white rounded"
            >
              Cancel
            </button>
          </>
        )}

        {order.status ===
          'CONFIRMED' && (
          <button
            onClick={() =>
              onTransition(
                order.id,
                'SHIPPED'
              )
            }
            className="px-3 py-2 bg-indigo-600 text-white rounded"
          >
            Ship
          </button>
        )}

        {order.status ===
          'SHIPPED' && (
          <button
            onClick={() =>
              onTransition(
                order.id,
                'DELIVERED'
              )
            }
            className="px-3 py-2 bg-green-600 text-white rounded"
          >
            Deliver
          </button>
        )}
      </div>
    )
  }

  return (
    <aside className="fixed right-0 top-0 bottom-0 w-full sm:w-1/3 bg-white border-l p-4 overflow-auto z-50">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-lg font-bold">
          Order{' '}
          {order.external_id}
        </h2>

        <button
          onClick={onClose}
          aria-label="close drawer"
          className="text-lg"
        >
          ✕
        </button>
      </div>

      <div className="space-y-4">
        <div>
          <strong>Status:</strong>{' '}
          <StatusBadge
            status={order.status}
          />
        </div>

        <div>
          <strong>Progress:</strong>

          <div className="mt-2">
            <ShipmentProgress
              status={order.status}
            />
          </div>
        </div>

        {isAdmin && (
          <div>
            <strong>
              Admin Actions
            </strong>

            <div className="mt-3">
              {renderActions()}
            </div>
          </div>
        )}

        <div>
          <strong>Customer:</strong>{' '}
          {order.customer_id ||
            '—'}
        </div>

        <div>
          <strong>Created:</strong>{' '}
          {new Date(
            order.created_at ||
              order.created ||
              Date.now()
          ).toLocaleString()}
        </div>

        <div>
          <strong>Metadata:</strong>

          <pre className="bg-gray-50 p-2 rounded text-sm">
            {JSON.stringify(
              order.meta || {},
              null,
              2
            )}
          </pre>
        </div>

        <div>
          <h3 className="font-semibold">
            Audit Timeline
          </h3>

          <div className="mt-2">
            <EnhancedTimeline
              events={audit}
            />
          </div>
        </div>
      </div>
    </aside>
  )
}