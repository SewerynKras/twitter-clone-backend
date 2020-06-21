from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from follow_object.models import FollowObject
from image_object.models import ImageObject
from tweet_item.models import TweetItem
from user_profile.models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    tweets = serializers.PrimaryKeyRelatedField(
        many=True, read_only=True)
    username = serializers.CharField(source='user.username')
    password = serializers.CharField(source='user.password', write_only=True)

    followers = serializers.SerializerMethodField(read_only=True)
    following = serializers.SerializerMethodField(read_only=True)

    image = serializers.ImageField(
        required=False,
        allow_null=True,
        default=None,
        label="image",
        write_only=True
    )
    image_url = serializers.CharField(
        source="image.url",
        allow_null=True,
        default=None,
        read_only=True
    )

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
            'following',
            'image',
            'image_url'
        ]

    def validate(self, data):
        """
        Check if that username is unique
        """
        if data.get("user"):
            try:
                User.objects.get(username=data['user']['username'])
            except User.DoesNotExist:
                pass
            else:
                raise serializers.ValidationError(
                    {"username": "username must be unique"})
        return data

    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data['user']['username'],
        )
        user.set_password(validated_data['user']['password'])
        user.save()
        validated_data['user'] = user

        # Since the ImageObject requires a profile the file gets cached here
        # (before the profile itself gets created) and added to it later
        imageFile = validated_data['image']
        del validated_data['image']

        instance = super().create(validated_data)

        # Create an ImageObject if a file has been provided
        if imageFile:
            file = ImageObject(author=instance)
            file.upload(imageFile)
            file.save()
            instance.image = file
            instance.save()

        return instance

    def update(self, instance, validated_data):
        """
        The serializer cannot change nested fields in here so it has to
        be done manually
        """
        if validated_data.get("user"):
            instance.user.username = validated_data['user']['username']
            instance.save()
            del validated_data['user']

        if validated_data.get('image'):
            file = ImageObject(author=instance)
            file.upload(validated_data['image'])
            file.save()
            validated_data['image'] = file

        return super().update(instance, validated_data)

    def get_followers(self, obj):
        return FollowObject.objects.filter(being_followed=obj).count()

    def get_following(self, obj):
        return FollowObject.objects.filter(following=obj).count()
