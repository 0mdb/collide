import { Icon } from '@blueprintjs/core'

function FabButton(props) {
  const { classes, children, onClick, ...other } = props

  return (
    <div className='fixed bottom-0 right-0 mb-4 mr-4'>
      <button
        type='button'
        className='fixed z-90 bottom-10 border border-transparent right-8 bg-primary shadow-sm w-20 h-20 rounded-full drop-shadow-lg flex justify-center items-center text-white text-4xl hover:bg-blue-700 hover:drop-shadow-2xl focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2'
        onClick={() => props.setOpen(true)}
      >
        <Icon icon='search' size={20} className='fill-white' />
      </button>
    </div>
  )
}

export default FabButton
