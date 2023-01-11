import React, { useState } from 'react'
import { AiOutlineClose, AiOutlineMenu } from 'react-icons/ai'
import { Icon } from '@blueprintjs/core'
import { ThemeIcon } from '../../components/NavBar'
import { Link } from 'react-router-dom'

const Navbar = () => {
  const [nav, setNav] = useState(false)

  const handleNav = () => {
    setNav(!nav)
  }

  return (
    <div className='mx-auto flex h-24 max-w-[1240px] items-center justify-between px-4'>
      <ThemeIcon />
      <h1 className='w-full text-3xl font-bold'>collide.io</h1>
      <ul className='hidden md:flex'>
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
        {nav ? <Icon icon='cross' size={20} /> : <Icon icon='menu' size={20} />}
      </div>
      <ul
        className={
          nav
            ? 'fixed left-0 top-0 h-full w-[60%] border-r border-r-gray-900 bg-gray-300 duration-500 ease-in-out dark:bg-gray-700'
            : 'fixed left-[-100%] duration-500 ease-in-out'
        }
      >
        <h1 className='m-4 w-full text-3xl font-bold text-[#00df9a]'>collide.io</h1>
        <Link to='login'>
          <li className='border-b border-gray-600 p-4'>Login</li>
        </Link>
        <Link to='register'>
          <li className='p-4'>Signup</li>
        </Link>
      </ul>
    </div>
  )
}

export default Navbar
