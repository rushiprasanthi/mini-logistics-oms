import React, {
  useState,
} from 'react'

import {
  useNavigate,
} from 'react-router-dom'

import orderService from '../services/orderService'

export default function CreateOrderPage() {
  const [externalId, setExternalId] =
    useState('')

  const [loading, setLoading] =
    useState(false)

  const [error, setError] =
    useState(null)

  const navigate = useNavigate()

  const submit = async (e) => {
    e.preventDefault()

    setError(null)

    try {
      setLoading(true)

      await orderService.createOrder(
        {
          external_id:
            externalId,
        }
      )

      navigate('/orders')
    } catch (err) {
      console.error(err)

      setError(
        err?.response?.data
          ?.detail ||
          err.message ||
          'Failed to create order'
      )
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="p-6">
      <div className="max-w-xl bg-white rounded shadow p-6">
        <h1 className="text-2xl font-bold mb-6">
          Create Order
        </h1>

        <form
          onSubmit={submit}
          className="space-y-4"
        >
          <div>
            <label className="block mb-2">
              External ID
            </label>

            <input
              type="text"
              value={externalId}
              onChange={(e) =>
                setExternalId(
                  e.target.value
                )
              }
              placeholder="ORD-1001"
              className="w-full border rounded p-3"
              required
            />
          </div>

          {error && (
            <div className="text-red-600">
              {error}
            </div>
          )}

          <button
            type="submit"
            disabled={loading}
            className="bg-blue-600 text-white px-4 py-2 rounded"
          >
            {loading
              ? 'Creating...'
              : 'Create'}
          </button>
        </form>
      </div>
    </div>
  )
}