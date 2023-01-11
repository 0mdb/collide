import React, { useRef } from 'react'
import { ForceGraph2D } from 'react-force-graph'
import { useQuery } from '@tanstack/react-query'
import { getGraph } from '../../api/graph'
import Loading from '../Loading'

import { useWindowSize } from '@react-hook/window-size'

function ForceGraph() {
  const fgRef = useRef()
  const [width, height] = useWindowSize()
  const { status, error, data } = useQuery({
    queryKey: ['forcegraph'],
    queryFn: getGraph,
  })

  if (status === 'loading') return <Loading />
  if (error === 'error') return <div>Error</div>

  return (
    <ForceGraph2D
      ref={fgRef}
      graphData={data}
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
