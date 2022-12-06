import React from 'react'
import { Link, useNavigate } from 'react-router-dom'
import {
  Alignment,
  Button,
  Classes,
  Position,
  Menu,
  Navbar,
  Colors,
  NavbarDivider,
  NavbarGroup,
  NavbarHeading,
} from '@blueprintjs/core'
import { Popover2, Tooltip2, MenuItem2 } from '@blueprintjs/popover2'
import DarkMode from '../../components/DarkMode'
import useLogout from '../../hooks/useLogout'
import useAuth from '../../hooks/useAuth'

function NavBar() {
  const navigate = useNavigate()
  const logout = useLogout()
  const { auth } = useAuth()

  const signOut = async () => {
    await logout()
    navigate('/')
  }

  const navStyle = {
    backgroundColor: Colors.DARK_GRAY3,
    backgroundOpacity: 0.9,
    outline: 'none',
    boxshadow: Colors.DARK_GRAY3,
    boarder: 'none',
  }

  return (
    <div className='Nav'>
      <Navbar fixedToTop={true} style={navStyle}>
        <NavbarGroup align={Alignment.RIGHT}>
          <Link to='/'>
            <Button className={Classes.MINIMAL} icon='home' />
          </Link>
          <Popover2
            placement='bottom-end'
            content={
              <Menu>
                <Link to='/'>
                  <Button className={Classes.MINIMAL} icon='home' text='Home' />
                </Link>
                <Link to='/graph1'>
                  <Button className={Classes.MINIMAL} icon='heatmap' text='    Graph 1    ' />
                </Link>
                <Link to='/graph2'>
                  <Button className={Classes.MINIMAL} icon='heatmap' text='    Graph 2' />
                </Link>
              </Menu>
            }
          >
            <Button className={Classes.MINIMAL} icon='series-configuration' />
          </Popover2>
          <Tooltip2 content='Search' placement='bottom-end'>
            <Popover2
              placement='bottom-end'
              content={
                <Menu>
                  <input className='bp4-input' placeholder='Search...' type='text' />
                </Menu>
              }
            >
              <Button className={Classes.MINIMAL} icon='search' />
            </Popover2>
          </Tooltip2>
          <NavbarDivider />
          {/* <DarkMode /> */}
          <Tooltip2 content='Light Mode' placement='bottom-end'>
            <Button className={Classes.MINIMAL} icon='flash' />
          </Tooltip2>
          <Tooltip2 content='Admin' placement='bottom-end'>
            <Link to='/admin'>
              <Button className={Classes.MINIMAL} icon='database' />
            </Link>
          </Tooltip2>
          {!auth.accessToken ? (
            <Link to='/login'>
              <Tooltip2 content='Login' placement='bottom-end'>
                <Button className={Classes.MINIMAL} icon='log-in' />
              </Tooltip2>
            </Link>
          ) : (
            <Tooltip2 content='Logout' placement='bottom-end'>
              <Button className={Classes.MINIMAL} icon='log-out' onClick={() => signOut()} />
            </Tooltip2>
          )}
        </NavbarGroup>
      </Navbar>
    </div>
  )
}

export default NavBar
