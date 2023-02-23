import React from 'react'

import { loginUser, getMe } from '../../api/authApi'
import { useMutation, useQuery } from '@tanstack/react-query'
import useAuth from '../../hooks/useAuth'
import DarkModeSwitch from '../../components/DarkModeSwitch'
import { useState } from 'react'
import { Switch } from '@headlessui/react'
import { ChevronLeftIcon } from '@heroicons/react/20/solid'

function classNames(...classes) {
  return classes.filter(Boolean).join(' ')
}

export default function UserSettings() {
  const [email, setEmail] = useState(true)
  const [preferDark, setPreferDark] = useState(false)
  const [privateAccount, setPrivateAccount] = useState(false)
  const [allowMentions, setAllowMentions] = useState(true)

  const [isActive, setIsActive] = useState(false)
  const [isVerified, setIsVerified] = useState(false)
  const [isSuperuser, setIsSuperuser] = useState(false)

  const { user, setUser } = useAuth()

  const {
    data: me,
    isLoading: meLoading,
    error: meError,
  } = useQuery({
    queryKey: 'me',
    queryFn: getMe,
    config: {
      enabled: !!user,
    },

    onSuccess: (data) => {
      console.log(data)
      setIsActive(data.is_active)
      setIsVerified(data.is_verified)
      setIsSuperuser(data.is_superuser)
    },
  })

  return (
    <>
      <div className='flex h-full'>
        <main className='flex flex-1 overflow-hidden'>
          <div className='flex flex-1 flex-col overflow-y-auto xl:overflow-hidden'>
            {/* Breadcrumb */}
            <nav
              aria-label='Breadcrumb'
              className='border-b border-blue-gray-200 bg-white xl:hidden'
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
                  <h1 className='text-3xl font-bold tracking-tight text-blue-gray-900'>Settings</h1>

                  <form className='divide-y-blue-gray-200 mt-6 space-y-8 divide-y'>
                    <div className='grid grid-cols-1 gap-y-6 sm:grid-cols-6 sm:gap-x-6'>
                      <div className='sm:col-span-6'>
                        <h2 className='text-xl font-medium text-blue-gray-900'>Profile</h2>
                        <p className='mt-1 text-sm text-blue-gray-500'>
                          This information will be displayed publicly so be careful what you share.
                        </p>
                      </div>

                      <div className='sm:col-span-3'>
                        <label
                          htmlFor='organization'
                          className='block text-sm font-medium text-blue-gray-900'
                        >
                          Company
                        </label>
                        <input
                          type='text'
                          name='organization'
                          id='organization'
                          autoComplete='organization'
                          className='mt-1 block w-full rounded-md border-blue-gray-300 text-blue-gray-900 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm'
                        />
                      </div>

                      <div className='sm:col-span-3'></div>
                      <div className='sm:col-span-3'>
                        <label
                          htmlFor='first-name'
                          className='block text-sm font-medium text-blue-gray-900'
                        >
                          First name
                        </label>
                        <input
                          type='text'
                          name='first-name'
                          id='first-name'
                          autoComplete='given-name'
                          className='mt-1 block w-full rounded-md border-blue-gray-300 text-blue-gray-900 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm'
                        />
                      </div>

                      <div className='sm:col-span-3'>
                        <label
                          htmlFor='last-name'
                          className='block text-sm font-medium text-blue-gray-900'
                        >
                          Last name
                        </label>
                        <input
                          type='text'
                          name='last-name'
                          id='last-name'
                          autoComplete='family-name'
                          className='mt-1 block w-full rounded-md border-blue-gray-300 text-blue-gray-900 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm'
                        />
                      </div>
                      <div className='sm:col-span-3'>
                        <label
                          htmlFor='email-address'
                          className='block text-sm font-medium text-blue-gray-900'
                        >
                          Email address
                        </label>
                        <input
                          type='text'
                          name='email-address'
                          value={
                            me?.email ? me.email : 'You need to login to see your email address'
                          }
                          id='email-address'
                          autoComplete='email'
                          className='mt-1 block w-full rounded-md border-blue-gray-300 text-blue-gray-900 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm'
                        />
                      </div>

                      <div className='sm:col-span-3'>
                        <label
                          htmlFor='phone-number'
                          className='block text-sm font-medium text-blue-gray-900'
                        >
                          Phone number
                        </label>
                        <input
                          type='text'
                          name='phone-number'
                          id='phone-number'
                          autoComplete='tel'
                          className='mt-1 block w-full rounded-md border-blue-gray-300 text-blue-gray-900 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm'
                        />
                      </div>

                      <div className='sm:col-span-3'>
                        <label
                          htmlFor='email-address'
                          className='block text-sm font-medium text-blue-gray-900'
                        >
                          id
                        </label>
                        <input
                          type='text'
                          name='user-id'
                          value={me ? me.id : 'You need to login to see your email address'}
                          id='user-'
                          className='mt-1 block w-full rounded-md border-blue-gray-300 text-blue-gray-900 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm'
                        />
                      </div>

                      <div className='sm:col-span-3'></div>

                      <div className='sm:col-span-3'>
                        <label
                          htmlFor='country'
                          className='block text-sm font-medium text-blue-gray-900'
                        >
                          Country
                        </label>
                        <select
                          id='country'
                          name='country'
                          autoComplete='country-name'
                          className='mt-1 block w-full rounded-md border-blue-gray-300 text-blue-gray-900 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm'
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
                          className='block text-sm font-medium text-blue-gray-900'
                        >
                          Language
                        </label>
                        <select
                          name='language'
                          autoComplete='language'
                          value='English'
                          id='language'
                          className='mt-1 block w-full rounded-md border-blue-gray-300 text-blue-gray-900 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm'
                        >
                          <option />
                          <option>English</option>
                        </select>
                      </div>
                    </div>
                    <div className='px-4 sm:px-6'>
                      <div>
                        <h2 className='text-lg font-medium leading-6 text-gray-900'>Preferences</h2>
                        <p className='mt-1 text-sm text-gray-500'>
                          Select your preferences from the options below.
                        </p>
                      </div>
                      <ul role='list' className='mt-2 divide-y divide-gray-200'>
                        <Switch.Group as='li' className='flex items-center justify-between py-4'>
                          <div className='flex flex-col'>
                            <Switch.Label
                              as='p'
                              className='text-sm font-medium text-gray-900'
                              passive
                            >
                              Dark mode
                            </Switch.Label>
                            <Switch.Description className='text-sm text-gray-500'>
                              Save your eyes and energy by using the dark theme.
                            </Switch.Description>
                          </div>
                          <DarkModeSwitch>
                            <span
                              aria-hidden='true'
                              className={classNames(
                                preferDark ? 'translate-x-5' : 'translate-x-0',
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
                              className='text-sm font-medium text-gray-900'
                              passive
                            >
                              Is active
                            </Switch.Label>
                            <Switch.Description className='text-sm text-gray-500'>
                              Is active
                            </Switch.Description>
                          </div>
                          <Switch
                            checked={isActive}
                            onChange={setIsActive}
                            className={classNames(
                              isActive ? 'bg-teal-500' : 'bg-gray-200',
                              'relative ml-4 inline-flex h-6 w-11 flex-shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out focus:outline-none focus:ring-2 focus:ring-sky-500 focus:ring-offset-2',
                            )}
                          >
                            <span
                              aria-hidden='true'
                              className={classNames(
                                isActive ? 'translate-x-5' : 'translate-x-0',
                                'inline-block h-5 w-5 transform rounded-full bg-white shadow ring-0 transition duration-200 ease-in-out',
                              )}
                            />
                          </Switch>
                        </Switch.Group>

                        <Switch.Group as='li' className='flex items-center justify-between py-4'>
                          <div className='flex flex-col'>
                            <Switch.Label
                              as='p'
                              className='text-sm font-medium text-gray-900'
                              passive
                            >
                              Is Super User
                            </Switch.Label>
                            <Switch.Description className='text-sm text-gray-500'>
                              Is Super User
                            </Switch.Description>
                          </div>
                          <Switch
                            checked={isSuperuser}
                            onChange={setIsSuperuser}
                            className={classNames(
                              isSuperuser ? 'bg-teal-500' : 'bg-gray-200',
                              'relative ml-4 inline-flex h-6 w-11 flex-shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out focus:outline-none focus:ring-2 focus:ring-sky-500 focus:ring-offset-2',
                            )}
                          >
                            <span
                              aria-hidden='true'
                              className={classNames(
                                isSuperuser ? 'translate-x-5' : 'translate-x-0',
                                'inline-block h-5 w-5 transform rounded-full bg-white shadow ring-0 transition duration-200 ease-in-out',
                              )}
                            />
                          </Switch>
                        </Switch.Group>
                        <Switch.Group as='li' className='flex items-center justify-between py-4'>
                          <div className='flex flex-col'>
                            <Switch.Label
                              as='p'
                              className='text-sm font-medium text-gray-900'
                              passive
                            >
                              Is verified
                            </Switch.Label>
                            <Switch.Description className='text-sm text-gray-500'>
                              Is verified
                            </Switch.Description>
                          </div>
                          <Switch
                            checked={isVerified}
                            onChange={setIsVerified}
                            className={classNames(
                              isVerified ? 'bg-teal-500' : 'bg-gray-200',
                              'relative ml-4 inline-flex h-6 w-11 flex-shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out focus:outline-none focus:ring-2 focus:ring-sky-500 focus:ring-offset-2',
                            )}
                          >
                            <span
                              aria-hidden='true'
                              className={classNames(
                                isVerified ? 'translate-x-5' : 'translate-x-0',
                                'inline-block h-5 w-5 transform rounded-full bg-white shadow ring-0 transition duration-200 ease-in-out',
                              )}
                            />
                          </Switch>
                        </Switch.Group>
                        <Switch.Group as='li' className='flex items-center justify-between py-4'>
                          <div className='flex flex-col'>
                            <Switch.Label
                              as='p'
                              className='text-sm font-medium text-gray-900'
                              passive
                            >
                              Automatic timezone
                            </Switch.Label>
                            <Switch.Description className='text-sm text-gray-500'>
                              Use your location to determine your timezone.
                            </Switch.Description>
                          </div>
                          <Switch
                            checked={allowMentions}
                            onChange={setAllowMentions}
                            className={classNames(
                              allowMentions ? 'bg-teal-500' : 'bg-gray-200',
                              'relative ml-4 inline-flex h-6 w-11 flex-shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out focus:outline-none focus:ring-2 focus:ring-sky-500 focus:ring-offset-2',
                            )}
                          >
                            <span
                              aria-hidden='true'
                              className={classNames(
                                allowMentions ? 'translate-x-5' : 'translate-x-0',
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
                        className='rounded-md border border-gray-300 bg-white py-2 px-4 text-sm font-medium text-blue-gray-900 shadow-sm hover:bg-blue-gray-50 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2'
                      >
                        Cancel
                      </button>
                      <button
                        type='submit'
                        className='ml-3 inline-flex justify-center rounded-md border border-transparent bg-blue-600 py-2 px-4 text-sm font-medium text-white shadow-sm hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2'
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
