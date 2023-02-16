export default function Stats() {
  return (
    <div className='bg-slate-300'>
      <div className='mx-auto max-w-7xl py-12 px-6 sm:py-16 lg:px-8 lg:py-20'>
        <div className='mx-auto max-w-4xl text-center'>
          <h2 className='text-3xl font-bold tracking-tight text-primary sm:text-4xl'>LobbyRadar</h2>
          <p className='mt-3 text-xl text-gray-600 sm:mt-4'>
            Just some wild people making politics more accessible
          </p>
        </div>
        <dl className='mt-10 text-center sm:mx-auto sm:grid sm:max-w-3xl sm:grid-cols-3 sm:gap-8'>
          <div className='flex flex-col'>
            <dt className='order-2 mt-2 text-lg font-medium leading-6 text-black'>Lobbyists</dt>
            <dd className='order-1 text-5xl font-bold tracking-tight dark:text-primary-d text-primary-l'>
              178,647
            </dd>
          </div>
          <div className='mt-10 flex flex-col sm:mt-0'>
            <dt className='order-2 mt-2 text-lg font-medium leading-6 text-black'>
              Tracked Donations
            </dt>
            <dd className='order-1 text-5xl font-bold tracking-tight text-primary-l dark:text-primary-d'>
              592,285,701
            </dd>
          </div>
          <div className='mt-10 flex flex-col sm:mt-0'>
            <dt className='order-2 mt-2 text-lg font-medium leading-6 text-black'>Legislation</dt>
            <dd className='order-1 text-5xl font-bold tracking-tight text-primary-l dark:text-primary-d'>
              6,761
            </dd>
          </div>
        </dl>
      </div>
    </div>
  )
}
