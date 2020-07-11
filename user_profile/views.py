from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework import generics, viewsets
from rest_framework.decorators import action
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.response import Response

from follow_object.models import FollowObject
from follow_object.serializers import (BeingFollowedSerializer,
                                       FollowingSerializer)
from user_profile.models import Profile
from user_profile.permissions import CanOnlyEditYourself
from user_profile.serializers import ProfileSerializer


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [CanOnlyEditYourself]
    parser_classes = [JSONParser, MultiPartParser]
    lookup_field = "user__username"

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
