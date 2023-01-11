import React, { useRef } from 'react'
import { ForceGraph2D } from 'react-force-graph'
import { useQuery } from '@tanstack/react-query'
import { getGraph } from '../../api/graph'
import Loading from '../Loading'
import { useWindowSize } from '@react-hook/window-size'
import { Icon, FormGroup, InputGroup, MenuItem } from '@blueprintjs/core'
import { Suggest2 } from '@blueprintjs/select'

// searchbar for nodes in myData that uses Suggest2 for names and stores filtered results in state
function SearchBar() {
  const [filteredNodes, setFilteredNodes] = React.useState([])
  const [query, setQuery] = React.useState('')
  const [selected, setSelected] = React.useState(null)
  const [node, setNode] = React.useState(null)

  const { status, error, data } = useQuery({
    queryKey: ['forcegraph'],
    queryFn: getGraph,
  })

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
        active={modifiers.active}
        disabled={modifiers.disabled}
        key={node.id}
        onClick={handleClick}
        text={node.name}
      />
    )
  }

  return (
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
      >
        <InputGroup
          Icon='search'
          type='search'
          className='bottom-bar-input'
          placeholder='Search for nodes...'
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />
      </Suggest2>
    </FormGroup>
  )
}

const SearchIcon = () => (
  <Icon icon='search' size={22} className='dark:text-primary mx-2 text-green-500 dark:shadow-lg' />
)

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
    <>
      <ForceGraph2D
        ref={fgRef}
        graphData={data}
        height={height}
        width={width - height / 3}
        cooldownTicks={100}
        nodeAutoColorBy='id'
        linkDirectionalParticles='value'
        linkCurvature='curvature'
        onEngineStop={() => fgRef.current.zoomToFit(400)}
      />
      <div className='flex'>
        {/* <SearchBar /> */}
        <div className='bottom-bar'>
          <SearchIcon />
          <input type='search' placeholder='Search...' className='bottom-bar-input' />
        </div>
      </div>
    </>
  )
}

export default ForceGraph
