import { getMe } from '../api/authApi'
import useAuth from '../hooks/useAuth'

const useCurrentUser = () => {
  const { auth, setUser } = useAuth()

  const userData = async () => {
    const { data } = await getMe(auth)

    setUser((prev) => {
      console.log(prev)
      return { ...prev, user: data }
    })
    return data
  }
  return userData
}

export default useCurrentUser
