import React from 'react'
import { Link } from 'react-router-dom'

const Hero = () => {
  return (
    <div>
      <div className='mx-auto mt-[-96px] flex h-screen w-full max-w-[800px] flex-col justify-center text-center'>
        <p className='p-2 font-bold text-primary dark:text-primary-l'>
          Lobbying Information Resource
        </p>
        <h1 className='text-4xl font-bold sm:text-6xl md:py-6 md:text-7xl'>
          EXPLORE CANADIAN LOBBYING
        </h1>
        <div className='flex items-center justify-center'>
          <p className='py-4 text-xl font-bold sm:text-4xl md:text-5xl'>
            API for Goverment lobbying data in Canada for
          </p>
        </div>
        <p className='text-xl font-bold text-gray-500 md:text-2xl'>
          Researchers, journalists, and the public
        </p>
        <Link to='/home'>
          <button
            className='my-6 mx-auto w-[200px] border-2 border-primary bg-primary
                         hover:bg-primary-l hover: text-primary hover:border-primary-l
                         hover:shadow-md rounded-md py-3 font-medium text-morp
                         dark:bg-primary-d dark:text-white
                             rounded-md bg-primary dark:bg-primary-d py-3 font-medium text-morp'
          >
            Get Started
          </button>
        </Link>
      </div>
    </div>
  )
}

export const HeroSection = () => {
  return (
    <div className='w-full bg-white py-16 px-4 dark:bg-gray-600'>
      <div className='mx-auto grid max-w-[1240px] md:grid-cols-2'>
        <div className='flex flex-col justify-center'>
          <p className='font-bold text-primary dark:text-secondary-l dark:text-primary-d'>
            EXPLORE CANADIAN LOBBYING ACTIVITIES
          </p>
          <h1 className='py-2 text-2xl font-bold sm:text-3xl md:text-4xl'>
            LobbyRadar - Your Comprehensive Lobbying Information Resource
          </h1>
          <p>
            At LobbyRadar, we provide a powerful data analytics dashboard to help you easily
            navigate through vast amounts of government data related to lobbying activities. Our
            cutting-edge technology combines the power of force graphs and AI to give you a new way
            to understand and interact with government data. Whether you're a researcher, student,
            or just curious about lobbying, our website is the perfect tool for you. Sign up today
            and start exploring!
          </p>

          <Link to='/home'>
            <button
              className='my-6 mx-auto w-[200px] border-2 border-primary bg-primary
                         hover:bg-primary-l hover: text-primary hover:border-primary-l
                         hover:shadow-md rounded-md py-3 font-medium text-morp
                         dark:bg-primary-d dark:text-white
                             rounded-md bg-primary dark:bg-primary-d py-3 font-medium text-morp'
            >
              Get Started
            </button>
          </Link>
        </div>
      </div>
    </div>
  )
}

export default Hero
