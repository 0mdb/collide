import React, { useRef } from 'react'
import { ForceGraph2D } from 'react-force-graph'
import myData from './sample_graph3.json'

import { useWindowSize } from '@react-hook/window-size'

function ForceGraph() {
  const fgRef = useRef()
  const [width, height] = useWindowSize()

  return (
    <ForceGraph2D
      ref={fgRef}
      graphData={myData}
      height={height - 400}
      width={width - 200}
      cooldownTicks={100}
      nodeAutoColorBy='id'
      linkDirectionalParticles='value'
      linkCurvature='curvature'
      onEngineStop={() => fgRef.current.zoomToFit(400)}
    />
  )
}
export default ForceGraph
