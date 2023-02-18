import React from 'react'
import { Outlet } from 'react-router-dom'
import SideBar from './SideBar'

function Home() {
  return (
    <div className='flex flex-col'>
      <SideBar />
      <div className='ml-16'>
        <Outlet />
      </div>
    </div>
  )
}

export default Home
