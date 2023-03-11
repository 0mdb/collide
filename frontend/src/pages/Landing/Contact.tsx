import { useState } from 'react'
import { ChevronDownIcon } from '@heroicons/react/20/solid'
import { Switch } from '@headlessui/react'
import { Link } from 'react-router-dom'

import React from 'react'

function classNames(...classes) {
  return classes.filter(Boolean).join(' ')
}

function ContactLanding() {
  const [agreed, setAgreed] = useState(false)

  return (
    <div className='isolate bg-secondary-l dark:bg-secondary text-secondary-l-text dark:text-secondary-text py-16 px-6 sm:py-24 lg:px-8'>
      <div className='mx-auto max-w-2xl text-center'>
        <h2 className='text-3xl font-bold tracking-tight sm:text-4xl'>Contact us</h2>
        <p className='mt-2 text-lg leading-8 text-gray-600 dark:text-gray-200'>
          We're here to help. Send us a message and we'll respond as soon as possible.
        </p>
      </div>
      <form action='#' method='POST' className='mx-auto mt-16 max-w-xl sm:mt-10'>
        <div className='grid grid-cols-1 gap-y-6 gap-x-8 sm:grid-cols-2'>
          <div>
            <label
              htmlFor='first-name'
              className='block text-sm font-semibold leading-6'
            >
              First name
            </label>
            <div className='mt-2.5'>
              <input
                type='text'
                name='first-name'
                id='first-name'
                autoComplete='given-name'
                className='block w-full rounded-md
                border border-secondary dark:border-secondary-d
                text-secondary-l-text dark:text-secondary-l-text
                py-2 px-3.5 placeholder-secondary shadow-sm text-sm leading-6
                ring-1 ring-inset ring-gray-300
                focus:border-primary focus:outline-none focus:ring-primary'
              />
            </div>
          </div>
          <div>
            <label
              htmlFor='last-name'
              className='block text-sm font-semibold leading-6'
            >
              Last name
            </label>
            <div className='mt-2.5'>
              <input
                type='text'
                name='last-name'
                id='last-name'
                autoComplete='family-name'
                className='block w-full rounded-md
                border border-secondary dark:border-secondary-d
                text-secondary-l-text dark:text-secondary-l-text
                py-2 px-3.5 placeholder-secondary shadow-sm text-sm leading-6
                ring-1 ring-inset ring-gray-300
                focus:border-primary focus:outline-none focus:ring-primary'
              />
            </div>
          </div>
          <div className='sm:col-span-2'>
            <label
              htmlFor='company'
              className='block text-sm font-semibold leading-6'
            >
              Company
            </label>
            <div className='mt-2.5'>
              <input
                type='text'
                name='company'
                id='company'
                autoComplete='organization'
                className='block w-full rounded-md
                border border-secondary dark:border-secondary-d
                text-secondary-l-text dark:text-secondary-l-text
                py-2 px-3.5 placeholder-secondary shadow-sm text-sm leading-6
                ring-1 ring-inset ring-gray-300
                focus:border-primary focus:outline-none focus:ring-primary'
              />
            </div>
          </div>
          <div className='sm:col-span-2'>
            <label htmlFor='email' className='block text-sm font-semibold leading-6'>
              Email
            </label>
            <div className='mt-2.5'>
              <input
                type='email'
                name='email'
                id='email'
                autoComplete='email'
                className='block w-full rounded-md
                border border-secondary dark:border-secondary-d
                text-secondary-l-text dark:text-secondary-l-text
                py-2 px-3.5 placeholder-secondary shadow-sm text-sm leading-6
                ring-1 ring-inset ring-gray-300
                focus:border-primary focus:outline-none focus:ring-primary'
              />
            </div>
          </div>
          <div className='sm:col-span-2'>
            <label
              htmlFor='phone-number'
              className='block text-sm font-semibold leading-6'
            >
              Phone number
            </label>
            <div className='relative mt-2.5'>
              <div className='absolute inset-y-0 left-0 flex items-center'>
                <label htmlFor='country' className='sr-only'>
                  Country
                </label>
                <select
                  id='country'
                  name='country'
                  className='h-full rounded-md border-0 bg-transparent bg-none py-0 pl-4 pr-9 text-sm text-gray-400 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-indigo-600'
                >
                  <option>US</option>
                  <option>CA</option>
                  <option>EU</option>
                </select>
                <ChevronDownIcon
                  className='pointer-events-none absolute top-0 right-3 h-full w-5 text-gray-400'
                  aria-hidden='true'
                />
              </div>
              <input
                type='tel'
                name='phone-number'
                id='phone-number'
                autoComplete='tel'
                className='block w-full rounded-md pl-20
                border border-secondary dark:border-secondary-d
                text-secondary-l-text dark:text-secondary-l-text
                py-2 px-3.5 placeholder-secondary shadow-sm text-sm leading-6
                ring-1 ring-inset ring-gray-300
                focus:border-primary focus:outline-none focus:ring-primary'
              />
            </div>
          </div>
          <div className='sm:col-span-2'>
            <label
              htmlFor='message'
              className='block text-sm font-semibold leading-6'
            >
              Message
            </label>
            <div className='mt-2.5'>
              <textarea
                name='message'
                id='message'
                rows={4}
                className='block w-full rounded-md
                border border-secondary dark:border-secondary-d
                text-secondary-l-text dark:text-secondary-l-text
                py-2 px-3.5 placeholder-secondary shadow-sm text-sm leading-6
                ring-1 ring-inset ring-gray-300
                focus:border-primary focus:outline-none focus:ring-primary'
                defaultValue={''}
              />
            </div>
          </div>
          <Switch.Group as='div' className='flex gap-x-4 sm:col-span-2'>
            <div className='flex h-6 items-center'>
              <Switch
                checked={agreed}
                onChange={setAgreed}
                className={classNames(
                  agreed ? 'bg-indigo-600' : 'bg-gray-200',
                  'flex w-8 flex-none cursor-pointer rounded-full p-px ring-1 ring-inset ring-gray-900/5 transition-colors duration-200 ease-in-out focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600',
                )}
              >
                <span className='sr-only'>Agree to policies</span>
                <span
                  aria-hidden='true'
                  className={classNames(
                    agreed ? 'translate-x-3.5' : 'translate-x-0',
                    'h-4 w-4 transform rounded-full bg-white shadow-sm ring-1 ring-gray-900/5 transition duration-200 ease-in-out',
                  )}
                />
              </Switch>
            </div>
            <Switch.Label className='text-sm leading-6 text-secondary-l-text-accent dark:text-secondary-text-accent'>
              By selecting this, you agree to our{' '}
              <Link to='/privacypolicy' className='font-semibold'>
                privacy&nbsp;policy
              </Link>
              .
            </Switch.Label>
          </Switch.Group>
        </div>
        <div className='mt-10'>
          <button
            type='submit'
            className='block w-full rounded-md
            border border-primary
            bg-primary
            px-3.5 py-2.5 text-center text-sm
            font-medium text-secondary-d-text
            shadow-sm
            hover:border-primary-d hover:bg-primary-d hover:text-secondary-d-text hover:shadow-md
            dark:border-primary-d dark:bg-primary-d dark:text-secondary-d-text
            dark:hover:border-primary dark:hover:bg-primary
            focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2'
          >
            Let's talk
          </button>
        </div>
      </form>
    </div>
  )
}

function Contact() {
  return (
    <div>
      <ContactLanding />
    </div>
  )
}

export default Contact
