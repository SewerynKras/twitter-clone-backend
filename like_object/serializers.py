from rest_framework import serializers
from like_object.models import LikeObject
from tweet_object.models import TweetObject


class LikeObjectSerializer(serializers.HyperlinkedModelSerializer):

    tweet_id = serializers.CharField(write_only=True)
    author = serializers.SerializerMethodField()

    class Meta:
        model = LikeObject
        fields = [
            'author',
            'tweet_id',
        ]

    def get_author(self, obj):
        return obj.author.user.username

    def validate(self, data):
        """
        Check that the tweet exists
        """
        try:
            TweetObject.objects.get(id=data['tweet_id'])
        except TweetObject.DoesNotExist:
            raise serializers.ValidationError(
                {"tweet_id": "Not found"})

        """
        Check if like object is unique (you cannot like the same tweet twice!)
        """
        try:
            LikeObject.objects.get(
                tweet=data['tweet_id'],
                author=self.context['request'].user.profile)
        except LikeObject.DoesNotExist:
            return data
        raise serializers.ValidationError(
            {"tweet_id": "You already like this tweet"})
