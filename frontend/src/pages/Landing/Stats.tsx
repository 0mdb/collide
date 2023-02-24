import { ProjectName, StatsPunchline, Stat1Label, Stat1Value, Stat2Label, Stat2Value, Stat3Label, Stat3Value  } from '../../assets/landing_strings.tsx'

export default function Stats() {
  return (
    <div className='bg-secondary-l dark:bg-secondary'>
      <div className='mx-auto max-w-7xl py-12 px-6 sm:py-16 lg:px-8 lg:py-20'>
        <div className='mx-auto max-w-4xl text-center'>
          <h2 className='text-3xl font-bold tracking-tight text-primary-d dark:text-primary-d sm:text-4xl'>
          <ProjectName />
          </h2>
          <p className='mt-3 text-xl text-secondary-l-text dark:text-secondary-text sm:mt-4'>
            <StatsPunchline />
          </p>
        </div>
        <dl className='mt-10 text-center sm:mx-auto sm:grid sm:max-w-3xl sm:grid-cols-3 sm:gap-8'>
          <div className='flex flex-col'>
            <dt className='order-2 mt-2 text-lg font-medium leading-6 text-secondary-l-text dark:text-secondary-text'>
            <Stat1Label />
            </dt>
            <dd className='order-1 text-5xl font-bold tracking-tight text-primary-d dark:text-primary-d'>
            <Stat1Value />
            </dd>
          </div>
          <div className='mt-10 flex flex-col sm:mt-0'>
            <dt className='order-2 mt-2 text-lg font-medium leading-6 text-secondary-l-text dark:text-secondary-text'>
            <Stat2Label />
            </dt>
            <dd className='order-1 text-5xl font-bold tracking-tight text-primary-d dark:text-primary-d'>
            <Stat2Value />
            </dd>
          </div>
          <div className='mt-10 flex flex-col sm:mt-0'>
            <dt className='order-2 mt-2 text-lg font-medium leading-6 text-secondary-l-text dark:text-secondary-text'>
            <Stat3Label />
            </dt>
            <dd className='order-1 text-5xl font-bold tracking-tight text-primary-d dark:text-primary-d'>
            <Stat3Value />
            </dd>
          </div>
        </dl>
      </div>
    </div>
  )
}
