from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics
from user_profile.serializers import ProfileSerializer
from user_profile.models import Profile
from rest_framework import viewsets
from user_profile.permissions import CanOnlyEditYourself
from rest_framework.response import Response
from rest_framework.decorators import action
from follow_object.models import FollowObject
from follow_object.serializers import FollowingSerializer, BeingFollowedSerializer


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    ordering = ['id']
    permission_classes = [CanOnlyEditYourself]

    @action(detail=True, methods=["GET"])
    def followers(self, request, *args, **kwargs):
        """
        Get and serialize a list of FollowObject objects where the selected
        user is being followed
        """
        profile = self.get_object()
        followers = FollowObject.objects.filter(being_followed=profile)
        followers = FollowingSerializer(followers, many=True)
        return Response(followers.data)

    @action(detail=True, methods=["GET"])
    def following(self, request, *args, **kwargs):
        """
        Get and serialize a list of FollowObject objects where the selected
        user is the follower
        """
        profile = self.get_object()
        following = FollowObject.objects.filter(following=profile)
        following = BeingFollowedSerializer(following, many=True)
        return Response(following.data)
