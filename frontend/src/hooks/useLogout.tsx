import axios from '../api/axios'
import useAuth from './useAuth'

const useLogout = () => {
  const { setAuth } = useAuth()

  const logout = async () => {
    // setAuth({}) // clear auth
    try {
      const response = await axios.post('auth/cookie/logout', {
        withcredentials: true,
      })
    } catch (err) {
      console.error(err)
    }
  }
  return logout
}

export default useLogout
