import axios from '../../api/axios'
import React, { useCallback, useRef, useState } from 'react'
import { ForceGraph2D } from 'react-force-graph'
import { ForceGraph3D } from 'react-force-graph'
import { useQuery } from '@tanstack/react-query'
import Loading from '../../components/Loading'
import { useWindowSize } from '@react-hook/window-size'
import { Icon } from '@blueprintjs/core'
import AsyncSelect from 'react-select/async'
import useDarkMode from '../../hooks/useDarkMode'
import useGraphType from '../../hooks/useGraphType'

async function getSampleGraph() {
  return await axios.get<graphDataType>('/forcegraph/sample').then((res) => res.data)
}

async function getOptions(query: string) {
  const SEARCH_URL = 'forcegraph/search_options?query='
  const match_name = query.toLowerCase().split(' ').join('')
  return await axios.post(SEARCH_URL + match_name).then((res) => res.data)
}

export async function getGraph(query: string) {
  console.log('getGraph', query)
  return await axios.post('forcegraph/search/' + query).then((res) => res.data)
}

const SearchIcon = () => (
  <Icon icon='search' size={28} className='mx-2 dark:fill-muted dark:shadow-lg' />
)

function ForceGraph() {
  const [width, height] = useWindowSize()

  const [searchSelection, setSearchSelection] = useState(null)

  const {
    status: sampleStatus,
    error: sampleError,
    data: sampleData,
  } = useQuery({
    queryKey: ['getSampleGraph'],
    queryFn: () => getSampleGraph(),
    refetchOnWindowFocus: false,
  })

  /* const {
   *   status: optionStatus,
   *   error: optionError,
   *   data: optionData,
   * } = useQuery({
   *   queryKey: ['getOptions', inputValue],
   *   queryFn: () => getOptions(inputValue),
   *   refetchOnWindowFocus: false,
   * })
   */
  const {
    status: graphStatus,
    error: graphError,
    data: newGraphData,
    isFetching,
  } = useQuery({
    queryKey: ['getGraph', searchSelection],
    queryFn: () => getGraph(searchSelection),
    enabled: !!searchSelection,
    refetchOnWindowFocus: false,
  })

  if (graphStatus === 'loading' && searchSelection) return <Loading />
  if (graphError === 'error' && searchSelection) return <div>Error</div>
  if (sampleStatus === 'loading') return <Loading />
  if (sampleError === 'error') return <div>Error</div>

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

  function GetGraph() {
    const fgRef = useRef()

    const { graphType } = useGraphType()
    const [darkMode] = useDarkMode()

    if (graphType === '2D') {
      return (
        <ForceGraph2D
          ref={fgRef}
          graphData={newGraphData ? newGraphData : sampleData}
          height={height - 100}
          width={width - 200}
          cooldownTicks={100}
          nodeAutoColorBy='id'
          linkDirectionalParticles='value'
          linkCurvature='curvature'
          onEngineStop={() => fgRef.current.zoomToFit(400)}
          // on clicking node add to search and combine graphs and highlight selected node
          onNodeClick={(node) => {
            console.log('node', node)
            setSearchSelection(node.id)
          }}
          // makes the currently selected node more visible
        />
      )
    } else {
      return (
        <ForceGraph3D
          ref={fgRef}
          graphData={newGraphData ? newGraphData : sampleData}
          height={height}
          width={width - 200}
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

  return (
    <>
      <div>
        <div className='top-6 flex h-12 flex-row items-center justify-center'>
          <SearchIcon />
          <AsyncSelect
            // unstyled={true}
            isClearable={true}
            className='dark:text-black w-64 rounded-md border-gray-200 dark:border-gray-800 shadow-sm focus:outline-none focus:ring-primary'
            loadOptions={loadOptions}
            onChange={handleChange}
          />
        </div>
      </div>
      {/* <div className='bg-white dark:bg-slate-700'></div> */}
      <div className='flex flex-row m-6 justify-center'>
        {isFetching ? <Loading /> : <GetGraph />}
      </div>
    </>
  )
}

export default ForceGraph
AbortController
