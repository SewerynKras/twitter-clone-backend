from rest_framework import serializers
from user_profile.models import Profile
from follow_object.models import FollowObject


class FollowObjectSerializer(serializers.ModelSerializer):

    being_followed = serializers.CharField()

    class Meta:
        model = FollowObject
        fields = [
            'following',
            'being_followed'
        ]
        extra_kwargs = {
            'following': {'read_only': True},
        }

    def validate(self, data):
        """
        Check if that follow target exists and is different that the follower
        """
        try:
            # Profile exists?
            prof = Profile.objects.get(
                user__username=data['being_followed'])
            # Profile is different than the current user?
            if prof == self.context['request'].user.profile:
                raise serializers.ValidationError(
                    {"being_followed": "You cannot follow yourself"})
            # Override the username with the queried profile so that it's ready
            # for object creation
            data['being_followed'] = prof
        except Profile.DoesNotExist:
            raise serializers.ValidationError(
                {"being_followed": "Not found"})

        """
        Check if that follow target is unique
        """
        try:
            FollowObject.objects.get(
                following=self.context['request'].user.profile,
                being_followed=data['being_followed'])
        except FollowObject.DoesNotExist:
            return data
        raise serializers.ValidationError(
            {"being_followed": "You are already following this user"})


class FollowingSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField('get_user_id')

    class Meta:
        model = FollowObject
        fields = [
            'username'
        ]

    def get_user_id(self, obj):
        return obj.following.user.username


class BeingFollowedSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField('get_user_id')

    class Meta:
        model = FollowObject
        fields = [
            'username'
        ]

    def get_user_id(self, obj):
        return obj.being_followed.user.username
