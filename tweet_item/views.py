from tweet_item.serializer import TweetItemSerializer
from tweet_item.models import TweetItem
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action


class TweetItemViewSet(viewsets.ModelViewSet):
    queryset = TweetItem.objects.all()
    serializer_class = TweetItemSerializer
    ordering = ['-id']

    @action(detail=True, methods=["GET"])
    def text(self, request, *args, **kwargs):
        tweet = self.get_object()
        return Response(tweet.text)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
