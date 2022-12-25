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

export function AuthProvider({ children }: AuthProviderProps) {
  const [auth, setAuth] = useState({})
  const [persist, setPersist] = useState<Persist | null>(null)

  return (
    <AuthContext.Provider value={{ auth, setAuth, persist, setPersist }}>
      {children}
    </AuthContext.Provider>
  )
}

export default AuthContext
