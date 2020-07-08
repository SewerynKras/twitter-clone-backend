from django.shortcuts import render
from follow_object.models import FollowObject
from follow_object.serializers import FollowObjectSerializer
from rest_framework import viewsets
from follow_object.permissions import MustBeLoggedIn
from django.http.response import Http404
from rest_framework.permissions import IsAuthenticated


class FollowObjectViewSet(
        viewsets.mixins.CreateModelMixin,
        viewsets.mixins.DestroyModelMixin,
        viewsets.GenericViewSet):
    queryset = FollowObject.objects.all()
    serializer_class = FollowObjectSerializer
    permission_classes = [MustBeLoggedIn]

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
                being_followed=self.kwargs['pk'])
        except FollowObject.DoesNotExist:
            raise Http404
