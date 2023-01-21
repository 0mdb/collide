import React from 'react'
import { Link } from 'react-router-dom'
import { Icon } from '@blueprintjs/core'
import useLogout from '../../hooks/useLogout'
import { useNavigate } from 'react-router-dom'
import ThemeIcon from '../../components/ThemeButton'

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
      icon={<Icon icon='log-out' size={24} className='dark:fill-muted' onClick={() => signOut()} />}
    />
  )
}

const SideBar = () => {
  return (
    <div
      className='fixed top-0 left-0 flex h-screen w-16 flex-col
                  bg-white shadow-lg dark:bg-gray-900'
    >
      {/* <Link to='/'>
        <SideBarIcon
          icon={<Icon icon='home' size={28} className='dark:fill-muted' />}
          text={'Home'}
        />
      </Link> */}
      <Link to='/home/force'>
        <SideBarIcon
          icon={<Icon icon='layout-auto' size={28} className='dark:fill-muted' />}
          text={'Force'}
        />
      </Link>
      <Link to='/home/law'>
        <SideBarIcon
          icon={<Icon icon='take-action' size={28} className='dark:fill-muted' />}
          text={'Bills'}
        />
      </Link>
      <Link to='/home/money'>
        <SideBarIcon
          icon={<Icon icon='dollar' size={28} className='dark:fill-muted' />}
          text={'Sankey2'}
        />
      </Link>
      <Divider />
      <Link to='/home/settings'>
        <SideBarIcon
          icon={<Icon icon='cog' size={28} className='dark:fill-muted' />}
          text={'Settings'}
        />
      </Link>
      <SignOutButton />
    </div>
  )
}

const SideBarIcon = ({ icon, text = 'tooltip 💡' }) => (
  <div
    className='group relative mx-auto mt-2 
    mb-2 flex h-12 w-12 cursor-pointer  
  items-center justify-center rounded-3xl bg-gray-400 
  text-green-500 shadow-lg
    transition-all duration-300
    ease-linear hover:rounded-xl hover:bg-primary
    hover:fill-muted hover:text-white
  
  dark:bg-gray-800'
  >
    {icon}
    <span
      className='
    origin-left; absolute left-14 m-2 w-auto min-w-max scale-0 rounded-md
    bg-gray-900 p-2 
    text-xs font-bold 
    text-white shadow-md transition-all duration-100
    group-hover:scale-100'
    >
      {text}
    </span>
  </div>
)

const Divider = () => (
  <hr
    className='bg-gray-201 border-gray-201 
    mx-3 rounded-full border dark:border-gray-800
    dark:bg-gray-800
'
  />
)

export default SideBar
