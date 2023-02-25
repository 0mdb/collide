import React from 'react'
import { Link } from 'react-router-dom'
import { FaFacebookSquare, FaGithubSquare, FaInstagram, FaTwitterSquare } from 'react-icons/fa'

const Footer = () => {
  return (
    <div className='mx-auto grid max-w-[1240px] gap-8 py-16 px-4 lg:grid-cols-3'>
      <div>
        <h1 className='w-full text-3xl font-bold'>LobbyRadar</h1>
        <p className='py-4'>
          Easily navigate through vast amounts of lobbying data with LobbyRadar's powerful analytics
          dashboard, powered by force graphs and AI.
        </p>
        <div className='my-6 flex justify-between md:w-[75%]'>
          <FaFacebookSquare size={30} />
          <FaInstagram size={30} />
          <FaTwitterSquare size={30} />
          <FaGithubSquare size={30} />
        </div>
      </div>
      <div className='mt-6 flex justify-between lg:col-span-2'>
        <div>
          <h6 className='font-medium'>Solutions</h6>
          <ul>
            <Link to='/'>
              <li className='py-2'>Home</li>
            </Link>
            <Link to='/apinotify'>
              <li className='py-2 text-sm'>API</li>
            </Link>
          </ul>
        </div>
        <div>
          <h6 className='font-medium'>Support</h6>
          <ul>
            <Link to='/faq'>
              <li className='py-2 text-sm'>FAQ</li>
            </Link>
            <Link to='/contact'>
              <li className='py-2 text-sm'>Contact</li>
            </Link>
          </ul>
        </div>
        <div>
          <h6 className='font-medium'>Company</h6>
          <ul>
            <Link to='/about'>
              <li className='py-2 text-sm'>About</li>
            </Link>
            <li className='py-2 text-sm text-gray-400'>Blog</li>
          </ul>
        </div>
        <div>
          <h6 className='font-medium'>Legal</h6>
          <ul>
            <Link to='/privacypolicy'>
              <li className='py-2 text-sm'>Privacy Policy</li>
            </Link>
            <Link to='/termsofuse'>
              <li className='py-2 text-sm'>Terms of Use</li>
            </Link>
            <Link to='/opensource'>
              <li className='py-2 text-sm'>Open Source</li>
            </Link>
          </ul>
        </div>
      </div>
    </div>
  )
}

export default Footer
