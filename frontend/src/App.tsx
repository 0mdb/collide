/* import React, { lazy, Suspense } from 'react' */
import React from 'react'
import jsonserverprovider from 'ra-data-json-server'
import { Route, Routes } from 'react-router-dom'
import { H1 } from '@blueprintjs/core'
import { Admin, Resource, ListGuesser } from 'react-admin'
import PersistLogin from './components/PersistLogin'
import Home from './pages/Home'
import Landing from './pages/Landing'
import Layout from './pages/Layout'
import Sankey from './components/SankeyGraph'
import Login from './pages/Login'
import Unauthorized from './components/Unauthorized'
import RequireAuth from './components/RequireAuth'
import Register from './pages/Register'

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
        <Route path='login' element={<Login />} />
        <Route path='register' element={<Register />} />
        <Route path='/' element={<Landing />} />
        <Route path='unauthorized' element={<Unauthorized />} />
        <Route path='home' element={<Home />} />
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
        <Route path='*' element={<H1>Page Missing</H1>} />
      </Route>
      {/* </Suspense> */}
    </Routes>
  )
}
export default App
