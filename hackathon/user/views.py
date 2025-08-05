
from django.contrib.auth.models import User

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import CreateAPIView



from user.serializers import CreateUserSerializer

class UserLoginView(TokenObtainPairView):
    pass

class UserRefreshView(TokenRefreshView):
    pass

class UserCreateView(CreateAPIView):
    serializer_class = CreateUserSerializer