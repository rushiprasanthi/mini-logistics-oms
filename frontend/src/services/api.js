import axios from 'axios'

const API_BASE =
  import.meta.env
    .VITE_API_BASE ||
  'http://localhost:8000/api/v1'

const instance = axios.create({
  baseURL: API_BASE,
  headers: {
    'Content-Type':
      'application/json',
    Accept:
      'application/json',
  },
  timeout: 10000,
})

// attach token directly
instance.interceptors.request.use(
  (config) => {
    const token =
      localStorage.getItem(
        'token'
      ) ||
      localStorage.getItem(
        'access_token'
      )

    console.log(
      'REQUEST TOKEN:',
      token
    )

    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }

    return config
  },
  (error) =>
    Promise.reject(error)
)

// global auth handling
instance.interceptors.response.use(
  (response) => response,
  (error) => {
    const status =
      error?.response?.status

    console.error(
      'API ERROR:',
      error?.response
    )

    if (status === 401) {
      localStorage.removeItem(
        'token'
      )

      localStorage.removeItem(
        'access_token'
      )

      window.location.href =
        '/login'
    }

    return Promise.reject(error)
  }
)

export default {
  instance,
}