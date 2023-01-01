import { useRef, useState, useEffect } from 'react'
import useAuth from '../../hooks/useAuth'
import axios from '../../api/axios'
import { Link, useNavigate, useLocation } from 'react-router-dom'
import React from 'react'
import loginImage from './login_img.png'

const LOGIN_URL = 'login/access-token'

// function Login() {
//   const { setAuth, persist, setPersist } = useAuth()

//   const navigate = useNavigate()
//   const location = useLocation()
//   const from = location.state?.from?.pathname || '/'
//   const userRef = useRef<HTMLHeadingElement>()
//   const errRef = useRef()
//   const [user, setUser] = useState('')
//   const [pwd, setPwd] = useState('')
//   const [errMsg, setErrMsg] = useState('')

//   useEffect(() => {
//     userRef.current.focus()
//   }, [])

//   useEffect(() => {
//     setErrMsg('')
//   }, [user, pwd])

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

//   const togglePersist = () => {
//     setPersist(!persist)
//   }
//   useEffect(() => {
//     localStorage.setItem('persist', persist)
//   }, [persist])

//   return (
//     <div className='login'>
//       <div>
//         <form onSubmit={handleSubmit}>
//           <h1>Collide</h1>
//           <FormGroup label='Email' labelFor='username'>
//             <input
//               type='email'
//               placeholder='Email'
//               id='username'
//               ref={userRef}
//               autoComplete='off'
//               onChange={(e) => setUser(e.target.value)}
//               value={user}
//               required
//             />
//           </FormGroup>
//           <FormGroup label='Password' labelFor='password'>
//             <input
//               type='password'
//               id='password'
//               placeholder='Password'
//               ref={userRef}
//               onChange={(e) => setPwd(e.target.value)}
//               value={pwd}
//               required
//             />
//           </FormGroup>
//           <p>
//             <Button intent='primary' type='submit' text='Login' />
//           </p>
//         </form>
//         <Checkbox
//           checked={persist}
//           label='Remember me'
//           onChange={togglePersist}
//           alignIndicator='left'
//         />
//         <p>
//           Need an Account?
//           <br />
//           <span className='line'>
//             <Link to='/register'>Sign up</Link>
//           </span>
//         </p>
// <p ref={errRef} className={errMsg ? 'errmsg' : 'offscreen'} aria-live='assertive'>
// {errMsg}
// </p>
//       </div>
//     </div>
//   )

// }
function Login() {
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
              className='rounded-lg border p-2 shadow-lg'
            />
          </div>
          <div className='flex flex-col py-2'>
            {/* <label>Password</label> */}
            <input
              ref={userRef}
              placeholder='Password'
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
            Sign In
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
                <Link to='/register'>Create an account</Link>
              </span>
            </p>
          </div>
        </form>
      </div>
    </div>
  )
}

export default Login
