import React, { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { Icon } from '@blueprintjs/core'
import { getSearchResults } from '../../api/graph'
import { Dialog, Combobox } from '@headlessui/react'
import { useDebounce } from 'use-debounce'

function classNames(...classes) {
  return classes.filter(Boolean).join(' ')
}

const CheckIcon = () => (
  <Icon icon='small-tick' iconSize={16} className='h-5 w-5 fill-muted' aria-hidden='true' />
)

const ChevronIcon = () => (
  <Icon icon='expand-all' iconSize={16} className='h-5 w-5 fill-muted' aria-hidden='true' />
)

const MagnifyingGlassIcon = () => <Icon icon='search' size={20} className='mx-2 fill-muted' />

function SearchForm(props) {
  const [searchInput, setSearchInput] = useState('')
  const [debouncedSearchInput] = useDebounce(searchInput, 500)
  const [isOpen, setIsOpen] = useState(true)

  const { data: searchResults = [], isLoading } = useQuery(
    ['searchResults', debouncedSearchInput],
    async () => {
      if (debouncedSearchInput) {
        const results = await getSearchResults(debouncedSearchInput)
        return results
      }
      return []
    },
  )

  const handleSelect = async (selectedOption) => {
    {
      console.log(selectedOption)
      props.setSelected(selectedOption)
      setSearchInput('')
    }
    console.log('selected Search is :', props.selected)
  }

  /* const filteredPeople =
   *   searchInput === ''
   *     ? people
   *     : people.filter((person) => {
   *         return person.toLowerCase().includes(searchInput.toLowerCase())
   *       })
   */
  return (
    <Combobox onChange={handleSelect} className='flex w-full md:ml-0' as='div'>
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
          autoFocus={true}
          autoComplete='off'
          onChange={(event) => {
            setSearchInput(event.target.value)
          }}
        />
        <Combobox.Button className='absolute inset-y-0 right-0 flex items-center pr-2 rounded-r-md px-2 focus:outline-none text-gray-400 hover:text-gray-500'>
          <ChevronIcon className='h-5 w-5' aria-hidden='true' />
        </Combobox.Button>
      </div>
      <Combobox.Options className='absolute z-10 mt-1 max-h-60 w-full overflow-auto rounded-md py-1 text-baase shadow-lg ring-1 dark:ring-primary ring-muted  ring-opaacity-5 focus:outline-none sm:text-sm px-4 bg-white rounded-md'>
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
                <span className={classNames('block truncate', selected && 'font-semibold')}>
                  {result.label}
                </span>

                {selected && (
                  <span
                    className={classNames(
                      'absolute inset-y-0 right-0 flex items-center pr-4',
                      active ? 'text-white' : 'text-indigo-600',
                    )}
                  >
                    <CheckIcon className='h-5 w-5' aria-hidden='true' />
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
