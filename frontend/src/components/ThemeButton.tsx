import React from 'react'
import { Icon } from '@blueprintjs/core'
import useDarkMode from '../hooks/useDarkMode'

export const ThemeButton = () => {
  const [darkTheme, setDarkTheme] = useDarkMode()
  const handleMode = () => setDarkTheme(!darkTheme)
  return (
    <span onClick={handleMode}>
      {darkTheme ? (
        <Icon icon='flash' size={28} className='fill-secondary-l' />
      ) : (
        <Icon icon='moon' size={28} />
      )}
    </span>
  )
}

export default ThemeButton
