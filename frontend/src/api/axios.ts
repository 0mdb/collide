import axios from 'axios';
const BASE_URL = 'http://localhost/api'

export default axios.create({
  baseURL: BASE_URL
});

export const axiosPrivate = axios.create({
  baseURL: BASE_URL,
  headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
  withCredentials: true

});
