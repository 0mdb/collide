import { Outlet } from 'react-router-dom'
import React, { useState, useEffect } from 'react'
import useAuth from '../hooks/useAuth'
import { getMe } from '../api/authApi'

export default function PersistLogin() {
  const [isLoading, setIsLoading] = useState(true)
  const { auth, persist, setPersist, setUser } = useAuth()

  useEffect(() => {
    let isMounted = true

    const verifyToken = async () => {
      try {
        // If the auth object is empty, there's nothing to verify
        if (!auth) {
          setPersist(false)
        } else {
          const user = await getMe(auth)
          setUser(user)
          setPersist(true)
        }
      } catch (error) {
        console.error(error)
        setPersist(false)
      } finally {
        isMounted && setIsLoading(false)
      }
    }

    verifyToken()

    return () => (isMounted = false)
  }, [auth])

  useEffect(() => {
    console.log(`isLoading: ${isLoading}`)
  }, [isLoading])

  return <>{!persist ? <Outlet /> : isLoading ? <p>Loading...</p> : <Outlet />}</>
}
