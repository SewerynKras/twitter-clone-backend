from django.http.response import Http404
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.response import Response

from like_object.models import LikeObject
from like_object.serializers import LikeObjectSerializer
from tweet_item.models import TweetItem
from tweet_item.permissions import OnlyAuthorCanEdit
from tweet_item.serializers import TweetItemSerializer


class TweetItemViewSet(viewsets.ModelViewSet):
    queryset = TweetItem.objects.all()
    serializer_class = TweetItemSerializer
    ordering = ['-id']
    permission_classes = [OnlyAuthorCanEdit]
    parser_classes = [JSONParser, MultiPartParser]

    @action(detail=True, methods=["GET"])
    def text(self, request, *args, **kwargs):
        tweet = self.get_object()
        return Response(tweet.text)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=["GET"])
    def likes(self, request, *args, **kwargs):
        tweet = self.get_object()
        likes = LikeObject.objects.filter(tweet=tweet)
        likes = LikeObjectSerializer(likes, many=True)
        # This will return a list of users that have liked the selected tweet
        return Response(likes.data)

    @action(detail=True, methods=["GET"])
    def retweet(self, request, *args, **kwargs):
        tweet = self.get_object()
        if not tweet.retweet:
            raise Http404
        retweet = TweetItemSerializer(tweet.retweet)
        return Response(retweet.data)

    @action(detail=True, methods=["GET"])
    def comment(self, request, *args, **kwargs):
        tweet = self.get_object()
        if not tweet.comment:
            raise Http404
        comment = TweetItemSerializer(tweet.comment)
        return Response(comment.data)
