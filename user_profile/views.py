from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics
from user_profile.serializers import ProfileSerializer
from user_profile.models import Profile
from rest_framework import viewsets
from user_profile.permissions import CanOnlyEditYourself


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    ordering = ['id']
    permission_classes = [CanOnlyEditYourself]
