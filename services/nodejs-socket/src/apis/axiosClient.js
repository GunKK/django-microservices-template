import axios from 'axios'


const axiosClient = axios.create({
  baseURL: process.env.BE_APP_SERVER_URL,
  headers: {
    "Content-Type": "application/json",
  },
  withCredentials: true,
})


axiosClient.interceptors.request.use(async (config) => {
  const accessToken = config.token;
  config.headers.Authorization = `Bearer ${accessToken}`;
  return config;
});


axiosClient.interceptors.response.use(
  (res) => res.data,
  (err) => {
    console.log(err)
    return Promise.reject({
        status: false,
        message: err.message,
        data: undefined,
      });
  }
)


export default axiosClient