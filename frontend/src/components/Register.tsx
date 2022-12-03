import React, { useContext, useState } from 'react';
import { Button, Label, H1 } from '@blueprintjs/core';

function Register() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmationPassword, setConfirmationPassword] = useState('');
  const [errorMessage, setErrorMessage] = useState('');

  const submitRegistration = async () => {
    const requestOptions = {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email: email, hashed_password: password }),
    };

    const response = await fetch('/api/users', requestOptions);
    const data = await response.json();

    if (!response.ok) {
      setErrorMessage(data.detail);
    } else {
      setToken(data.access_token);
    }
  };
  const handleSubmit = (e) => {
    e.preventDefault();
    if (password === confirmationPassword && password.length > 4) {
      submitRegistration();
    } else {
      setErrorMessage(
        'Ensure that passwords match and greater than 5 charecters'
      );
    }
  };

  return (
    <div className="column">
      <form className="box">
        <H1 className="title">Register</H1>
        <div className="field">
          <Label className="Label">Email Address</Label>
          <div className="control">
            <input
              type="email"
              placeholder="Enter email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="input"
              required
            />
          </div>
        </div>
        <div className="field">
          <Label Password />
          <div className="control">
            <input
              type="password"
              placeholder="Enter password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="input"
              required
            />
          </div>
        </div>
        <div className="field">
          <Label className="Label">Confirm Password</Label>
          <div className="control">
            <input
              type="password"
              placeholder="Enter password"
              value={password}
              onChange={(e) => setConfirmationPassword(e.target.value)}
              className="input"
              required
            />
          </div>
        </div>
        <br />
        <Button className="button is-primary" type="submit" text="Register" />
      </form>
    </div>
  );
}

export default Register;