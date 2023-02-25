/* import React, { lazy, Suspense } from 'react' */
import React from 'react'
import jsonserverprovider from 'ra-data-json-server'
import { Route, Routes } from 'react-router-dom'
import { Admin, Resource, ListGuesser } from 'react-admin'
/* import PersistLogin from './components/PersistLogin' */
import Home from './pages/Home'
import Landing from './pages/Landing'
import APILanding from './pages/Landing/APINotify'
import FAQLanding from './pages/Landing/FAQ'
import About from './pages/Landing/About'
import Contact from './pages/Landing/Contact'
import PrivacyPolicy from './pages/Landing/PrivacyPolicy'
import TermsOfUse from './pages/Landing/TermsOfUse'
import OpenSource from './pages/Landing/OpenSource'
import Layout from './pages/Layout'
import GraphDisplay from './pages/Home/ForceGraph'
import Login from './pages/Login'
import Unauthorized from './components/Unauthorized'
import RequireAuth from './components/RequireAuth'
import Register from './pages/Register'
import PasswordReset from './pages/Password'
import PageNotFound from './components/PageNotFound'
import { UserSettings } from './pages/Home'
import APINotify from './pages/Landing/APINotify'

const dataProvider = jsonserverprovider('http://jsonplaceholder.typicode.com')

// const Home = lazy(() => import('./pages/Home'))
// const Login = lazy(() => import('./pages/Login'))
// const Register = lazy(() => import('./pages/Register'))
// const Unauthorized = lazy(() => import('./components/Unauthorized'))
// const RequireAuth = lazy(() => import('./components/RequireAuth'))

const ROLES = {
  User: 'user',
  Admin: 'admin',
}

function App() {
  return (
    <Routes>
      {/* <Suspense fallback={<H1>Loading...</H1>}> */}
      <Route path='/' element={<Layout />}>
        {/* public routes */}
        <Route index element={<Landing />} />
        <Route path='landing ' element={<Landing />} />
        <Route path='api' element={<APILanding />} />
        <Route path='privacypolicy' element={<PrivacyPolicy />} />
        <Route path='termsofuse' element={<TermsOfUse />} />
        <Route path='opensource' element={<OpenSource />} />
        <Route path='contact' element={<Contact />} />
        <Route path='faq' element={<FAQLanding />} />
        <Route path='forgotpass' element={<PasswordReset />} />
        <Route path='about' element={<About />} />
        <Route path='login' element={<Login />} />
        <Route path='register' element={<Register />} />
        <Route path='unauthorized' element={<Unauthorized />} />
        <Route path='apinotify' element={<APINotify />} />
        <Route path='home' element={<Home />}>
          <Route index element={<GraphDisplay />} />
          <Route path='force' element={<GraphDisplay />} />
          <Route path='settings' element={<UserSettings />} />
        </Route>
        {/* protected routes */}
        {/* <Route element={<PersistLogin />}> */}
        {/* <Route element={<RequireAuth allowedRoles={[ROLES.User, ROLES.Admin]} />}>
          <Route path='home' element={<Home />} />
        </Route> */}
        <Route element={<RequireAuth allowedRoles={[ROLES.Admin]} />}>
          <Route
            path='admin/*'
            element={
              <Admin dataProvider={dataProvider} basename='/admin'>
                <Resource name='users' list={ListGuesser} />
              </Admin>
            }
          />
        </Route>
        {/* </Route> */}
        {/* catch all */}
        <Route path='*' element={<PageNotFound />} />
      </Route>
      {/* </Suspense> */}
    </Routes>
  )
}
export default App
