import React, {
  useState,
} from 'react'

import {
  Link,
  useNavigate,
} from 'react-router-dom'

import { useAuth } from '../context/AuthContext'

import { useToast } from '../context/ToastContext'

import Loader from '../components/Loader'

export default function LoginPage() {
  const [email, setEmail] =
    useState('')

  const [password, setPassword] =
    useState('')

  const [error, setError] =
    useState(null)

  const { login, loading } =
    useAuth()

  const navigate = useNavigate()

  const toast = useToast()

  const submit = async (e) => {
    e.preventDefault()

    setError(null)

    try {
      const response =
        await login(
          email,
          password
        )

      console.log(
        'LOGIN SUCCESS:',
        response
      )

      toast?.addToast(
        'Login successful',
        'success'
      )

      navigate('/dashboard')
    } catch (err) {
      console.error(err)

      const msg =
        err?.response?.data
          ?.detail ||
        err.message ||
        'Login failed'

      setError(msg)

      toast?.addToast(
        msg,
        'error'
      )
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100">
      <div className="w-full max-w-md bg-white rounded-lg shadow p-6">
        <h1 className="text-2xl font-bold mb-6">
          Login
        </h1>

        <form
          onSubmit={submit}
          className="space-y-4"
        >
          <input
            type="email"
            placeholder="Email"
            className="w-full border rounded p-3"
            value={email}
            onChange={(e) =>
              setEmail(
                e.target.value
              )
            }
          />

          <input
            type="password"
            placeholder="Password"
            className="w-full border rounded p-3"
            value={password}
            onChange={(e) =>
              setPassword(
                e.target.value
              )
            }
          />

          {error && (
            <div className="text-red-600 text-sm">
              {error}
            </div>
          )}

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-blue-600 text-white rounded p-3"
          >
            {loading ? (
              <Loader />
            ) : (
              'Login'
            )}
          </button>
        </form>

        <div className="mt-4 text-sm">
          Don't have an account?{' '}
          <Link
            to="/signup"
            className="text-blue-600"
          >
            Signup
          </Link>
        </div>
      </div>
    </div>
  )
}