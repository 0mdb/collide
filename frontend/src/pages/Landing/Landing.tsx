import React from 'react'
import Analytics, { LobbyRadar } from './Analytics'
import Footer from './Footer'
import Hero, { HeroSection } from './Hero'
import Navbar from './Nav'
import Newsletter from './Newsletter'
import Stats from './Stats'

function Landing() {
  return (
    <div className='bg-gray-400 dark:bg-gray-700'>
      <Navbar />
      <HeroSection />
      <Hero />
      <Stats />
      {/* <Analytics /> */}
      {/* <Newsletter /> */}
      {/* <Cards /> */}
      <Footer />
    </div>
  )
}

export default Landing
