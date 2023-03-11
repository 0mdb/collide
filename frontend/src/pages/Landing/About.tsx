import React from 'react'

function AboutLayout() {
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
            At LobbyRadar, we believe in the power of data to help people understand the
            complexities of lobbying activities. Our mission is to make it easy for anyone to
            navigate through vast amounts of government data related to lobbying activities and to
            provide meaningful insights into the people, organizations, and issues involved.
          </p>

          <p>
            We built LobbyRadar to provide a comprehensive lobbying information resource to
            researchers, students, journalists, and anyone who wants to explore the influence of
            lobbying on Canadian politics. Our cutting-edge technology combines the power of force
            graphs and AI to give you a new way to understand and interact with government data.
          </p>

          <p>
            LobbyRadar is committed to transparency and accountability in lobbying activities. We
            believe that everyone should have access to information on who is lobbying, on what
            issues, and how much money is involved. With LobbyRadar, you can monitor the latest
            lobbying trends, track specific organizations or issues, and stay informed about the
            influence of lobbying on government decision-making.
          </p>
        </div>
      </div>
    </div>
  )
}

function About() {
  return (
    <div>
      <AboutLayout />
    </div>
  )
}

export default About
