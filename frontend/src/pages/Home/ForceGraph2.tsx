import React, { useRef, useState } from 'react'
import { ForceGraph2D, ForceGraph3D } from 'react-force-graph'
import { useQuery } from '@tanstack/react-query'
import Loading from '../../components/Loading'
import { useWindowSize } from '@react-hook/window-size'
import { Icon } from '@blueprintjs/core'
import AsyncSelect from 'react-select/async'
import useDarkMode from '../../hooks/useDarkMode'
import { getOptions, getSampleGraph, getGraph } from '../../api/graph'

const SearchIcon = () => (
  <Icon icon='search' size={28} className='mx-2 dark:fill-muted dark:shadow-lg' />
)

function Search() {
  const handleChange = async (selectedOption) => {
    {
      setSearchSelection(selectedOption.value)
    }
    console.log('selected Search is :', searchSelection)
  }

  const loadOptions = (inputValue: string, callback) => {
    console.log('inputValue', inputValue)

    getOptions(inputValue).then(async (options) => {
      const filteredOptions = await options.filter((option) =>
        option.label.toLowerCase().includes(inputValue.toLowerCase()),
      )
      console.log('loadOptions', inputValue, filteredOptions)
      callback(filteredOptions)
    })
  }

  ;<div className='fixed top-4 left-24 flex h-12 flex-row items-center justify-center'>
    <SearchIcon />
    <AsyncSelect
      unstyled={true}
      isClearable={true}
      className='dark: w-64 rounded-md border-2 border-gray-200 border-gray-800 shadow-sm focus:outline-none focus:ring-primary'
      loadOptions={loadOptions}
      onChange={handleChange}
    />
    <GraphTypeButton graphType={graphType} setGraphType={setGraphType} />
  </div>
}

function ForceGraph() {
  const fgRef = useRef()
  const [width, height] = useWindowSize()
  const [graphType, setGraphType] = useState('2D')
  const [searchSelection, setSearchSelection] = useState(null)
  const [darkMode] = useDarkMode()

  const {
    status: sampleStatus,
    error: sampleError,
    data: sampleData,
  } = useQuery({
    queryKey: ['getSampleGraph'],
    queryFn: getSampleGraph,
    refetchOnWindowFocus: false,
  })

  const {
    status: graphStatus,
    error: graphError,
    data: newGraphData,
    isFetching,
  } = useQuery({
    queryKey: ['getGraph', searchSelection],
    queryFn: getGraph,
    enabled: !!searchSelection,
  })

  if (graphStatus === 'loading' && searchSelection) return <Loading />
  if (graphError === 'error' && searchSelection) return <div>Error</div>
  if (sampleStatus === 'loading') return <Loading />
  if (sampleError === 'error') return <div>Error</div>

  function GetGraph() {
    if (graphType === '2D') {
      return (
        <ForceGraph2D
          ref={fgRef}
          graphData={newGraphData ? newGraphData : sampleData}
          height={height - height / 4}
          width={width - width / 4}
          cooldownTicks={100}
          nodeAutoColorBy='id'
          linkDirectionalParticles='value'
          linkCurvature='curvature'
          onEngineStop={() => fgRef.current.zoomToFit(400)}
        />
      )
    } else {
      return (
        <ForceGraph3D
          ref={fgRef}
          graphData={newGraphData ? newGraphData : sampleData}
          height={height - height / 4}
          width={width - width / 4}
          cooldownTicks={100}
          nodeAutoColorBy='id'
          backgroundColor={darkMode ? '#334155' : 'white'}
          linkDirectionalParticles='value'
          linkCurvature='curvature'
          onEngineStop={() => fgRef.current.zoomToFit(400)}
        />
      )
    }
  }

  return <div className='bg-white dark:bg-slate-700'>{isFetching ? <Loading /> : <GetGraph />}</div>
}

export default ForceGraph
