import React, { useRef, useState, useEffect } from 'react'
import { Link, useNavigate, useLocation } from 'react-router-dom'
import useAuth from '../../hooks/useAuth'
import loginImage from '../Login/login_img.png'
import axios from '../../api/axios'

const REGISTER_URL = 'auth/register'

function Register() {
  const { setAuth, persist, setPersist } = useAuth()

  const navigate = useNavigate()
  const location = useLocation()
  const from = location.state?.from?.pathname || '/'
  const userRef = useRef<HTMLHeadingElement>()
  const errRef = useRef()
  const [email, setUser] = useState('')
  const [password, setPwd] = useState('')
  const [errMsg, setErrMsg] = useState('')

  useEffect(() => {
    userRef.current.focus()
  }, [])

  useEffect(() => {
    setErrMsg('')
  }, [email, password])

  const handleSubmit = async (e) => {
    e.preventDefault()
    try {
      const response = await axios.post(REGISTER_URL, { email, password })
      const accessToken = response?.data?.access_token

      setAuth({ email, accessToken })
      setUser('')
      setPwd('')
      // navigate(from, { replace: true })
      navigate('/home')
    } catch (err) {
      if (!err?.response) {
        setErrMsg('No Server Response')
      } else if (err.response?.status === 400) {
        setErrMsg('User already exists')
      } else {
        setErrMsg('Login Failed')
      }
      errRef.current.focus()
    }
  }

  const togglePersist = () => {
    setPersist(!persist)
  }
  useEffect(() => {
    localStorage.setItem('persist', persist)
  }, [persist])

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
            {/* <label>Username</label> */}
            <input
              type='email'
              placeholder='Email'
              id='email'
              ref={userRef}
              autoComplete='off'
              onChange={(e) => setUser(e.target.value)}
              value={email}
              required={true}
              className='first: rounded-lg border p-2 shadow-lg'
            />
          </div>
          <div className='flex flex-col py-2'>
            <input
              placeholder='Password'
              autoComplete='off'
              id='password'
              className='rounded-lg border p-2 shadow-lg'
              type='password'
              onChange={(e) => setPwd(e.target.value)}
              value={password}
              required
            />
          </div>
          <div className='flex flex-col py-2'>
            <input
              placeholder='Confirm password'
              id='password'
              className='rounded-lg border p-2 shadow-lg'
              type='password'
              onChange={(e) => setPwd(e.target.value)}
              value={password}
              required
            />
          </div>
          <button
            type='submit'
            className='my-5 w-full rounded-lg bg-indigo-600 py-2 text-white hover:bg-indigo-500'
          >
            Sign up
          </button>
          <div className='flex justify-between'>
            <p className='flex items-center'>
              <input onChange={togglePersist} checked={persist} className='mr-2' type='checkbox' />{' '}
              Remember me
            </p>
            <p ref={errRef} className={errMsg ? 'errmsg' : 'offscreen'} aria-live='assertive'>
              {errMsg}
            </p>

            <p>
              <span className='line'>
                <Link to='/login'>Sign in</Link>
              </span>
            </p>
            {/* <h5>
              Have an account?
              <br />
              <Link to='/login'>Sign in</Link>
            </h5> */}
          </div>
        </form>
      </div>
    </div>
  )
}

export default Register
