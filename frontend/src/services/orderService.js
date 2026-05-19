import api from './api'

const normalizeListResponse = (
  response
) => {
  return {
    items:
      response?.data?.data || [],
    meta:
      response?.data?.meta || {},
  }
}

const normalizeSingleResponse = (
  response
) => {
  return (
    response?.data?.data || null
  )
}

const listOrders = async (
  params = {}
) => {
  const response =
    await api.instance.get(
      '/orders/my',
      {
        params,
      }
    )

  console.log(
    'LIST ORDERS RESPONSE:',
    response.data
  )

  return normalizeListResponse(
    response
  )
}

const createOrder = async (
  payload
) => {
  console.log(
    'CREATE ORDER PAYLOAD:',
    payload
  )

  const response =
    await api.instance.post(
      '/orders',
      {
        external_id:
          payload.external_id,
      }
    )

  console.log(
    'CREATE ORDER RESPONSE:',
    response.data
  )

  return normalizeSingleResponse(
    response
  )
}

const getOrder = async (id) => {
  const response =
    await api.instance.get(
      `/orders/${id}`
    )

  return normalizeSingleResponse(
    response
  )
}

const confirmOrder = async (
  id
) => {
  const response =
    await api.instance.post(
      `/orders/${id}/confirm`
    )

  return normalizeSingleResponse(
    response
  )
}

const shipOrder = async (id) => {
  const response =
    await api.instance.post(
      `/orders/${id}/ship`
    )

  return normalizeSingleResponse(
    response
  )
}

const deliverOrder = async (
  id
) => {
  const response =
    await api.instance.post(
      `/orders/${id}/deliver`
    )

  return normalizeSingleResponse(
    response
  )
}

const cancelOrder = async (
  id
) => {
  const response =
    await api.instance.post(
      `/orders/${id}/cancel`
    )

  return normalizeSingleResponse(
    response
  )
}

const getOrderAudit =
  async (id) => {
    const response =
      await api.instance.get(
        `/orders/${id}/audit`
      )

    return normalizeListResponse(
      response
    )
  }

export default {
  listOrders,
  createOrder,
  getOrder,
  confirmOrder,
  shipOrder,
  deliverOrder,
  cancelOrder,
  getOrderAudit,
}