import React from 'react'
import ForceGraph from '../../components/ForceGraph'
import SideBar from '../../components/SideBar'

function Home() {
  return (
    <div className='ml-16 flex'>
      <SideBar />
      <div>
        <ForceGraph />
      </div>
    </div>
  )
}

export default Home
