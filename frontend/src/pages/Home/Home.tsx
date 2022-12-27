import React from 'react'
import { ForceGraph2D } from 'react-force-graph'
import { FormGroup, InputGroup, MenuItem } from '@blueprintjs/core'
import { Suggest2 } from '@blueprintjs/select'
import myData from './sample_graph4.json'

// searchbar for nodes in myData that uses Suggest2 for names and stores filtered results in state 
function SearchBar() {
  const [filteredNodes, setFilteredNodes] = React.useState([])
  const [query, setQuery] = React.useState('')
  const [selected, setSelected] = React.useState(null)
  const [node, setNode] = React.useState(null)

  const handleQueryChange = (query) => {
    setQuery(query)
    setFilteredNodes(
      myData.nodes.filter((node) => node.name.toLowerCase().includes(query.toLowerCase()))
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
      <FormGroup
        labelFor='text-input'
        className='searchbar'
      >
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
            leftIcon='search'
            type='search'
            placeholder='Search for nodes...'
            value={query}
            onChange={(e) => setQuery(e.target.value)}
          />
        </Suggest2>
      </FormGroup>
  )
}


function Home() {
  return (
    <div className='Home'>
      <SearchBar />
      <ForceGraph2D
        graphData={myData}
        nodeAutoColorBy='id'
        linkDirectionalParticles='value'
        linkCurvature='curvature'
        linkDirectionalParticles={1}
      />
    </div>
  )
}


export default Home
