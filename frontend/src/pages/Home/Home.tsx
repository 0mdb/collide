import React from 'react'
import ForceGraph from '../../components/ForceGraph'
import SideBar from '../../components/SideBar'

function Home() {
  return (
    <div className='ml-16 flex h-full dark:bg-gray-700'>
      <SideBar />
      <ForceGraph />
    </div>
  )
}

export default Home
