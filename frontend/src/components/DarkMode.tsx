import React from 'react'
import { Classes } from '@blueprintjs/core'
import { MenuItem2 } from '@blueprintjs/popover2'
import '@blueprintjs/core/lib/css/blueprint.css'
import 'normalize.css'

function DarkMode() {
  const { body } = document
  const darkTheme = 'dark'
  const lightTheme = 'light'
  let theme
  let icon
  let text

  if (localStorage) {
    theme = localStorage.getItem('theme')
  }

  if (theme === lightTheme) {
    body.classList.remove(Classes.DARK)
    localStorage.setItem('theme', 'light')
    text = 'Dark theme'
    icon = 'moon'
  } else {
    body.classList.add(Classes.DARK)
    localStorage.setItem('theme', 'dark')
    text = 'Light theme'
    icon = 'flash'
  }

  const switchTheme = (e) => {
    if (theme === darkTheme) {
      e.target.classList.remove(Classes.DARK)
      localStorage.setItem('theme', 'light')
      text = 'Light theme'
      icon = 'flash'
    } else {
      e.target.classList.add(Classes.DARK)
      localStorage.setItem('theme', 'dark')
      text = 'Dark theme'
      icon = 'moon'
    }
  }

  return <MenuItem2 onClick={(e) => switchTheme(e)} text={text} icon={icon} />
}

export default DarkMode
