import React from 'react'
import Footer from './Footer'
import Navbar from './Nav'
import {
  FaqHeader,
  FaqQ1,
  FaqA1,
  FaqQ2,
  FaqA2,
  FaqQ3,
  FaqA3,
  FaqQ4,
  FaqA4,
  FaqQ5,
  FaqA5,
} from '../../assets/landing_faq.tsx'

const faqs = [
  {
    id: 1,
    question: <FaqQ1 />,
    answer: <FaqA1 />,
  },

  {
    id: 2,
    question: <FaqQ2 />,
    answer: <FaqA2 />,
  },

  {
    id: 3,
    question: <FaqQ3 />,
    answer: <FaqA3 />,
  },

  {
    id: 4,
    question: <FaqQ4 />,
    answer: <FaqA4 />,
  },

  {
    id: 5,
    question: <FaqQ5 />,
    answer: <FaqA5 />,
  },
]

function FAQ() {
  return (
    <div className='bg-secondary-l dark:bg-secondary'>
      <div className='mx-auto max-w-7xl divide-y divide-gray-900/10 px-6 py-24 sm:py-32 lg:py-40 lg:px-8'>
        <h2 className='text-2xl font-bold leading-10 tracking-tight text-secondary-l-text dark:text-secondary-text'>
          <FaqHeader />
        </h2>
        <dl className='mt-10 space-y-8 divide-y divide-gray-900/10'>
          {faqs.map((faq) => (
            <div key={faq.id} className='pt-8 lg:grid lg:grid-cols-12 lg:gap-8'>
              <dt className='text-base font-semibold leading-7 text-secondary-l-text dark:text-secondary-text lg:col-span-5'>
                {faq.question}
              </dt>
              <dd className='mt-4 lg:col-span-7 lg:mt-0'>
                <p className='text-base leading-7 text-gray-600 dark:text-secondary-text'>
                  {faq.answer}
                </p>
              </dd>
            </div>
          ))}
        </dl>
      </div>
    </div>
  )
}

function FAQLanding() {
  return (
    <div className='bg-secondary dark:bg-secondary-d'>
      <FAQ />
    </div>
  )
}

export default FAQLanding
