from rest_framework import serializers
from tweet_object.models import TweetObject
from like_object.models import LikeObject
from image_object.models import ImageObject
from django.contrib.auth.models import AnonymousUser


class TweetObjectSerializer(serializers.ModelSerializer):

    id = serializers.ReadOnlyField(source='uuid')
    author = serializers.ReadOnlyField(source='author.user.username')
    likes = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    is_retweeted = serializers.SerializerMethodField()
    retweets = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()
    retweet = serializers.CharField(
        source="retweet.uuid",
        allow_null=True,
        default=None,
        read_only=True
    )
    retweet_id = serializers.CharField(
        allow_null=True,
        default=None,
        label="retweet",
        write_only=True,
    )
    comment = serializers.CharField(
        source="comment.uuid",
        allow_null=True,
        default=None,
        read_only=True
    )
    comment_id = serializers.CharField(
        allow_null=True,
        default=None,
        label="comment",
        write_only=True,
    )
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
        model = TweetObject
        fields = (
            'id',
            'text',
            'author',
            'likes',
            'comments',
            'retweets',
            'retweet',
            'retweet_id',
            'comment',
            'comment_id',
            'image',
            'image_url',
            'is_liked',
            'is_retweeted',
            'created_date'
        )
        extra_kwargs = {
            "text": {"allow_null": True,
                     "default": None},
            "created_date": {"read_only": True}
        }

    def create(self, validated_data):
        # Create an ImageObject if a file has been provided
        if validated_data['image']:
            file = ImageObject(author=validated_data['author'])
            file.upload(validated_data['image'])
            file.save()
            validated_data['image'] = file
        return super().create(validated_data)

    def validate(self, data):
        """
        A tweet cannot be a retweet and a comment at the same time
        """
        if (data.get("retweet_id") and data.get("comment_id")):
            raise serializers.ValidationError(
                {"comment_id": "A tweet cannot be a retweet and a comment at the same time"})

        """
        No text is only allowed when making a retweet
        """
        if (
            not data.get("text")
            and
            not data.get("retweet_id")
        ):
            raise serializers.ValidationError(
                {"text": "No text is only allowed when making a retweet"})

        """
        Retweet must exist
        """
        if data.get("retweet_id"):
            try:
                tweet = TweetObject.objects.get(uuid=data['retweet_id'])
                data['retweet_id'] = tweet.id
            except TweetObject.DoesNotExist:
                raise serializers.ValidationError(
                    {"retweet_id": "Not found"})

        """
        Comment must exist
        """
        if data.get("comment_id"):
            try:
                tweet = TweetObject.objects.get(uuid=data['comment_id'])
                data['comment_id'] = tweet.id
            except TweetObject.DoesNotExist:
                raise serializers.ValidationError(
                    {"comment_id": "Not found"})
        return data

    def get_likes(self, obj):
        return LikeObject.objects.filter(tweet=obj).count()

    def get_retweets(self, obj):
        return TweetObject.objects.filter(retweet=obj).count()

    def get_comments(self, obj):
        return TweetObject.objects.filter(comment=obj).count()

    def get_is_liked(self, obj):
        user = self.context['request'].user
        if not isinstance(user, AnonymousUser):
            return LikeObject.objects.filter(
                tweet=obj, author=user.profile).count() > 0
        # If the user is not logged in simply return False
        return False

    def get_is_retweeted(self, obj):
        user = self.context['request'].user
        if not isinstance(user, AnonymousUser):
            return TweetObject.objects.filter(
                retweet=obj, author=user.profile).count() > 0
        # If the user is not logged in simply return False
        return False
