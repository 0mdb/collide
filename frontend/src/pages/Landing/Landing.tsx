import React from 'react'
import Analytics from './Analytics'
import Footer from './Footer'
import Hero from './Hero'
import Navbar from './Nav'
import Newsletter from './Newsletter'

function Landing() {
  return (
    <div className='bg-gray-400 dark:bg-gray-700'>
      <Navbar />
      <Hero />
      <Analytics />
      <Newsletter />
      {/* <Cards /> */}
      <Footer />
    </div>
  )
}

export default Landing
