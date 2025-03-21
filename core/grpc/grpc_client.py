import os

import grpc

from core.grpc import notification_pb2, notification_pb2_grpc


def send_notification(users):
    try:
        channel = grpc.insecure_channel(
            os.getenv("GRPC_SERVER")
        )  # Node.js gRPC server address
        stub = notification_pb2_grpc.NotificationServiceStub(channel)

        request = notification_pb2.NotificationRequest(users=users)

        response = stub.EmitNotification(request)
        print("Notification response: ", response)
        return response.status
    except grpc.RpcError as e:
        print(f"gRPC error: {e}")
