import React from 'react'
import Footer from './Footer'
import Navbar from './Nav'
import { Outlet } from 'react-router-dom'

function Landing() {
  return (
    <div className='bg-secondary dark:bg-secondary-d'>
      <Navbar />
      <div>
        <Outlet />
      </div>
      <Footer />
    </div>
  )
}

export default Landing
