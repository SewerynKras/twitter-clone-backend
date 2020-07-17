from django.http.response import Http404
from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated

from follow_object.models import FollowObject
from follow_object.permissions import MustBeLoggedIn
from follow_object.serializers import FollowObjectSerializer


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
