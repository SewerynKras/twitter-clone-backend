import uuid
from django.db import models


class TweetItem(models.Model):
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
        'tweet_item.TweetItem',
        related_name='retweet_to',
        null=True,
        default=None,
        on_delete=models.SET_NULL
    )
    comment = models.ForeignKey(
        'tweet_item.TweetItem',
        related_name='comment_to',
        null=True,
        default=None,
        on_delete=models.SET_NULL
    )

    class Meta:
        ordering = ['-id']
