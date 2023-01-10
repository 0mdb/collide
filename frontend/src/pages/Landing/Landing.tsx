import React, { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { Icon } from '@blueprintjs/core'
import Analytics from './Analytics'
import Cards from './Cards'
import Footer from './Footer'
import Hero from './Hero'
import Navbar from './Nav'
import Newsletter from './Newsletter'

function Landing() {
  return (
    <div className='landing'>
      <Navbar />
      {/* <Hero /> */}
      <Analytics />
      <Newsletter />
      {/* <Cards /> */}
      <Footer />
    </div>
  )
}

export default Landing
