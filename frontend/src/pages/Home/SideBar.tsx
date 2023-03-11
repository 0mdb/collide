import React from 'react'
import { Link } from 'react-router-dom'
import { Icon } from '@blueprintjs/core'
import useLogout from '../../hooks/useLogout'
import useGraphType from '../../hooks/useGraphType'
import { useNavigate } from 'react-router-dom'
import { ThemeButton } from '../../components/ThemeButton'

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

function GraphTypeButton() {
  const { graphType, changeGraphType } = useGraphType('2D')
  return (
    <button className='dark:text-muted text-black font-bold' onClick={changeGraphType}>
      {graphType === '2D' ? '3D' : '2D'}
    </button>
  )
}
const SideBar = () => {
  return (
    <div
      className='fixed top-0 left-0 flex h-screen w-16 flex-col
                  bg-white shadow-lg dark:bg-gray-900'
    >
      <Link to='/'>
        <SideBarIcon
          text='Home'
          icon={<Icon icon='home' size={24} className='dark:fill-muted' />}
        />
      </Link>
      {/* <Link to='/home/force'>
        <SideBarIcon
          icon={<Icon icon='layout-auto' size={28} className='dark:fill-muted' />}
          text={'Force'}
        />
      </Link> */}
      <SideBarIcon icon={<GraphTypeButton />} text='Graph Type' />
      <Divider />
      <SideBarIcon icon={<ThemeButton />} text='Theme'></SideBarIcon>
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
               hover:dark:bg-primary-l
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
