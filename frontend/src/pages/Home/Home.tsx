import { Colors } from '@blueprintjs/core'
import React from 'react'
import { ForceGraph3D } from 'react-force-graph'
import myData from './dataset.json'

const ForceGraph3Dprops = {
  graphData: myData,
  nodeAutoColorBy: 'group',
  backgroundColor: Colors.DARK_GRAY3,
}

function Home() {
  return (
    <div className='Home'>
      <ForceGraph3D {...ForceGraph3Dprops} />
    </div>
  )
}

export default Home
