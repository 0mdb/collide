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
  org: string
  darkmkode: false
  country: string
  province: string
  language: string
  timezone: string
  search: [string]
}

export interface LoginAuth {
  access_token: string
  token_type: string
}

export const loginUser = async (formData) => {
  const response = await axios.post<LoginAuth>('auth/jwt/login/', formData, {
    withCredentials: true,
  })
  return response.data
}

export const registerUser = async (email: string, password: string) => {
  const response = await axios.post('auth/register/', email, password)
  return response.data
}

export const forgotPassword = async (email: string) => {
  const response = await axios.post('auth/forgot-password/', email)
  return response.data
}

export const resetPassword = async (token: string, password: string) => {
  const response = await axios.post('auth/reset-password/', { token, password })
  return response.data
}

export const getMe = async () => {
  const response = await axios.get('users/me/', { withCredentials: true })
  return response.data
}

export const updateCurrentUser = async (data: ApiUser) => {
  const response = await axios.patch('users/me/', data, { withCredentials: true })
  return response.data
}
