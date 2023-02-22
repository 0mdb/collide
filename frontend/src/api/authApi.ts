import axios from './axios'
import { useQuery, useMutation } from '@tanstack/react-query'

export interface graphDataType {
  nodes: {
    id: string
    name: string
    type: string
    val: number
  }
  links: {
    source: 'string'
    target: 'string'
    type: 'string'
    color: 'string'
    dash: [0]
    amount: 0
  }
}

export interface ApiUser {
  id: string
  email: string
  is_active: string
  is_superuser: string
  is_verified: string
}

export const login = async (username: string, password: string) => {
  const response = await axios.post('auth/jwt/login', { username, password })
  return response.data
}

export const registerUser = async (email: string, password: string) => {
  const response = await axios.post('auth/register/', email, password)
  return response.data
}

export const forgotPassword = async (email: string) => {
  const response = await axios.post('auth/forgot-password/', { email })
  return response.data
}

export const resetPassword = async (token: string, password: string) => {
  const response = await axios.post('auth/reset-password/', { token, password })
  return response.data
}

export const getUser = async (token: string) => {
  const response = await axios.post<ApiUser>('auth/verify', { token })

  return response.data
}
