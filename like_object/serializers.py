from rest_framework import serializers
from like_object.models import LikeObject
from tweet_item.models import TweetItem


class LikeObjectSerializer(serializers.HyperlinkedModelSerializer):

    author = serializers.ReadOnlyField(
        source='author.username', read_only=True)
    tweet_id = serializers.CharField(write_only=True)

    class Meta:
        model = LikeObject
        fields = [
            'author',
            'tweet_id'
        ]

    def validate(self, data):
        """
        Check that the tweet exists
        """
        try:
            TweetItem.objects.get(id=data['tweet_id'])
        except TweetItem.DoesNotExist:
            raise serializers.ValidationError(
                {"tweet_id": "Not found"})

        """
        Check if like object is unique (you cannot like the same tweet twice!)
        """
        try:
            LikeObject.objects.get(
                tweet=data['tweet_id'],
                author=self.context['request'].user)
        except LikeObject.DoesNotExist:
            return data
        raise serializers.ValidationError(
            {"tweet_id": "You already like this tweet"})
