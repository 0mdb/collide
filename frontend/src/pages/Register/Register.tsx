import { Link } from 'react-router-dom'
import React, { useState, useRef } from 'react'
import { Card, Button, H1, H5, InputGroup } from '@blueprintjs/core'

const LOGIN_URL = 'login/access-token'

function Register() {
  const [user, setUser] = useState('')
  const [pwd, setPwd] = useState('')
  const [errMsg, setErrMsg] = useState('')
  const [errorMessage, setErrorMessage] = useState('')
  const errRef = useRef()
  const userRef = useRef<HTMLHeadingElement>()

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
  return (
    <div className='register'>
      <Card className='highlight-card' interactive={true}>
        <form onSubmit={handleSubmit}>
          <H1>Collide</H1>
          <br />
          <InputGroup type='email' placeholder='Email' id='username' autoComplete='off' required />
          <br />
          <InputGroup type='password' id='password' placeholder='Password' required />
          <br />
          <InputGroup
            type='password'
            id='confirmpassword'
            placeholder='Confirm password'
            required
          />
          <br />
          <p>
            <Button intent='primary' type='submit' text='Sign up' />
          </p>
        </form>
      </Card>
      <Card className='highlight-card' interactive={true}>
        <H5>
          Have an account?
          <br />
          <Link to='/login'>Sign in</Link>
        </H5>
      </Card>
    </div>
  )
}
export default Register
/* return (
*   <section className='register'>
*     <form className='box'>
*       <H1>Register</H1>
*       <div className='field'>
*         <Label className='Label'>Email Address</Label>
*         <div className='control'>
*           <input
*             type='email'
*             placeholder='Enter email'
*             value={email}
*             onChange={(e) => setEmail(e.target.value)}
*             className='input'
*             required
*           />
*         </div>
*       </div>
*       <div className='field'>
*         <Label Password />
*         <div className='control'>
*           <input
*             type='password'
*             placeholder='Enter password'
*             value={password}
*             onChange={(e) => setPassword(e.target.value)}
*             className='input'
*             required
*           />
*         </div>
*       </div>
*       <div className='field'>
*         <Label className='Label'>Confirm Password</Label>
*         <div className='control'>
*           <input
*             type='password'
*             placeholder='Enter password'
*             value={password}
*             onChange={(e) => setConfirmationPassword(e.target.value)}
*             className='input'
*             required
*           />
*         </div>
*       </div>
*       <br />
*       <Button intent='primary' type='submit' text='Register' />
*     </form>
*   </section>
* )
}

export default Register */
