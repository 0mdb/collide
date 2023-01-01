import React from 'react'
import { ForceGraph2D } from 'react-force-graph'
import myData from './sample_graph4.json'

function ForceGraph() {
  return (
    <div className='overflow-hidden rounded-lg shadow-lg'>
      <div className='light:bg-inherit py-3 px-5 dark:bg-inherit'>
        <ForceGraph2D
          graphData={myData}
          nodeAutoColorBy='id'
          linkDirectionalParticles='value'
          linkCurvature='curvature'
        />
      </div>
    </div>
  )
}

export default ForceGraph
