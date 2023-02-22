import React from 'react'
import { Link } from 'react-router-dom'

export default function CallToAction() {
  return (
    <div className='bg-white'>
      <div className='mx-auto max-w-7xl py-24 px-6 sm:py-32 lg:px-8'>
        <h2 className='text-4xl font-bold tracking-tight text-gray-900'>
          Explore the power of lobbying data analytics.
          <br />
          Start tracking today with LobbyRadar.
        </h2>
        <div className='mt-10 flex items-center gap-x-6'>
          <Link to='/home'>
            <a
              href='#'
              className='rounded-md bg-primary dark:bg-primary-d px-3.5 py-1.5 text-base font-semibold leading-7 text-morp shadow-sm hover:bg-primary-l dark:hover:bg-primary focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-primary'
            >
              Get started
            </a>
          </Link>
          <>
            <Link to='/faq'>
              <a href='#' className='text-base font-semibold leading-7 text-gray-900'>
                Learn more <span aria-hidden='true'>→</span>
              </a>
            </Link>
          </>
        </div>
      </div>
    </div>
  )
}
