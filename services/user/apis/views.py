from django.contrib.auth import authenticate
from drf_spectacular.utils import extend_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView
from core.jwt import MyTokenObtainPairSerializer

from core.serializers.user_serializers import (
    RefreshTokenSerializer,
    RegisterUserSerializer,
    UserLoginSerializer,
    UserSerializerWithToken,
)
from core.utils import global_response_errors

from .documents import (
    login_user_document,
    refresh_token_document,
    register_user_document,
)


class AuthenViewSet(viewsets.ViewSet):
    @extend_schema(**register_user_document)
    @action(detail=False, methods=["post"], url_path="register")
    def create_user(self, request):
        serializer = RegisterUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            return Response(
                {
                    "status": True,
                    "message": "User created successfully!",
                },
                status=status.HTTP_201_CREATED,
            )

        return global_response_errors(serializer.errors)


    @extend_schema(**login_user_document)
    @action(methods=["post"], detail=False, url_path="login")
    def login_user(self, request):
        serializer = UserLoginSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            user = authenticate(
                request,
                username=serializer.validated_data["username"].lower(),
                password=serializer.validated_data["password"],
            )
            if user:
                refresh = MyTokenObtainPairSerializer.get_token(user)
                return Response(
                    {
                        "status": True,
                        "data": UserSerializerWithToken(
                            user,
                            context={
                                "access_token": str(refresh.access_token),
                                "refresh_token": str(refresh),
                            },
                        ).data,
                        "message": "Login successfully!",
                    },
                    status=status.HTTP_200_OK,
                )

            return Response(
                {"status": False, "message": "Username or password is incorrect!"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        return global_response_errors(serializer.errors)


    @action(methods=["post"], detail=False, url_path="logout")
    def logout_user(self, request):
        try:
            refresh_token = RefreshToken(request.data.get("refresh_token"))
            if not refresh_token:
                raise AuthenticationFailed("No refresh token provided.")
            request.user.set_new_token_version()
            refresh_token.blacklist()
            return Response(
                {"status": True, "message": "Logout successfully!"},
                status=status.HTTP_200_OK,
            )
        except TokenError as e:
            raise AuthenticationFailed(f"{str(e)}!")
        except InvalidToken as e:
            raise AuthenticationFailed(f"{str(e)}!")



# refresh token view
class CustomTokenRefreshView(TokenRefreshView):
    @extend_schema(**refresh_token_document)
    def post(self, request, *args, **kwargs):
        serializer = RefreshTokenSerializer(data=request.data)
        if serializer.is_valid():
            access_token = serializer.validated_data["access_token"]
            refresh_token = serializer.validated_data.get("refresh_token")
            user = serializer.validated_data.get("user")

            return Response(
                {
                    "status": True,
                    "data": UserSerializerWithToken(
                        user,
                        context={
                            "access_token": str(access_token),
                            "refresh_token": str(refresh_token),
                        },
                    ).data,
                    "message": "Refresh token successfully!",
                },
                status=status.HTTP_200_OK,
            )

        return global_response_errors(serializer.errors)
