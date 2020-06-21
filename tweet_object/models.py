import uuid
from django.db import models


class TweetObject(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    text = models.CharField(
        max_length=256,
        null=True,
        default=None
    )
    author = models.ForeignKey(
        'user_profile.Profile',
        related_name='tweets',
        on_delete=models.CASCADE
    )
    retweet = models.ForeignKey(
        'tweet_object.TweetObject',
        related_name='retweet_to',
        null=True,
        default=None,
        on_delete=models.SET_NULL
    )
    comment = models.ForeignKey(
        'tweet_object.TweetObject',
        related_name='comment_to',
        null=True,
        default=None,
        on_delete=models.SET_NULL
    )
    image = models.ForeignKey(
        'image_object.ImageObject',
        null=True,
        default=None,
        on_delete=models.CASCADE
    )

    class Meta:
        ordering = ['-id']
