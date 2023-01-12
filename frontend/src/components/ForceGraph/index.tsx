import React, { useRef, useState } from 'react'
import { ForceGraph2D } from 'react-force-graph'
import { useQuery } from '@tanstack/react-query'
import { getGraph } from '../../api/graph'
import Loading from '../Loading'
import { useWindowSize } from '@react-hook/window-size'
import { Icon, FormGroup, InputGroup, MenuItem } from '@blueprintjs/core'
import { Suggest2 } from '@blueprintjs/select'

const SearchIcon = () => (
  <Icon icon='search' size={28} className='dark:text-primary mx-2 text-green-500 dark:shadow-lg' />
)

function ForceGraph() {
  const fgRef = useRef()
  const [width, height] = useWindowSize()
  const [filteredNodes, setFilteredNodes] = useState([])
  const [query, setQuery] = useState('')
  const [selected, setSelected] = useState(null)
  const [node, setNode] = useState(null)
  const { status, error, data } = useQuery({
    queryKey: ['forcegraph'],
    queryFn: getGraph,
  })

  if (status === 'loading') return <Loading />
  if (error === 'error') return <div>Error</div>

  const handleQueryChange = (query) => {
    setQuery(query)
    setFilteredNodes(
      data.nodes.filter((node) => node.name.toLowerCase().includes(query.toLowerCase())),
    )
  }

  const handleNodeSelect = (node) => {
    setNode(node)
    setQuery('')
  }

  const renderNode = (node, { handleClick, modifiers }) => {
    if (!modifiers.matchesPredicate) {
      return null
    }
    return (
      <MenuItem
        className='text-gray-500 
         dark:text-gray-400
        '
        active={modifiers.active}
        disabled={modifiers.disabled}
        key={node.id}
        onClick={handleClick}
        text={node.name}
      />
    )
  }

  return (
    <>
      <ForceGraph2D
        ref={fgRef}
        graphData={filteredNodes.length ? { nodes: filteredNodes, links: [] } : data}
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
          <FormGroup labelFor='text-input'>
            <Suggest2
              inputValueRenderer={(node) => node.name}
              items={filteredNodes}
              itemRenderer={renderNode}
              noResults={<MenuItem disabled={true} text='No results.' />}
              onItemSelect={handleNodeSelect}
              onQueryChange={handleQueryChange}
              query={query}
              resetOnSelect={true}
            ></Suggest2>
          </FormGroup>
        </div>
      </>
    </>
  )
}

export default ForceGraph
