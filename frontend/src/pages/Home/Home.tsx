import React from 'react'
import ForceGraph from '../../components/ForceGraph'
import TopNavigation from '../../components/NavBar'
import GraphBar from '../../components/GraphBar'
import SideBar from '../../components/SideBar'

function Home () {
  return (
    <div className='flex'>
      <SideBar />
      <GraphBar />
      <div className='content-container'>
      <TopNavigation />
      <div className='content-list'>
      <ForceGraph />
      </div>
      </div>
    </div>
  )
}

export default Home