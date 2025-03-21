import { io } from "../socket/index.js"

const getToken = (socket) => {
    return socket.handshake.auth.token;
}

export {
    getToken,
}
