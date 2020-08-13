from django.http.response import Http404
from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from follow_object.models import FollowObject
from follow_object.permissions import MustBeLoggedIn
from follow_object.serializers import FollowObjectSerializer
from user_profile.models import Profile
from user_profile.serializers import ProfileSerializer
from django.db.models import Q


class FollowObjectViewSet(
        viewsets.mixins.CreateModelMixin,
        viewsets.mixins.DestroyModelMixin,
        viewsets.GenericViewSet):
    queryset = FollowObject.objects.all()
    serializer_class = FollowObjectSerializer
    permission_classes = [MustBeLoggedIn]
    lookup_field = "username"

    def perform_create(self, serializer):
        serializer.save(following=self.request.user.profile)

    def get_object(self):
        """
        Override the default get_object() to return a FollowObject
        where the currently logged in user is following and user with
        the selected pk is being_followed

        In this case get_object() is only called when deleting a follow
        """
        try:
            return FollowObject.objects.get(
                following=self.request.user.profile,
                being_followed__user__username=self.kwargs['username'])
        except FollowObject.DoesNotExist:
            raise Http404

    def create(self, request, *args, **kwargs):
        """
        Override the default create method to return a custom
        response message
        """
        response = super().create(request, *args, **kwargs)
        if response.status_code == status.HTTP_201_CREATED:
            response.data = {"created": True}
        return response


class RecommendationsView(
        viewsets.mixins.ListModelMixin,
        viewsets.GenericViewSet):
    """
    View designed to return a list of recommended profiles
    that the user doesn't follow yet
    """
    permission_classes = [MustBeLoggedIn]
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def list(self, request, *args, **kwargs):
        profile = request.user.profile
        following = FollowObject.objects.filter(following=profile)
        # Query profiles that are not being followed and feed that to the
        # serializer (return full profiles not FollowObjects)
        following = Profile.objects.filter(~Q(user__username__in=following.values_list(
            'being_followed__user__username', flat=True)) & ~Q(user=profile.user)).order_by('-followers')

        # Apply pagination to the queryset
        following = self.paginate_queryset(following)
        following = ProfileSerializer(
            following, many=True, context={
                "request": request})
        return self.get_paginated_response(following.data)
