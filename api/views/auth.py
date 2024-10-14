from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import NotAuthenticated
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response

from api.serializers.auth import LoginUserSerializer, RegisterUserSerializer, UserAuthResponseSerializer
from authentication.services import AuthenticationService


@api_view(["POST"])
@permission_classes([AllowAny])
def register_user_via_email_password(request: Request):
    serializer = RegisterUserSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        AuthenticationService().register(
            email=serializer.validated_data["email"], password=serializer.validated_data["password"]
        )

        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["POST"])
@permission_classes([AllowAny])
def login_user_via_email_password(request: Request):
    serializer = LoginUserSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        _, token = AuthenticationService().login(
            email=serializer.validated_data["email"], password=serializer.validated_data["password"]
        )

        return Response(data=UserAuthResponseSerializer({"token": token}).data)


@api_view(["DELETE"])
@permission_classes([AllowAny])
def logout_user(request: Request):
    if not request.user.is_authenticated:
        raise NotAuthenticated

    AuthenticationService().logout(email=request.user.email)

    return Response(status=200)
