from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions

from follow_object.models import FollowObject
from user_profile.models import Profile
from user_profile.permissions import CanOnlyEditYourself
from user_profile.serializers import ProfileSerializer
from tweet_object.models import TweetObject
from tweet_object.serializers import TweetObjectSerializer


class ProfileViewSet(viewsets.GenericViewSet,
                     mixins.CreateModelMixin,
                     mixins.DestroyModelMixin,
                     mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin):
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
        # Query profiles that are following the selected user and
        # feed that to the serializer (return full profiles not FollowObjects)
        followers = Profile.objects.filter(
            user__username__in=followers.values_list(
                'following__user__username', flat=True))

        # Apply pagination to the queryset
        followers = self.paginate_queryset(followers)
        followers = ProfileSerializer(followers, many=True)
        return self.get_paginated_response(followers.data)

    @action(detail=True, methods=["GET"])
    def following(self, request, *args, **kwargs):
        # This will return a list of profiles that
        # are being followed by the selected user

        profile = self.get_object()
        following = FollowObject.objects.filter(following=profile)
        # Query profiles that are being followed and feed that to the
        # serializer (return full profiles not FollowObjects)
        following = Profile.objects.filter(
            user__username__in=following.values_list(
                'being_followed__user__username', flat=True))

        # Apply pagination to the queryset
        following = self.paginate_queryset(following)
        following = ProfileSerializer(following, many=True)
        return self.get_paginated_response(following.data)

    @action(detail=True, methods=["GET"])
    def tweets(self, request, *args, **kwargs):
        # This will return a list of tweets created
        # by the selected user

        profile = self.get_object()
        tweets = TweetObject.objects.filter(author=profile)

        # Apply pagination to the queryset
        tweets = self.paginate_queryset(tweets)
        tweets = TweetObjectSerializer(tweets, many=True)
        return self.get_paginated_response(tweets.data)

    def update(self, request, *args, **kwargs):
        # PUT requests are not allowed
        if not kwargs.get('partial'):
            raise MethodNotAllowed("PUT", "Use PATCH instead")
        return super().update(request, *args, **kwargs)


class MyProfileView(APIView):
    """
    View designed to return information about the currently logged in user
    """
    permission_classes = [permissions.IsAuthenticated]
    queryset = Profile.objects.all()

    def get(self, request, *args, **kwargs):
        user = request.user.profile
        user = ProfileSerializer(user)
        return Response(user.data)
