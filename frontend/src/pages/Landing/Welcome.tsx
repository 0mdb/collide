import React from 'react'

import CallToAction from './Cta'

import Stats from './Stats'
import Hero, { HeroSection } from './Hero'

export function Welcome() {
  return (
    <>
      <Hero />
      <CallToAction />
      <HeroSection />
      <Stats />
    </>
  )
}

export default Welcome
