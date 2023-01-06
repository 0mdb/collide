import React from 'react'
import { Link, useNavigate } from 'react-router-dom'

function Landing() {
  const navigate = useNavigate()
  return (
    <div className='flex h-screen flex-col items-center justify-center'>
      <h1 className='text-4xl font-bold'>Collide.io</h1>
      <button
        className='rounded bg-blue-500 py-2 px-4 font-bold text-white hover:bg-blue-700'
        onClick={() => navigate('/Login')}
      >
        Login
      </button>
      <h1 className='text-4xl font-bold'>or</h1>
      <button
        className='rounded bg-blue-500 py-2 px-4 font-bold text-white hover:bg-blue-700'
        onClick={() => navigate('/Register')}
      >
        Sign up
      </button>
    </div>
  )
}

export default Landing
