from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics
from user_profile.serializers import UserSerializer
from rest_framework import viewsets


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    ordering = ['id']
