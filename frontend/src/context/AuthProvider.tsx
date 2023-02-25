import React, { createContext, useState } from 'react'

const AuthContext = createContext({})

type AuthProviderProps = {
  children: React.ReactNode
}

type Persist = {
  auth: {
    token: string
    user: {
      id: string
      name: string
      email: string
      avatar: string
    }
  }
}

type User = {
  id: string
  email: string
  is_active: boolean
  is_superuser: boolean
  is_verifed: boolean
}

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState<User | null>(null)
  const [token, setToken] = useState<string | null>(null)
  const [loading, setLoading] = useState<boolean>(true)
  const [error, setError] = useState<string | null>(null)
  const [auth, setAuth] = useState<Persist | null>(null)

  return (
    <AuthContext.Provider
      value={{
        user,
        setUser,
        token,
        setToken,
        loading,
        setLoading,
        error,
        setError,
        auth,
        setAuth,
      }}
    >
      {children}
    </AuthContext.Provider>
  )
}

export default AuthContext
