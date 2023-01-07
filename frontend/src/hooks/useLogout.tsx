import axios from '../api/axios'
import useAuth from './useAuth'
import cookie from 'js-cookie'

const useLogout = () => {
  const { setAuth } = useAuth()

  const logout = async () => {
    setAuth({}) // clear auth
    try {
      await axios.post('auth/cookie/logout', {
        withcredentials: true,
      }) // clear cookie
    } catch (err) {
      console.error(err)
    }
  }
  return logout
}

export default useLogout
