from django.http.response import Http404
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.response import Response

from like_object.models import LikeObject
from like_object.serializers import LikeObjectSerializer
from tweet_object.models import TweetObject
from tweet_object.permissions import OnlyAuthorCanEdit
from tweet_object.serializers import TweetObjectSerializer


class TweetObjectViewSet(viewsets.ModelViewSet):
    queryset = TweetObject.objects.all()
    serializer_class = TweetObjectSerializer
    ordering = ['-id']
    permission_classes = [OnlyAuthorCanEdit]
    parser_classes = [JSONParser, MultiPartParser]

    @action(detail=True, methods=["GET"])
    def text(self, request, *args, **kwargs):
        tweet = self.get_object()
        return Response(tweet.text)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user.profile)

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
        retweet = TweetObjectSerializer(tweet.retweet)
        return Response(retweet.data)

    @action(detail=True, methods=["GET"])
    def comment(self, request, *args, **kwargs):
        tweet = self.get_object()
        if not tweet.comment:
            raise Http404
        comment = TweetObjectSerializer(tweet.comment)
        return Response(comment.data)

    @action(detail=True, methods=["GET"])
    def comments(self, request, *args, **kwargs):
        # This will return a list of tweets that
        # have replied the selected tweet

        tweet = self.get_object()
        comments = TweetObject.objects.filter(comment=tweet)

        # Apply pagination to the queryset
        comments = self.paginate_queryset(comments)
        comments = TweetObjectSerializer(comments, many=True)
        return self.get_paginated_response(comments.data)

    @action(detail=True, methods=["GET"])
    def retweets(self, request, *args, **kwargs):
        # This will return a list of tweets that
        # have retweeted the selected tweet

        tweet = self.get_object()
        retweets = TweetObject.objects.filter(retweet=tweet)

        # Apply pagination to the queryset
        retweets = self.paginate_queryset(retweets)
        retweets = TweetObjectSerializer(retweets, many=True)
        return self.get_paginated_response(retweets.data)
