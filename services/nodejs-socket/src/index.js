import dotenv from 'dotenv';
import grpc from '@grpc/grpc-js';
import { app, server, grpcServer } from './socket/index.js';

dotenv.config();

const grpcPort = process.env.GRPC_PORT || 50051;

grpcServer.bindAsync(`0.0.0.0:${grpcPort}`, grpc.ServerCredentials.createInsecure(), (err, port) => {
    if (err) {
        // Catch errors during binding
        console.error(`Failed to bind gRPC server: ${err.message}`);
        return;
    }
    console.log(`gRPC server running on 0.0.0.0:${port}`);
});

const port = process.env.PORT || 9000;

server.listen(port, async () => {
    console.log(`Serving on port .....${port}`);
});
