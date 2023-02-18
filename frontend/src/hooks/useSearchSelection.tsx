//function that keeps track of the state of the search bar selection. it returns seletedSearch and setSelectedSearch
import React, { useState } from 'react'

function useSearchSelection() {
  const [selectedSearch, setSelectedSearch] = useState('')
  console.log('selected search set to ', selectedSearch)
  return [selectedSearch, setSelectedSearch]
}

export default useSearchSelection
