import { useRef, useState, useEffect } from 'react'
import { Checkbox, Button, FormGroup, H1, InputGroup, Label, Card } from '@blueprintjs/core'
import useAuth from '../../hooks/useAuth'
import axios from '../../api/axios'
import { Link, useNavigate, useLocation } from 'react-router-dom'
import React from 'react'

const LOGIN_URL = 'login/access-token'

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
    <div className='login'>
      <Card>
        <form onSubmit={handleSubmit}>
          <H1>Collide</H1>
          <FormGroup label='Email' labelFor='username'>
            <input
              type='email'
              placeholder='Email'
              id='username'
              ref={userRef}
              autoComplete='off'
              onChange={(e) => setUser(e.target.value)}
              value={user}
              required
            />
          </FormGroup>
          <FormGroup label='Password' labelFor='password'>
            <input
              type='password'
              id='password'
              placeholder='Password'
              ref={userRef}
              onChange={(e) => setPwd(e.target.value)}
              value={pwd}
              required
            />
          </FormGroup>
          <p>
            <Button intent='primary' type='submit' text='Login' />
          </p>
        </form>
        <Checkbox
          checked={persist}
          label='Remember me'
          onChange={togglePersist}
          alignIndicator='left'
        />
        <p>
          Need an Account?
          <br />
          <span className='line'>
            <Link to='/register'>Sign up</Link>
          </span>
        </p>
        <p ref={errRef} className={errMsg ? 'errmsg' : 'offscreen'} aria-live='assertive'>
          {errMsg}
        </p>
      </Card>
    </div>
  )
}

export default Login
