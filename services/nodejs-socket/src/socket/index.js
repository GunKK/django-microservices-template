import { Server } from 'socket.io';
import grpc from '@grpc/grpc-js';
import protoLoader from '@grpc/proto-loader';
import path, { dirname } from 'path';
import { fileURLToPath } from 'url';
import http from 'http'
import morgan from 'morgan'
import express from 'express';
import dotenv from 'dotenv';
import { verifyTokenSocket } from "../utils/auth.js"
import userApi from '../apis/userApi.js';
import { getToken } from '../utils/common.js';
import { NOTIFICATION_TYPE } from '../utils/constans.js';
import NotificationEvent from '../classes/NotificationsEvent.js';
dotenv.config();

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const PROTO_PATH = '../proto/notification.proto';
const packageDefinition = protoLoader.loadSync(path.join(__dirname, PROTO_PATH), {
  keepCase: true,
  longs: String,
  enums: String,
  defaults: true,
  oneofs: true
});
const notificationProto = grpc.loadPackageDefinition(packageDefinition).NotificationService;

const app = express();

const server = http.createServer(app);
const io = new Server(server, {
    pingTimeout: 60000,
    cors: {
        origin: ["*"],
        methods: ['GET', 'POST', 'PUT', 'PATCH'],
    },
});

if (process.env.NODE_ENV !== 'development') {
    app.use(morgan.dev);
}
io.use(verifyTokenSocket)
io.on('connection', (socket)=>{
    socket.join(`user:${socket.user.user_id}`);
    console.log(`user with id ${socket.user.user_id} connected`);

    // ==================================global =================================

    socket.on('globalNotify', async (res) => {
        try {
            const token = getToken(socket)
            const data = {
                message: res?.data?.message ?? "Notification System!"
            }
            const receivers = await userApi.getAll(token);
            const receiverIds = receivers.data.filter(user => user.id !== socket.user.user_id).map(user => user.id)
            if (receiverIds.length > 0) {
                const notification = new NotificationEvent(token, data, receiverIds, NOTIFICATION_TYPE.SYSTEM_NOTIFICATION);
                await notification.create();

                io.emit("myNotification", { data: { change: 1 } })
            }
        } catch (err) {
            console.log(err);
        }
    });

    socket.on('disconnect', (socket) => {
        console.log(`User with SID ${socket?.id} disconnected`);
        console.log(socket?.user);
        console.log(`Socket ${socket?.id} left room: ${socket?.user?.user_id}`);
    });
})

const emitNotification = (call, callback) => {
    const { users } = call.request;

    const notificationPromises = users.map(userId =>
        new Promise(resolve => {
            io.to(`user:${userId}`).emit("myNotification", { data: { change: 1 } });
            resolve();
        })
    );
    Promise.all(notificationPromises);

    // Respond to gRPC client (Django)
    callback(null, { status: true, message: 'Notification grpc sent successfully' });
};

const grpcServer = new grpc.Server();

grpcServer.addService(notificationProto.service, { emitNotification: emitNotification });

export { app, io, server, grpcServer };
