import React from 'react'
import { Outlet } from 'react-router-dom'
/* import NavBar from '../NavBar' */
import NavGroup from '../NavBar/NavGroup'

function Layout() {
  return (
    <main className='App + bp4-dark'>
      <NavGroup />
      {/* <NavBar /> */}
      <Outlet />
    </main>
  )
}

export default Layout
