from rest_framework import serializers
from user_profile.models import Profile
from follow_object.models import FollowObject


class FollowObjectSerializer(serializers.ModelSerializer):
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
        Check if that follow target is different that the follower
        """
        if data['being_followed'] == self.context['request'].user.profile:
            raise serializers.ValidationError(
                {"being_followed": "You cannot follow yourself"})

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

    def create(self, validated_data):
        return super().create(validated_data)


class FollowingSerializer(serializers.ModelSerializer):
    user_id = serializers.SerializerMethodField('get_user_id')

    class Meta:
        model = FollowObject
        fields = [
            'user_id'
        ]

    def get_user_id(self, obj):
        return obj.following.id


class BeingFollowedSerializer(serializers.ModelSerializer):
    user_id = serializers.SerializerMethodField('get_user_id')

    class Meta:
        model = FollowObject
        fields = [
            'user_id'
        ]

    def get_user_id(self, obj):
        return obj.being_followed.id
