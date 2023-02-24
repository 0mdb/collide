import React from 'react'
import Footer from './Footer'
import Navbar from './Nav'
import { PrivacyLicense } from '../../assets/license_privacy.tsx'

/*
  This example requires some changes to your config:
  
  ```
  // tailwind.config.js
  module.exports = {
    // ...
    plugins: [
      // ...
      require('@tailwindcss/typography'),
    ],
  }
  ```
*/
function PrivacyPolicyLayout() {
  return (
    <div className='relative overflow-hidden bg-white dark:bg-secondary py-16'>
      <div className='hidden lg:absolute lg:inset-y-0 lg:block lg:h-full lg:w-full lg:[overflow-anchor:none]'>
        <div className='relative mx-auto h-full max-w-prose text-lg' aria-hidden='true'>
          <svg
            className='absolute top-12 left-full translate-x-32 transform'
            width={404}
            height={384}
            fill='none'
            viewBox='0 0 404 384'
          >
            <defs>
              <pattern
                id='74b3fd99-0a6f-4271-bef2-e80eeafdf357'
                x={0}
                y={0}
                width={20}
                height={20}
                patternUnits='userSpaceOnUse'
              >
                <rect
                  x={0}
                  y={0}
                  width={4}
                  height={4}
                  className='text-secondary-l'
                  fill='currentColor'
                />
              </pattern>
            </defs>
            <rect width={404} height={384} fill='url(#74b3fd99-0a6f-4271-bef2-e80eeafdf357)' />
          </svg>
          <svg
            className='absolute top-1/2 right-full -translate-y-1/2 -translate-x-32 transform'
            width={404}
            height={384}
            fill='none'
            viewBox='0 0 404 384'
          >
            <defs>
              <pattern
                id='f210dbf6-a58d-4871-961e-36d5016a0f49'
                x={0}
                y={0}
                width={20}
                height={20}
                patternUnits='userSpaceOnUse'
              >
                <rect
                  x={0}
                  y={0}
                  width={4}
                  height={4}
                  className='text-secondary-l'
                  fill='currentColor'
                />
              </pattern>
            </defs>
            <rect width={404} height={384} fill='url(#f210dbf6-a58d-4871-961e-36d5016a0f49)' />
          </svg>
          <svg
            className='absolute bottom-12 left-full translate-x-32 transform'
            width={404}
            height={384}
            fill='none'
            viewBox='0 0 404 384'
          >
            <defs>
              <pattern
                id='d3eb07ae-5182-43e6-857d-35c643af9034'
                x={0}
                y={0}
                width={20}
                height={20}
                patternUnits='userSpaceOnUse'
              >
                <rect
                  x={0}
                  y={0}
                  width={4}
                  height={4}
                  className='text-secondary-l'
                  fill='currentColor'
                />
              </pattern>
            </defs>
            <rect width={404} height={384} fill='url(#d3eb07ae-5182-43e6-857d-35c643af9034)' />
          </svg>
        </div>
      </div>
      <div className='relative px-6 lg:px-8'>
        <div className='prose prose-lg prose-indigo mx-auto mt-6 text-secondary-l-text dark:text-secondary-text'>
          <PrivacyLicense />
        </div>
      </div>
    </div>
  )
}

function PrivacyPolicy() {
  return (
    <div>
      <Navbar />
      <PrivacyPolicyLayout />
      <Footer />
    </div>
  )
}

export default PrivacyPolicy
