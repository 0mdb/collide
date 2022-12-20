import { Colors } from '@blueprintjs/core'
import React from 'react'
import { ForceGraph2D } from 'react-force-graph'
import myData from './sample_graph3.json'

const ForceGraph3Dprops = {
  graphData: myData,
}

function Home() {
  return (
    <div className='Home'>
      <ForceGraph2D
        graphData={myData}
        nodeAutoColorBy='id'
        linkColor={Colors.GOLD3}
        linkDirectionalParticles='value'
        linkCurvature='curvature'
        linkDirectionalParticles={1}
      />
    </div>
  )
}

export default Home
