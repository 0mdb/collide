import { Spinner } from '@blueprintjs/core'

import React from 'react'

function Loading() {
  return (
    <div className='grid min-h-screen'>
      <div className='flex items-center gap-2 text-gray-500'>
        <span className='block h-16 w-16 animate-spin rounded-full border-4 border-t-primary'></span>
      </div>
    </div>
  )
}

export default Loading
