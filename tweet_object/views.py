from django.db.models import Q
from django.http.response import Http404
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.response import Response

from follow_object.models import FollowObject
from like_object.models import LikeObject
from like_object.serializers import LikeObjectSerializer
from tweet_object.models import TweetObject
from tweet_object.permissions import OnlyAuthorCanEdit, OnlyLoggedInUserCanViewList
from tweet_object.serializers import TweetObjectSerializer


class TweetObjectViewSet(viewsets.ModelViewSet):
    queryset = TweetObject.objects.all()
    serializer_class = TweetObjectSerializer
    permission_classes = [OnlyLoggedInUserCanViewList, OnlyAuthorCanEdit]
    parser_classes = [JSONParser, MultiPartParser]
    lookup_field = "uuid"

    def list(self, request):
        user = self.request.user.profile
        who_is_the_user_following = FollowObject.objects.filter(following=user)
        tweets = TweetObject.objects.filter(
            # Return tweets created by the user
            Q(author=user) |
            # Return tweets created by people the user follows
            Q(author__user__username__in=who_is_the_user_following.values_list(
                'being_followed__user__username', flat=True)))

        # Apply pagination to the queryset
        tweets = self.paginate_queryset(tweets)
        tweets = TweetObjectSerializer(tweets, many=True)
        return self.get_paginated_response(tweets.data)

    @action(detail=True, methods=["GET"])
    def text(self, request, *args, **kwargs):
        tweet = self.get_object()
        return Response(tweet.text)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user.profile)

    @action(detail=True, methods=["GET"])
    def likes(self, request, *args, **kwargs):
        # This will return a list of users that
        # have liked the selected tweet

        tweet = self.get_object()
        likes = LikeObject.objects.filter(tweet=tweet)

        # Apply pagination to the queryset
        likes = self.paginate_queryset(likes)
        likes = LikeObjectSerializer(likes, many=True)
        return self.get_paginated_response(likes.data)

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
