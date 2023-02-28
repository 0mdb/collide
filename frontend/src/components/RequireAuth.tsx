import { useLocation, Navigate, Outlet } from 'react-router-dom'
import useAuth from '../hooks/useAuth'
import React from 'react'

function RequireAuth({ allowedRoles }) {
  const { auth, user } = useAuth()
  const location = useLocation()

  console.log('Rquireauth auth', { auth })
  console.log('Requireauth user', { user })

  /* const decoded = auth?.accessToken ? jwt_decode(auth?.accessToken) : null */

  //const roles = decoded?.roles || []
  // roles array made up of user.is_superuser and user.is_verified
  const roles = user?.is_superuser ? ['superuser'] : []
  if (user?.is_verified) {
    roles.push('verified')
  }

  console.log('Requireauth roles', roles)

  // TODO - check if user has any of the allowed roles
  console.log(`roles are: ${roles}`)

  return roles?.find((role) => allowedRoles?.includes(role)) ? (
    <Outlet />
  ) : auth?.access_token ? (
    <Navigate to='/unauthorized' state={{ from: location }} replace />
  ) : (
    <Navigate to='/login' state={{ from: location }} replace />
  )
}

export default RequireAuth
