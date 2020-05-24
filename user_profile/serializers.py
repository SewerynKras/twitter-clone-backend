from django.contrib.auth.models import User
from tweet_item.models import TweetItem
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    tweets = serializers.PrimaryKeyRelatedField(
        many=True, queryset=TweetItem.objects.all())

    class Meta:
        model = User
        fields = ['id', 'username', 'tweets']
