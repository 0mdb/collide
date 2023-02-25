import React from 'react'
import Footer from './Footer'
import Navbar from './Nav'

import CallToAction from './Cta'

import Stats from './Stats'
import Hero, { HeroSection } from './Hero'

function Landing() {
  return (
    <div className='bg-secondary dark:bg-secondary-d'>
      <Navbar />
      <Hero />
      <CallToAction />
      <HeroSection />
      <Stats />
      <Footer />
    </div>
  )
}

export default Landing
