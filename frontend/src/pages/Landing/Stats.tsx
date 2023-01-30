export default function Stats() {
  return (
    <div className='bg-slate-300'>
      <div className='mx-auto max-w-7xl py-12 px-6 sm:py-16 lg:px-8 lg:py-20'>
        <div className='mx-auto max-w-4xl text-center'>
          <h2 className='text-3xl font-bold tracking-tight text-black sm:text-4xl'>
            Trusted by developers from over 80 planets
          </h2>
          <p className='mt-3 text-xl text-morp sm:mt-4'>
            Lorem ipsum dolor, sit amet consectetur adipisicing elit. Repellendus repellat
            laudantium.
          </p>
        </div>
        <dl className='mt-10 text-center sm:mx-auto sm:grid sm:max-w-3xl sm:grid-cols-3 sm:gap-8'>
          <div className='flex flex-col'>
            <dt className='order-2 mt-2 text-lg font-medium leading-6 text-morp'>Pepperoni</dt>
            <dd className='order-1 text-5xl font-bold tracking-tight dark:text-primary-d text-primary-l'>
              100%
            </dd>
          </div>
          <div className='mt-10 flex flex-col sm:mt-0'>
            <dt className='order-2 mt-2 text-lg font-medium leading-6 text-morp'>Delivery</dt>
            <dd className='order-1 text-5xl font-bold tracking-tight text-primary-l dark:text-primary-d'>
              24/7
            </dd>
          </div>
          <div className='mt-10 flex flex-col sm:mt-0'>
            <dt className='order-2 mt-2 text-lg font-medium leading-6 text-morp'>Calories</dt>
            <dd className='order-1 text-5xl font-bold tracking-tight text-primary-l dark:text-primary-d'>
              100k+
            </dd>
          </div>
        </dl>
      </div>
    </div>
  )
}
