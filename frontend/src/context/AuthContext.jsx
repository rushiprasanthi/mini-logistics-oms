import React, {
  createContext,
  useContext,
  useEffect,
  useState,
} from 'react'

import authService from '../services/authService'

export const AuthContext =
  createContext()

// IMPORTANT FIX
export const useAuth = () =>
  useContext(AuthContext)

export function AuthProvider({
  children,
}) {
  const [user, setUser] =
    useState(null)

  const [loading, setLoading] =
    useState(false)

  useEffect(() => {
    const storedUser =
      localStorage.getItem(
        'user'
      )

    if (storedUser) {
      setUser(
        JSON.parse(storedUser)
      )
    }
  }, [])

  const login = async (
    email,
    password
  ) => {
    try {
      setLoading(true)

      const response =
        await authService.login(
          email,
          password
        )

      console.log(
        'LOGIN RESPONSE:',
        response
      )

      const token =
        response?.data
          ?.access_token

      const authUser =
        response?.data?.user

      if (!token) {
        console.error(
          'FULL RESPONSE:',
          response
        )

        throw new Error(
          'Token missing from response'
        )
      }

      localStorage.setItem(
        'token',
        token
      )

      localStorage.setItem(
        'user',
        JSON.stringify(
          authUser
        )
      )

      setUser(authUser)

      return response
    } finally {
      setLoading(false)
    }
  }

  const signup = async (
    email,
    password
  ) => {
    return authService.signup(
      email,
      password
    )
  }

  const logout = () => {
    localStorage.removeItem(
      'token'
    )

    localStorage.removeItem(
      'user'
    )

    setUser(null)
  }

  return (
    <AuthContext.Provider
      value={{
        user,
        loading,
        login,
        signup,
        logout,
      }}
    >
      {children}
    </AuthContext.Provider>
  )
}