from rest_framework import serializers
from tweet_item.models import TweetItem


class TweetItemSerializer(serializers.HyperlinkedModelSerializer):

    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = TweetItem
        fields = ['id', 'text', 'author']
