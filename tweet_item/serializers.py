from rest_framework import serializers
from tweet_item.models import TweetItem
from like_object.models import LikeObject


class TweetItemSerializer(serializers.HyperlinkedModelSerializer):

    author = serializers.ReadOnlyField(source='author.username')
    likes = serializers.SerializerMethodField()

    class Meta:
        model = TweetItem
        fields = ['id', 'text', 'author', 'likes']

    def get_likes(self, obj):
        return LikeObject.objects.filter(tweet=obj).count()
