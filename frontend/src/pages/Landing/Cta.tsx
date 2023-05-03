import React from 'react'
import { Link } from 'react-router-dom'
import { CtaPunchline1, CtaPunchline2, CtaButton, CtaLearnMore } from '../../assets/landing_strings.tsx'

export default function CallToAction() {
  return (
    <div className='bg-white dark:bg-secondary-l'>
      <div className='mx-auto max-w-7xl py-24 px-6 sm:py-32 lg:px-8'>
        <h2 className='text-4xl font-bold tracking-tight text-secondary-l-text'>
          <CtaPunchline1 />
          <br />
          <CtaPunchline2 />
        </h2>
        <div className='mt-10 flex items-center gap-x-6'>
          <>
            <Link to='/faq'>
              <div className='text-base font-semibold leading-7 text-secondary-d'>
                <CtaLearnMore /> <span aria-hidden='true'>→</span>
              </div>
            </Link>
          </>
        </div>
      </div>
    </div>
  )
}
