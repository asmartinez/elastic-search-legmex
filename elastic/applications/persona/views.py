from django.shortcuts import render

from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    RetrieveAPIView,
    DestroyAPIView,
    UpdateAPIView,
    RetrieveUpdateAPIView,

    
)

from .models import User

from .serializer import UserSerializer

# Create your views here.

class UserListApiView(ListAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.all()


class UserCreateView(CreateAPIView):
    serializer_class = UserSerializer

class UserDetailView(RetrieveAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.filter()

class UserDeleteView(DestroyAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserUpdateView(UpdateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserRetriveUpdateView(RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    



