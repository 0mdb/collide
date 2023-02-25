import React from 'react'
import { Link } from 'react-router-dom'
import {
  HeroSectionPurpose,
  HeroSectionSolution,
  HeroSectionDescription,
  HeroSectionButton,
  HeroAccent,
  HeroPurpose,
  HeroDescription,
  HeroTarget,
  HeroButton
} from '../../assets/landing_strings.tsx'

const Hero = () => {
  return (
    <div>
      <div className='mx-auto mt-[-96px] flex h-screen w-full max-w-[800px] flex-col justify-center text-center'>
        <p className='text-xl p-2 font-bold text-primary dark:text-primary-l'>
          <HeroAccent />
        </p>
        <h1 className='text-4xl font-bold sm:text-6xl md:py-6 md:text-7xl'>
          <HeroPurpose />
        </h1>
        <div className='flex items-center justify-center'>
          <p className='py-4 text-xl font-bold sm:text-4xl md:text-5xl'>
            <HeroDescription />
          </p>
        </div>
        <p className='text-xl font-bold text-secondary-d dark:text-secondary md:text-2xl'>
          <HeroTarget />
        </p>
        <Link to='/home'>
          <button
              className='my-6 mx-auto w-[200px] border-2 py-3 font-medium
              border-primary bg-primary text-secondary-d-text rounded-md
              hover:border-primary-l hover:bg-primary-l hover:text-secondary-d-text hover:shadow-md
              dark:border-primary-l dark:bg-primary-l dark:text-secondary-d-text
              dark:md:hover:border-primary-d dark:md:hover:bg-primary-d'
            >
              <HeroButton />
          </button>
        </Link>
      </div>
    </div>
  )
}

export const HeroSection = () => {
  return (
    <div className='w-full py-16 px-4'>
      <div className='mx-auto grid max-w-[1240px] md:grid-cols-2'>
        <div className='flex flex-col justify-center'>
          <p className='text-xl font-bold text-primary dark:text-primary-l'>
            <HeroSectionPurpose />
          </p>
          <h1 className='py-2 text-2xl font-bold sm:text-3xl md:text-4xl text-secondary-l-text dark:text-secondary-d-text'>
            <HeroSectionSolution />
          </h1>
          <p className='py-2 text-lg sm:text-lg md:text-lg text-secondary-l-text dark:text-secondary-d-text'>
            <HeroSectionDescription />
          </p>

          <Link to='/home'>
            <button
              className='my-6 mx-auto w-[200px] border-2 py-3 font-medium
              border-primary bg-primary text-secondary-d-text rounded-md
              hover:border-primary-l hover:bg-primary-l hover:text-secondary-d-text hover:shadow-md
              dark:border-primary-l dark:bg-primary-l dark:text-secondary-d-text
              dark:md:hover:border-primary-d dark:md:hover:bg-primary-d'
            >
              <HeroSectionButton />
            </button>
          </Link>
        </div>
      </div>
    </div>
  )
}

export default Hero
