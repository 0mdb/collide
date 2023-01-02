import React, { useRef, useState, useEffect } from 'react'
import { Link, useNavigate, useLocation } from 'react-router-dom'
import useAuth from '../../hooks/useAuth'
import loginImage from '../Login/login_img.png'
const LOGIN_URL = 'login/access-token'

// function Register() {
//   const [user, setUser] = useState('')
//   const [pwd, setPwd] = useState('')
//   const [errMsg, setErrMsg] = useState('')
//   const [errorMessage, setErrorMessage] = useState('')
//   const errRef = useRef()
//   const userRef = useRef<HTMLHeadingElement>()

//   const handleSubmit = async (e) => {
//     e.preventDefault()
//     try {
//       const formData = new FormData()
//       formData.append('username', user)
//       formData.append('password', pwd)
//       const response = await axios.post(LOGIN_URL, formData)
//       const accessToken = response?.data?.access_token
//       const refreshToken = response?.data?.refresh_token
//       setAuth({ user, accessToken, refreshToken })
//       setUser('')
//       setPwd('')
//       navigate(from, { replace: true })
//     } catch (err) {
//       if (!err?.response) {
//         setErrMsg('No Server Response')
//       } else if (err.response?.status === 400) {
//         setErrMsg('Incorrect email or password')
//       } else {
//         setErrMsg('Login Failed')
//       }
//       errRef.current.focus()
//     }
//   }
//   return (
//     <div className='login'>
//       <Card className='highlight-card' interactive={true}>
//         <form onSubmit={handleSubmit}>
//           <H1>Collide</H1>
//           <br />
//           <InputGroup type='email' placeholder='Email' id='username' autoComplete='off' required />
//           <br />
//           <InputGroup type='password' id='password' placeholder='Password' required />
//           <br />
//           <InputGroup
//             type='password'
//             id='confirmpassword'
//             placeholder='Confirm password'
//             required
//           />
//           <br />
//           <p>
//             <Button intent='primary' type='submit' text='Sign up' />
//           </p>
//         </form>
//       </Card>
//       <Card className='highlight-card' interactive={true}>
//         <H5>
//           Have an account?
//           <br />
//           <Link to='/login'>Sign in</Link>
//         </H5>
//       </Card>
//     </div>
//   )
// }

function Register() {
  const { setAuth, persist, setPersist } = useAuth()

  const navigate = useNavigate()
  const location = useLocation()
  const from = location.state?.from?.pathname || '/'
  const userRef = useRef<HTMLHeadingElement>()
  const errRef = useRef()
  const [user, setUser] = useState('')
  const [pwd, setPwd] = useState('')
  const [errMsg, setErrMsg] = useState('')

  useEffect(() => {
    userRef.current.focus()
  }, [])

  useEffect(() => {
    setErrMsg('')
  }, [user, pwd])

  const handleSubmit = async (e) => {
    e.preventDefault()
    try {
      const formData = new FormData()
      formData.append('username', user)
      formData.append('password', pwd)
      const response = await axios.post(LOGIN_URL, formData)
      const accessToken = response?.data?.access_token
      const refreshToken = response?.data?.refresh_token
      setAuth({ user, accessToken, refreshToken })
      setUser('')
      setPwd('')
      navigate(from, { replace: true })
    } catch (err) {
      if (!err?.response) {
        setErrMsg('No Server Response')
      } else if (err.response?.status === 400) {
        setErrMsg('Incorrect email or password')
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
              id='username'
              ref={userRef}
              autoComplete='off'
              onChange={(e) => setUser(e.target.value)}
              value={user}
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
              value={pwd}
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
              value={pwd}
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
