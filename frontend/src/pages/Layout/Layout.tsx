import React from 'react'
import { Outlet } from 'react-router-dom'
function Layout() {
  return (
    <main className='dark:bg-gray-700 dark:text-morp'>
      <Outlet />
    </main>
  )
}

export default Layout
