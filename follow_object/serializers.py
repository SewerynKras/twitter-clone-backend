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
