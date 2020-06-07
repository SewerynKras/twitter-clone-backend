from rest_framework import serializers
from tweet_item.models import TweetItem
from like_object.models import LikeObject


class TweetItemSerializer(serializers.HyperlinkedModelSerializer):

    author = serializers.ReadOnlyField(source='author.username')
    likes = serializers.SerializerMethodField()
    retweet = serializers.IntegerField(
        source="retweet.id",
        allow_null=True,
        default=None,
        read_only=True)
    retweet_id = serializers.IntegerField(
        allow_null=True,
        default=None,
        label="retweet",
        write_only=True,
    )

    class Meta:
        model = TweetItem
        fields = ('id', 'text', 'author', 'likes', 'retweet', 'retweet_id')
        extra_kwargs = {
            "text": {"allow_null": True,
                     "default": None}
        }

    def validate(self, data):
        """
        No text is only allowed when making a retweet
        """
        if data.get("text") is None and data.get("retweet_id") is None:
            raise serializers.ValidationError(
                {"text": "No text is only allowed when making a retweet"})
        return data

    def get_likes(self, obj):
        return LikeObject.objects.filter(tweet=obj).count()
