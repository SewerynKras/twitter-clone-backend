from django.shortcuts import render
from follow_object.models import FollowObject
from follow_object.serializers import FollowObjectSerializer
from rest_framework import viewsets


class FollowObjectViewSet(
        viewsets.mixins.CreateModelMixin,
        viewsets.mixins.DestroyModelMixin,
        viewsets.GenericViewSet):
    queryset = FollowObject.objects.all()
    serializer_class = FollowObjectSerializer
    # ordering = ['id']
    # permission_classes = [CanOnlyEditYourself]
