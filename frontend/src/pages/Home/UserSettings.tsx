import React from 'react'

import useAuth from '../../hooks/useAuth'
/* import useCurrentUser from '../../hooks/useCurrentUser' */
import DarkModeSwitch from '../../components/DarkModeSwitch'
import { Switch } from '@headlessui/react'
import { ChevronLeftIcon } from '@heroicons/react/20/solid'
import useDarkMode from '../../hooks/useDarkMode'
import useCurrentUser from '../../hooks/useCurrentUser'

function classNames(...classes) {
  return classes.filter(Boolean).join(' ')
}

export default function UserSettings() {
  const [darkMode] = useDarkMode()
  const { user, auth } = useAuth()
  const { currentUser } = useCurrentUser()

  const handleSubmit = (e) => {
    e.preventDefault()

    const org = e.target.elements.organization.value
    const province = e.target.elements.province.value
    const country = e.target.elements.country.value
    const language = e.target.elements.language.value

    const data = {
      org: org,
      darkmode: darkMode,
      country: country,
      province: province,
      language: language,
    }

    // TODO replace with update user
    const darkModeData = {
      id: user.id,
      email: user.email,
      is_superuser: user.is_superuser,

      darkmode: darkMode,
    }
    console.log(darkModeData)
    console.log('user', user)
    console.log('auth', auth)
    console.log('currentuser', currentUser)

    /* updateCurrentUser(darkModeData) */
  }

  return (
    <>
      <div className='flex h-full bg-secondary-l dark:bg-secondary text-secondary-l-text dark:text-secondary-text'>
        <main className='flex flex-1 overflow-hidden'>
          <div className='flex flex-1 flex-col overflow-y-auto xl:overflow-hidden'>
            {/* Breadcrumb */}
            <nav
              aria-label='Breadcrumb'
              className='border-b border-blue-gray-200 bg-secondary-l dark:bg-secondary xl:hidden'
            >
              <div className='mx-auto flex max-w-3xl items-start py-3 px-4 sm:px-6 lg:px-8'>
                <a
                  href='/home'
                  className='-ml-1 inline-flex items-center space-x-3 text-sm font-medium text-blue-gray-900'
                >
                  <ChevronLeftIcon className='h-5 w-5 text-blue-gray-400' aria-hidden='true' />
                  <span>Back</span>
                </a>
              </div>
            </nav>

            <div className='flex flex-1 xl:overflow-hidden'>
              {/* Main content */}
              <div className='flex-1 xl:overflow-y-auto'>
                <div className='mx-auto max-w-3xl py-10 px-4 sm:px-6 lg:py-12 lg:px-8'>
                  <h1 className='divide-y divide-secondary-l-text dark:divide-secondary-text text-3xl font-bold tracking-tight'>Settings</h1>

                  <form
                    onSubmit={handleSubmit}
                    className='mt-6 space-y-8 '
                  >
                    <div className='grid grid-cols-1 gap-y-6 sm:grid-cols-6 sm:gap-x-6'>
                      <div className='sm:col-span-6'>
                        <h2 className='text-xl font-medium'>Profile</h2>
                        <p className='mt-1 text-sm text-gray-600 dark:text-gray-200'>
                          Adjust your profile settings.
                        </p>
                      </div>

                      <div className='sm:col-span-3'>
                        <label
                          htmlFor='organization'
                          className='block text-sm font-medium'
                        >
                          Company
                        </label>
                        <input
                          type='text'
                          name='organization'
                          id='organization'
                          value={user ? user?.org : 'You need to login to see your email address'}
                          autoComplete='organization'
                          className='block w-full rounded-md
                           border border-secondary dark:border-secondary-d
                           text-secondary-l-text dark:text-secondary-l-text
                           shadow-sm
                           focus:border-primary focus:outline-none focus:ring-primary
                           sm:text-sm'
                        />
                      </div>

                      <div className='sm:col-span-3'></div>

                      <div className='sm:col-span-3'>
                        <label
                          htmlFor='province'
                          className='block text-sm font-medium'
                        >
                          Province
                        </label>
                        <select
                          id='province'
                          name='province'
                          autoComplete='address-level11'
                          className='mt-1 block w-full rounded-md
                          border border-secondary dark:border-secondary-d
                          text-secondary-l-text dark:text-secondary-l-text
                          shadow-sm
                          focus:border-primary focus:outline-none focus:ring-primary
                          sm:text-sm'
                        >
                          <option />
                          <option>United States</option>
                          <option>Canada</option>
                          <option>Mexico</option>
                        </select>
                      </div>
                      <div className='sm:col-span-3'>
                        <label
                          htmlFor='email-address'
                          className='block text-sm font-medium'
                        >
                          Email address
                        </label>
                        <input
                          type='text'
                          name='email-address'
                          value={
                            user?.email ? user.email : 'You need to login to see your email address'
                          }
                          id='email-address'
                          autoComplete='email'
                          className='mt-1 block w-full rounded-md
                          border border-secondary dark:border-secondary-d
                          text-secondary-l-text dark:text-secondary-l-text
                          shadow-sm
                          focus:border-primary focus:outline-none focus:ring-primary
                          sm:text-sm'
                        />
                      </div>

                      <div className='sm:col-span-3'>
                        <label
                          htmlFor='email-address'
                          className='block text-sm font-medium'
                        >
                          id
                        </label>
                        <input
                          type='text'
                          name='user-id'
                          value={user ? user.id : 'You need to login to see your email address'}
                          id='user-'
                          className='mt-1 block w-full rounded-md
                          border border-secondary dark:border-secondary-d
                          text-secondary-l-text dark:text-secondary-l-text
                          shadow-sm
                          focus:border-primary focus:outline-none focus:ring-primary
                          sm:text-sm'
                        />
                      </div>

                      <div className='sm:col-span-3'></div>

                      <div className='sm:col-span-3'>
                        <label
                          htmlFor='country'
                          className='block text-sm font-medium'
                        >
                          Country
                        </label>
                        <select
                          id='country'
                          name='country'
                          autoComplete='country-name'
                          className='mt-1 block w-full rounded-md
                          border border-secondary dark:border-secondary-d
                          text-secondary-l-text dark:text-secondary-l-text
                          shadow-sm
                          focus:border-primary focus:outline-none focus:ring-primary
                          sm:text-sm'
                        >
                          <option />
                          <option>United States</option>
                          <option>Canada</option>
                          <option>Mexico</option>
                        </select>
                      </div>

                      <div className='sm:col-span-3'>
                        <label
                          htmlFor='language'
                          className='block text-sm font-medium'
                        >
                          Language
                        </label>
                        <select
                          name='language'
                          autoComplete='language'
                          value='English'
                          id='language'
                          className='mt-1 block w-full rounded-md
                          border border-secondary dark:border-secondary-d
                          text-secondary-l-text dark:text-secondary-l-text
                          shadow-sm
                          focus:border-primary focus:outline-none focus:ring-primary
                          sm:text-sm'
                        >
                          <option />
                          <option>English</option>
                        </select>
                      </div>
                    </div>
                      <div>
                        <h2 className='text-lg font-medium leading-6'>Preferences</h2>
                        <p className='mt-1 text-sm text-gray-600 dark:text-gray-200'>
                          Select your preferences from the options below.
                        </p>
                      <ul role='list' className='mt-2 divide-y divide-secondary-l-text dark:divide-secondary-text'>
                        <Switch.Group as='li' className='flex items-center justify-between py-4'>
                          <div className='flex flex-col'>
                            <Switch.Label
                              as='p'
                              className='text-sm font-medium'
                              passive
                            >
                              Dark mode
                            </Switch.Label>
                            <Switch.Description className='text-sm text-gray-600 dark:text-gray-200'>
                              Save your eyes and energy by using the dark theme.
                            </Switch.Description>
                          </div>
                          <DarkModeSwitch>
                            <span
                              aria-hidden='true'
                              className={classNames(
                                darkMode ? 'translate-x-5' : 'translate-x-0',
                                'inline-block h-5 w-5 transform rounded-full bg-white shadow ring-0 transition duration-200 ease-in-out',
                              )}
                            />
                          </DarkModeSwitch>
                          {/* </Switch> */}
                        </Switch.Group>

                        <Switch.Group as='li' className='flex items-center justify-between py-4'>
                          <div className='flex flex-col'>
                            <Switch.Label
                              as='p'
                              className='text-sm font-medium'
                              passive
                            >
                              Is active
                            </Switch.Label>
                            <Switch.Description className='text-sm text-gray-600 dark:text-gray-200'>
                              Is active
                            </Switch.Description>
                          </div>
                          <Switch
                            checked={user?.is_active}
                            className={classNames(
                              user?.is_active ? 'bg-indigo-600' : 'bg-gray-200',
                              'relative ml-4 inline-flex h-6 w-11 flex-shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2',
                            )}
                          >
                            <span
                              aria-hidden='true'
                              className={classNames(
                                user?.is_active ? 'translate-x-5' : 'translate-x-0',
                                'inline-block h-5 w-5 transform rounded-full bg-white shadow ring-0 transition duration-200 ease-in-out',
                              )}
                            />
                          </Switch>
                        </Switch.Group>

                        <Switch.Group as='li' className='flex items-center justify-between py-4'>
                          <div className='flex flex-col'>
                            <Switch.Label
                              as='p'
                              className='text-sm font-medium'
                              passive
                            >
                              Is Super User
                            </Switch.Label>
                            <Switch.Description className='text-sm text-gray-600 dark:text-gray-200'>
                              Is Super User
                            </Switch.Description>
                          </div>
                          <Switch
                            checked={user?.is_superuser}
                            className={classNames(
                              user?.is_superuser ? 'bg-indigo-600' : 'bg-gray-200',
                              'relative ml-4 inline-flex h-6 w-11 flex-shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2',
                            )}
                          >
                            <span
                              aria-hidden='true'
                              className={classNames(
                                user?.is_superuser ? 'translate-x-5' : 'translate-x-0',
                                'inline-block h-5 w-5 transform rounded-full bg-white shadow ring-0 transition duration-200 ease-in-out',
                              )}
                            />
                          </Switch>
                        </Switch.Group>
                        <Switch.Group as='li' className='flex items-center justify-between py-4'>
                          <div className='flex flex-col'>
                            <Switch.Label
                              as='p'
                              className='text-sm font-medium'
                              passive
                            >
                              Is verified
                            </Switch.Label>
                            <Switch.Description className='text-sm text-gray-600 dark:text-gray-200'>
                              Is verified
                            </Switch.Description>
                          </div>
                          <Switch
                            checked={user?.is_verified}
                            className={classNames(
                              user?.is_verified ? 'bg-indigo-600' : 'bg-gray-200',
                              'relative ml-4 inline-flex h-6 w-11 flex-shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2',
                            )}
                          >
                            <span
                              aria-hidden='true'
                              className={classNames(
                                user?.is_verified ? 'translate-x-5' : 'translate-x-0',
                                'inline-block h-5 w-5 transform rounded-full bg-white shadow ring-0 transition duration-200 ease-in-out',
                              )}
                            />
                          </Switch>
                        </Switch.Group>
                      </ul>
                    </div>

                    <div className='flex justify-end pt-8'>
                      <button
                        type='button'
                        className='rounded-md
                        border border-secondary-l-accent dark:border-secondary-l-accent
                        bg-secondary-l-accent dark:bg-secondary-l-accent
                        py-2 px-4 text-sm
                        font-medium
                        text-secondary-text dark:text-secondary-text
                        shadow-sm
                        hover:border-secondary-l-accent-hov hover:bg-secondary-l-accent-hov
                        dark:hover:border-secondary-l-accent-hov dark:hover:bg-secondary-l-accent-hov
                        hover:text-secondary-text
                        hover:shadow-md
                        focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2'
                      >
                        Cancel
                      </button>
                      <button
                        type='submit'
                        className='ml-3 inline-flex justify-center rounded-md
                        border border-primary dark:border-primary
                        bg-primary dark:bg-primary
                        py-2 px-4 text-sm
                        font-medium
                        text-secondary-d-text dark:text-secondary-d-text
                        shadow-sm
                        hover:border-primary-d hover:bg-primary-d hover:text-secondary-d-text hover:shadow-md
                        dark:hover:border-primary-d dark:hover:bg-primary-d
                        focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2'
                      >
                        Save
                      </button>
                    </div>
                  </form>
                </div>
              </div>
            </div>
          </div>
        </main>
      </div>
    </>
  )
}
