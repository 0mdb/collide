import React from 'react'
import { Icon } from '@blueprintjs/core'
import useDarkMode from '../hooks/useDarkMode'

import { Switch } from '@headlessui/react'

function classNames(...classes) {
  return classes.filter(Boolean).join(' ')
}

export default function DarkModeSwitch() {
  const [darkTheme, setDarkTheme] = useDarkMode()

  return (
    <Switch
      checked={darkTheme}
      onChange={setDarkTheme}
      className={classNames(
        darkTheme ? 'bg-indigo-600' : 'bg-gray-200',
        'relative inline-flex h-6 w-11 flex-shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2',
      )}
    >
      <span className='sr-only'>Use setting</span>
      <span
        className={classNames(
          darkTheme ? 'translate-x-5' : 'translate-x-0',
          'pointer-events-none relative inline-block h-5 w-5 transform rounded-full bg-white shadow ring-0 transition duration-200 ease-in-out',
        )}
      >
        <span
          className={classNames(
            darkTheme ? 'opacity-0 ease-out duration-100' : 'opacity-100 ease-in duration-200',
            'absolute inset-0 flex h-full w-full items-center justify-center transition-opacity',
          )}
          aria-hidden='true'
        >
          <Icon icon='moon' size={14} className="fill-none' text-gray-400" />
        </span>
        <span
          className={classNames(
            darkTheme ? 'opacity-100 ease-in duration-200' : 'opacity-0 ease-out duration-100',
            'absolute inset-0 flex h-full w-full items-center justify-center transition-opacity',
          )}
          aria-hidden='true'
        >
          <Icon icon='flash' size={14} className='fill-currentColor text-indigo-600' />
        </span>
      </span>
    </Switch>
  )
}
