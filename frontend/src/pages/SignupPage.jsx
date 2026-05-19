import React, {
  useState,
} from 'react'

import {
  useNavigate,
} from 'react-router-dom'

import { useAuth } from '../context/AuthContext'

import Loader from '../components/Loader'

import { useToast } from '../context/ToastContext'

export default function SignupPage() {
  const [email, setEmail] =
    useState('')

  const [password, setPassword] =
    useState('')

  const [error, setError] =
    useState(null)

  const { signup, loading } =
    useAuth()

  const navigate = useNavigate()

  const toast = useToast()

  const submit = async (e) => {
    e.preventDefault()

    setError(null)

    if (!email || !password) {
      setError(
        'Email and password are required'
      )

      return
    }

    try {
      await signup(
        email,
        password
      )

      toast?.addToast(
        'Account created',
        'info'
      )

      navigate('/dashboard')
    } catch (err) {
      console.error(err)

      setError(
        err?.response?.data
          ?.detail ||
          err.message ||
          'Signup failed'
      )
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center">
      <div className="w-full max-w-md bg-white p-6 rounded shadow">
        <h2 className="text-xl font-bold mb-4">
          Sign up
        </h2>

        <form
          onSubmit={submit}
          className="space-y-3"
        >
          <input
            className="w-full p-2 border rounded"
            placeholder="Email"
            value={email}
            onChange={(e) =>
              setEmail(
                e.target.value
              )
            }
          />

          <input
            className="w-full p-2 border rounded"
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) =>
              setPassword(
                e.target.value
              )
            }
          />

          {error && (
            <div className="text-red-600">
              {error}
            </div>
          )}

          <button
            disabled={loading}
            className="w-full py-2 bg-green-600 text-white rounded disabled:opacity-60"
          >
            {loading ? (
              <Loader />
            ) : (
              'Create account'
            )}
          </button>
        </form>
      </div>
    </div>
  )
}