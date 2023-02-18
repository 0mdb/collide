import React, { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { Icon } from '@blueprintjs/core'
import { getSearchResults } from '../../api/graph'
import { Combobox } from '@headlessui/react'

function classNames(...classes) {
  return classes.filter(Boolean).join(' ')
}

const CheckIcon = () => (
  <Icon icon='small-tick' iconSize={16} className='h-5 w-5' aria-hidden='true' />
)

function SearchForm(props) {
  const MagnifyingGlassIcon = () => (
    <Icon icon='search' size={20} className='mx-2 dark:fill-muted dark:shadow-lg' />
  )
  const [searchInput, setSearchInput] = useState('')

  const { data: searchResults = [], isLoading } = useQuery(
    ['searchResults', searchInput],
    async () => {
      if (searchInput) {
        const results = await getSearchResults(searchInput)
        return results
      }
      return []
    },
  )

  return (
    <Combobox onChange={props.setSelected} className='flex w-full md:ml-0' as='div'>
      <label htmlFor='search-field' className='sr-only'>
        Search
      </label>
      <div className='relative w-full text-gray-400 focus-within:text-gray-600'>
        <div className='pointer-events-none absolute inset-y-0 left-0 flex items-center'>
          <MagnifyingGlassIcon className='h-5 w-5' aria-hidden='true' />
        </div>
        <Combobox.Input
          id='search-field'
          className='block h-full w-full border-transparent py-2 pl-8 pr-3 text-gray-900 placeholder-gray-500 focus:border-transparent focus:placeholder-gray-400 focus:outline-none focus:ring-0 sm:text-sm'
          placeholder='Search'
          name='search'
          value={searchInput}
          onChange={(event) => {
            setSearchInput(event.target.value)
          }}
          onClick={() => {
            setSearchInput('')
          }}
        />
      </div>
      <Combobox.Options className='mt-2 py-2 px-4 bg-white rounded-md shadow-md'>
        {searchResults.map((result) => (
          <Combobox.Option
            key={result.label}
            value={result.value}
            className={({ active }) =>
              classNames(
                'relative cursor-default select-none py-2 pl-3 pr-9',
                active ? 'bg-indigo-600 text-white' : 'text-gray-900',
              )
            }
          >
            {({ active, selected }) => (
              <>
                <div className='flex items-center'>
                  <span
                    className={classNames(
                      'inline-block h-2 w-2 flex-shrink-0 rounded-full',
                      result.value ? 'bg-green-400' : 'bg-gray-200',
                    )}
                    aria-hidden='true'
                  />
                  <span className={classNames('ml-3 truncate', selected && 'font-semibold')}>
                    {result.label}

                    <span className='sr-only'> is {result.value ? 'online' : 'offline'}</span>
                  </span>
                </div>

                {selected && (
                  <span
                    className={classNames(
                      'absolute inset-y-0 right-0 flex items-center pr-4',
                      active ? 'text-white' : 'text-indigo-600',
                    )}
                  >
                    <CheckIcon />
                  </span>
                )}
              </>
            )}
          </Combobox.Option>
        ))}
      </Combobox.Options>
    </Combobox>
  )
}

export default SearchForm
