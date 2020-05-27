from tweet_item.models import TweetItem
from rest_framework import serializers
from user_profile.models import Profile
from rest_framework.validators import UniqueTogetherValidator
from django.contrib.auth.models import User
from follow_object.models import FollowObject


class ProfileSerializer(serializers.ModelSerializer):
    tweets = serializers.PrimaryKeyRelatedField(
        many=True, read_only=True)
    username = serializers.CharField(source='user.username')
    password = serializers.CharField(source='user.password', write_only=True)

    followers = serializers.SerializerMethodField(read_only=True)
    following = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Profile
        fields = [
            'id',
            'username',
            'display_name',
            'bio',
            'website',
            'location',
            'birth_date',
            'tweets',
            'password',
            'followers',
            'following'
        ]

    def validate(self, data):
        """
        Check if that username is unique
        """
        try:
            User.objects.get(username=data['user']['username'])
        except User.DoesNotExist:
            return data
        raise serializers.ValidationError(
            {"username": "username must be unique"})

    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data['user']['username'],
        )
        user.set_password(validated_data['user']['password'])
        user.save()
        validated_data['user'] = user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        """
        The serializer cannot change nested fields in here so it has to
        be done manually
        """
        instance.user.username = validated_data['user']['username']
        instance.save()
        del validated_data['user']
        return super().update(instance, validated_data)

    def get_followers(self, obj):
        return FollowObject.objects.filter(being_followed=obj).count()

    def get_following(self, obj):
        return FollowObject.objects.filter(following=obj).count()
