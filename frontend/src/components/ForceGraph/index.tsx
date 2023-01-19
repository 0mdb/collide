import React, { useRef, useState } from 'react'
import { ForceGraph2D } from 'react-force-graph'
import { useQuery } from '@tanstack/react-query'
import { getSampleGraph } from '../../api/graph'
import Loading from '../Loading'
import { useWindowSize } from '@react-hook/window-size'
import { Icon } from '@blueprintjs/core'
import AsyncSelect from 'react-select/async'
import axios from '../../api/axios'

const SearchIcon = () => (
  <Icon icon='search' size={28} className='mx-2 text-green-500 dark:text-primary dark:shadow-lg' />
)

function ForceGraph() {
  const fgRef = useRef()
  const [width, height] = useWindowSize()
  const [graphData, setGraphData] = useState(null)
  const { status, error, data } = useQuery({
    queryKey: ['forcegraph'],
    queryFn: getSampleGraph,
  })
  if (status === 'loading') return <Loading />
  if (error === 'error') return <div>Error</div>

  const SEARCH_URL = 'forcegraph/search_options?query='

  async function getOptions(query: string) {
    const match_name = query.toLowerCase().split(' ').join('')
    return axios.post(SEARCH_URL + match_name).then((res) => res.data)
  }

  async function getGraph(query: string) {
    console.log('getGraph', query)
    return axios.post('forcegraph/search/' + query).then((res) => res.data)
  }

  const handleChange = (selectedOption) => {
    getGraph(selectedOption.value).then((response) => {
      setGraphData(response)
      console.log(`selectedOption`, selectedOption, 'response', graphData)
    })
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

  return (
    <>
      <ForceGraph2D
        ref={fgRef}
        graphData={graphData ? graphData : data}
        height={height}
        width={width - 100}
        cooldownTicks={100}
        nodeAutoColorBy='id'
        linkDirectionalParticles='value'
        linkCurvature='curvature'
        onEngineStop={() => fgRef.current.zoomToFit(400)}
      />
      <>
        <div className='fixed top-4 left-24 flex h-12 flex-row items-center justify-center'>
          <SearchIcon />
          <AsyncSelect
            unstyled={true}
            className='dark: w-64 rounded-md border-2 border-gray-200 border-gray-800 shadow-sm focus:outline-none focus:ring-primary'
            loadOptions={loadOptions}
            onChange={handleChange}
          />
        </div>
      </>
    </>
  )
}

// function ForceGraph() {
//   const fgRef = useRef()
//   const [width, height] = useWindowSize()
//   const [filteredNodes, setFilteredNodes] = useState([])
//   const [query, setQuery] = useState('')
//   const [selected, setSelected] = useState(null)
//   const [node, setNode] = useState(null)
//   const { status, error, data } = useQuery({
//     queryKey: ['forcegraph'],
//     queryFn: getGraph,
//   })

//   if (status === 'loading') return <Loading />
//   if (error === 'error') return <div>Error</div>

//   const handleQueryChange = (query) => {
//     setQuery(query)
//     setFilteredNodes(
//       data.nodes.filter((node) => node.name.toLowerCase().includes(query.toLowerCase())),
//     )
//   }

//   const handleNodeSelect = (node) => {
//     setNode(node)
//     setQuery('')
//   }

//   const renderNode = (node, { handleClick, modifiers }) => {
//     if (!modifiers.matchesPredicate) {
//       return null
//     }
//     return (
//       <MenuItem
//         className='text-gray-500
//          dark:text-gray-400
//         '
//         active={modifiers.active}
//         disabled={modifiers.disabled}
//         key={node.id}
//         onClick={handleClick}
//         text={node.name}
//       />
//     )
//   }

//   return (
//     <>
//       <ForceGraph2D
//         ref={fgRef}
//         graphData={filteredNodes.length ? { nodes: filteredNodes, links: [] } : data}
//         height={height}
//         width={width - 100}
//         cooldownTicks={100}
//         nodeAutoColorBy='id'
//         linkDirectionalParticles='value'
//         linkCurvature='curvature'
//         onEngineStop={() => fgRef.current.zoomToFit(400)}
//       />
//       <>
//         <div className='fixed top-4 left-24 flex h-12 flex-row items-center justify-center'>
//           <Search />
//           {/* <FormGroup labelFor='text-input'>
//             <Suggest2
//               inputValueRenderer={(node) => node.name}
//               items={filteredNodes}
//               itemRenderer={renderNode}
//               noResults={<MenuItem disabled={true} text='No results.' />}
//               onItemSelect={handleNodeSelect}
//               onQueryChange={handleQueryChange}
//               query={query}
//               resetOnSelect={true}
//             ></Suggest2>
//           </FormGroup> */}
//         </div>
//       </>
//     </>
//   )
// }

export default ForceGraph
