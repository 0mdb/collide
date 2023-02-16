import React from 'react'
import {
  FaDribbbleSquare,
  FaFacebookSquare,
  FaGithubSquare,
  FaInstagram,
  FaTwitterSquare,
} from 'react-icons/fa'

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
          <FaDribbbleSquare size={30} />
        </div>
      </div>
      <div className='mt-6 flex justify-between lg:col-span-2'>
        <div>
          <h6 className='font-medium'>Solutions</h6>
          <ul>
            <li className='py-2 text-sm'>API</li>
            <li className='py-2 text-sm'>Consulting</li>
          </ul>
        </div>
        <div>
          <h6 className='font-medium'>Support</h6>
          <ul>
            <li className='py-2 text-sm'>Pricing</li>
            <li className='py-2 text-sm'>Documentation</li>
            <li className='py-2 text-sm'>Guides</li>
            <li className='py-2 text-sm'>API Status</li>
          </ul>
        </div>
        <div>
          <h6 className='font-medium'>Company</h6>
          <ul>
            <li className='py-2 text-sm'>About</li>
            <li className='py-2 text-sm'>Blog</li>
            <li className='py-2 text-sm'>Jobs</li>
            {/* <li className='py-2 text-sm'>Press</li> */}
            <li className='py-2 text-sm'>Join the Team</li>
          </ul>
        </div>
        <div>
          <h6 className='font-medium'>Legal</h6>
          <ul>
            <li className='py-2 text-sm'>Claim</li>
            <li className='py-2 text-sm'>Policy</li>
            <li className='py-2 text-sm'>Terms</li>
          </ul>
        </div>
      </div>
    </div>
  )
}

export default Footer
