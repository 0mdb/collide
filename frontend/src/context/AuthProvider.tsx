import React, { createContext, useState } from 'react'

const AuthContext = createContext({})

type AuthProviderProps = {
  children: React.ReactNode
}

/* type Persist = {
 *   auth: {
 *     token: string
 *     user: {
 *       id: string
 *       name: string
 *       email: string
 *       avatar: string
 *     }
 *   }
 * }
 *  */
type User = {
  id: string
  email: string
  is_active: boolean
  is_superuser: boolean
  is_verifed: boolean
}

export const AuthProvider = ({ children }) => {
  const [auth, setAuth] = useState('')
  const [user, setUser] = useState('')
  const [persist, setPersist] = useState<boolean>(false)
  const [loading, setLoading] = useState<boolean>(true)

  return (
    <AuthContext.Provider
      value={{
        auth,
        setAuth,
        user,
        setUser,
        persist,
        setPersist,
        loading,
        setLoading,
      }}
    >
      {children}
    </AuthContext.Provider>
  )
}

export default AuthContext
