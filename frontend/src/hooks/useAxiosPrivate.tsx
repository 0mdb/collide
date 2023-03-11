import { axiosPrivate } from '../api/axios'
import { useEffect } from 'react'
import { useAuthHeader } from 'react-auth-kit'

const useAxiosPrivate = () => {
  const authHeader = useAuthHeader()
  const auth = authHeader()

  useEffect(() => {
    const requestIntercept = axiosPrivate.interceptors.request.use(
      (config) => {
        console.log('config', config)
        if (!config.headers['Authorization']) {
          config.headers['Authorization'] = `${auth}`
        }
        return config
      },
      (error) => Promise.reject(error),
    )

    return () => {
      axiosPrivate.interceptors.request.eject(requestIntercept)
    }
  }, [auth])

  return axiosPrivate
}

export default useAxiosPrivate
