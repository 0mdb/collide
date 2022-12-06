import { Link } from 'react-router-dom'
import React, { useContext, useState } from 'react'
import { Card, Button, Label, H1, H5, FormGroup, InputGroup } from '@blueprintjs/core'

function Register() {
  const [user, setUser] = useState('')
  const [pwd, setPwd] = useState('')
  const [errMsg, setErrMsg] = useState('')
  const [confirmationPwd, setConfirmationPwd] = useState('')
  const [errorMessage, setErrorMessage] = useState('')

  const submitRegistration = async () => {
    const requestOptions = {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email: email, hashed_password: password }),
    }

    const response = await fetch('/api/users', requestOptions)
    const data = await response.json()

    if (!response.ok) {
      setErrorMessage(data.detail)
    } else {
      setToken(data.access_token)
    }
  }
  const handleSubmit = (e) => {
    e.preventDefault()
    if (password === confirmationPassword && password.length > 4) {
      submitRegistration()
    } else {
      setErrorMessage('Ensure that passwords match and greater than 5 charecters')
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
