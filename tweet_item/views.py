from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import viewsets, permissions
from tweet_item.serializer import TweetItemSerializer
from tweet_item.models import TweetItem
from rest_framework import mixins
from rest_framework import generics


class TweetItemList(mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    generics.GenericAPIView):
    queryset = TweetItem.objects.all()
    serializer_class = TweetItemSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
