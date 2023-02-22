import React from 'react'
import Footer from './Footer'
import Navbar from './Nav'

/*
  This example requires some changes to your config:
  
  ```
  // tailwind.config.js
  module.exports = {
    // ...
    plugins: [
      // ...
      require('@tailwindcss/typography'),
    ],
  }
  ```
*/
function LegalLayout() {
  return (
    <div className='relative overflow-hidden bg-white py-16'>
      <div className='hidden lg:absolute lg:inset-y-0 lg:block lg:h-full lg:w-full lg:[overflow-anchor:none]'>
        <div className='relative mx-auto h-full max-w-prose text-lg' aria-hidden='true'>
          <svg
            className='absolute top-12 left-full translate-x-32 transform'
            width={404}
            height={384}
            fill='none'
            viewBox='0 0 404 384'
          >
            <defs>
              <pattern
                id='74b3fd99-0a6f-4271-bef2-e80eeafdf357'
                x={0}
                y={0}
                width={20}
                height={20}
                patternUnits='userSpaceOnUse'
              >
                <rect
                  x={0}
                  y={0}
                  width={4}
                  height={4}
                  className='text-gray-200'
                  fill='currentColor'
                />
              </pattern>
            </defs>
            <rect width={404} height={384} fill='url(#74b3fd99-0a6f-4271-bef2-e80eeafdf357)' />
          </svg>
          <svg
            className='absolute top-1/2 right-full -translate-y-1/2 -translate-x-32 transform'
            width={404}
            height={384}
            fill='none'
            viewBox='0 0 404 384'
          >
            <defs>
              <pattern
                id='f210dbf6-a58d-4871-961e-36d5016a0f49'
                x={0}
                y={0}
                width={20}
                height={20}
                patternUnits='userSpaceOnUse'
              >
                <rect
                  x={0}
                  y={0}
                  width={4}
                  height={4}
                  className='text-gray-200'
                  fill='currentColor'
                />
              </pattern>
            </defs>
            <rect width={404} height={384} fill='url(#f210dbf6-a58d-4871-961e-36d5016a0f49)' />
          </svg>
          <svg
            className='absolute bottom-12 left-full translate-x-32 transform'
            width={404}
            height={384}
            fill='none'
            viewBox='0 0 404 384'
          >
            <defs>
              <pattern
                id='d3eb07ae-5182-43e6-857d-35c643af9034'
                x={0}
                y={0}
                width={20}
                height={20}
                patternUnits='userSpaceOnUse'
              >
                <rect
                  x={0}
                  y={0}
                  width={4}
                  height={4}
                  className='text-gray-200'
                  fill='currentColor'
                />
              </pattern>
            </defs>
            <rect width={404} height={384} fill='url(#d3eb07ae-5182-43e6-857d-35c643af9034)' />
          </svg>
        </div>
      </div>
      <div className='relative px-6 lg:px-8'>
        <div className='mx-auto max-w-prose text-lg'>
          <h1>
            <span className='block text-center text-lg font-semibold text-indigo-600'>
              Introducing
            </span>
            <span className='mt-2 block text-center text-3xl font-bold leading-8 tracking-tight text-gray-900 sm:text-4xl'>
              LobbyRadar
            </span>
          </h1>
        </div>
        <div className='prose prose-lg prose-indigo mx-auto mt-6 text-gray-500'>
          <p>
            Welcome to LobbyRadar, a website that provides free and open source public data to
            represent registered lobbying interactions on forcegraphs.
          </p>
          <h2>Disclaimer</h2>
          <p>
            Please note that the information presented on this website is for informational purposes
            only and should not be construed as legal advice. The website owner and any affiliates
            or representatives make no representations or warranties with respect to the accuracy or
            completeness of the content and will not be liable for any errors or omissions in this
            information. Any reliance on the information on this website is at your own risk.
            LobbyRadar does not guarantee that the website will be error-free, uninterrupted, or
            free of viruses or other harmful components. Please be aware that the content on this
            website may change at any time without notice. We recommend that you seek professional
            legal advice before taking any action based on the information presented on this
            website. By using this website, you acknowledge and agree to these terms and conditions.
          </p>

          <h2>Privacy</h2>
          <p>
            At LobbyRadar, we are committed to protecting the privacy and personal information of
            our users. This Privacy Policy explains how we collect, use, and protect the personal
            information that we receive from our users. Information Collection and Use: We collect
            personal information such as name and email address when users sign up for our service.
            This information is used to create user accounts, and to communicate with users about
            our service. We may also collect non-personal information such as IP address, browser
            type, and operating system. This information is used to help us understand how our
            service is being used and to improve our service. We will not share, sell, or rent
            personal information to third parties except in the following circumstances: With the
            user's consent To comply with legal requirements or to protect our legal rights In the
            event of a merger, acquisition, or sale of assets
          </p>

          <h2>Security</h2>
          <p>
            We take reasonable measures to protect personal information from unauthorized access,
            disclosure, alteration, and destruction. However, no method of transmission over the
            internet or electronic storage is completely secure.
          </p>
          <h2>Cookies</h2>
          <p>
            We may use cookies to store information about user preferences and to record
            user-specific information on visits and pages the user views.
          </p>

          <h2>Links to Other Sites</h2>
          <p>
            Our service may contain links to other websites that are not operated by us. We are not
            responsible for the content or privacy practices of these sites and encourage users to
            review the privacy policies of these sites.
          </p>

          <h2>Changes to this Privacy Policy</h2>
          <p>
            We reserve the right to modify this Privacy Policy at any time. If we make material
            changes, we will notify users via email or by posting a notice on our website.
          </p>

          <h2>Contact Us</h2>
          <p>
            If you have any questions or concerns about this Privacy Policy, please contact us at{' '}
            <a href='mailto: info@lobbyradar.io' className='text-indigo-600'></a>
          </p>
        </div>
      </div>
    </div>
  )
}

function Legal() {
  return (
    <div>
      <Navbar />
      <LegalLayout />
      <Footer />
    </div>
  )
}

export default Legal
