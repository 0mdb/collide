import { Outlet } from 'react-router-dom'
import NavBar from '../NavBar'

function Layout() {
  return (
    <main className='App'>
      <NavBar />
      <Outlet />
    </main>
  )
}

export default Layout
