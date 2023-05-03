/* import React, { lazy, Suspense } from 'react' */
import React from 'react'
import { useLocation, Navigate, Outlet } from 'react-router-dom'
import { Route, Routes } from 'react-router-dom'
import Home from './pages/Home'
import Landing from './pages/Landing'
import Welcome from './pages/Landing/Welcome'
import APILanding from './pages/Landing/APINotify'
import FAQLanding from './pages/Landing/FAQ'
import About from './pages/Landing/About'
import Contact from './pages/Landing/Contact'
import PrivacyPolicy from './pages/Landing/PrivacyPolicy'
import TermsOfUse from './pages/Landing/TermsOfUse'
import OpenSource from './pages/Landing/OpenSource'
import Layout from './pages/Layout'
import GraphDisplay from './pages/Home/ForceGraph'
// import Login from './pages/Login'
// import Register from './pages/Register'
// import PasswordReset from './pages/Password'
import PageNotFound from './components/PageNotFound'
import { UserSettings } from './pages/Home'
import APINotify from './pages/Landing/APINotify'
// import { useIsAuthenticated } from 'react-auth-kit'

// const Home = lazy(() => import('./pages/Home'))
// const Login = lazy(() => import('./pages/Login'))

// function RequireAuth() {
//   const isAuthenticated = useIsAuthenticated()
//   const auth = isAuthenticated()
//   console.log('auth', auth)
//   const location = useLocation()
//
//   return auth ? <Outlet /> : <Navigate to='/login' state={{ from: location }} replace />
// }

function App() {
  return (
    <Routes>
      <Route path='/' element={<Layout />}>
        {/* public routes */}
        <Route path='/' element={<Landing />}>
          <Route index element={<Welcome />} />
          <Route path='api' element={<APILanding />} />
          <Route path='privacypolicy' element={<PrivacyPolicy />} />
          <Route path='termsofuse' element={<TermsOfUse />} />
          <Route path='opensource' element={<OpenSource />} />
          <Route path='contact' element={<Contact />} />
          <Route path='faq' element={<FAQLanding />} />
           <Route path='home' element={<Home />}>
             <Route index element={<GraphDisplay />} />
             <Route path='force' element={<GraphDisplay />} />
             <Route path='settings' element={<UserSettings />} />
           </Route>
          <Route path='about' element={<About />} />

          <Route path='apinotify' element={<APINotify />} />
        </Route>
{/*           <Route path='login' element={<Login />} /> */}
{/*           <Route path='register' element={<Register />} /> */}
{/*           <Route path='forgotpass' element={<PasswordReset />} /> */}
{/*         <Route element={<RequireAuth />}> */}
{/*           <Route path='home' element={<Home />}> */}
{/*             <Route index element={<GraphDisplay />} /> */}
{/*             <Route path='force' element={<GraphDisplay />} /> */}
{/*             <Route path='settings' element={<UserSettings />} /> */}
{/*           </Route> */}
{/*         </Route> */}

        {/* catch all */}
        <Route path='*' element={<PageNotFound />} />
      </Route>
    </Routes>
  )
}
export default App
