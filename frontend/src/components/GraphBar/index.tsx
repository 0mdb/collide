import React, { useState } from 'react'
import { Icon } from '@blueprintjs/core'

const level = ['Federal', 'Provincial', 'Municipal']
const plots = ['Force', 'Sankey']
const random = ['Thing1', 'Thing2']

const GraphBar = () => {
  return (
    <div className='channel-bar shadow-lg'>
      <ChannelBlock />
      <div className='channel-container'>
        <Dropdown header='Government' selections={level} />
        <Dropdown header='Plots' selections={plots} />
        <Dropdown header='Random' selections={random} />
      </div>
    </div>
  )
}

const Dropdown = ({ header, selections }) => {
  const [expanded, setExpanded] = useState(true)

  return (
    <div className='dropdown'>
      <div onClick={() => setExpanded(!expanded)} className='dropdown-header'>
        <ChevronIcon expanded={expanded} />
        <h5 className={expanded ? 'dropdown-header-text-selected' : 'dropdown-header-text'}>
          {header}
        </h5>
        <Icon icon='plus' size={12} className='text-accent my-auto ml-auto text-opacity-80' />
      </div>
      {expanded &&
        selections &&
        selections.map((selection) => <TopicSelection selection={selection} />)}
    </div>
  )
}

const ChevronIcon = ({ expanded }) => {
  const chevClass = 'text-accent text-opacity-80 my-auto mr-1'
  return expanded ? (
    <Icon icon='chevron-down' className={chevClass} />
  ) : (
    <Icon icon='chevron-right' size={14} className={chevClass} />
  )
}

const TopicSelection = ({ selection }) => (
  <div className='dropdown-selection'>
    <Icon icon='grid' size={24} className='text-gray-400' />
    <h5 className='dropdown-selection-text'>{selection}</h5>
  </div>
)

const ChannelBlock = () => (
  <div className='channel-block'>
    <h5 className='channel-block-text'>Discover</h5>
  </div>
)

export default GraphBar
