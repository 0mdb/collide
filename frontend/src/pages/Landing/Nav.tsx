import React, { useState } from 'react'
import { Icon } from '@blueprintjs/core'
import { Link } from 'react-router-dom'
import DarkModeSwitch from '../../components/DarkModeSwitch'
import { ProjectName, WebsiteName, LoginStr, SignUpStr } from '../../assets/landing_strings.tsx'

const Navbar = () => {
  const [nav, setNav] = useState(false)

  const handleNav = () => {
    setNav(!nav)
  }

  return (
    <div className='mx-auto flex h-24 max-w-[1240px] items-center justify-between px-4 text-secondary-l-text dark:text-secondary-d-text'>
      <h1 className='w-full text-3xl font-bold'>
        <ProjectName />
      </h1>
      <ul className='hidden md:flex'>
        <li className='p-4'>
          <DarkModeSwitch />
        </li>

        {/* <Link to='/'>
          <li className='p-4'>Home</li>
        </Link> */}
        <Link to='/login'>
          <li className='p-4'>Login</li>
        </Link>
        <Link to='/register'>
          <li className='p-4'>Signup</li>
        </Link>
      </ul>
      <div onClick={handleNav} className='block md:hidden'>
        {nav ? (
          <Icon icon='cross' className='dark:fill-secondary-d-text' size={20} />
        ) : (
          <Icon icon='menu' size={20} className='dark:fill-secondary-l' />
        )}
      </div>
      <ul
        className={
          nav
            ? 'fixed left-0 top-0 h-full w-[60%] border-r border-secondary dark:border-secondary duration-500 ease-in-out bg-white dark:bg-secondary-d'
            : 'fixed left-[-100%] duration-500 ease-in-out'
        }
      >
        <h1 className='m-4 w-full text-3xl font-bold'>
          <WebsiteName />
        </h1>

        <Link to='login'>
          <li className='p-4 text-xl'>
            <LoginStr />
          </li>
        </Link>
        <Link to='register'>
          <li className='p-4 text-xl'>
            <SignUpStr />
          </li>
        </Link>
        <li className='text-xl mr-4 p-4'>
          <DarkModeSwitch />
        </li>
      </ul>
    </div>
  )
}

export default Navbar
