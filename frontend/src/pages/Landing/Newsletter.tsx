import React from 'react'

const Newsletter = () => {
  return (
    <div className='w-full py-16 px-4'>
      <div className='mx-auto grid max-w-[1240px] lg:grid-cols-3'>
        <div className='my-4 lg:col-span-2'>
          <h1 className='py-2 text-2xl font-bold sm:text-3xl md:text-4xl'>
            Want tips & tricks to optimize your flow?
          </h1>
          <p>Sign up to our newsletter and stay up to date.</p>
        </div>
        <div className='my-4'>
          <div className='flex w-full flex-col items-center justify-between sm:flex-row'>
            <input
              // className='flex w-full rounded-md p-3 text-black'
              className='flex w-full rounded-md bg-gray-400 p-3 text-gray-500 dark:bg-gray-600 dark:text-gray-400'
              type='email'
              placeholder='Enter Email'
            />
            <button className='my-6 ml-4 w-[200px] rounded-md bg-[#00df9a] px-6 py-3 font-medium text-black'>
              Notify Me
            </button>
          </div>
          <p>
            We care bout the protection of your data. Read our{' '}
            <span className='text-[#00df9a]'>Privacy Policy.</span>
          </p>
        </div>
      </div>
    </div>
  )
}

export default Newsletter
