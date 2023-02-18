import React, { useRef } from 'react'
import { ForceGraph2D } from 'react-force-graph'
import { useQuery } from '@tanstack/react-query'
import Loading from '../../components/Loading'
import { useWindowSize } from '@react-hook/window-size'
import { getGraph } from '../../api/graph'
import useSearchSelection from '../../hooks/useSearchSelection'

function ForceGraph() {
  const [selectedSearch, setSelectedSearch] = useSearchSelection()
  const [width, height] = useWindowSize()
  const fgRef = useRef()

  const {
    status: graphStatus,
    error: graphError,
    data: graphData,
    isFetching,
  } = useQuery({
    queryKey: ['getGraph', selectedSearch],
    queryFn: () => getGraph(selectedSearch),
    enabled: selectedSearch !== null,
    refetchOnWindowFocus: false,
  })

  if (graphStatus === 'loading' && selectedSearch) return <Loading />
  if (graphError === 'error' && selectedSearch) return <div>Error</div>

  const handleChange = async (selectedOption) => {
    {
      setSelectedSearch(selectedOption)
    }
    console.log('selected Search is :', selectedSearch)
  }

  return (
    <div className='flex flex-row m-6 justify-center'>
      {isFetching ? (
        <Loading />
      ) : (
        <ForceGraph2D
          ref={fgRef}
          graphData={graphData}
          height={height}
          width={width}
          cooldownTicks={100}
          nodeAutoColorBy='id'
          linkDirectionalParticles='value'
          linkCurvature='curvature'
          onEngineStop={() => fgRef.current.zoomToFit(400)}
          onNodeClick={(node) => {
            console.log('node', node)
            setSelectedSearch(node.id)
          }}
        />
      )}
    </div>
  )
}

export default ForceGraph
