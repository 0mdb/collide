import React from 'react'
import ForceGraph from '../../components/ForceGraph'
import TopNavigation from '../../components/NavBar'
import GraphBar from '../../components/GraphBar'
import SideBar from '../../components/SideBar'
import Sankey from '../../components/SankeyGraph'
import { Icon } from '@blueprintjs/core'

const PlusIcon = () => (
  <Icon icon='search' size={22} className='dark:text-primary mx-2 text-green-500 dark:shadow-lg' />
)

const BottomBar = () => (
  <div className='bottom-bar'>
    <PlusIcon />
    <input type='text' placeholder='Search...' className='bottom-bar-input' />
  </div>
)

function Home() {
  return (
    <div className='flex'>
      <SideBar />
      <GraphBar />
      <div className='content-container'>
        <TopNavigation />
        <div className='inline-block grid'>
          <Sankey />
          <ForceGraph />
        </div>
        <BottomBar />
      </div>
    </div>
  )
}

export default Home
