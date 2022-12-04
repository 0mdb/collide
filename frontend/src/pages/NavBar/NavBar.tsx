import React from 'react'
import { Link, useNavigate } from 'react-router-dom'
import {
  Alignment,
  Button,
  Classes,
  Navbar,
  NavbarDivider,
  NavbarGroup,
  Position,
  Menu,
} from '@blueprintjs/core'
import { Popover2, MenuItem2 } from '@blueprintjs/popover2'
import DarkMode from '../../components/DarkMode'
import useLogout from '../../hooks/useLogout'
import useAuth from '../../hooks/useAuth'

function NavBar() {
  const navigate = useNavigate()
  const logout = useLogout()
  const { auth, setAuth } = useAuth()

  const signOut = async () => {
    await logout()
    navigate('/')
  }

  return (
    <div className='my-navbar'>
      <Navbar fixedToTop={true}>
        <NavbarGroup align={Alignment.LEFT}>
          <Link to='/'>
            <Button className={Classes.MINIMAL} icon='home' text='Home' />
          </Link>
          <Link to='/graph1'>
            <Button className={Classes.MINIMAL} icon='chart' text='Graph1' />
          </Link>
          <Link to='/graph2'>
            <Button className={Classes.MINIMAL} icon='heatmap' text='Graph2' />
          </Link>
          <NavbarDivider />
        </NavbarGroup>
        <NavbarGroup align={Alignment.RIGHT}>
          <Popover2
            content={
              <Menu>
                <DarkMode />
                <MenuItem2 icon='new-object' text='Other thing!' />
              </Menu>
            }
            position={Position.BOTTOM}
          >
            <Button className={Classes.MINIMAL} icon='cog' text='Settings' />
          </Popover2>
          <Link to='/admin'>
            <Button className={Classes.MINIMAL} icon='database' text='Admin' />
          </Link>
          <NavbarDivider />
          {!auth.accessToken ? (
            <Link to='/login'>
              <Button className={Classes.MINIMAL} icon='log-in' text='Login' />
            </Link>
          ) : (
            <Button
              className={Classes.MINIMAL}
              icon='log-out'
              text='Logout'
              onClick={(e) => signOut(e)}
            />
          )}
        </NavbarGroup>
      </Navbar>
    </div>
  )
}

export default NavBar
