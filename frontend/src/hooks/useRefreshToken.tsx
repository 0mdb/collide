import axios from '../api/axios';
import useAuth from './useAuth';

const REFRESH_URL = '/login/access-token';

const useRefreshToken = () => {
  const { setAuth, auth } = useAuth();

  const refresh = async () => {
    const formData = new FormData();
    formData.append('grant_type', "refresh_token");
    formData.append('refresh_token', auth?.accessToken);

    const response = await axios.post(REFRESH_URL, formData, {
      headers: {
        'Content-Type': 'www-form-urlencoded',
      },
      withCredentials: true,
    });
    setAuth((prev) => {
      return {
        ...prev,
        roles: response.data.roles,
        refreshToken: response.data.refresh_token,
      };
    });
    return response.data.refresh_token;
  };
  return refresh;
};

export default useRefreshToken;
