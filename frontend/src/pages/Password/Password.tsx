import { useRef, useState, useEffect } from 'react'
import useAuth from '../../hooks/useAuth'
import axios from '../../api/axios'
import { Link, useNavigate, useLocation } from 'react-router-dom'
import React from 'react'
import loginImage from '../../pages/Login/login_img.png'

const PW_URL = 'auth/forgot-password'

function PasswordReset() {
  const navigate = useNavigate()
  const location = useLocation()
  const from = location.state?.from?.pathname || '/'
  const userRef = useRef<HTMLHeadingElement>()
  const [user, setUser] = useState('')
  const [errMsg, setErrMsg] = useState('')

  useEffect(() => {
    setErrMsg('')
  }, [user])

  const handleSubmit = async (e) => {
    e.preventDefault()

    try {
      await axios.post(PW_URL, { email: user })
      navigate('/login')

      setErrMsg('Password reset email sent')
    } catch (err) {
      if (!err?.response) {
        setErrMsg('No Server Response')
      } else if (err.response?.status === 400) {
        setErrMsg('Incorrect email or password')
      } else {
        setErrMsg('Login Failed')
      }
    }
  }

  return (
    <div className='grid h-screen w-full grid-cols-1 sm:grid-cols-2'>
      <div className='hidden sm:block'>
        <img className='h-full w-full object-cover' src={loginImage} alt='' />
      </div>
      <div className='flex flex-col justify-center bg-gray-400 dark:bg-gray-800'>
        <form
          className='mx-auto w-full max-w-[400px] rounded-xl bg-gray-100 p-4 shadow-xl'
          onSubmit={handleSubmit}
        >
          <h2 className='py-6 text-center text-4xl font-bold'>collide.io</h2>
          <div className='flex flex-col py-2'>
            <input
              type='email'
              placeholder='Email'
              id='username'
              ref={userRef}
              autoComplete='off'
              onChange={(e) => setUser(e.target.value)}
              value={user}
              required={true}
              className='rounded-lg border p-2 shadow-lg'
            />
          </div>
          <button
            type='submit'
            className='my-5 w-full rounded-lg bg-indigo-600 py-2 text-white hover:bg-indigo-500'
          >
            Reset
          </button>
        </form>
      </div>
    </div>
  )
}

export default PasswordReset
