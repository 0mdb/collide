import React, { useState } from 'react'
import ForceGraph from '../../components/ForceGraph'
import SideBar from '../../components/SideBar'
import Loading from '../../components/Loading'

import { useQuery } from '@tanstack/react-query'
import { getOptions } from '../../api/graph'
import AsyncSelect from 'react-select/async'
import axios from '../../api/axios'
import { getTabbedFormTabFullPath } from 'react-admin'

function Search() {
  const SEARCH_URL = 'forcegraph/search_options?query='
  // const selectQuery = useQuery({
  //   queryKey: ['options', 'search'],
  //   queryFn: getOptions,
  // })

  // if (selectQuery.status === 'loading') return <Loading />
  // if (selectQuery.error === 'error') return <div>Error</div>

  // TODO disable default behaviour of react-select
  const getOptions = (query: string) => {
    const match_name = query.toLowerCase().split(' ').join('')
    return axios.post(SEARCH_URL + match_name).then((res) => res.data)
  }

  const handleChange = (selectedOption: string) => {
    console.log(`handleChange`, selectedOption)
  }

  const loadOptions = (inputValue: string, callback) => {
    console.log('options', inputValue)

    getOptions(inputValue).then((options) => {
      const filteredOptions = options.filter((option) =>
        option.label.toLowerCase().includes(inputValue.toLowerCase()),
      )
      console.log('loadOptions', inputValue, filteredOptions)
      callback(filteredOptions)
    })
  }

  return <AsyncSelect loadOptions={loadOptions} onChange={handleChange} />
}

function Home() {
  return (
    <div className='flex h-12 flex-row items-center justify-center'>
      <Search />
      {/* <SideBar /> */}
      {/* <ForceGraph /> */}
    </div>
  )
}

export default Home
