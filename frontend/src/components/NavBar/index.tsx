import React from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { Icon, Button, Classes } from '@blueprintjs/core'
import { Tooltip2 } from '@blueprintjs/popover2'
import useDarkMode from '../../hooks/useDarkMode'
import useAuth from '../../hooks/useAuth'
import useLogout from '../../hooks/useLogout'
import SearchBar from '../Search'

const TopNavigation = () => {
  const navigate = useNavigate()
  const logout = useLogout()
  const { auth } = useAuth()

  const signOut = async () => {
    await logout()
    navigate('/')
  }
  return (
    <div className='top-navigation'>
      <Title />
      <ThemeIcon />
      {/* <LogoutIcon /> */}
      <Icon icon='log-out' size={24} className='top-navigation-icon' onClick={() => signOut()} />
      {/* <Search /> */}
      {/* <BellIcon /> */}
      {/* <ThemeIcon /> */}
      {/* <SankeyGraph /> */}
      {/* <UserCircle /> */}
    </div>
  )
}

const ForceGraph = () => {
  return (
    <Link to='/'>
      <Icon icon='graph' size={24} className='top-navigation-icon' text='Force' />
    </Link>
  )
}

const SankeyGraph = () => {
  return (
    <Link to='/sankey'>
      <Icon icon='diagram-tree' size={24} className='top-navigation-icon' text='Sankey' />
    </Link>
  )
}

const ThemeIcon = () => {
  const [darkTheme, setDarkTheme] = useDarkMode()
  const handleMode = () => setDarkTheme(!darkTheme)
  return (
    <span onClick={handleMode}>
      {darkTheme ? (
        <Icon icon='flash' size={24} className='top-navigation-icon' />
      ) : (
        <Icon icon='moon' size={24} className='top-navigation-icon' />
      )}
    </span>
  )
}
const Search = () => (
  <div className='search'>
    <input className='search-input' type='text' placeholder='Search...' />
    <Icon icon='search' size={18} className='text-secondary my-auto px-2' />
  </div>
)
const BellIcon = () => <Icon icon='notifications' size={24} className='top-navigation-icon' />
const UserCircle = () => <Icon icon='user' size={24} className='top-navigation-icon' />
const Title = () => <h5 className='title-text'>collide.io</h5>

// {
//   !auth.accessToken ? (
//     <Link to='/login'>
//       <Tooltip2 content='Login' placement='bottom-end'>
//         <Button className={Classes.MINIMAL} icon='log-in' />
//       </Tooltip2>
//     </Link>
//   ) : (
//     <Tooltip2 content='Logout' placement='bottom-end'>
//       <Button className={Classes.MINIMAL} icon='log-out' onClick={() => signOut()} />
//     </Tooltip2>
//   )
// }
// export { default as NavGroup } from './NavGroup'
export default TopNavigation
