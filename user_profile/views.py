from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics
from user_profile.serializer import UserSerializer


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
