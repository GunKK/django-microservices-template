import axiosClient from "./axiosClient.js";

const authApi = {
  me: (token) => {
    const url = `${process.env.BE_APP_SERVER_URL}/auth/me/`;
    return axiosClient.get(url, { token });
  },
};

export default authApi;
