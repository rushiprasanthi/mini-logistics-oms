import api from './api'

const login = async (email, password) => {
  const response = await api.instance.post(
    '/auth/login',
    {
      email,
      password
    }
  )

  return response.data
}

const signup = async (
  email,
  password
) => {
  const response =
    await api.instance.post(
      '/auth/register',
      {
        email,
        password
      }
    )

  return response.data
}

const getProfile = async () => {
  const response =
    await api.instance.get('/auth/me')

  return response.data
}

const authService = {
  login,
  signup,
  getProfile
}

export default authService