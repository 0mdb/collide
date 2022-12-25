import { useContext } from 'react'
import AuthContext from '../context/AuthProvider'

type Auth = {
    auth: {
        token: string
        user: {
            id: string
            name: string
            email: string
            avatar: string
        }
    }
}
const useAuth = () => useContext(AuthContext) as Auth
// const useAuth = () => useContext(AuthContext)

export default useAuth
