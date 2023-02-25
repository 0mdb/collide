import React from 'react'
import { Link } from 'react-router-dom'
import Footer from './Footer'
import Navbar from './Nav'

const APINotify = () => {
  return (
    <div className='w-full py-16 px-4'>
      <div className='mx-auto max-w-[800px]'>
        <h1 className='py-2 text-2xl font-bold sm:text-3xl md:text-4xl text-center'>
          Get early access to the LobbyRadar API.
        </h1>
        <p className='text-center'>
          Sign up to our waiting list and be the first to know when it's ready.
        </p>
        <div className='my-8 flex flex-col items-center justify-between sm:flex-row'>
          <input
            className='flex w-full rounded-md bg-gray-400 p-3 text-gray-500 placeholder-gray-500 dark:bg-gray-600 dark:text-gray-400'
            type='email'
            placeholder='Enter Email'
          />
          <button className='my-6 ml-4 w-[250px] rounded-md bg-primary dark:bg-primary-d px-6 py-3 font-medium text-morp'>
            Join the waiting list
          </button>
        </div>
        <Link to='/legal'>
          <p className='text-center'>
            By signing up, you agree to our <span className='text-muted'>Privacy Policy</span>.
          </p>
        </Link>
      </div>
    </div>
  )
}

function APILanding() {
  return (
    <div>
      <Navbar />
      <APINotify />
      <Footer />
    </div>
  )
}

export default APILanding
