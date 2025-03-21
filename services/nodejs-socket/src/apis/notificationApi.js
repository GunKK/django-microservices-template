import axiosClient from "./axiosClient.js";

const notificaitonsApi = {
  create: (token) => {
    const url = `${process.env.BE_APP_SERVER_URL}/notifications/`;
    return axiosClient.post(url, { token });
  },
};

export default notificaitonsApi;
