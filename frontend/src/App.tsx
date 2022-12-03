import React from 'react';
import jsonServerProvider from 'ra-data-json-server';
import { Routes, Route } from 'react-router-dom';
import { H1 } from '@blueprintjs/core';
import { Admin, Resource, ListGuesser } from 'react-admin';
import PersistLogin from './components/PersistLogin';
import './App.scss';
import Home from './pages/Home/Home';
import Layout from './pages/Layout/Layout';
import Graph2 from './pages/Graph2/Graph2';
import Graph1 from './pages/Graph1/Graph1';
import Login from './pages/Login/Login';
import Unauthorized from './components/Unauthorized';
import RequireAuth from './components/RequireAuth';
import Register from './components/Register';

const dataProvider = jsonServerProvider('http://jsonplaceholder.typicode.com');

const ROLES = {
  User: 'user',
  Admin: 'admin',
};

function App() {
  return (
    <Routes>
      <Route path="/" element={<Layout />}>
        {/* public routes */}
        <Route path="login" element={<Login />} />
        <Route path="register" element={<Register />} />
        <Route path="/" element={<Home />} />
        <Route path="unauthorized" element={<Unauthorized />} />
        {/* protected routes */}
        <Route element={<PersistLogin />}>
          <Route element={<RequireAuth allowedRoles={[ROLES.User]} />}>
            <Route path="graph1" element={<Graph1 />} />
          </Route>
          <Route element={<RequireAuth allowedRoles={[ROLES.User]} />}>
            <Route path="graph2" element={<Graph2 />} />
          </Route>
          <Route element={<RequireAuth allowedRoles={[ROLES.Admin]} />}>
            <Route
              path="admin/*"
              element={(
                <Admin
                  dataProvider={dataProvider}
                  basename="/admin"
                >
                  <Resource name="users" list={ListGuesser}/>
                  </Admin>
              )}
            />
          </Route>
        </Route>
        {/* catch all */}
        <Route path="*" element={<H1>Page Missing</H1>} />
      </Route>
    </Routes>
  );
}
export default App;
