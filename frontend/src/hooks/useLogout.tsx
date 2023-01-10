// import axios from '../api/axios'
import useAuth from './useAuth'
import useAxiosPrivate from './useAxiosPrivate'

const useLogout = () => {
  const { setAuth } = useAuth()
  const axios = useAxiosPrivate()

  const logout = async () => {
    // setAuth({}) // clear auth
    try {
      await axios.post('auth/jwt/logout', null, {
        headers: {
          'Content-Type': 'application/json',
          // Cookie: 'fastapiusersauth=${TOKEN}',
        },
      }) // clear cookie
    } catch (err) {
      console.error(err)
    }
  }
  return logout
}

export default useLogout

// const logout = async () => {
//   axios
//     .post('http://localhost:8000/auth/cookie/logout', null, {
//       headers: {
//         Cookie: `fastapiusersauth=${TOKEN}`,
//       },
//     })
//     .then((response) => console.log(response))
//     .catch((error) => console.log(error))
//   return logout
// }
