import React from 'react'

const Analytics = () => {
  return (
    <div className='w-full bg-white py-16 px-4'>
      <div className='mx-auto grid max-w-[1240px] md:grid-cols-2'>
        <img className='mx-auto my-4 w-[500px]' alt='/' />
        <div className='flex flex-col justify-center'>
          <p className='font-bold text-[#00df9a] '>DATA ANALYTICS DASHBOARD</p>
          <h1 className='py-2 text-2xl font-bold sm:text-3xl md:text-4xl'>
            Manage Data Analytics Centrally
          </h1>
          <p>
            Lorem ipsum dolor sit amet consectetur adipisicing elit. Voluptatum molestiae delectus
            culpa hic assumenda, voluptate reprehenderit dolore autem cum ullam sed odit
            perspiciatis. Doloribus quos velit, eveniet ex deserunt fuga?
          </p>
          <button className='my-6 mx-auto w-[200px] rounded-md bg-black py-3 font-medium text-[#00df9a] md:mx-0'>
            Get Started
          </button>
        </div>
      </div>
    </div>
  )
}

export default Analytics
