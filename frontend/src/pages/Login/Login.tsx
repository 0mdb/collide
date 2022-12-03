import { useRef, useState, useEffect } from 'react';
import { Button, H1, Label } from '@blueprintjs/core';
import useAuth from '../../hooks/useAuth';
import axios from '../../api/axios';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import React from 'react';

const LOGIN_URL = 'login/access-token';

function Login() {
  const { setAuth, persist, setPersist } = useAuth();

  const navigate = useNavigate();
  const location = useLocation();
  const from = location.state?.from?.pathname || '/';
  const userRef = useRef<HTMLHeadingElement>();
  const errRef = useRef();
  const [user, setUser] = useState('');
  const [pwd, setPwd] = useState('');
  const [errMsg, setErrMsg] = useState('');

  useEffect(() => {
    userRef.current.focus();
  }, []);

  useEffect(() => {
    setErrMsg('');
  }, [user, pwd]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const formData = new FormData();
      formData.append('username', user);
      formData.append('password', pwd);
      const response = await axios.post(LOGIN_URL, formData);
      const accessToken = response?.data?.access_token;
      const refreshToken = response?.data?.refresh_token;
      setAuth({ user, accessToken, refreshToken });
      setUser('');
      setPwd('');
      navigate(from, { replace: true });
    } catch (err) {
      if (!err?.response) {
        setErrMsg('No Server Response');
      } else if (err.response?.status === 400) {
        setErrMsg('Incorrect email or password');
      } else {
        setErrMsg('Login Failed');
      }
      errRef.current.focus();
    }
  };

  const togglePersist = () => {
    setPersist(!persist);
  };
  useEffect(() => {
    localStorage.setItem('persist', persist);
  }, [persist]);

  return (
    <section>
      <p
        ref={errRef}
        className={errMsg ? 'errmsg' : 'offscreen'}
        aria-live="assertive"
      >
        {errMsg}
      </p>
      <H1>Sign In</H1>
      <form onSubmit={handleSubmit}>
        <Label htmlFor="username">Email</Label>
        <input
          type="email"
          id="username"
          ref={userRef}
          autoComplete="off"
          onChange={(e) => setUser(e.target.value)}
          value={user}
          required
        />
        <Label htmlFor="password">Password</Label>
        <input
          type="password"
          id="password"
          ref={userRef}
          onChange={(e) => setPwd(e.target.value)}
          value={pwd}
          required
        />
        <p>
          <br />
          <Button 
          // intent="primary" 
          type="submit" 
          text="Login" />
        </p>
      </form>
      <div className="persistCheck">
        <input
          type="checkbox"
          id="persist"
          onChange={togglePersist}
          checked={persist}
        />
      </div>
      <label htmlFor="persist">Remember Me</label>
      <p>
        Need an Account?
        <br />
        <span className="line">
          <Link to="/register">Sign up</Link>
        </span>
      </p>
    </section>
  );
}

export default Login;
