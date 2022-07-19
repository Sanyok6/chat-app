from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from rest_framework import permissions, status, views, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from messaging.models import ChatRoom
from messaging.serializers import ChatRoomSerializer
from . import serializers
from . import models


def get_full_data(user):
    return {
        "user": serializers.UserSerializer(user).data,
        "public_chats": ChatRoomSerializer(ChatRoom.objects.filter(is_public=True), many=True).data,
    }

class LoginView(views.APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        login_serializer = serializers.LoginSerializer(data=request.data)
        login_serializer.is_valid(raise_exception=True)

        user = authenticate(request, **login_serializer.data)

        if user is None:
            return Response({'detail': 'Account with the given credentials does not exist'},
                            status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        if not user.is_active:
            return Response({'detail': 'User is not active'}, status=status.HTTP_401_UNAUTHORIZED)

        login(request, user)
        response = Response(get_full_data(user))
        response.set_cookie('isLoggedIn', 'yes', expires=settings.SESSION_COOKIE_AGE)

        return response


class SignupView(views.APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = serializers.UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        login(request, user)
        response = Response(get_full_data(user))
        response.set_cookie('isLoggedIn', 'yes', expires=settings.SESSION_COOKIE_AGE)
        return response


class LogoutView(views.APIView):
    def post(self, request):
        logout(request)
        response = Response(status=status.HTTP_204_NO_CONTENT)
        response.delete_cookie('isLoggedIn')
        return response


class UserViewSet(viewsets.ModelViewSet):
    http_method_names = ("get", "put", "patch", "delete", "options")
    queryset = models.CustomUser.objects.all()
    serializer_class = serializers.UserSerializer

    @action(methods=("GET",), detail=False, url_path="me")
    def get_current_user_data(self, request):
        return Response(get_full_data(request.user))
