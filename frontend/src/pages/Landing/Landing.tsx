import React from 'react'
import Footer from './Footer'
import Navbar from './Nav'

import CallToAction from './Cta'

import Stats from './Stats'
import Hero, { HeroSection } from './Hero'
import { Outlet } from 'react-router-dom'

function Landing() {
  return (
    <div className='bg-gray-400 dark:bg-gray-700'>
      <Navbar />
      <Outlet />
      <Hero />
      <CallToAction />
      <HeroSection />
      <Stats />
      <Footer />
    </div>
  )
}

export default Landing
