import axios from '../../api/axios'
import React, { useRef, useState } from 'react'
import { ForceGraph2D } from 'react-force-graph'
import { ForceGraph3D } from 'react-force-graph'
import { useQuery } from '@tanstack/react-query'
import Loading from '../../components/Loading'
import { useWindowSize } from '@react-hook/window-size'
import { Icon } from '@blueprintjs/core'
import AsyncSelect from 'react-select/async'
import useDarkMode from '../../hooks/useDarkMode'

async function getSampleGraph() {
  return axios.get<graphDataType[]>('/forcegraph/sample').then((res) => res.data)
}

async function getOptions(query: string) {
  const SEARCH_URL = 'forcegraph/search_options?query='
  const match_name = query.toLowerCase().split(' ').join('')
  return axios.post(SEARCH_URL + match_name).then((res) => res.data)
}

export async function getGraph(query: string) {
  console.log('getGraph', query)
  return axios.post('forcegraph/search/' + query).then((res) => res.data)
}

function GraphTypeButton({ graphType, setGraphType }) {
  const changeGraphType = () => {
    if (graphType === '2D') {
      setGraphType('3D')
    } else {
      setGraphType('2D')
    }
  }
  return (
    <button
      className='hover:bg-primary-dark flex h-10 w-10 items-center justify-center rounded-full bg-primary text-white shadow-lg'
      onClick={changeGraphType}
    >
      {graphType === '2D' ? '3D' : '2D'}
    </button>
  )
}

const SearchIcon = () => (
  <Icon icon='search' size={28} className='mx-2 dark:fill-muted dark:shadow-lg' />
)

function ForceGraph() {
  const fgRef = useRef()
  const [width, height] = useWindowSize()
  const [graphData, setGraphData] = useState(null)
  const [graphType, setGraphType] = useState('2D')
  const [darkMode] = useDarkMode()

  const {
    status: sampleStatus,
    error: sampleError,
    data: sampleData,
  } = useQuery({
    queryKey: ['getSampleGraph'],
    queryFn: () => getSampleGraph(),
  })

  const {
    status: optionStatus,
    error: optionError,
    data: optionData,
  } = useQuery({
    queryKey: ['getOptions'],
    queryFn: () => getOptions(''),
  })

  // const {
  //   status: graphStatus,
  //   error: graphError,
  //   data: newGraphData,
  // } = useQuery({
  //   queryKey: ['getGraph'],
  //   queryFn: () => getGraph(''),
  // })

  // if (graphStatus === 'loading') return <div>Loading</div>
  // if (graphError === 'error') return <div>Error</div>
  if (sampleStatus === 'loading') return <div>Loading</div>
  if (sampleError === 'error') return <div>Error</div>
  if (optionStatus === 'loading') return <div>Loading</div>
  if (optionError === 'error') return <div>Error</div>

  const handleChange = async (selectedOption) => {
    await getGraph(selectedOption.value).then((response) => {
      setGraphData(response)
      console.log(`selectedOption`, selectedOption, 'response', graphData)
    })
  }

  const loadOptions = async (inputValue: string, callback) => {
    console.log('inputValue', inputValue)

    const filteredOptions = await optionData.filter((option) =>
      option.label.toLowerCase().includes(inputValue.toLowerCase()),
    )
    callback(filteredOptions)
  }

  return (
    <>
      {graphType === '2D' ? (
        <ForceGraph2D
          ref={fgRef}
          graphData={graphData ? graphData : sampleData}
          height={height}
          width={width - 100}
          cooldownTicks={100}
          nodeAutoColorBy='id'
          linkDirectionalParticles='value'
          linkCurvature='curvature'
          onEngineStop={() => fgRef.current.zoomToFit(400)}
        />
      ) : (
        <ForceGraph3D
          ref={fgRef}
          graphData={graphData ? graphData : sampleData}
          height={height}
          width={width - 100}
          cooldownTicks={100}
          nodeAutoColorBy='id'
          backgroundColor={darkMode ? '#334155' : 'white'}
          linkDirectionalParticles='value'
          linkCurvature='curvature'
          onEngineStop={() => fgRef.current.zoomToFit(400)}
        />
      )}
      <>
        <div className='fixed top-4 left-24 flex h-12 flex-row items-center justify-center'>
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
      </>
    </>
  )
}

export default ForceGraph
