import React, { useState } from 'react'

export default function useGraphType() {
  const [graphType, setGraphType] = useState('2D')
  const changeGraphType = () => {
    if (graphType === '2D') {
      setGraphType('3D')
    } else {
      setGraphType('2D')
    }
  }
  return { graphType, changeGraphType }
}
