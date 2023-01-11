import React from 'react'
import { Link } from 'react-router-dom'
import { Icon } from '@blueprintjs/core'
import useDarkMode from '../../hooks/useDarkMode'
import useLogout from '../../hooks/useLogout'
import { useNavigate } from 'react-router-dom'

const ThemeIcon = () => {
  const [darkTheme, setDarkTheme] = useDarkMode()
  const handleMode = () => setDarkTheme(!darkTheme)
  return (
    <span onClick={handleMode}>
      {darkTheme ? <Icon icon='flash' size={28} /> : <Icon icon='moon' size={32} />}
    </span>
  )
}

const SignOutButton = () => {
  const navigate = useNavigate()
  const logout = useLogout()
  const signOut = async () => {
    await logout()
    navigate('/')
  }
  return (
    <SideBarIcon
      text='Sign Out'
      icon={<Icon icon='log-out' size={24} onClick={() => signOut()} />}
    />
  )
}

const SideBar = () => {
  return (
    <div
      className='fixed top-0 left-0 flex h-screen w-16 flex-col
                  bg-white shadow-lg dark:bg-gray-900'
    >
      <Link to='/'>
        <SideBarIcon icon={<Icon icon='home' size={28} />} text={'Home'} />
      </Link>
      <Divider />
      <Divider />
      <SideBarIcon icon={<Icon icon='cog' size={28} />} text='Settings ' />
      <SideBarIcon icon={<ThemeIcon />} text='Theme' />
      <SignOutButton />
    </div>
  )
}

const SideBarIcon = ({ icon, text = 'tooltip 💡' }) => (
  <div className='sidebar-icon group'>
    {icon}
    <span className='sidebar-tooltip group-hover:scale-100'>{text}</span>
  </div>
)

const Divider = () => <hr className='sidebar-hr' />

export default SideBar
