import React from 'react'
import { useSettings } from '../../hooks'
import ThemeButton from '../../components/ThemeButton'

function UserSettings() {
  // const { t } = useTranslation()
  // const { settings, updateSettings } = useSettings()

  return (
    <div className='flex flex-col gap-4'>
      <div className='flex flex-col gap-2'>
        <h1>Settings</h1>
        <label className='text-sm font-semibold text-gray-500 dark:text-gray-400'>
          {/* {t('settings.language')} */}
          Language
        </label>
        <select
          className='block w-full appearance-none rounded-md border border-gray-300 bg-white px-4 py-2 text-sm text-gray-700 shadow-sm focus:border-primary focus:outline-none focus:ring-primary dark:border-gray-600 dark:bg-gray-800 dark:text-gray-300 dark:focus:border-primary dark:focus:ring-primary'
          // onChange={(e) => updateSettings({ language: e.target.value })}
        >
          <option value='en'>English</option>
          <option value='es'>French</option>
        </select>
      </div>
      <div className='flex flex-col gap-2'>
        <label className='text-sm font-semibold text-gray-500 dark:text-gray-400'>User theme</label>

        <ThemeButton />
        <select
          className='block w-full appearance-none rounded-md border border-gray-300 bg-white px-4 py-2 text-sm text-gray-700 shadow-sm focus:border-primary focus:outline-none focus:ring-primary dark:border-gray-600 dark:bg-gray-800 dark:text-gray-300 dark:focus:border-primary dark:focus:ring-primary'
          // value={settings.theme}
          // onChange={(e) => updateSettings({ theme: e.target.value })}
        >
          <option value='light'>Light</option>
          <option value='dark'>Dark</option>
        </select>
      </div>
      <div className='flex flex-col gap-2'>
        <label className='text-sm font-semibold text-gray-500 dark:text-gray-400'>Logout</label>
      </div>
    </div>
  )
}

export default UserSettings
