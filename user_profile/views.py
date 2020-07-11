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
        # This will return a list of profiles that
        # follow the selected user

        profile = self.get_object()
        followers = FollowObject.objects.filter(being_followed=profile)

        # Apply pagination to the queryset
        followers = self.paginate_queryset(followers)
        followers = FollowingSerializer(followers, many=True)
        return self.get_paginated_response(followers.data)

    @action(detail=True, methods=["GET"])
    def following(self, request, *args, **kwargs):
        # This will return a list of profiles that
        # are being followed by the selected user

        profile = self.get_object()
        following = FollowObject.objects.filter(following=profile)

        # Apply pagination to the queryset
        following = self.paginate_queryset(following)
        following = BeingFollowedSerializer(following, many=True)
        return self.get_paginated_response(following.data)
