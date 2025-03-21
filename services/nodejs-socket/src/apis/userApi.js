import axiosClient from "./axiosClient.js";

const userApi = {
  getAll: (token) => {
    const url = `${process.env.BE_APP_SERVER_URL}/users/`;
    return axiosClient.get(url,{ token });
  },
};

export default userApi;
