import React from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { Button, Classes, ButtonGroup, AnchorButton, InputGroup } from '@blueprintjs/core'
import { Tooltip2 } from '@blueprintjs/popover2'
import useLogout from '../../hooks/useLogout'
import useAuth from '../../hooks/useAuth'
import SearchBar from '../../components/SearchBar'

function NavGroup() {
  const navigate = useNavigate()
  const logout = useLogout()
  const { auth } = useAuth()

  const signOut = async () => {
    await logout()
    navigate('/')
  }

  return (
    <div className='navgroup'>
      <ButtonGroup minimal={true}>
        <Link to='/'>
          <Button className={Classes.MINIMAL} icon='home' />
        </Link>
        <Button className={Classes.MINIMAL} icon='series-configuration' />
        <Tooltip2 content='Light Mode' placement='bottom-end'>
          <Button className={Classes.MINIMAL} icon='flash' />
        </Tooltip2>
        <Tooltip2 content='Admin' placement='bottom-end'>
          <Link to='/admin'>
            <Button className={Classes.MINIMAL} icon='database' />
          </Link>
        </Tooltip2>
        <AnchorButton icon='cog ' rightIcon='caret-down'></AnchorButton>
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
      </ButtonGroup>
      {/* <SearchBar /> */}
    </div>
  )
}

export default NavGroup
