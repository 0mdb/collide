import React from 'react'
import { ForceGraph2D } from 'react-force-graph'
import myData from './sample_graph4.json'

function ForceGraph () {
    return (
      <div className='force-graph'>
      <ForceGraph2D
        graphData={myData}
        nodeAutoColorBy='id'
        linkDirectionalParticles='value'
        linkCurvature='curvature'
      />
      </div>
    )   
}

export default ForceGraph