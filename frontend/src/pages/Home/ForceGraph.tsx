import React, { useRef } from 'react'
import { ForceGraph2D } from 'react-force-graph'
import { useQuery } from '@tanstack/react-query'
import Loading from '../../components/Loading'
import { useWindowSize } from '@react-hook/window-size'
import { getGraph } from '../../api/graph'

function ForceGraph(props) {
  const [width, height] = useWindowSize()
  const fgRef = useRef()

  const {
    status: graphStatus,
    error: graphError,
    data: graphData,
    isFetching,
  } = useQuery({
    queryKey: ['getGraph', props.selected],
    queryFn: () => getGraph(props.selected),
    enabled: !!props.selected,
    refetchOnWindowFocus: false,
  })

  if (graphStatus === 'loading' && props.selected) return <Loading />
  if (graphError === 'error' && props.selected) return <div>Error</div>

  const handleChange = async (selectedOption) => {
    {
      props.setSelected(selectedOption)
    }
    console.log('selected Search is :', props.selected)
  }

  return (
    <div className='flex flex-row m-6 justify-center'>
      {isFetching ? (
        <Loading />
      ) : (
        <ForceGraph2D
          ref={fgRef}
          graphData={graphData}
          height={0.75 * height}
          width={width * 0.75}
          cooldownTicks={100}
          nodeAutoColorBy='id'
          linkDirectionalParticles='value'
          linkCurvature='curvature'
          onEngineStop={() => fgRef.current.zoomToFit(400)}
          onNodeClick={(node) => {
            console.log('node', node)
            props.setSelected(node.id)
          }}
        />
      )}
    </div>
  )
}

export default ForceGraph
